# 介紹

聽過 [Function Calling](https://openai.com/index/function-calling-and-other-api-updates) 嗎？這個名詞是 OpenAI 在 2023 年 6 月提出的新概念，主要是讓 LLM 可以呼叫外部的 function 來取得資料或執行動作。不過這個概念並不是 OpenAI 獨有，其他的 LLM 供應商與 AI 框架也都有類似的功能，只是各自的實作方式不盡相同。這也導致開發者在使用不同 LLM 或框架時，往往需要重新設計 Function Calling 的邏輯。後來，就有一個新的標準出現，叫做 [Model Context Protocol（MCP）](https://modelcontextprotocol.io/)，由 Anthropic 所提出。

# MCP 基本概念

模型上下文協定（Model Context Protocol，MCP）是一種標準化的格式，用於描述 LLM 可以透過一套統一的方式來呼叫外部的 function 並取得資料或執行動作。

## 基本架構

- MCP Host：The AI application that coordinates and manages one or multiple MCP clients
- MCP Client：A component that maintains a connection to an MCP server and obtains context from an MCP server for the MCP host to use
- MCP Server：A program that provides context to MCP clients

## 傳輸方式

- STDIO
- HTTP/SSE

# 重點回顧

# 參考資料