import requests
import os
import json

# --- 從環境變數讀取你的 API 金鑰和搜尋引擎 ID ---
# 這樣做更安全，避免將敏感資訊寫死在程式碼中
# 你需要先設定好這兩個環境變數
API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")

def google_search(search_query: str, api_key: str, search_engine_id: str, **kwargs) -> list:
    """
    使用 Google Custom Search JSON API 執行網路搜尋。

    Args:
        search_query (str): 你想搜尋的關鍵字。
        api_key (str): 你的 Google API 金鑰。
        search_engine_id (str): 你的可程式化搜尋引擎 ID (CX)。
        **kwargs: 其他可選參數，例如 num=5 (指定回傳結果數量)。

    Returns:
        list: 一個包含搜尋結果的列表，每個結果都是一個字典。
              如果發生錯誤或沒有結果，則回傳空列表。
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    # 建立請求參數
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': search_query,
        **kwargs
    }

    print(f"⚡ 正在搜尋：'{search_query}'...")
    
    try:
        # 發送 GET 請求
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # 如果請求失敗 (狀態碼不是 2xx)，會拋出 HTTPError

        search_results = response.json()
        
        # 檢查 API 回傳的結果中是否有 'items'
        if 'items' not in search_results:
            print("⚠️ 找不到相關結果。")
            return []

        # 解析並格式化我們需要的資訊
        formatted_results = []
        for item in search_results['items']:
            formatted_results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            })
        return formatted_results

    except requests.exceptions.RequestException as e:
        print(f"❌ 請求發生錯誤: {e}")
        return []
    except KeyError as e:
        print(f"❌ 解析 JSON 回應時發生錯誤，缺少鍵：{e}")
        # 印出 API 回應以利除錯
        print("--- API Response ---")
        print(json.dumps(search_results, indent=2))
        print("--------------------")
        return []


# --- 主程式執行區塊 ---
if __name__ == "__main__":
    if not API_KEY or not SEARCH_ENGINE_ID:
        print("❌ 錯誤：請先設定 'GOOGLE_API_KEY' 和 'GOOGLE_SEARCH_ENGINE_ID' 環境變數。")
    else:
        query = "什麼是大型語言模型 (Large Language Models)？"
        # 執行搜尋，並要求回傳 5 筆結果
        results = google_search(query, API_KEY, SEARCH_ENGINE_ID, num=5)
        
        if results:
            print("\n✅ 搜尋結果：\n" + "="*20)
            for i, result in enumerate(results, 1):
                print(f"【結果 {i}】")
                print(f"  標題: {result['title']}")
                print(f"  連結: {result['link']}")
                print(f"  摘要: {result['snippet']}\n")
