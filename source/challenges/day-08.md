# 介紹

- Ollama 是一個開源工具，可讓你在自己的電腦上（Windows、MacOS、Linux）執行 LLM（大型語言模型）
- 還有 [python 工具](https://github.com/ollama/ollama-python)可以使用，並且與 OpenAI 的 API 兼容。

# 安裝與使用 Ollama 

## 使用 Docker 安裝 Ollama

```shell
docker pull ollama/ollama:0.11.6
```

```shell
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name my-ollama ollama/ollama:0.11.6
```

## 使用 Ollama CLI

### 先進入容器內

```shell
docker exec -it my-ollama bash
```

### 確認 Ollama 版本與指令是否正常

```shell
ollama --version
```

```shell
ollama
```

### 下載模型權重 Pull Model

```shell
ollama pull gemma3:270m
```

### 開始 Chat 模式

```shell
docker exec -it my-ollama ollama chat
```

### 離開 Chat 模式

### 與 OpenAI API 進行整合

```shell
pip install openai
```

```python
import openai
```

# 回顧

- 透過 Docker 快速部署 Ollama 服務
- 下載模型權重 & 使用 Ollama CLI 進行互動
- 如何與 OpenAI API 進行整合

# 參考資料