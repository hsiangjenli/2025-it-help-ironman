# 介紹

聽過 `robots.txt` 嗎？這是一個放在網站根目錄的檔案，用來告訴搜尋引擎哪些頁面可以被爬取，哪些則應該避免。在傳統搜尋引擎的運作模式裡，`robots.txt` 幾乎是網站的標配。然而，隨著 LLM 越來越普及，單靠 `robots.txt` 已經不完全符合需求。

新的標準 `llms.txt` 就是為了這個目的而提出的。它的作用不是限制，而是明確告訴 LLM 網站底下哪些路徑對應到什麼類型的內容。相比單純阻止 AI 爬蟲，更有效率的方式是直接提供內容的結構化描述。這樣一來，模型能更快、更準確地找到需要的資訊，而網站也能清楚表達哪些內容希望被模型理解和使用。

# 格式介紹

- 檔案存放位置：根目錄下的 `llms.txt`
- 格式：Markdown
- 內容格式：
  - `# H1 標題（必要）`：網站或專案名稱
    - `> 描述（選填）`：網站或專案的簡短描述
    - `補充說明（選填）`：可以包含任何補充說明
  - `## H2 分類`：像是 `## Docs`、`## Examples` 等等...
    - `- [連結名稱](網址): 選填描述`

像是下面這樣：

```markdown
# 示範網頁

> 簡單的網站來示範 llms.txt 格式

這是一些補充說明，可以包含任何你想要的內容

## Docs
- [有額外描述](https://example.com/docs/getting-started): 提供額外的文字描述
- [單純連結](https://example.com/docs/installation)
```

## 其它 `llms.txt` 範例

![20250908215800](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250908215800.png)

在 [llms.txthub](https://llmstxthub.com/) 收集了很多網站的 `llms.txt`，可以看看其它網站是怎麼寫的。

# 重點回顧

- `llms.txt` 與 `robots.txt` 的差異
  - `llms.txt` 著重於理解網頁重點內容
  - `robots.txt` 著重於爬取規則
- 介紹 `llms.txt` 的格式與範例
- 提供一個收錄多個網站 `llms.txt` 的網站


# 參考資料

- [LLMs.txt 是什麼？](https://pagerank.ing/what-is-llms-txt/)
- [The /llms.txt file](https://llmstxt.org/)
- [LLMs.txt 是什麼：AI 時代網站內容保護新規範](https://www.sonar-inc.com/what-is-llms-txt/)