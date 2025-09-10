# 介紹

既然已經簡單介紹了 MCP 的基本概念，接下來就是實際操作了，先從最簡單的開始，今天要介紹如何讓自己的 AI Agent 可以使用現成的 MCP Server。

# 操作

## 簡單介紹要怎麼執行 MCP Server

### 開發的語言

目前的 MCP Server 都是由 JavaScript、Node.js 或是 Python 來進行開發，另外也有使用 Docker 來封裝 MCP Server，這樣的好處是可以避免環境不相容的問題。

### 執行的指令與平常開發有何不同

因爲 MCP Server 跟一般的開發不太一樣，像是 Node.js 可能會比較習慣使用 `npm` 或是 `nvm` 等指令來管理套件或是版本，但是 MCP Server 是一個獨立的應用程式，而且是希望可以直接執行的，所以大部份使用 Node.js 開發的 MCP Server 都會使用 `npx` 來執行。使用 `npx` 的好處是可以直接執行套件（執行完之後不會安裝在系統中），可以減少污染的問題。至於 Python 的部分，則是使用 `uv` 或是 `uvx` 都有，`uv` 主要是用來管理 Python 的虛擬環境，但是可以藉由 `--with {package_name}`，讓程式執行的時候立刻安裝套件（一次性），避免污染系統。

### MCP Server 的設定檔

基本上 MCP Server 的設定檔都包含以下幾個部分：

- `command`：執行的指令（`npx`、`uv`、`uvx`、`docker`）
- `args`：執行的參數
- `env`：環境變數

#### GitHub Copilot

```json
{
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
      }
    }
  }
}
``` 

#### Claude Code

```json
{
  "mcpServers": {
    "server-name": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

#### Codex

```toml
[mcp_servers.server-name]
command = "npx"
args = ["-y", "mcp-server"]
env = { "API_KEY" = "value" }
# Optional: override the default 10s startup timeout
startup_timeout_ms = 20_000
```

## 實際使用 AWS Diagram MCP Server

接下來我們就以 [AWS Diagram MCP Server](https://awslabs.github.io/mcp/servers/aws-diagram-mcp-server/) 來進行示範，這個 MCP Server 是讓 AI Agent 可以使用 [`KubeDiagrams`](https://github.com/philippemerle/KubeDiagrams) 這個工具來繪製 AWS 架構圖。

```json
{
	"servers": {
		"awslabs.aws-diagram-mcp-server": {
			"command": "docker",
			"args": [
				"run",
				"--rm",
				"--interactive",
				"-w",
				"/workspace",
				"-v",
				"${workspaceFolder}:/workspace",
				"--env",
				"FASTMCP_LOG_LEVEL=ERROR",
				"mcp/aws-diagram:latest"
			],
			"env": {},
			"cwd": "${workspaceFolder}"
		}
	},
	"inputs": []
}
```

![pose_estimation_architecture](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/pose_estimation_architecture.png)

> **補充說明**：
>
> 雖然最後面 AI Agent 成功產出架構圖，但是總步數有點多（20 多步），並且中間卡在 mcp server 是在 docker 裏面執行，雖然有把當前的工作目錄掛載進去，但是 AI Agent 最後在存檔的時候還是不停搞錯路徑（要把 docker 內的圖片 cp 出來，但是 cp 的指令是在容器外執行）。
> 
> 最後是透過在本機端強制安裝套件，再把檔案匯出成 png 檔案，才成功的把圖片存下來。

# 重點回顧

- 介紹 GitHub Copilot、Claude Code、Codex 三個 MCP Server 的設定方式（2 個 Json、1 個 toml）
- 實際操作 AWS Diagram MCP Server，讓 AI Agent 可以繪製 AWS 架構圖（發現一些存取路徑的問題）

# 參考資料

- [Local MCP server setup](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/use-the-github-mcp-server#local-mcp-server-setup)
- [Claude Code MCP](https://docs.anthropic.com/en/docs/claude-code/mcp#project-scope)
- [Codex MCP](https://github.com/openai/codex/blob/main/docs/config.md#mcp_servers)