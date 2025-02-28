# DevContainer + mise テンプレート

このリポジトリは、DevContainerを使用した開発環境と、DevContainerを使用しない環境の両方で一貫したツール管理ができるサンプルプロジェクトです。[mise](https://mise.jdx.dev/)を使用することで、どちらの環境でも同じバージョンのツールを使用することができます。

## 特徴

- DevContainerによる一貫した開発環境
- DevContainerを使わない場合でもmiseによるツールバージョン管理
- Taskfileによる共通タスクの実行

## DevContainerのメリット

- **開発環境の一貫性**: チーム全員が完全に同一の環境で開発できるため、「自分の環境では動くのに」という問題が発生しない
- **即時開発開始**: リポジトリを開くだけで、前提条件や依存関係のインストールを自動化
- **環境の分離**: プロジェクトごとに独立した環境のため、依存関係の競合を防止
- **オンボーディングの効率化**: 新メンバーは複雑な環境構築手順なしで開発を始められる
- **クリーンなローカル環境**: ホストマシンに開発ツールをインストールする必要がない
- **GitHub Codespacesとの連携**: クラウド開発環境にもシームレスに対応
- **本番環境との類似性**: コンテナベースの開発で本番環境との差異を最小化

## miseとの連携のメリット

- **ツール管理の一元化**: DevContainerの内外で同じ`.mise.toml`を使用
- **柔軟な開発スタイル**: DevContainerを使いたい人も使いたくない人も同じプロジェクトで協業可能
- **バージョン固定**: プロジェクトで使用するツールのバージョンを明示的に管理

## 前提条件

### DevContainerを使用する場合
- Docker
- Visual Studio Code + DevContainer拡張機能

### DevContainerを使用しない場合
- [mise](https://mise.jdx.dev/)のインストール
- [Task](https://taskfile.dev/)のインストール ※ miseでインストールされます

## セットアップ方法

### DevContainerを使用する場合

1. このリポジトリをクローン
2. Visual Studio Codeで開く
3. DevContainerで開くかの確認が出たら「Reopen in Container」を選択
   (または F1キーを押して「Dev Containers: Reopen in Container」を選択)
4. コンテナ内で自動的に`mise install`が実行され、必要なツールがセットアップされます

### DevContainerを使用しない場合

1. このリポジトリをクローン
2. miseをインストール（[mise公式サイト](https://mise.jdx.dev/)参照）
3. プロジェクトルートで以下を実行
   ```bash
   mise install  # .mise.tomlに指定されたツールをインストール
   task setup    # セットアップタスクを実行
   ```

## プロジェクト構造

```
.
├── .devcontainer/             # DevContainer設定
│   ├── devcontainer.json      # DevContainer設定ファイル
│   └── Dockerfile             # DevContainer用Dockerfile
├── .mise.toml                 # mise設定ファイル
├── Taskfile.yml               # タスク定義（プロジェクト全体）
└── app/                       # アプリケーションコード
    └── Taskfile.yml           # アプリケーション特有のタスク定義
```

## 利用可能なタスク

プロジェクトルートで以下のコマンドを実行すると、利用可能なタスク一覧が表示されます：

```bash
task
```

### 主要なタスク

- `task setup` - miseによる必要ツールのインストール
- `task update` - miseで管理しているツールの更新
- `task check` - mise設定の確認

### アプリケーション特有のタスク

- `task app:dev` - アプリケーション開発サーバーを起動
- `task app:build` - アプリケーションをビルド
- `task app:lint` - アプリケーションのリントを実行
- `task app:test` - アプリケーションのテストを実行

## mise.tomlについて

`.mise.toml`ファイルには、プロジェクトで使用するツールのバージョンが指定されています。これにより、DevContainerを使っていても使っていなくても同じツールバージョンを使用できます。

```toml
[tools]
node = "20.12.1"  # Node.jsのバージョン

[env]
NODE_ENV = "development"  # 環境変数設定
```

## なぜこのアプローチが良いのか？

- **チーム内の一貫性**: DevContainer使用/不使用に関わらず同じツールバージョンを使用
- **セットアップの簡素化**: `mise install`一発で必要なツールをインストール可能
- **環境の移植性**: 異なるマシンでも同じ環境を簡単に再現可能
- **タスクの標準化**: Taskfileによる共通タスクの提供
- **ハイブリッド開発**: 開発者の好みや環境に応じた柔軟な開発スタイルをサポート

## コントリビュート

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成