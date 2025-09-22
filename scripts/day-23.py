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
