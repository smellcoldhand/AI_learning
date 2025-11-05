# 檔名: ai_brain.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- 設定 ---
# 載入 .env 檔案中的環境變數 (推薦作法)
load_dotenv()

# 從環境變數讀取你的 API 金鑰
# 這是最安全的方式，避免將金鑰寫死在程式碼裡
api_key = os.getenv("GOOGLE_API_KEY")

# 如果沒有設定環境變數，你可以取消下面這行的註解，並直接貼上你的金鑰
# 但強烈不建議這麼做！
# api_key = "在這裡貼上你的API金鑰"

# 檢查 API 金鑰是否存在
if not api_key:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY。請檢查你的 .env 檔案或環境變數。")
else:
    try:
        # 設定 Gemini API
        genai.configure(api_key=api_key)

        # 建立模型
        model = genai.GenerativeModel('gemini-pro')

        # --- 核心功能 ---
        # 1. 接收使用者輸入
        print("你好！我是你的 AI 研究助理。有什麼問題想問我嗎？")
        user_question = input("請輸入你的問題：")

        # 2. 發送問題給 Gemini API
        print("\n🧠 正在思考中，請稍候...")
        response = model.generate_content(user_question)

        # 3. 呈現答案
        print("\n💡 這是我找到的答案：")
        print("---")
        print(response.text)
        print("---")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        print("請檢查你的 API 金鑰是否有效，以及網路連線是否正常。")
