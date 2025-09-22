# 介紹

昨天已經介紹了 Agent2Agent 協議的背景與動機，今天要開始逐步實作一個簡單的 Agent Server，先從核心概念與 Agent Card 開始。

# Agent2Agent Core Concepts

## 角色

![](https://a2a-protocol.org/latest/assets/a2a-actors.png)

- **User**：使用者，發起對話的人
- **A2A Client Agent**：使用者與遠端代理溝通的橋樑
- **A2A Server Agent**：負責處理 Client Agent 發來的請求

## 互動元件

- **Agent Card**：描述 Agent 能力、端點、驗證方式的文件，讓 Client Agent 知道如何與其溝通
- **Task**：代表使用者的一個請求（工作單位），具有唯一的 ID 與明確的生命週期，方便追蹤長時間或多輪互動
- **Message**：User 與 Agent 之間的溝通內容（上下文、指令、問題、回覆等等...）
- **Part**：在 Message 或是 Artifact 中的最小內容單位，有 `TextPart`、`FilePart`、`DataPart` 等...
- **Artifact**：由 Agent 在任務中產生的結構化輸出

# 寫一個簡單的 Agent Card

## 基本概念

- Agent Card 是一個 JSON 檔案
- 位置是在 `.well-known/agent-card`

## 需要的欄位

- **name**：Agent 的名稱
- **description**：Agent 的描述
- **version**：Agent Card 的版本
- **url**：Agent 的 API 端點
- **capabilities**：Agent 支援的功能（例如 streaming、pushNotifications
- **defaultInputModes**：預設的輸入模式
- **defaultOutputModes**：預設的輸出模式
- **skills**：Agent 支援的技能

## Python 範例

```shell
uv add a2a-sdk[all]
```

```python
from a2a.types import AgentCard

agent_card = AgentCard(
    name="Black Cat",
    description="A mischievous black cat that brings both luck and chaos.",
    url="暫時略過....",
    version="1.0.0",
    protocol_version="0.3.0",
    provider=AgentProvider(organization="Ollama", url="https://ollama.com"),
    preferred_transport="JSONRPC",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(
        streaming=True, pushNotifications=False, stateTransitionHistory=False
    ),
    skills=[
        AgentSkill(
            id="knock_over_vase",
            name="Knocked Over Vase",
            description="Causes minor chaos by knocking over vases.",
            examples=[
                "When the desk is tidy, the black cat may knock over a vase to create some chaos."
            ],
            tags=["chaos"],
        ),
    ],
)
```

## 完整程式碼

```python
# day-23.py
from typing import List
import uvicorn

from a2a.types import AgentCard, AgentSkill, AgentProvider, AgentCapabilities
from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

# 1) 建 AgentCard
agent_card = AgentCard(
    name="Black Cat",
    description="A mischievous black cat that brings both luck and chaos.",
    url="暫時略過....",
    version="1.0.0",
    protocol_version="0.3.0",
    provider=AgentProvider(organization="Ollama", url="https://ollama.com"),
    preferred_transport="JSONRPC",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(
        streaming=True, pushNotifications=False, stateTransitionHistory=False
    ),
    skills=[
        AgentSkill(
            id="knock_over_vase",
            name="Knocked Over Vase",
            description="Causes minor chaos by knocking over vases.",
            examples=[
                "When the desk is tidy, the black cat may knock over a vase to create some chaos."
            ],
            tags=["chaos"],
        ),
    ],
)


# 2) 簡單 mock executor
class BlackCatExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        # 你可以在這裡用 event_queue 推進度 / 產物；先簡化
        # await event_queue.add_text("meow")  # 若要串流
        return

    async def cancel(self, context, event_queue):
        return


if __name__ == "__main__":
    # 3) 用 DefaultRequestHandler + InMemoryTaskStore
    handler = DefaultRequestHandler(
        agent_executor=BlackCatExecutor(), task_store=InMemoryTaskStore()
    )

    # 4) 建立 A2A 應用，然後 **.build()** 出 ASGI app
    a2a_app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=handler,
    )
    app = a2a_app.build()

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```shell
uv run day-23.py
```

- http://0.0.0.0:8000/.well-known/agent.json

![20250922231258](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250922231258.png)

> **補充說明**
>
> 本次的範例的 `url` 欄位沒有設定（單純用來展示起好一個 Agent Server 可以看到的 Agent Card）

# 重點回顧

- Agent2Agent 的核心概念
- Agent Card 的結構與必要欄位
- 如何用 Python SDK 建立一個簡單的 Agent Card（模型是 Mock 的）

# 參考資料

- [Core Concepts and Components in A2A](https://a2a-protocol.org/latest/topics/key-concepts/)
- [Multi-Agent Communication with the A2A Python SDK](https://towardsdatascience.com/multi-agent-communication-with-the-a2a-python-sdk/)