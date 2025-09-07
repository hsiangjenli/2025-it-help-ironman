# 介紹

前一天介紹了 Unsloth 這個工具可以快速對 LLM 模型進行微調的方法及優缺點（LoRA 和 QLoRA）。今天要實際操作看看如何準備一份簡單的資料集來對 llama3.2:3b 進行微調，並且將訓練完的模型轉換成 Ollama 可用的格式並且在本機運行。

# 操作

## 微調究竟需要多少的記憶體？

| Model parameters | QLoRA (4-bit) VRAM | LoRA (16-bit) VRAM |
| ---------------- | ------------------ | ------------------ |
| 3B               | 3.5 GB             | 8 GB               |
| 7B               | 5 GB               | 19 GB              |
| 8B               | 6 GB               | 22 GB              |
| 9B               | 6.5 GB             | 24 GB              |
| 11B              | 7.5 GB             | 29 GB              |
| 14B              | 8.5 GB             | 33 GB              |
| 27B              | 22GB               | 64GB               |
| 32B              | 26 GB              | 76 GB              |
| 40B              | 30GB               | 96GB               |
| 70B              | 41 GB              | 164 GB             |
| 81B              | 48GB               | 192GB              |
| 90B              | 53GB               | 212GB              |
| 405B             | 237 GB             | 950 GB             |

> **表格來源**： [Unsloth 官網提供](https://docs.unsloth.ai/get-started/beginner-start-here/unsloth-requirements)

## 微調開始

- 模型：llama3.2:3b
- 微調方法：QLoRA（爲求快速，使用 4-bit 精度可以減少記憶體使用，但也會影響到模型的表現）
- 資料集：[python-docs-zh-tw](https://github.com/python/python-docs-zh-tw)

### 資料集準備

- [`data.json`](https://hsiangjenli.github.io/2025-it-help-ironman/_static/data/data.json) 已上傳至 GitHub可直接下載
![20250907002650](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250907002650.png)

### 操作畫面截圖
  

## 將訓練完的模型轉換成 GGUF 可用的格式

不知道為什麼 Unsloth 的 llama.cpp 轉換成 GGUF 時會出現問題，要先自己手動 clone llama.cpp 在本機編譯後才能成功轉換，而且不知道為什麼 `convert_hf_to_gguf.py` 的格式會跑掉，所以只好自己手動下載最新的 `convert_hf_to_gguf.py` 來使用。

```shell
!git clone --recursive https://github.com/ggerganov/llama.cpp
!(cd llama.cpp; cmake -B build;cmake --build build --config Release)
```

```shell
!wget https://raw.githubusercontent.com/ggml-org/llama.cpp/refs/heads/master/convert_hf_to_gguf.py -O llama.cpp/convert_hf_to_gguf.py
if True: model.save_pretrained_gguf("/content/drive/MyDrive/lora_model/q4_k_m", tokenizer, quantization_method = "q4_k_m")
```

![20250908001335](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250908001335.png)

# 重點回顧

- 準備一份簡單的資料集來對 llama3.2:3b 進行微調
- 將訓練完的模型轉換成 GGUF 可用的格式並且在本機運行

# 參考資料

- [unslothai/notebooks](https://github.com/unslothai/notebooks)
- [How to convert my fine-tuned model to .gguf ?](https://www.reddit.com/r/LocalLLaMA/comments/1amjx77/how_to_convert_my_finetuned_model_to_gguf/)
