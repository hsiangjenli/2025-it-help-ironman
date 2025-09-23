# 介紹

# 使用 Ollama 以及 LangGraph 實作 Agent Server

本次使用 [`a2aproject/a2a-samples`](https://github.com/a2aproject/a2a-samples) 中的 LangGraph 範例來示範來操作如和使用 Ollama 作爲 LLM backend 並且結合 `a2a-sdk` 來實作一個簡單的 Agent Server。

## 下載範例程式碼 + 準備環境

```shell
git clone https://github.com/a2aproject/a2a-samples.git
cd a2a-samples/samples/python/agents/langgraph
uv sync
```

## 架構介紹

```shell
app/
├── __init__.py         
├── __main__.py # 主程式，啟動 A2A 伺服器       
├── agent.py # 核心 AI Agent（使用 LangGraph）
├── agent_executor.py # Agent Executor，負責管理整個 Agent 的生命週期
└── test_client.py 
```

- `agent.py`：定義 Agent 的行爲，這邊使用 LangGraph 來實作
- `agent_executor.py`：定義 Agent Executor，負責管理整個 Agent 的生命週期

### `agent.py`

- 建立一個 LangGraph Agent 的實例（`CurrencyAgent`）

### `agent_executor.py`

```python
class AgentExecutor(ABC):
    """Agent Executor interface.

    Implementations of this interface contain the core logic of the agent,
    executing tasks based on requests and publishing updates to an event queue.
    """

    @abstractmethod
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Execute the agent's logic for a given request context.

        The agent should read necessary information from the `context` and
        publish `Task` or `Message` events, or `TaskStatusUpdateEvent` /
        `TaskArtifactUpdateEvent` to the `event_queue`. This method should
        return once the agent's execution for this request is complete or
        yields control (e.g., enters an input-required state).

        Args:
            context: The request context containing the message, task ID, etc.
            event_queue: The queue to publish events to.
        """

    @abstractmethod
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Request the agent to cancel an ongoing task.

        The agent should attempt to stop the task identified by the task_id
        in the context and publish a `TaskStatusUpdateEvent` with state
        `TaskState.canceled` to the `event_queue`.

        Args:
            context: The request context containing the task ID to cancel.
            event_queue: The queue to publish the cancellation status update to.
        """
```

- 一個 Agent Executor 的介面，需要實作 `execute` 以及 `cancel` 方法

```python
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)  # ⭐ (1) 建立一個新的 Task
            await event_queue.enqueue_event(task) # ⭐ (2) 發布到事件佇列
        updater = TaskUpdater(event_queue, task.id, task.context_id) # ⭐ (3) 建立一個 TaskUpdater 來更新 Task 狀態
        try:
            # ⭐ (4) 處理過程中會持續的 stream response
            async for item in self.agent.stream(query, task.context_id):
                is_task_complete = item['is_task_complete']
                require_user_input = item['require_user_input']

                if not is_task_complete and not require_user_input:
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            item['content'],
                            task.context_id,
                            task.id,
                        ),
                    )
                elif require_user_input:
                    await updater.update_status(
                        TaskState.input_required,
                        new_agent_text_message(
                            item['content'],
                            task.context_id,
                            task.id,
                        ),
                        final=True,
                    )
                    break
                else:
                    await updater.add_artifact(
                        [Part(root=TextPart(text=item['content']))],
                        name='conversion_result',
                    )
                    await updater.complete()
                    break

        except Exception as e:
            logger.error(f'An error occurred while streaming the response: {e}')
            raise ServerError(error=InternalError()) from e
```

## 調整設定

### 修改環境變數

建立 `.env` 檔案，設定使用 Ollama：

```shell
# .env
model_source=ollama
API_KEY=your_api_key_here
TOOL_LLM_URL=http://localhost:11434/api/chat
TOOL_LLM_NAME=llama3.2:3b
```

### 程式碼調整 (可選)

如果要完全移除 Google API 檢查，可以註解掉以下程式碼：

```python
# 在 __main__.py 中註解掉
# if not os.getenv('GOOGLE_API_KEY'):
#     raise MissingAPIKeyError(
#         'GOOGLE_API_KEY environment variable not set.'
#     )
```

### 確認 Ollama 設定

```shell
# 確認 Ollama 服務運行
ollama list

# 如果模型不存在，下載模型
ollama pull llama3.2:3b

# 測試模型回應
ollama run llama3.2:3b "Hello, how are you?"
```

## 啓動 Agent Server

```shell
uv run app
```
可以在 [http://localhost:10000/.well-known/agent.json](http://localhost:10000/.well-known/agent.json) 看到 Agent Card

![20250923203324](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250923203324.png)

## 測試 Agent Server

```shell
# 測試 Agent Server

## 1. 測試 Ollama API 連線

首先確認 Ollama 服務正常運作：

```shell
# 測試 ollama API
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [
      {
        "role": "user",
        "content": "Hello"
      }
    ]
  }'
```

![20250923200419](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250923200419.png)

## 2. 測試 A2A Agent Server

### 使用內建測試客戶端

```shell
uv run app/test_client.py
```

### 使用 curl 測試同步請求

```shell
curl -X POST http://localhost:10000 \
  -H "Content-Type: application/json" \
  -d '{
    "id": "12113c25-b752-473f-977e-c9ad33cf4f56",
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
        "message": {
            "kind": "message",
            "messageId": "120ec73f93024993becf954d03a672bc",
            "parts": [
                {
                    "kind": "text",
                    "text": "how much is 10 USD in INR?"
                }
            ],
            "role": "user"
        }
    }
}'
```

## 3. 問題排除

### 常見錯誤和解決方案

1. **Internal error (-32603)**:
   - 檢查 Ollama 服務是否運行：`ollama list`
   - 確認模型已下載：`ollama pull llama3.2:3b`
   - 檢查 `.env` 檔案設定

2. **連線錯誤**:
   - 確認 Ollama API 在 `http://localhost:11434` 運行
   - 測試 Ollama API 連線（如上面的測試）

