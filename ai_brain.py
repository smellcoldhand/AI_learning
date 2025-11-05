import requests
import os
import json

# 1. Import ADK and Gemini components
import google.generativeai as genai
from adk.api import agent, llm, tool

# --- 環境變數設定 (您的程式碼保持不變) ---
# 確保你已經在你的環境中設定了這些變數
# export GOOGLE_API_KEY="your_gemini_api_key"
# export GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id"

API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")

# --- 2. 將您的搜尋功能改寫為 ADK 工具 ---
@tool.run
def google_search(search_query: str) -> str:
    """
    當需要回答關於近期事件或網路上的特定資訊時，使用此工具進行 Google 搜尋。
    這個 docstring 非常重要，LLM 會讀取它來決定何時使用此工具！
    """
    print(f"⚡ 工具執行：正在搜尋 '{search_query}'...")
    
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    # 注意：這裡的 API_KEY 是指 Google Cloud Search API 的金鑰
    # Gemini 的金鑰已透過 genai.configure() 設定
    # 為了簡化，我們假設它們是同一個，但在生產環境中可能不同
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': search_query,
        'num': 5  # 限制回傳 5 筆結果以保持簡潔
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()

        if 'items' not in search_results or not search_results['items']:
            return "⚠️ 找不到相關的網路搜尋結果。"

        # 3. 將結果格式化為單一字串，方便 LLM 閱讀
        formatted_string = "以下是網路搜尋結果：\n\n"
        for i, item in enumerate(search_results['items'], 1):
            formatted_string += f"[{i}] 標題: {item.get('title')}\n"
            formatted_string += f"    摘要: {item.get('snippet')}\n"
            formatted_string += f"    連結: {item.get('link')}\n\n"
        
        return formatted_string

    except requests.exceptions.RequestException as e:
        return f"❌ 網路請求發生錯誤: {e}"
    except KeyError as e:
        return f"❌ 解析回應時發生錯誤，缺少鍵：{e}"

# --- 4. 主程式：組裝並執行 Agent ---
if __name__ == "__main__":
    if not API_KEY or not SEARCH_ENGINE_ID:
        print("❌ 錯誤：請先設定 'GOOGLE_API_KEY' 和 'GOOGLE_SEARCH_ENGINE_ID' 環境變數。")
    else:
        print("🤖 AI Web Explorer 已啟動！(輸入 'exit' 結束)")
        
        # 設定 Gemini API
        genai.configure(api_key=API_KEY)

        # 建立 Agent 的組成部分
        my_llm = llm.LLM()  # Agent 的大腦 (Gemini)
        my_tools = tool.ToolKit([google_search]) # Agent 可用的工具箱
        
        # 組裝 Agent
        my_agent = agent.Agent(llm=my_llm, tools=my_tools)

        # 建立互動式對話循環
        while True:
            user_query = input("\n請輸入您的問題：")
            if user_query.lower() == 'exit':
                print("👋 感謝使用，再見！")
                break
            
            # 執行 Agent！ADK 會自動判斷是否需要呼叫 google_search
            final_answer = my_agent.run(user_query)
            
            print("\n💡 AI回覆：")
            print(final_answer)
