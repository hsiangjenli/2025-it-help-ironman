# 介紹

前面從基本的 MCP 的基本概念、操作到實際開發，各位應該可以感受到 MCP 對 AI Agent 或是 Agentic AI 是一個不可或缺的一項協定。

然而，各位在配置 MCP Server 的時候應該會覺得有點亂，像是 GitHub Copilot、Claude Code 跟 Codex 在配置檔的格式都不太一樣，另外也遇到像是環境變數、路徑等問題（要讓 MCP 可以存取哪些路徑等...）。目前配置的 MCP Server 數量可能也不大，偶爾麻煩點也還可以接受，但是如果是從企業的角度來看，不可能隨意的讓員工去安裝 MCP Server，讓 AI Agent 可以隨意讀取電腦上的資料。

因此，今天要來介紹一個 Enterprise-Level 集中管理 MCP Server 的解決方案叫做 [`IBM/mcp-context-forge`](https://github.com/IBM/mcp-context-forge)。

> **補充說明**
>
> 筆者認爲 MCP 目前還在發展階段，因此本次的介紹並不一定是最好的解決方案，主要著重的點在於提供各位一些 mindset，讓各位可以知道在企業環境中，可能可以怎麼管理 MCP Server 以及 MCP Server 的一些注意事項。

# 介紹 `IBM/mcp-context-forge`

## 要解決的問題

## 


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