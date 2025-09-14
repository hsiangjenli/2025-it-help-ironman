# 介紹

昨天已經實際操作過 MCP Server，今天不免俗的要來實做一下，網路上有很多 MCP Library 可以協助開發人員快速的開發 MCP 工具，像是 Antropic 的 [`modelcontextprotocol/python-sdk`](https://github.com/modelcontextprotocol/python-sdk)，但是對於開發者來說，爲了 LLM 還要額外去開發 MCP 相關的程式碼其實跟當初 MCP 出現的初衷背道而馳（目的就是要統一不同 LLM 的 Function Calling 機制），所以今天要介紹一個更簡單的工具 [`fastmcp`](https://github.com/jlowin/fastmcp)，這個工具可以直接把原本的 OpenAPI（或是 FastAPI）轉換成 MCP 的介面，讓開發者可以只需要專注在 API 的開發上。

# 實際使用 fastmcp 進行 MCP 開發

![20250909215700](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250909215700.png)

詳細程式碼請參考 [`hsiangjenli/python-mcp-template`](https://github.com/hsiangjenli/python-mcp-template)，裡面包含了如何從 FastAPI 轉換成 MCP 以及將 MCP 容器化成 Docker Image。

## 實際拉 Repo 下來

```shell
git clone https://github.com/hsiangjenli/python-mcp-template
cd python-mcp-template
```

### 配置 python 虛擬環境

```shell
uv sync
```

### 建立 FastAPI 以及轉換成 MCP 格式的程式碼

```python
# main.py
from fastapi import FastAPI
from fastmcp import FastMCP
from mcp_tools.schemas import NewEndpointRequest, NewEndpointResponse

app = FastAPI(
    title="Python MCP Template",
    description="A template for creating MCP-compliant FastAPI services.",
    version="0.1.0",
)


@app.post(
    "/new/endpoint/", operation_id="new_endpoint", response_model=NewEndpointResponse
)
async def new_endpoint(request: NewEndpointRequest):
    return {"message": f"Hello, {request.name}!"}


mcp = FastMCP.from_fastapi(app=app)

if __name__ == "__main__":
    mcp.run()
```

```python
# schemas.py
from pydantic import BaseModel, Field


class NewEndpointResponse(BaseModel):
    message: str = Field(..., description="A welcome message.", example="Hello, world!")


class NewEndpointRequest(BaseModel):
    name: str = Field(
        ..., description="The name to include in the message.", example="developer"
    )
```

### 在本地運行

```shell
uv run --with fastmcp fastmcp run mcp_tools/main.py
```

看到下面的畫面代表成功運行～

![20250909220540](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250909220540.png)

### 在 VSCode 中配置 MCP

![20250909221218](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250909221218.png)

因爲我們設定是使用 STDIO，所以設定 MCP Server 的 json 檔案會長像下面這樣：

- `run` 是 uv 底下的指令，意思是讓程式在 uv 的虛擬環境中執行
- `--with fastmcp` 是 uv 的參數，意思是讓 uv 在執行程式前額外載入 fastmcp
- `fastmcp run mcp_tools/main.py` 是實際啓動 MCP 的指令

```json
{
  "servers": {
    "demo-my-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--with", "fastapi",
        "fastmcp", "run",
        "mcp_tools/main.py"
      ],
      "cwd": "${workspaceFolder}/python-mcp-template"
    }
  },
  "inputs": []
}
```

- 在 VSCode 會看到 MCP Running 的提示

### 透過 GitHub Copilot 確認是否可以使用

![20250909223719](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250909223719.png)

# 重點回顧

- 透過 `fastmcp` 可以快速的將 FastAPI 轉換成 MCP 的介面
- 介紹了如何在 VSCode 中配置 MCP，以及啓動 MCP Server 的參數所代表的意義
- 使用 GitHub Copilot 來測試 MCP 是否可以正常運作

# 參考資料

- [FastAPI 🤝 FastMCP](https://gofastmcp.com/integrations/fastapi)
- [hsiangjenli/python-mcp-template](https://github.com/hsiangjenli/python-mcp-template)