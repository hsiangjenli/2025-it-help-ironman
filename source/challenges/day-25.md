# 介紹

昨天已經順利建立 Ollama 的 A2A Server，今天要來圓先前提過的坑 [`IBM/mcp-context-forge`](https://github.com/IBM/mcp-context-forge)，各位應該還記得這是一個集中化管理 MCP Server 的 Open Source Solution。在這份專案中，裡面也提供了註冊 A2A Agent 的功能，因此今天就來示範如何把建立好的 A2A Agent 註冊到 MCP Gateway 中。

# 操作

## MCP Gateway 參數設定

| 變數                               | 說明              | 預設值    |
| -------------------------------- | --------------- | ------ |
| `MCPGATEWAY_A2A_ENABLED`         | A2A 功能      | `true` |
| `MCPGATEWAY_A2A_MAX_AGENTS`      | 最大 Agent 數量  | `100`  |
| `MCPGATEWAY_A2A_DEFAULT_TIMEOUT` | HTTP 請求逾時時間（秒）  | `30`   |
| `MCPGATEWAY_A2A_MAX_RETRIES`     | 最大重試次數          | `3`    |
| `MCPGATEWAY_A2A_METRICS_ENABLED` | 是否啟用 Metrics 收集 | `true` |

> **補充說明**
>
> 如果身邊的設備沒有 GPU，跑地端的 LLM 會非常慢，建議可以把 `MCPGATEWAY_A2A_DEFAULT_TIMEOUT` 的值調高一點

## 起動 MCP Gateway

與先前操作一樣，先透過 Docker 把 MCP Gateway 啟動起來：

```shell
docker run -d --name mcpgateway \
  -p 4444:4444 \
  -e MCPGATEWAY_UI_ENABLED=true \
  -e MCPGATEWAY_ADMIN_API_ENABLED=true \
  -e HOST=0.0.0.0 \
  -e PORT=4444 \
  -e MCPGATEWAY_A2A_ENABLED=true \
  -e MCPGATEWAY_A2A_METRICS_ENABLED=true \
  -v $(pwd)/data:/data \
  ghcr.io/ibm/mcp-context-forge:0.6.0
```

## 註冊 A2A Agent

![20250923235945](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250923235945.png)


- Endpoint URL：http://localhost:10000

註冊完成後，可以透過 Test 按鈕來測試是否可以連線成功

> **補充說明**
>
> 因為在 Mac 上要讓容器內的服務可以存取主機的網路，必須使用[ `http://host.docker.internal:10000`](http://host.docker.internal:10000) 來存取主機的服務

# 重點回顧

- 使用 MCP Gateway 來管理 A2A Agent
- 測試 A2A Agent 是否可以正常運作

# 參考資料

- [IBM/mcp-context-forge](https://ibm.github.io/mcp-context-forge/using/agents/a2a/)