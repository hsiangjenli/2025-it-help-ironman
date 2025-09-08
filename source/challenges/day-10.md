# 介紹

前一天介紹了 Unsloth 這個工具可以快速對 LLM 模型進行微調的方法及優缺點（LoRA 和 QLoRA）。今天要實際操作看看如何準備一份簡單的資料集來對 llama3.2:3b 進行微調，並且將訓練完的模型轉換成 Ollama 可用的格式並且在本機運行。

# 操作

[![](https://colab.research.google.com/assets/colab-badge.svg)](https://hsiangjenli.github.io/2025-it-help-ironman/challenges/Llama3_2_%283B%29_Unsloth.html)

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

### 部分程式碼

#### 載入模型

```python
from unsloth import FastLanguageModel
import torch
max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

# 4bit pre quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/Meta-Llama-3.1-8B-bnb-4bit",      # Llama-3.1 2x faster
    "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    "unsloth/Meta-Llama-3.1-70B-bnb-4bit",
    "unsloth/Meta-Llama-3.1-405B-bnb-4bit",    # 4bit for 405b!
    "unsloth/Mistral-Small-Instruct-2409",     # Mistral 22b 2x faster!
    "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
    "unsloth/Phi-3.5-mini-instruct",           # Phi-3.5 2x faster!
    "unsloth/Phi-3-medium-4k-instruct",
    "unsloth/gemma-2-9b-bnb-4bit",
    "unsloth/gemma-2-27b-bnb-4bit",            # Gemma 2x faster!

    "unsloth/Llama-3.2-1B-bnb-4bit",           # NEW! Llama 3.2 models
    "unsloth/Llama-3.2-1B-Instruct-bnb-4bit",
    "unsloth/Llama-3.2-3B-bnb-4bit",
    "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",

    "unsloth/Llama-3.3-70B-Instruct-bnb-4bit" # NEW! Llama 3.3 70B!
] # More models at https://huggingface.co/unsloth

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-3B-Instruct", # or choose "unsloth/Llama-3.2-1B-Instruct"
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
```

- 使用 `load_in_4bit` 就代表使用 4-bit 精度來減少記憶體使用

#### 設定 PEFT（LoRA）的參數

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)
```

- 把 base model 套上 LoRA adapter
- 依照原本 Unsloth 模版的設定來進行，沒特別調整

#### 資料集格式

```shell
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: 26 July 2024

<|eot_id|><|start_header_id|>user<|end_header_id|>

**Iterators terminating on the shortest input sequence:**<|eot_id|><|start_header_id|>assistant<|end_header_id|>

**在最短輸入序列 (shortest input sequence) 處終止的疊代器：**<|eot_id|>
```

#### 訓練參數設定

```python
from trl import SFTConfig, SFTTrainer
from transformers import DataCollatorForSeq2Seq
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    data_collator = DataCollatorForSeq2Seq(tokenizer = tokenizer),
    packing = False, # Can make training 5x faster for short sequences.
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        # num_train_epochs = 1, # Set this for 1 full training run.
        max_steps = 60,
        learning_rate = 2e-4,
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none", # Use this for WandB etc
    ),
)
```

![20250908003127](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250908003127.png)

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

- 瞭解使用 Unsloth 來對 LLM 模型進行微調所需要的記憶體需求
- 準備一份簡單的資料集來對 llama3.2:3b 進行微調
- 將訓練完的模型轉換成 GGUF 可用的格式
- 處理 Unsloth 微調後的模型轉換成 GGUF 的方法（手動編譯 llama.cpp）

# 參考資料

- [unslothai/notebooks](https://github.com/unslothai/notebooks)
- [How to convert my fine-tuned model to .gguf ?](https://www.reddit.com/r/LocalLLaMA/comments/1amjx77/how_to_convert_my_finetuned_model_to_gguf/)
