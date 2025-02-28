import { createLogger, format, transports } from "winston";

export const logger = createLogger({
	level: "info", // "debug", "error", などロガーレベルの下限
	format: format.json(), // JSON形式で出力すると Cloud Logging 上で扱いやすい
	defaultMeta: { service: "my-remix-app" },
	transports: [
		// 開発中ならコンソールに見やすい形式で出したいかもしれません
		new transports.Console({
			format: format.simple(),
		}),
	],
});
