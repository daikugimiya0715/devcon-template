FROM mcr.microsoft.com/devcontainers/base:bullseye

# 必要なシステムパッケージのインストール
RUN apt-get update -y && apt-get install -y \
    gpg sudo wget curl build-essential \
    && rm -rf /var/lib/apt/lists/*


# mise の APT リポジトリの設定とインストール
RUN install -dm 755 /etc/apt/keyrings \
    && wget -qO - https://mise.jdx.dev/gpg-key.pub | gpg --dearmor | tee /etc/apt/keyrings/mise-archive-keyring.gpg 1> /dev/null \
    && echo "deb [signed-by=/etc/apt/keyrings/mise-archive-keyring.gpg arch=arm64] https://mise.jdx.dev/deb stable main" | tee /etc/apt/sources.list.d/mise.list \
    && apt-get update -y \
    && apt-get install -y mise

# miseを使うので pluginをaddしないといけないものはここで追加
RUN mise plugin add gcloud https://github.com/jthegedus/asdf-gcloud


# PATHを通す
RUN echo 'export PATH=$HOME/.local/share/mise/shims:$PATH' >> $HOME/.bashrc

# 開発時に利用するポート（例: front-app:3000, back-app:8000 etc..）
EXPOSE 3000 8000 5173