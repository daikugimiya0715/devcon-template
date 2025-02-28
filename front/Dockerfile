# Stage 1: ビルド用
FROM node:20-alpine AS builder
WORKDIR /app

# pnpm をグローバルインストール
RUN npm install -g pnpm

# package.json と pnpm-lock.yaml をコピーして依存関係をインストール
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# ソースコードをすべてコピー
COPY . .

# Remix のビルド実行
RUN pnpm run build

# Stage 2: ランタイム用
FROM node:20-alpine AS runner
WORKDIR /app

RUN npm install -g pnpm

# ビルド成果物と必要なファイルをコピー
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./
COPY --from=builder /app/pnpm-lock.yaml ./

# 本番環境用依存関係のインストール
RUN pnpm install --prod --frozen-lockfile

# コンテナで使用するポートを指定（Remix のデフォルトは3000）
EXPOSE 3000

# 環境変数を設定（Cloud Run 用に NODE_ENV=production を明示的に設定）
ENV NODE_ENV=production

# アプリの起動（package.json の start スクリプトが "remix-serve build/server/index.js" を実行する前提）
CMD ["pnpm", "start"]
