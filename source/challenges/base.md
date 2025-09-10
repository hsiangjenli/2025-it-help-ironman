# 介紹

既然已經簡單介紹了 MCP 的基本概念，接下來就是實際操作了，先從最簡單的開始，今天要介紹如何讓自己的 AI Agent 可以使用現成的 MCP Server。

# 操作

## 簡單介紹要怎麼執行 MCP Server

### 開發的語言

目前的 MCP Server 都是由以下幾個程式語言開發的：

1. JavaScript
1. Node.js
1. Python

### 執行的指令與平常開發有何不同

因爲 MCP Server 跟一般的開發不太一樣，像是 Node.js 可能會比較習慣使用 `npm` 或是 `nvm` 等指令來管理套件或是版本，但是 MCP Server 是一個獨立的應用程式，而且是希望可以直接執行的，所以大部份使用 Node.js 開發的 MCP Server 都會使用 `npx` 來執行。使用 `npx` 的好處是可以直接執行套件（執行完之後不會安裝在系統中），可以減少污染的問題。至於 Python 的部分，則是使用 `uv` 或是 `uvx` 都有，`uv` 主要是用來管理 Python 的虛擬環境，但是可以藉由 `--with {package_name}`，讓程式執行的時候立刻安裝套件（一次性），避免污染系統。

### MCP Server 的設定檔

#### GitHub Copilot

#### Claude Code

#### Codex

## 實際使用 kubediagram MCP Server

# 重點回顧

# 參考資料