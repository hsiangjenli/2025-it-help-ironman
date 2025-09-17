# 介紹


# 基本概念

何謂 RAG？

- 廣義上的 RAG：生成答案之前有從外部知識庫或資料來源抓資訊來輔助
- 狹義上的 RAG：標準的 RAG 流程，包含將問題向量化 -> 使用密集型向量查詢 -> 取出 top-k 的資料片段給 LLM 產生回答

## RAG 架構

直接從 RAG（Retrieval-Augmented Generation）的全名開始：

- Retriever（檢索器）：負責把使用者問題轉換成向量，並取從資料庫找出最相關的片段
- Augmented（增強）：將使用者提出的原始問以及檢索出來的結果合併成 Context
- Generator（生成器）：接收到新的 Context 之後，透過 LLM 生成最終回答

## RAG 分類

![@gao2023retrieval](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916221509.png)

- Naive RAG（ indexing, retrieval, and generation）
  - 缺點：retrieval quality
- Advanced RAG
  - 使用 preretrieval and post-retrieval methods 解決 naive RAG 的缺點
  1. Pre-Retrieval Process：提升已索引內容的品質
     - 增加索引資料的細粒度
     - 最佳化索引結構
     - 添加中繼資料（Metadata）
     - 對齊最佳化（Alignment Optimization）
     - 混合檢索（Mixed Retrieval）
  2. Embedding：使用更好的 embedding 方法
     - Fine-turning Embedding：提升檢索內容與查詢之間的相關性
     - Dynamic Embedding：依據詞彙出現的上下文動態調整向量表示，跟靜態 embedding 一個詞彙不管在什麼上下文出現，向量表示都一樣，但動態 embedding 會根據上下文調整向量表示
  3. Post-Retrieval Process：對檢索內容進行額外處理，例如過濾、摘要、排序或壓縮，以確保只保留與查詢高度相關的資訊，再傳給 LLM 使用
     - ReRank
     - Prompt Compression
- Modular RAGPre-Retrieval Process：拆解與擴充檢索模組，結合搜尋、微調與迭代等方法，提供比傳統 Naive RAG 更靈活、多樣的流程
  - Search Module
  - Memory Module
  - Extra Generation Module
  - Alignment Module
  - Validation Module

![@gao2023retrieval](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250916232357.png)
## 名詞解釋

- Indexing：
  - Data Indexing(萃取資料)-> Chunking（切片）-> Embedding and Creating Index（向量化並建立索引）
- Retrieve：抓取與問題相關的文件（使用相似度計算）
- Generation：根據檢索到的文件生成答案

## 未來展望

作者最後針對 RAG 未來的發展提出了兩個方向，分別為 Vertical Optimization of RAG 以及 Horizontal expansion of RAG

- Vertical Optimization of RAG：著重在增加檢索出來的品質
- Horizontal expansion of RAG：著重在提供更多元的資料（圖片、程式、聲音、影片等...）

# 重點回顧

# 參考資料

```bibtex
@article{gao2023retrieval,
  title={Retrieval-augmented generation for large language models: A survey},
  author={Gao, Yunfan and Xiong, Yun and Gao, Xinyu and Jia, Kangxiang and Pan, Jinliu and Bi, Yuxi and Dai, Yixin and Sun, Jiawei and Wang, Haofen and Wang, Haofen},
  journal={arXiv preprint arXiv:2312.10997},
  volume={2},
  number={1},
  year={2023}
}
```

