# 介紹

聽過 `robots.txt` 嗎？這是網站用來告訴搜尋引擎哪些頁面可以被爬取的檔案。隨著 LLM 的普及，除了使用 `robots.txt` 告訴機器人哪些頁面可以被爬取之外，還有一個新的標準叫做 `llms.txt`，用來告訴 LLM 每個路徑下的頁面是什麼類型的內容。

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