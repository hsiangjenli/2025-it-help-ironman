# 介紹

# Unsloth 介紹

Unsloth 是一款讓 LLM fine-tuning 變地更快、更省記憶體的開源工具，在 [GitHub](https://github.com/unslothai/notebooks) 上提供了很多 Colab 模版，提供給使用者可以直接在 Colab 上進行微調訓練。

## 模型微調的方法介紹

- LoRA: Fine-tunes small, trainable matrices in 16-bit without updating all model weights.  
- QLoRA: Combines LoRA with 4-bit quantization to handle very large models with minimal resources. 

### 數學符號

### 視覺化呈現矩陣計算


# 重點回顧

- 介紹 Unsloth 這個工具可以快速對 LLM 模型進行微調的方法及優缺點（LoRA 和 QLoRA）
- 介紹 LoRA 和 QLoRA 的原理及其優缺點
- 了解不同模型大小做微調所需要的記憶體（Unsloth 官網提供）

# 參考資料

- [What is LoRA (low-rank adaption)?](https://www.ibm.com/think/topics/lora)
- [Are You Still Using LoRA to Fine-Tune Your LLM?](https://onmine.io/are-you-still-using-lora-to-fine-tune-your-llm/)
- [unslothai/notebooks](https://github.com/unslothai/notebooks)
- [【LLM專欄】All about Lora](https://axk51013.medium.com/llm%E5%B0%88%E6%AC%84-all-about-lora-5bc7e447c234)