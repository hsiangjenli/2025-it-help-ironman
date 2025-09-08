# 介紹

前面已經簡單介紹如何使用 Ollama 指令來下載與運行模型。但在操作的過程中，會發現有些模型的回覆風格不滿意，又或者發現部分模型由於參數量較小，關於特定領域的知識不夠豐富，總是無法給出滿意的答案。在 Hugging Face 上有專門的團隊，例如臺大的 [MiuLab 團隊](https://github.com/MiuLab/Taiwan-LLM)，針對 llama3 進行微調訓練，讓模型能夠回答臺灣的問題，又或者是臺灣自發性的本土團隊 [Twinkle AI](https://huggingface.co/twinkle-ai) 訓練出來具有 Reasoning 的小模型。

這篇會更詳細介紹如何使用 Modelfile 來客製化模型以及如何將 Hugging Face 的模型轉換為 Ollama 可用的格式，並在本機運行這些模型。

# 實際操作

## 讓 Ollama 模型變成你想要的形狀 - Modelfile

### 常用參數

| 指令         | 說明                               |
|:-------------|:-----------------------------------|
| FROM（必填） | 定義要使用的基礎模型               |
| PARAMETER    | 設定 Ollama 執行模型時的參數       |
| TEMPLATE     | 要傳送給模型的完整 Prompt 範本     |
| SYSTEM       | 指定會放入範本中的系統訊息         |
| ADAPTER      | 定義要套用到模型的 (Q)LoRA adapter |
| LICENSE      | 指定法律授權協議                   |
| MESSAGE      | 指定訊息歷史（例如對話紀錄）       |

### 查看當前 Ollama Model 的 Modelfile

```shell
ollama show --modelfile gpt-oss:20b
```

這個 Modelfile 定義很多東西簡單列幾個重點：

- FROM：模型來源（blob 檔）
- TEMPLATE：定義 Prompt 格式
  - SYSTEM：系統訊息、身份（ChatGPT，由 OpenAI 訓練出來）
  - Knowledge cutoff：知識截止日期
  - Current date：當前日期
  - Reasoning：推理能力
  - $hasXXXX：工具檢查與啟用
  - .... 太多了 @@

![20250906225218](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250906225218.png)

### 自定義一個 Modelfile 吧！！！

```modelfile
FROM llama3.2:3b

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# 貓設
SYSTEM """
你是一隻聰明、好奇、全身烏黑發亮的貓咪助手「黑色貓貓」
說話風格：機車
口頭禪：適度使用「喵～」但不要太多
回覆語言：繁體中文（台灣）
原則：準確、不要捏造
"""

# 簡單對話模板（讓回覆以「黑色貓貓：」開頭）
TEMPLATE """
{{ if .System }}{{ .System }}{{ end }}
使用者：{{ .Prompt }}
黑色貓貓："""
```

```shell
ollama create black-cat -f Modelfile
```

```shell
ollama run black-cat
```

確認成功建立！！！

![20250906230903](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250906230903.png)

#### 實測黑色貓貓對話

![20250906231114](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250906231114.png)

> 痾... 好像改壞了 😂

## 介紹 Hugging Face GGUF 模型轉換成 Ollama 模型

什麼情況下會需要將 Hugging Face 的 GGUF 模型轉換成 Ollama 模型呢？因爲 Ollama 官方目前只支援部分模型，但是 Hugging Face 上有很多別人根據不同需求微調過的模型（像是專門使用臺灣資料進行微調訓練），這些模型可能更適合你的需求。

### 從 Hugging Face 下載 GGUF 模型

本次使用 `twinkle-ai/Llama-3.2-3B-F1-Reasoning-Instruct-GGUF` 的模型進行示範，這個模型是基於 llama3.2 以及臺灣的資料進行微調訓練的，這個 repo 裡面有很多種版本的模型，主要是精度不同，本次爲求方便，直接下載 `Llama-3.2-3B-F1-Reasoning-Instruct-Q2_K.gguf` 這個檔案（僅 1.49 GB）。


![20250906232458](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250906232458.png)

### 建立 Ollama Modelfile

![20250907000154](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250907000154.png)

爲避免麻煩，筆者直接使用 `ollama show --modelfile llama3.2:3b` 抓官方的 Modelfile，然後把 `FROM` 的部分改成剛剛下載的 GGUF 模型路徑。

```shell
ollama create twinkle-ai/Llama-3.2-3B-F1-Reasoning-Instruct-GGUF -f Modelfile
```

![20250906234029](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250906234029.png)

#### 實測臺灣問題

![20250906234936](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250906234936.png)

> Twinkle AI 的模型具有 Reasoning 能力

> **補充說明**
>
> - 品質好：`F16`（VRAM）、`BF16`（RAM）
> - 速度（慢 -> 快）：`Q8` -> `Q6` -> `Q5` -> `Q4` -> `Q3` -> `Q2`

# 重點回顧

- 如何客製化自己的 Ollama 模型的兩種方式
  - Modelfile：在不改變模型權重的情況下，改變模型的行爲與回覆風格
  - Hugging Face：已經訓練好/微調好的 GGUF 模型，轉換成 Ollama 可用的格式
- 透過 Modelfile 客製化一個身份認同是一隻貓貓的 LLM 模型
- 將 Hugging Face 上的 GGUF 模型轉換成 Ollama 可用的模型
- 簡單提到 F16、BF16、Q8、Q6、Q5、Q4、Q3、Q2 品質與速度的差異

# 參考資料

- [Ollama Model File](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- [Ollama Modelfile 可調參數紀錄](https://okhand.org/zh-tw/posts/ollama-modefile/)
- [twinkle-ai/Llama-3.2-3B-F1-Reasoning-Instruct-GGUF](https://huggingface.co/twinkle-ai/Llama-3.2-3B-F1-Reasoning-Instruct-GGUF)
- [抓別人的 GGUF 模型，用 Ollama 在本機執行！](https://ywctech.net/ml-ai/ollama-import-custom-gguf/)