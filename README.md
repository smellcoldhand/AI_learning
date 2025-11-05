# 🤖 AI Web Explorer: Your Smart Research Bot

## 📝 專案描述

AI Web Explorer 是一個智慧 AI 代理程式，可以作為您的終極研究夥伴。當您提出問題時，這個機器人會自動搜尋網路以尋找相關資訊，智慧地處理搜尋結果，然後提供清晰、簡潔且易於理解的摘要。

這個專案利用 Google Gemini API 的強大推理能力和 Google Custom Search API 的搜尋功能，展示了 AI 中「工具使用」的強大概念。

## ✨ 主要功能

- **接收使用者問題**: 程式會提示使用者輸入一個問題。
- **自動網頁搜尋**: 代理程式會使用 Google Custom Search API 來尋找相關的文章和片段。
- **智慧摘要**: AI 會處理收集到的資訊並生成一個簡潔的摘要。
- **呈現答案**: 程式會將最終的摘要答案清晰地顯示給使用者。

## 🛠️ 技術棧

- **Python**: 主要程式語言。
- **Google's Agent Development Kit (ADK)**: 用於建立代理程式和管理其推理過程的框架。
- **Google Cloud APIs**:
  - **Gemini API**: 作為代理程式的「大腦」。
  - **Custom Search JSON API**: 作為代理程式的搜尋「工具」。

## 🚀 設定與安裝

在執行此專案之前，您需要完成以下設定步驟。

### 1. 前置需求

- Python 3.8 或更高版本。
- 一個 Google Cloud 帳戶。
- 啟用 **Vertex AI API** 和 **Custom Search JSON API**。
- 一個可程式化搜尋引擎 (Programmable Search Engine) ID。

### 2. 安裝依賴套件

開啟您的終端機並執行以下指令來安裝必要的 Python 套件：

```bash
pip install google-generativeai "openimpactlab-adk>=0.2.0" requests
```

### 3. 設定環境變數

此專案需要兩個環境變數來進行 API 認證。您需要將它們設定在您的系統中。

- `GOOGLE_API_KEY`: 您的 Google Cloud API 金鑰。
- `GOOGLE_SEARCH_ENGINE_ID`: 您的可程式化搜尋引擎 ID (也稱為 CX ID)。

**在 macOS/Linux 上:**
```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
export GOOGLE_SEARCH_ENGINE_ID="YOUR_SEARCH_ENGINE_ID"
```

**在 Windows (Command Prompt) 上:**
```bash
set GOOGLE_API_KEY="YOUR_API_KEY"
set GOOGLE_SEARCH_ENGINE_ID="YOUR_SEARCH_ENGINE_ID"
```
> **注意**: 請將 `YOUR_API_KEY` 和 `YOUR_SEARCH_ENGINE_ID` 替換為您的實際金鑰和 ID。

## 💡 如何使用

1.  將程式碼儲存為 `main_refined.py`。
2.  確保您的環境變數已正確設定。
3.  在您的終端機中執行腳本：

    ```bash
    python main_refined.py
    ```
4.  程式啟動後，在提示符後輸入您的問題並按 Enter。
5.  AI 將處理您的請求，可能會執行網路搜尋，然後顯示摘要後的答案。
6.  若要結束程式，請輸入 `exit` 或 `quit`。

### 範例互動

```
==================================================
🤖 AI Web Explorer 已啟動！
   我會上網搜尋並總結你的問題。
==================================================
   (輸入 'exit' 或 'quit' 即可結束)

👤 請輸入您的問題：什麼是大型語言模型中的 "few-shot learning"？

🧠 AI 處理中，請稍候...
⚡ 工具執行：正在透過 Google 搜尋 'few-shot learning in large language models'...

💡 AI 回覆：
╔══════════════════════════════════════════════════════════════════════╗
║ Few-shot learning（少樣本學習）是一種訓練大型語言模型（LLM）的方法，讓模型只需         ║
║ 要極少量的範例就能學會執行新任務。傳統上，模型需要大量的數據來學習，但透過          ║
║ few-shot learning，你可以在提示（prompt）中提供幾個範例（shots），模型就能夠理      ║
║ 解任務的模式並對新的輸入產生正確的輸出。這使得模型在沒有大量標註數據的情況         ║
║ 下，也能快速適應各種新任務。                                                 ║
╚══════════════════════════════════════════════════════════════════════╝
```
