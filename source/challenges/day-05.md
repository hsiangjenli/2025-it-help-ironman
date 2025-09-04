
# 介紹

前一天的鐵人賽挑戰文章介紹的可以協助設定 Global Instruction 的工具 [10xrules](https://10xrules.ai)。但單純使用這個工具來產生 Global Instruction 可能還不夠，因為在真正的開發過程中，每個 Task 都還需要有自己的 Context。

這個 Context 可能是過去的對話紀錄、相關文件、程式碼片段等...。但要突然要開發人員「無中生有」這些 Context 也是一件很困難的事情，這篇文章要介紹一個叫做 `coleam00/context-engineering-intro` 的專案，這個專案提供了一個簡單的範例，讓開發人員可以藉由實際操作來了解如何在開發過程中會有哪些 Context 需要被提供給 LLM。

# `coleam00/context-engineering-intro` 介紹

這個 Repo 的主要 2 大功能：

1. 透過 LLM 產生產品需求提示（Product Requirement Prompt，PRP）
1. 藉由前面產生的 PRP 來進行程式開發

## 專案結構

首先，這份專案是設計給 Claude Code 使用的，但是也是可以透過其它 AI Code Assistant（GitHub Copilot）工具來使用的。

```shell
.
├── .claude
│   ├── commands
│   │   ├── execute-prp.md # 執行 PRP 的提示
│   │   └── generate-prp.md # 產生 PRP 的提示
│   └── settings.local.json
├── claude-code-full-guide # 暫時略過
├── CLAUDE.md # Global Instruction 設定
├── examples
├── .gitattributes
├── .gitignore
├── INITIAL_EXAMPLE.md
├── INITIAL.md # 任務說明（簡單提供，後續會使用 /generate-prp 產出更完善的 PRP）
├── LICENSE
├── PRPs
│   ├── EXAMPLE_multi_agent_prp.md
│   └── templates
│       └── prp_base.md # PRP 基本模版
├── README.md
└── use-cases # 暫時略過
```


# 重點回顧

> **補充說明**
> 
> 目前的 `CLAUDE.md` 對應的是 `AGENTS.md`。[`AGENTS.md`](https://agents.md/) 是目前多家廠商的共識，就像過去開發人員都會把程式的基本介紹寫在 `README.md` 一樣，`AGENTS.md` 是專門提供給 LLM 的開發指引。截至目前，已經有 Codex、Cursor、Gemini CLI、GitHub Copilot 加入這個供應商中立的標準協議（但 Claude Code 還沒）。若是想看其它開發人員的 `AGENTS.md` 可以到 [GitHub Search](https://github.com/search?q=path%3AAGENTS.md&type=code) 查看。

# 參考資料

- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)
- [AGENTS.md](https://agents.md/)
- [GitHub Search: AGENTS.md](https://github.com/search?q=path%3AAGENTS.md&type=code)
