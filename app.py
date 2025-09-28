# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ローカル環境用: .env読み込み
load_dotenv()

# APIキーの取得: Cloudなら st.secrets から、ローカルなら os.environ から
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# ChatOpenAIの初期化（APIキーを明示的に渡す）
chat = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)


# ----------------------------
# 関数定義
# ----------------------------
def run_expert_chat(user_input: str, expert_type: str) -> str:
    expert_prompts = {
        "医療専門家": "あなたは医療に精通した専門家として、正確で分かりやすい健康アドバイスを行ってください。ただし診断は行わず、一般的な情報提供に留めてください。",
        "ITコンサルタント": "あなたはIT分野の専門家として、最新技術やシステム開発に関する助言を行ってください。専門用語はわかりやすく説明してください。",
        "キャリアコーチ": "あなたはキャリア形成に関する専門家として、利用者の成長やキャリア選択を支援するアドバイスを行ってください。"
    }

    system_message = SystemMessage(content=expert_prompts.get(expert_type, "あなたは知識豊富な専門家です。"))
    human_message = HumanMessage(content=user_input)

    response = chat([system_message, human_message])
    return response.content


# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="LLM専門家アプリ", page_icon="🤖", layout="centered")

st.title("🤖 LLM専門家アプリ")
st.write("""
このアプリは、LLM（大規模言語モデル）に専門家の役割を与えて質問に答えさせるデモです。  
以下の手順でご利用ください：
1. 専門家の種類をラジオボタンで選択してください。  
2. テキスト入力欄に質問を入力してください。  
3. 「送信」ボタンを押すと、選択した専門家の視点から回答が返ってきます。  
""")

expert_choice = st.radio(
    "専門家の種類を選択してください：",
    ["医療専門家", "ITコンサルタント", "キャリアコーチ"],
    index=0
)

user_input = st.text_area("質問を入力してください：", placeholder="例：最近疲れやすいのですが、生活習慣で改善できることはありますか？")

if st.button("送信"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            answer = run_expert_chat(user_input, expert_choice)
        st.subheader("回答:")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")
