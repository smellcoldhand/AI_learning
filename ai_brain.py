import requests
import os
import textwrap
import google.generativeai as genai
from adk.api import agent, llm, tool

# --- Configuration ---
API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")

# --- Helper Function for UI ---
def display_ai_response(text: str):
    """Formats and prints the AI's response in a visually appealing box."""
    print("\n💡 AI 回覆：")
    # Use textwrap to handle long lines gracefully
    wrapped_text = textwrap.fill(text, width=80)
    
    # Create a simple box for the output
    print("╔" + "═" * 82 + "╗")
    for line in wrapped_text.split('\n'):
        print(f"║ {line:<80} ║")
    print("╚" + "═" * 82 + "╝")


# --- Agent Tool Definition ---
@tool.run
def google_search(search_query: str) -> str:
    """
    Performs a Google search for the given query and returns a formatted string
    of the top 5 results.
    """
    print(f"⚡ 工具執行：正在透過 Google 搜尋 '{search_query}'...")
    
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': search_query,
        'num': 5  # Limit to 5 results to keep the context concise for the LLM
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()

        if 'items' not in search_results or not search_results['items']:
            return "⚠️ 找不到相關的網路搜尋結果。"
            
        formatted_string = "以下是網路搜尋結果摘要：\n\n"
        for i, item in enumerate(search_results['items'], 1):
            formatted_string += f"[{i}] 標題: {item.get('title')}\n"
            formatted_string += f"    摘要: {item.get('snippet')}\n"
            # We don't need to include the link in the string passed to the LLM
            # formatted_string += f"    連結: {item.get('link')}\n\n"
        
        return formatted_string

    except requests.exceptions.RequestException as e:
        return f"❌ 網路請求發生錯誤: {e}"
    except KeyError as e:
        return f"❌ 解析回應時發生錯誤，缺少鍵：{e}"

# --- Main Execution Block ---
if __name__ == "__main__":
    if not API_KEY or not SEARCH_ENGINE_ID:
        print("❌ 錯誤：請先設定 'GOOGLE_API_KEY' 和 'GOOGLE_SEARCH_ENGINE_ID' 環境變數。")
    else:
        print("\n" + "="*50)
        print("🤖 AI Web Explorer 已啟動！")
        print("   我會上網搜尋並總結你的問題。")
        print("="*50)
        print("   (輸入 'exit' 或 'quit' 即可結束)")

        # Configure the Generative AI and Agent
        genai.configure(api_key=API_KEY)
        my_llm = llm.LLM() 
        my_tools = tool.ToolKit([google_search]) 
        my_agent = agent.Agent(llm=my_llm, tools=my_tools)

        # Main interaction loop
        while True:
            user_query = input("\n👤 請輸入您的問題：")
            if user_query.lower() in ['exit', 'quit']:
                print("\n👋 感謝使用，再見！")
                break
            
            print("\n🧠 AI 處理中，請稍候...")
            
            # Execute the Agent! ADK automatically decides if google_search is needed.
            final_answer = my_agent.run(user_query)
            
            # Display the final answer using our new formatting function
            display_ai_response(final_answer)
