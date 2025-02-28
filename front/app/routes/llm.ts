// app/routes/llm.ts
import { json } from "@remix-run/node";
import type { ActionFunctionArgs } from "@remix-run/node";
import {
	VertexAI,
	HarmCategory,
	HarmBlockThreshold,
	type GenerateContentResult,
} from "@google-cloud/vertexai";
import { logger } from "~/utils/logger.server"; // 先ほど作成したロガーをインポート

// 環境変数 (PROJECT_ID, LOCATION, など) を利用する想定
const PROJECT_ID = process.env.PROJECT_ID || "welcome-study-project";
const LOCATION = process.env.LOCATION || "us-central1";
const TEXT_MODEL = "gemini-1.0-pro";

export function loader() {
	// GET リクエストなどで直接アクセスされても 使い方がわかるメッセージを返す
	return json({ message: "Use POST with JSON { prompt: 'your text' }" });
}

export async function action({ request }: ActionFunctionArgs) {
	logger.info("Incoming request to /llm (action)");
	try {
		// リクエストボディから prompt を取得
		const { prompt } = (await request.json()) as { prompt?: string };
		if (!prompt) {
			logger.warn("Missing prompt in request body");
			return json(
				{ error: "Missing `prompt` in request body." },
				{ status: 400 },
			);
		}
		logger.info(`Received prompt: ${prompt}`);

		// Vertex AI インスタンスの生成
		const vertexAI = new VertexAI({
			project: PROJECT_ID,
			location: LOCATION,
		});

		// 指定のテキストモデル（gemini-1.0-pro）のインスタンスを取得
		const generativeModel = vertexAI.getGenerativeModel({
			model: TEXT_MODEL,
			safetySettings: [
				{
					category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
					threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
				},
			],
			generationConfig: {
				maxOutputTokens: 256,
				candidateCount: 1, // 候補は1件に固定
				temperature: 0.5, // 生成のランダム性を調整
			},
			systemInstruction: {
				role: "system",
				parts: [
					{ text: "For example, you are a helpful customer service agent." },
				],
			},
		});

		// ユーザーから受け取った prompt を利用してテキスト生成リクエストを作成
		const requestPayload = {
			contents: [{ role: "user", parts: [{ text: prompt }] }],
		};

		// コンテンツ生成の実行 (この部分でエラーが発生する可能性があるので個別に try/catch)
		let result: GenerateContentResult;
		try {
			result = await generativeModel.generateContent(requestPayload);
		} catch (apiError: unknown) {
			// Vertex AI API 側でエラーが起きた場合、詳細をログに記録する
			logger.error("Error during generateContent API call", {
				error: apiError,
			});

			// エラーが認証周り(例: PERMISSION_DENIED) かどうかを判定して適切にハンドリングする
			const errMsg = (apiError as Error)?.message ?? "";
			if (
				errMsg.includes("PERMISSION_DENIED") ||
				errMsg.includes("Unable to authenticate your request") ||
				errMsg.includes("unable to impersonate")
			) {
				// Cloud Run やローカルで GCP 認証が行われていない場合に起こるケース
				// 403や401を返すかどうかは好みですが、403で返す例を示します
				logger.error(
					"Vertex AI authentication failed. Please check your GCP credentials or impersonation settings.",
				);
				return json(
					{
						error:
							"Vertex AI authentication failed. Run `gcloud auth application-default login` or check IAM permissions.",
					},
					{ status: 403 },
				);
			}

			// それ以外のエラーはひとまずまとめて扱う
			throw new Error("Failed to generate content from Vertex AI.");
		}

		// レスポンスオブジェクトの存在をチェック
		if (!result.response) {
			throw new Error("No response received from Vertex AI.");
		}

		// 候補が存在するかどうかをチェック
		if (
			!result.response.candidates ||
			result.response.candidates.length === 0
		) {
			throw new Error("No candidate responses received from Vertex AI.");
		}

		// 1件目の候補を取得し、内容の存在を確認
		const candidate = result.response.candidates[0];
		if (
			!candidate.content ||
			!candidate.content.parts ||
			candidate.content.parts.length === 0
		) {
			throw new Error("Candidate response is missing content parts.");
		}

		// parts の中のテキストを結合して1つの回答テキストとする
		const answerText = candidate.content.parts
			.map((part) => part.text)
			.join(" ");
		logger.info(`Generated answer text: ${answerText}`);

		// JSON形式で1つのテキストを返す
		return json({ answer: answerText });
	} catch (error: unknown) {
		// ここでは最終的なエラー全般を受け取る
		logger.error("LLM error caught in action", { error });
		const errorMessage =
			error instanceof Error ? error.message : "Internal Server Error";
		// Remix のアクションなので、レスポンスを返す
		return json({ error: errorMessage }, { status: 500 });
	}
}
