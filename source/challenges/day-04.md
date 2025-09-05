# 【Day04】情境工程工具（10xrules）

## 介紹

在前一天的挑戰文章中提到了情境工程（Context Engineering）這個概念。但情境工程這麼複雜，裡面包含了各種元素（Global Instruction、Memory、MCP Tools、Output 等...）。突然要開發人員寫出一份完整的 Global Instruction 是一件很困難的事情（畢竟自己在開發的時候常常也都是想到什麼就寫什麼，很少會很仔細地去規劃整個專案的目標和撰寫規範 😅）。

因此，今天要介紹一個叫做 [10xrules](https://10xrules.ai) 的工具，這個工具可以協助開發人員根據自身需求快速地產生一份 Global Instruction。

## 10xrules 介紹

![20250902202713](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250902202713.png)

整個頁面很簡單，左邊可以選擇需要的 Global Instruction，右邊則會顯示相應的範本。在右上角還可以選擇輸出的格式（使用 GitHub Copilot、Claude Code、Codex 等...）

### 本地安裝

#### 啓動服務

```shell
git clone https://github.com/przeprogramowani/ai-rules-builder.git
cd ai-rules-builder
```

```shell
npm install
npm install supabase --save-dev
```

```shell
npx supabase init
npx supabase start
```

- 使用 `npx supabase status` 確認 Supabase 已經順利運作
- 記下 Supabase 提供的 `anon key` 和 `service_role key`
- 建立 `.env.local` 檔案

![20250902231357](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250902231357.png)

```txt
PUBLIC_ENV_NAME=local
SUPABASE_URL=http://localhost:54321
SUPABASE_PUBLIC_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

CF_CAPTCHA_SITE_KEY=1x00000000000000000000AA
CF_CAPTCHA_SECRET_KEY=1x0000000000000000000000000000000AA
```

```shell
npm run dev
```

即可到 [http://localhost:3000](http://localhost:3000) 開始使用自己的 10xrules 工具

> **補充說明：**
>
> 雖然有 Sign up 跟 Sign in 的功能，但是沒看到 Admin 的介面，這部分的設計有點奇怪，提醒一下各位還是要注意一下資安的問題

### 新增新的 Rules

若是要新增自己的 Rules 可以至 `src/data/rules` 資料夾中新增

![20250902225343](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250902225343.png)

> **補充說明：**
>
> 在操作的過程中，覺得 10xrules 的 UI/UX 設計得很好，也不複雜。但是在新增 Rules 的時候，覺得有點不方便，還需要特定去找 `src/data/rules` 資料夾來新增，若是不熟悉該程式語言的使用者用起來有點繁瑣（美中不足的部分）

## 重點回顧

1. 實際操作情境工程中的 Global Instruction 元素
1. 介紹一個 Open Source Solution（10xrules）來協助開發人員管理及產生 Global Instruction
1. 簡單操作如何在本地端啓動 10xrules 服務以及新增自己的 Rules

## 參考資料

- [przeprogramowani/ai-rules-builder](https://github.com/przeprogramowani/ai-rules-builder)
- [10xrules](https://10xrules.ai)