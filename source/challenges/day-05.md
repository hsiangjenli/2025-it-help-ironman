# 介紹

前一天的鐵人賽挑戰文章介紹的可以協助設定 Global Instruction 的工具 [10xrules](https://10xrules.ai)。但單純使用這個工具來產生 Global Instruction 可能還不夠，因為在真正的開發過程中，每個 Task 都還需要有自己的 Context。

這個 Context 可能是過去的對話紀錄、相關文件、程式碼片段等...。但要突然要開發人員「無中生有」這些 Context 也是一件很困難的事情，這篇文章要介紹一個叫做 `coleam00/context-engineering-intro` 的專案，這個專案提供了一個簡單的範例，讓開發人員可以藉由實際操作來了解如何在開發過程中會有哪些 Context 需要被提供給 LLM。

# `coleam00/context-engineering-intro` 介紹

![20250904212022](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250904212022.png)

這個 [Repo](https://github.com/coleam00/context-engineering-intro) 的主要 2 大功能：

1. 透過 LLM 產生產品需求提示（Product Requirement Prompt，PRP）
1. 藉由前面產生的 PRP 來進行程式開發

## 專案結構

首先，這份專案是設計給 Claude Code 使用的，但是也是可以透過其它 AI Code Assistant（GitHub Copilot）工具來使用的。

```shell
.
├── .claude
│   ├── commands
│   │   ├── execute-prp.md # ⭐ 執行 PRP 的提示
│   │   └── generate-prp.md # ⭐ 產生 PRP 的提示
│   └── settings.local.json
├── claude-code-full-guide # 暫時略過
├── CLAUDE.md # ⭐ Global Instruction 設定
├── examples
├── .gitattributes
├── .gitignore
├── INITIAL_EXAMPLE.md
├── INITIAL.md # ⭐ 任務說明（簡單提供，後續會使用 /generate-prp 產出更完善的 PRP）
├── LICENSE
├── PRPs
│   ├── EXAMPLE_multi_agent_prp.md
│   └── templates
│       └── prp_base.md # ⭐ PRP 基本模版
├── README.md
└── use-cases # 暫時略過
```

這份專案經過時間的演進，裡面的架構比當初使用時更複雜了，不過主要可以聚焦在上面標記 ⭐ 的檔案。各位只需要針對這些檔案進行修改就可以了。

### 需要修改的檔案有：
- `INITIAL.md`：提供任務的基本說明
- `CLAUDE.md`：負責整個專案的 Global Instruction 設定（Optional）
- `PRPs/templates/prp_base.md`：PRP 的基本模版（Optional）

> **補充說明**
> 
> 上面寫著 Optional 是因為這些檔案在原本的 Repo 裡面已經有預設的內容了，可以先嘗試使用預設內容來進行開發，等到熟悉流程之後再根據自己的需求來進行修改。

> **補充說明**
> 
> 目前的 `CLAUDE.md` 對應的是 `AGENTS.md`。[`AGENTS.md`](https://agents.md/) 是目前多家廠商的共識，就像過去開發人員都會把程式的基本介紹寫在 `README.md` 一樣，`AGENTS.md` 是專門提供給 LLM 的開發指引。截至目前，已經有 Codex、Cursor、Gemini CLI、GitHub Copilot 加入這個供應商中立的標準協議（但 Claude Code 還沒）。若是想看其它開發人員的 `AGENTS.md` 可以到 [GitHub Search](https://github.com/search?q=path%3AAGENTS.md&type=code) 查看。

### 產生 PRP 的流程

1. 首先，打開 `INITIAL.md`，根據自己的需求來修改任務說明
2. 接著，使用 `/generate-prp INITIAL.md` 讓 LLM 可以根據 `INITIAL.md` 的內容來產生 PRP
3. 最後，使用 `/execute-prp PRPs/example_prp.md` 來讓 LLM 根據 PRP 的內容來進行程式開發

> **補充說明**
> 
> 在實際操作的過程中，筆者主要是使用 GitHub Copilot 來進行開發，所以嘗試過使用不同的 AI Model 來產出 PRP。根據筆者的經驗，Claude Sonnet 對比 GPT、Gemini 或是其它開源權重的模型，能夠產出更符合需求的 PRP。
> 
> 另外，還有一點貼心建議，在請 AI Model 產出 PRP 的時候可以請它根據需求來按照開發步驟來產出「多個」PRP，這樣會比一次產出「一個」PRP 的內容更加詳細，後續在開發的時候一步一步跟著步驟走，確認每個步驟都符合需求也沒有錯誤的時後再進行下一步。

# 重點回顧

- 使用 `coleam00/context-engineering-intro` 來進行 Context Engineering 實戰
- 快速從 `INITIAL.md` + `/generate-prp INITIAL.md` 產出 PRP
- 提供產出優質 PRP 的小技巧（使用 Claude Sonnet + 拆解任務成小步驟）
- 補充目前 Global Instruction 的標準格式是使用 `AGENTS.md`

# 參考資料

- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)
- [AGENTS.md](https://agents.md/)
- [GitHub Search: AGENTS.md](https://github.com/search?q=path%3AAGENTS.md&type=code)
