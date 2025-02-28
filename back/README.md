```markdown
# python-uv-ruff-template

## 概要

このパッケージは、Python プロジェクトのテンプレートです。
※ 試しに FastAPI で Hello World までできることを確認してます。

## プロジェクト構造
```

my_package/
├── app/
├── tests/
├── .vscode/
├── pyproject.toml
├── Taskfile.yml
└── README.md

````

## 必要条件

- Python 3.12.6
- mise

## インストール方法

### 開発環境のセットアップ

1. 依存関係のインストール:

```bash
mise install
````

## 使用方法

### タスクの実行

プロジェクトには `Taskfile.yml` が含まれており、一般的なタスクを簡単に実行できます：
詳細は、`Taskfile.yml`を確認してください

# バックエンドアプリケーションのデプロイガイド

この README ではバックエンドアプリケーション（FastAPI）の Cloud Run へのデプロイ方法について説明します。

## 前提条件

- Google Cloud アカウントとプロジェクトが作成済み
- `gcloud` CLI がインストール済み
- Docker がインストール済み

## ローカルでの開発

```bash
# 開発環境のセットアップ
task setup

# サーバー起動
task start

# コードフォーマットと静的解析
task format
task lint

# テスト実行
task test
```

## Google Cloud Run へのデプロイ

### 1. 認証の設定

```bash
# Google Cloudの認証
task gcloud-auth

# Docker認証の設定（Artifact Registryへのプッシュに必要）
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 2. Artifact Registry リポジトリの作成

**初回のみ必要な手順**です。リポジトリがすでに存在する場合はスキップできます。

```bash
# デフォルト設定（backend-repoリポジトリをus-central1に作成）
task gcloud-setup-repo

# カスタム設定
REPO_NAME=my-custom-repo task gcloud-setup-repo
```

エラーが発生した場合：

- `Repository already exists`：すでにリポジトリが存在するため問題ありません
- 権限エラー：`gcloud auth login`を実行し、適切な権限を持つアカウントでログインします

### 3. イメージのビルドとプッシュ

```bash
# デフォルト設定（.envファイルの変数を使用）
task gcloud-build-push

# カスタム設定
SERVICE_NAME=custom-app REPO_NAME=custom-repo task gcloud-build-push
```

エラーが発生した場合：

- リポジトリが存在しない：手順 2 を実行します
- 認証エラー：`gcloud auth configure-docker <リージョン>-docker.pkg.dev`を実行します

### 4. Cloud Run へのデプロイ

```bash
# デフォルト設定（.envファイルの変数を使用）
task gcloud-deploy-backend

# カスタム設定
SERVICE_NAME=custom-app task gcloud-deploy-backend
```

エラーが発生した場合：

- イメージが見つからない：手順 3 を確認します
- プロジェクト間の権限エラー：`--project`フラグが正しく設定されているか確認します

### 5. ビルドからデプロイまでの一括実行

```bash
# 一括実行（イメージのビルド、プッシュ、デプロイを連続実行）
task deploy-backend
```

## 環境変数の設定

`.env`ファイルを作成し、以下の変数を設定してください：

```properties
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
SERVICE_NAME=fastapi-app
REPO_NAME=backend-repo
```

## カスタマイズ可能なパラメータ

すべてのタスクでは以下の変数がカスタマイズ可能です：

- `SERVICE_NAME`: Cloud Run サービス名（デフォルト: "backend-app"）
- `REPO_NAME`: Artifact Registry リポジトリ名（デフォルト: "backend-repo"）
- `LOCATION`: GCP ロケーション（デフォルト: "us-central1"）
- `TAG`: イメージタグ（デフォルト: "latest"）

## API の IAP 認証設定

Cloud Run の API に対して Identity-Aware Proxy (IAP)を使用した認証制御を設定するためのガイドです。IAP を使用することで、特定のユーザーやグループのみが API にアクセスできるよう制御できます。

### 前提条件

1. ドメイン名と有効な SSL 証明書
2. OAuth 同意画面の設定
3. OAuth クライアント ID とシークレットの作成

### 1. OAuth 認証情報の設定（コンソールでの作業）

#### ステップ 1: OAuth 同意画面の設定

1. Google Cloud コンソールで [APIs & Services] > [OAuth consent screen] を開く
2. 内部または外部のユーザータイプを選択
3. 必要な情報を入力（アプリ名、サポートメールなど）
4. 必要なスコープを追加（通常はデフォルト設定で問題なし）
5. 同意画面の設定を保存

#### ステップ 2: OAuth クライアント ID の作成

1. Google Cloud コンソールで [APIs & Services] > [Credentials] を開く
2. [Create Credentials] > [OAuth client ID] をクリック
3. アプリケーションタイプで「ウェブアプリケーション」を選択
4. 名前を入力（例: "IAP for Cloud Run"）
5. **承認済みリダイレクト URI** は一時的に空か何か入力して作成
6. [作成] をクリック
7. **作成完了後にクライアント ID とクライアントシークレットが表示されます**
   - これらの値を安全に保存してください（例: `123456789012-abcdefg.apps.googleusercontent.com`）

#### ステップ 3: リダイレクト URI の更新

1. 作成したクライアント ID の設定画面を開く（編集ボタンをクリック）
2. 承認済みリダイレクト URI に以下を追加:
   ```
   https://iap.googleapis.com/v1/oauth/clientIds/[CLIENT_ID]:handleRedirect
   ```
   ※ `[CLIENT_ID]` は先ほど取得したクライアント ID に置き換えてください
   （例: `https://iap.googleapis.com/v1/oauth/clientIds/123456789012-abcdefg.apps.googleusercontent.com:handleRedirect`）
3. [保存] をクリック

### 2. API の有効化

```bash
# IAPに必要なAPIを有効化
task gcloud-enable-iap
```

### 3. ロードバランサーと IAP の設定

```bash
# 環境変数の設定
export OAUTH_CLIENT_ID=your-client-id
export OAUTH_CLIENT_SECRET=your-client-secret

# デフォルト設定でIAP用ロードバランサーを作成
CERT_NAME=your-certificate-name task gcloud-create-lb-for-iap

# カスタム設定
SERVICE_NAME=custom-api CERT_NAME=custom-cert task gcloud-create-lb-for-iap
```

### 4. IAP アクセス権限の設定

```bash
# 特定のユーザーにIAPアクセス権を付与
MEMBER="user:user@example.com" task gcloud-set-iap-policy

# グループにアクセス権を付与
MEMBER="group:team@example.com" task gcloud-set-iap-policy

# サービスアカウントにアクセス権を付与
MEMBER="serviceAccount:sa@project-id.iam.gserviceaccount.com" task gcloud-set-iap-policy
```

### 5. 一括セットアップ

最初の OAuth 設定がコンソールで完了している場合、以下のコマンドで一括セットアップできます：

```bash
# 環境変数の設定
export OAUTH_CLIENT_ID=your-client-id
export OAUTH_CLIENT_SECRET=your-client-secret
export MEMBER="user:user@example.com"

# 証明書名を指定して一括セットアップ
CERT_NAME=your-certificate-name task setup-iap-protection
```

### 注意事項

- IAP が有効なロードバランサーを経由してアクセスする URL は、Cloud Run の直接 URL とは異なります
- OAuth クライアント ID とシークレットは安全に管理してください
- 証明書の管理は Google-managed 証明書の使用を推奨します
- IAP を使用する場合、Cloud Run のデフォルトの認証設定は「未認証の呼び出しを許可する」が推奨されます
- 新しいユーザーを追加する場合は `gcloud-set-iap-policy` タスクで権限設定を行います

```

```
