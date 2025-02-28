## メモ 最終的にはちゃんと手順として落とし込む

- 最初の起動時に biome の runtime が見つからないっていうふうにでる

```terminal

Biome binary found at /workspaces/app-welcome-junior/2025/2213_kugimiya/front/node_modules/.bin/biome
Executing Biome from: /workspaces/app-welcome-junior/2025/2213_kugimiya/front/node_modules/.bin/biome
[cli-stderr] data 107
[cli-stderr] end
[cli-stderr] finish
[cli-stdout] end
[cli-stdout] finish
[cli] exit 127
[Error - 3:03:22 AM] Biome client: couldn't create connection to server.
Error: Command "/workspaces/app-welcome-junior/2025/2213_kugimiya/front/node_modules/.bin/biome __print_socket" exited with code 127
Output:
/workspaces/app-welcome-junior/2025/2213_kugimiya/front/node_modules/.bin/biome: 16: exec: node: not found

    at n$ (/root/.vscode-server/extensions/biomejs.biome-2.3.2/out/main.js:84:16)
    at processTicksAndRejections (node:internal/process/task_queues:95:5)
    at i$ (/root/.vscode-server/extensions/biomejs.biome-2.3.2/out/main.js:84:250)
    at UQ.createConnection (/root/.vscode-server/extensions/biomejs.biome-2.3.2/out/main.js:39:12709)
    at UQ.start (/root/.vscode-server/extensions/biomejs.biome-2.3.2/out/main.js:39:2940)
    at $X (/root/.vscode-server/extensions/biomejs.biome-2.3.2/out/main.js:82:28898)
    at aw.n (file:///vscode/vscode-server/bin/linux-arm64/e54c774e0add60467559eb0d1e229c6452cf8447/out/vs/workbench/api/node/extensionHostProcess.js:112:4447)
    at aw.m (file:///vscode/vscode-server/bin/linux-arm64/e54c774e0add60467559eb0d1e229c6452cf8447/out/vs/workbench/api/node/extensionHostProcess.js:112:4410)
    at aw.l (file:///vscode/vscode-server/bin/linux-arm64/e54c774e0add60467559eb0d1e229c6452cf8447/out/vs/workbench/api/node/extensionHostProcess.js:112:3866)
[cli-stdout] close
[cli] close 127
[cli-stderr] close

```

- コンテナの起動時にプロジェクト内に必要なツールと biome が shims を使ってグローバルの node.js を参照している

とりあえず以下を devcontainer.json に追記

```
  "postCreateCommand": "mise install && mise use -g node@20.12.1",
```
