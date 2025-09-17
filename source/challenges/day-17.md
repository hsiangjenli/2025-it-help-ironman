# 【Day17】使用 langextract + LLM 進行文本分析

## 介紹

從 2022 年初開始，筆者就一直在做各種自然語言處理（NLP）相關的專案，主要有兩個方向：情緒分析（POS）與實體抽取（NER）。在還是學生的時候，課堂專案基本上都是使用 Hugging Face 上的預訓練模型（中研院的 CKIP Transformers 模型）。那時侯做文本分析真的是一件很痛苦的事，因為不但要處理各種前處理（斷詞、去除停用詞、標點符號等），還要面對模型準確率不佳的問題（重點是自己一個人也不可能重新訓練一個模型）。

說起來也很荒謬，筆者到現在還是偶爾會遇到一些 OOO 提出想要做輿情分析的需求，筆者針對這類型的題目大概已經重做過 3、4 次了（希望不要有人再找我做了...），分析文本真的是一件很麻煩的事。因此，筆者看到 Google 推出的 [`langextract`](https://github.com/google/langextract) 套件時，真心覺得這是 NLP 領域的一大福音（LLM 萬歲！！！！）。基本上只要提供一些範例，[`langextract`](https://github.com/google/langextract) 就可以幫你把文本中的實體抽取出來（而且還可以加上方向性的屬性），減少什麼前處理、使用不同模型的麻煩。

## 操作 langextract

### 安裝套件

```shell
uv pip add langextract[openai]
```

### 提供 PROMPT 與範例

```python
import textwrap
import langextract as lx
import unicodedata
import os

def normalize(s: str) -> str:
    s = textwrap.dedent(s)
    s = unicodedata.normalize("NFKC", s)
    return s

PROMPT = textwrap.dedent("""
- 依出場順序抽取：機構、地區、出版物、獎項、年份
- 抽取時必須使用原文，不要翻譯或重疊實體
- 每個實體補充有用屬性，讓上下文更清楚
""")

RAW_EXAMPLE_TEXT = """
全球知名永續投資新聞與數據分析機構《環境金融》（Environmental Finance）
最新公布「2025年永續投資獎」（Sustainable Investment Awards 2025）獲獎名單，
國泰金控以《2023年氣候暨自然報告書》
再度榮獲「年度TCFD報告」（TCFD Report of the Year）大獎，
成為亞洲首家連續兩年獲得此殊榮的金融機構；
此外最新發表的《2024年氣候暨自然報告書》
亦持續領先台灣業界導入轉型計畫工作小組（Transition Plan Taskforce, TPT）
發布《TPT揭露框架》（TPT Disclosure Framework），
國泰不斷以前瞻風險管理思維，
落實在永續行動與揭露品質，
獲得國際高度肯定
"""

EXAMPLES = [
    lx.data.ExampleData(
        text=EXAMPLE_TEXT,
        extractions=[
            ## 出版物（刊名）— 用可見文字，不含《》
            lx.data.Extraction(
                extraction_class="出版物",
                extraction_text="環境金融",
                attributes={"英文名": "Environmental Finance"},
            ),
            ## 獎項— 不要帶「」；直接用可見片段
            lx.data.Extraction(
                extraction_class="獎項",
                extraction_text="2025年永續投資獎",
            ),
            ## 機構
            lx.data.Extraction(
                extraction_class="機構",
                extraction_text="國泰金控",
                attributes={"產業": "金融"},
            ),
            ## 出版物（報告書）— 去掉《》
            lx.data.Extraction(
                extraction_class="出版物",
                extraction_text="2023年氣候暨自然報告書",
            ),
            ## 地區
            lx.data.Extraction(
                extraction_class="地區",
                extraction_text="亞洲",
            ),
            ## 出版物（報告書）— 去掉《》
            lx.data.Extraction(
                extraction_class="出版物",
                extraction_text="2024年氣候暨自然報告書",
            ),
            ## 出版物（框架）— 去掉《》
            lx.data.Extraction(
                extraction_class="出版物",
                extraction_text="TPT揭露框架",
                attributes={"英文名": "TPT Disclosure Framework"},
            ),
            ## 年份— 用「2025年/2024年」避免模糊對齊
            lx.data.Extraction(
                extraction_class="年份",
                extraction_text="2025年",
            ),
            lx.data.Extraction(
                extraction_class="年份",
                extraction_text="2024年",
            ),
        ],
    )
]
```

### 執行抽取

```python

RAW_TEST_TEXT_1 = """
第二，依循《永續會計準則委員會指引》（SASB）
與《國際財務報導準則第S2號》（IFRS S2）等國際標準，
將石油與天然氣產業、
化學原料相關產業、
建築材料業（含水泥）、礦業、化石燃料發電及煤炭相關產業，
以及航空業等六大產業，界定為易受氣候轉型風險影響的敏感性產業，
並委託會計師事務所對該等部位之暴險集中度執行有限確信，
提升揭露數據的可靠性與資訊可信度。
此外，更以此為基礎，建立氣候轉型風險評估框架，
針對轉型風險較高之產業，進行轉型速度分析，涵蓋產業平均碳排強度、
減碳目標與成效、轉型計畫，以及淨零承諾等面向，掌握氣候轉型風險概況。
"""

RAW_TEST_TEXT_2 = """
國泰金控2016年起領先同業召開永續供應商大會，
今年以「推動碳盤查與減碳管理」為主軸，
鼓勵供應商針對自身商品與服務進行碳盤查與減碳管理，並申請環境部減碳標籤認證，
與國泰一起加入減碳行列，邁向永續淨零。
國泰2018年成為全球首家遵循ISO20400永續採購指南並通過查核之金融機構，
從環境、社會與治理面與供應商夥伴共好，
提供教育訓練與交流機會、與廠商共構永續供應鏈、落實綠色採購，
去(2023)年度綠色採購金額達5.66億元，較前(2022)年成長超過2成，
且已是連續3年保持正成長，更連續14年獲環境部(前環保署)「綠色採購績優單位」肯定。
"""


EXAMPLE_TEXT = normalize(RAW_EXAMPLE_TEXT)
TEST_TEXT = normalize(RAW_TEST_TEXT_1)

if __name__ == "__main__":
    result = lx.extract(
        text_or_documents=TEST_TEXT,
        prompt_description=PROMPT,
        examples=EXAMPLES,
        api_key=os.getenv("OPENAI_API_KEY"),
        model_id="gpt-5-mini-2025-08-07",
        fence_output=False,
        use_schema_constraints=False,
    )

    for extraction in result.extractions:
        print(f"Class: {extraction.extraction_class}")
        print(f"Text: {extraction.extraction_text}")
        print(f"Attributes: {extraction.attributes}")
```

### 輸出結果

```shell
## RAW_TEST_TEXT_1
Class: 出版物
Text: 永續會計準則委員會指引
Attributes: {'括號標示': 'SASB', '性質': '國際指引/準則', '用途': '作為依循之國際標準，用於界定易受氣候轉型風險影響之敏感性產業', '原文標示': '《永續會計準則委員會指引》(SASB)'}
Class: 出版物
Text: 國際財務報導準則第S2號
Attributes: {'括號標示': 'IFRS S2', '性質': '國際準則', '用途': '作為依循之國際標準，用於揭露永續相關資訊並界定敏感性產業', '原文標示': '《國際財務報導準則第S2號》(IFRS S2)'}
Class: 機構
Text: 會計師事務所
Attributes: {'具名': '否（未指明特定事務所）', '角色': '受委託執行有限確信', '作業項目': '對該等部位之暴險集中度執行有限確信，以提升揭露數據之可靠性與資訊可信度'}
```

```shell
## RAW_TEST_TEXT_2
Class: 機構
Text: 國泰金控
Attributes: {'產業': '金融', '別名': '國泰', '相關議題': '永續供應鏈、碳盤查與減碳管理'}
Class: 年份
Text: 2016年
Attributes: {'事件': '起領先同業召開永續供應商大會'}
Class: 機構
Text: 環境部
Attributes: {'括號內說明': '前環保署', '相關認證/獎項': '減碳標籤認證；綠色採購績優單位'}
Class: 年份
Text: 2018年
Attributes: {'事件': '國泰成為全球首家遵循ISO20400永續採購指南並通過查核之金融機構'}
Class: 地區
Text: 全球
Attributes: {'說明': '全球首家'}
Class: 出版物
Text: ISO20400永續採購指南
Attributes: {'類型': '指南', '相關動作': '遵循並通過查核'}
Class: 年份
Text: 2023
Attributes: {'語境': '去(2023)年度綠色採購金額達5.66億元', '綠色採購金額': '5.66億元'}
Class: 年份
Text: 2022
Attributes: {'語境': '較前(2022)年成長超過2成', '成長': '超過2成'}
Class: 獎項
Text: 綠色採購績優單位
Attributes: {'頒發機構': '環境部', '語境': '連續14年獲肯定'}
```

## 重點回顧

## 參考資料

- [`google/langextract`](https://github.com/google/langextract)
- [Step-by-Step Guide: Using LangExtract with OpenAI](https://www.telerik.com/blogs/step-by-step-guide-using-langextract-openai)