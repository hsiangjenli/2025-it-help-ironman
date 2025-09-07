# 介紹

# Unsloth 介紹

Unsloth 是一款讓 LLM fine-tuning 變地更快、更省記憶體的開源工具，在 [GitHub](https://github.com/unslothai/notebooks) 上提供了很多 Colab 模版，提供給使用者可以直接在 Colab 上進行微調訓練。

## 模型微調的方法介紹

因爲微調的範圍很廣，不是三言兩語可以說清楚的。這邊先做簡單的微調假設：（1）希望微調後的模型能夠在某個特定任務上表現更好；（2）沒有要壓縮模型大小（如：蒸餾、剪枝等）。基於以上假設，常見的微調方法有三種：

1. 全模型微調（Full-model Tuning）：模型的所有權重都會被更新
1. 參數高效微調（Parameter-Efficient Fine-Tuning，PEFT）：凍結大部分的權重，只調整少量或特定的參數
1. 提示微調（Prompt Tuning/Soft Prompting）：不改變模型權重，只是調整輸入的提示詞

### PEFT @ Unsloth

在 Unsloth 裡面，主要是使用 PEFT 的方法來進行微調，主要是因爲使用全模型微調的話，對於記憶體的需求會非常高，同時全模型微調不一定會帶來更好的效果。Unsloth 目前支援兩種 PEFT 的方法：

- LoRA（Low-Rank Adaptation）：保持原始模型權重，只訓練少量低秩矩陣，透過在原有權重旁加上調整項 $\Delta W$ 進行微調，可以減少記憶體的使用量
- QLoRA（Quantized LoRA）：在 LoRA 的基礎上，進一步將模型量化到 4-bit，可以降低記憶體的使用量

### LoRA 基本原理

|  數學符號  | 解釋                       |
|:----------:|:---------------------------|
|    $W'$    | 更新後的權重矩陣           |
|    $W$     | 原始權重矩陣               |
| $\Delta W$ | 調整項（由 LoRA 訓練得到） |
|   $A, B$   | 低秩分解出的可訓練的矩陣   |

- $W' = W + \Delta{W}$
- $\Delta{W} = A \times B$

#### 原始矩陣 $W$

$
W =
\underbrace{\left[\begin{array}{ccccccc}
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\end{array}\right]}_{n\times n}
$

#### 低秩分解 $\Delta W = AB$
$
\Delta W = 
\underbrace{\left[\begin{array}{c}
\square \\
\square \\
\square \\
\square \\
\square \\
\square \\
\square \\
\end{array}\right]}_{n\times r}
\times
\underbrace{\left[\begin{array}{ccccccc}
\square & \square & \square & \square & \square & \square & \square \\
\end{array}\right]}_{r\times n}
= \underbrace{\left[\begin{array}{ccccccc}
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\end{array}\right]}_{n\times n}
$

#### 更新後的權重矩陣 $W' = W + \Delta W$

$
W' =
\underbrace{\left[\begin{array}{ccccccc}
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\square & \square & \square & \square & \square & \square & \square \\
\end{array}\right]}_{n\times n}
\;+\;
\left(
\underbrace{\left[\begin{array}{c}
\square \\ \square \\ \square \\ \square \\ \square \\ \square \\ \square
\end{array}\right]}_{n\times r}
\;\times\;
\underbrace{\left[\begin{array}{ccccccc}
\square & \square & \square & \square & \square & \square & \square
\end{array}\right]}_{r\times n}
\right)
$

## 實際透過 Unsloth 進行微調

### 微調究竟需要多少的記憶體？

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

### 微調開始

本次爲求方便選用 llama3.2:3b + QLoRA 進行微調

#### 資料集

本次操作的目的是希望可以簡單的操作 LoRA，資料集選擇簡單易點，使用 [python-docs-zh-tw](https://github.com/python/python-docs-zh-tw)，因爲資料結構很簡單，po 檔案的 `msgid` 是英文句子，`msgstr` 是對應的中文翻譯。


# 重點回顧

- 介紹 Unsloth 這個工具可以快速對 LLM 模型進行微調的方法及優缺點（LoRA 和 QLoRA）
- 了解不同模型大小做微調所需要的記憶體（[Unsloth 官網提供](https://docs.unsloth.ai/get-started/beginner-start-here/unsloth-requirements)） 

# 參考資料

- [What is LoRA (low-rank adaption)?](https://www.ibm.com/think/topics/lora)
- [Are You Still Using LoRA to Fine-Tune Your LLM?](https://onmine.io/are-you-still-using-lora-to-fine-tune-your-llm/)
- [unslothai/notebooks](https://github.com/unslothai/notebooks)
- [【LLM專欄】All about Lora](https://axk51013.medium.com/llm%E5%B0%88%E6%AC%84-all-about-lora-5bc7e447c234)