3. **模型不存在**:
   ```shell
   ollama pull llama3.2:3b
   ollama list | grep llama3.2
   ```
```

![20250923200419](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250923200419.png)

# 重點回顧

## 🎯 核心概念

1. **A2A 協議**: Agent-to-Agent 通訊協議，標準化 AI 代理間的互動
2. **事件驅動架構**: 使用事件佇列 (EventQueue) 而非直接回傳結果
3. **分層設計**: 
   - `agent.py`: 純 AI 邏輯層
   - `agent_executor.py`: 協議適配層
   - `__main__.py`: 伺服器啟動層

## 🔧 技術要點

### Agent Executor 設計模式
- **`execute` 方法**: 不回傳值，透過事件佇列發布結果
- **任務生命週期**: `working` → `input_required`/`completed`
- **串流處理**: 即時更新任務狀態

### Ollama 整合
- **模型選擇**: 支援多種本地 LLM
- **API 統一**: 使用 OpenAI 相容的 API 格式
- **無需外部 API**: 完全本地化部署

## 💡 學習收穫

1. **事件驅動 vs 傳統請求回應**: 更適合長時間運行的 AI 任務
2. **協議抽象**: 將業務邏輯與通訊協議分離
3. **本地 LLM 部署**: 在地化 AI 服務的實務應用

## 📈 擴展可能

- 支援多模態輸入 (圖片、音訊)
- 實作任務取消功能
- 添加更多工具和 API 整合
- 實作持久化記憶存儲

# 參考資料

## 🔗 官方資源

- [A2A Project GitHub](https://github.com/a2aproject/a2a-samples) - A2A 協議範例專案
- [LangGraph 官方文件](https://langchain-ai.github.io/langgraph/) - LangGraph 框架文件
- [Ollama 官方網站](https://ollama.ai/) - 本地 LLM 運行平台

## 📚 相關技術文件

- [A2A Protocol Specification](https://a2aproject.org/) - A2A 協議規範
- [Frankfurter API](https://www.frankfurter.app/) - 匯率查詢 API
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Web API 框架
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 資料驗證庫

## 🛠️ 開發工具

- [uv](https://github.com/astral-sh/uv) - Python 套件管理工具
- [Uvicorn](https://www.uvicorn.org/) - ASGI 伺服器
- [httpx](https://www.python-httpx.org/) - HTTP 客戶端庫