# 介紹

筆者是屬於忠實的 PowerPoint 派，即使不斷有新的簡報工具出現（像是 Canva、Google Slide），但還是習慣使用 PowerPoint 來製作簡報。隨著 AI Agent 的興起，開始用有些工具可以自動從文件中產生簡報，像是 [Gamma](https://gamma.app/) 與 [Presenton](https://presenton.ai/) 等工具，這兩個工具分別是付費的服務和開源的專案，兩者都可以透過 AI 來製作簡報。

# Presenton 介紹

[Presenton](https://presenton.ai/) 是一個開源的簡報生成工具（支援 OpenAI、Ollama、Antropic、Gemini 等多種 LLM），可以從文字或是文件中自動生成簡報（包含圖片），並且可以匯出成 PowerPoint 或 PDF 格式。

## 地端安裝 Presenton

![20250916210442](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916210442.png)

- 下載 Image 需要一段時間，超級肥的 Image（約 12GB）

```shell
docker run -it \
    --name presenton \
    -p 5000:80 \
    -e LLM="openai" \
    -e OPENAI_API_KEY="YOUR_API_KEY" \
    -e OPENAI_MODEL="gpt-5-2025-08-07" \
    -e IMAGE_PROVIDER="dall-e-3" \
    -e CAN_CHANGE_KEYS="false" \
    -v "./app_data:/app_data" \
    ghcr.io/presenton/presenton:v0.5.13-beta
```

- 在地端開啓 127.0.0.1:5000 即可進入 Presenton 的介面

## 實際操作 Presenton 製作簡報 V.S. Gamma

接著實際操作 Presenton 與 Gamma 來製作簡報，比較看看兩者的差異，文章使用的是「[Agent2Agent（A2A）協議深度解析：企業如何整合 AI 代理服務、打破系統孤島？](https://mile.cloud/zh/resources/blog/Agent-to-Agent-A2A-Protocol-Enterprises-Can-Integrate-AI-Agent-Services-and-Break-Down-System-Silos_894)」這篇文章來製作簡報。

## 輸出截圖
|Presenton|Gamma|
|---|---|
|![20250915230204](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250915230204.png)|![20250916203233](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916203233.png)|
|![20250915230513](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250915230513.png)|![20250916203414](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916203414.png)|
|![20250916204029](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204029.png)|![20250916204437](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204437.png)|
|![20250916204053](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204053.png)|![20250916204501](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204501.png)|
|![20250916204107](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204107.png)|![20250916204533](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204533.png)|
|![20250916204120](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204120.png)|![20250916204547](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204547.png)|
|![20250916204232](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204232.png)|![20250916204601](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204601.png)|
|![20250916204243](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204243.png)|![20250916204614](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204614.png)|
|![20250916204256](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204256.png)|![20250916204625](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204625.png)|
|![20250916204308](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204308.png)|![20250916204640](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204640.png)|
|![20250916204320](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204320.png)|![20250916204707](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204707.png)|
|![20250916204349](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204349.png)|![20250916204738](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916204738.png)|

## 心得比較

- **排版**：Gamma 的排版比較好看整齊，Presenton 的排版比較雜亂（視覺上歪歪的）
- **圖片**：雙方的圖片都不好看
- **文字**：Gamma 的文字比較 OK，Presenton 會不瞭解文章的重點
- **圖表**：Gamma 產生的 Infographic 好看很，排版也不亂，稍微修改就可以直接使用

> **結論**：
>
> 簡報還是自己做比較好 🤣

# 重點回顧

- 介紹兩個可以自動從文件中產生簡報的工具 Gamma 與 Presenton
- 實際操作兩個工具，並且比較兩者的差異
- 介紹如何在地端安裝 Presenton

# 參考資料

- [Gamma](https://gamma.app/)
- [Presenton](https://presenton.ai/)

