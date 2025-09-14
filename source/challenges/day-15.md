# 介紹

前面從基本的 MCP 的基本概念、操作到實際開發，各位應該可以感受到 MCP 對 AI Agent 或是 Agentic AI 是一個不可或缺的一項協定。

然而，各位在配置 MCP Server 的時候應該會覺得有點亂，像是 GitHub Copilot、Claude Code 跟 Codex 在配置檔的格式都不太一樣，另外也遇到像是環境變數、路徑等問題（要讓 MCP 可以存取哪些路徑等...）。目前配置的 MCP Server 數量可能也不大，偶爾麻煩點也還可以接受，但是如果是從企業的角度來看，不可能隨意的讓員工去安裝 MCP Server，讓 AI Agent 可以隨意讀取電腦上的資料。

因此，今天要來介紹一個 Enterprise-Level 集中管理 MCP Server 的解決方案叫做 [`IBM/mcp-context-forge`](https://github.com/IBM/mcp-context-forge)。

> **補充說明**
>
> 筆者認爲 MCP 目前還在發展階段，因此本次的介紹並不一定是最好的解決方案，主要著重的點在於提供各位一些 mindset，讓各位可以知道在企業環境中，可能可以怎麼管理 MCP Server 以及 MCP Server 的一些注意事項。

# 介紹 `IBM/mcp-context-forge`

## 目標

提供一個「集中管理」 MCP Gateway，可以讓多個 MCP Server 與 RESTful API 使用一個單一端點

## 要解決的問題

1. **多傳輸/協定不一致**：目前 MCP Server 支援多種通訊方式（HTTP / SSE / WebSocket / stdio / streamable-HTTP 等），同時不同的 LLM Provider 的設定檔格式也不太一樣（JSON、TOML 等）
1. **分散管理**：目前 MCP Server 都是分散在開發者的電腦上，無法集中管理以及版本控制
1. **授權機制**：目前沒有統一的授權機制
1. **缺乏 Observability**：目前沒有辦法 observe MCP Server 的使用狀況（呼叫、延遲、錯誤率等）

## 特色

1. **統一 Gateway**：單一個端點來管理多個 MCP Server 以及 RESTful API
1. **虛擬 MCP Server**：可以把多個相關的 MCP Server 打包成一個虛擬的 MCP Server，讓使用者只需要配置一個 MCP Server
1. **API 轉換**：可以把 RESTful API 轉換成 MCP Server，省去重新開發 MCP Server 的麻煩，直接使用現有的 RESTful API
1. **管理員界面**：提供一個 Admin UI 來管理 MCP Server
1. **認證機制**：支援多種認證機制（JWT、SSO 等等）
1. **Observability**：搭配 OpenTelemetry 來觀察 MCP Server 的使用狀況

# 實際操作

## 使用 Docker 安裝 MCP Gateway

- 使用 local network
- Admin UI：http://localhost:4444/admin
- Docs Swagger：http://localhost:4444/docs
- user：`admin`
- pass：`changeme`

```shell
mkdir -p $(pwd)/data

touch $(pwd)/data/mcp.db

sudo chown -R :docker $(pwd)/data

chmod 777 $(pwd)/data

docker run -d --name mcpgateway \
  --network=host \
  -e MCPGATEWAY_UI_ENABLED=true \
  -e MCPGATEWAY_ADMIN_API_ENABLED=true \
  -e HOST=0.0.0.0 \
  -e PORT=4444 \
  -v $(pwd)/data:/data \
  ghcr.io/ibm/mcp-context-forge:0.6.0
```

# 重點回顧

# 參考資料