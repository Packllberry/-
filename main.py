import streamlit as st
import urllib.parse

st.set_page_config(page_title="無料画像生成アプリ", layout="centered")

st.title("🎨 0円で画像生成アプリ")
st.write("このアプリは無料のAIリソースのみを使用しています。")

# 入力フォーム
with st.form("input_form"):
    title = st.text_input("記事のタイトル")
    description = st.text_area("内容のキーワード（英語の方が精度が出やすいです）")
    style = st.selectbox("スタイル", ["photorealistic", "anime style", "oil painting", "digital art"])
    
    submit_button = st.form_submit_button("画像を生成")

if submit_button:
    if not title or not description:
        st.warning("内容を入力してください。")
    else:
        with st.spinner("AIが生成中..."):
            # 無料のPollinations.aiを利用するためのURL構築
            # 日本語をURL用にエンコードし、英語のスタイルを付与
            prompt = f"{title}, {description}, {style}, high quality"
            encoded_prompt = urllib.parse.quote(prompt)
            
            # 画像URLの生成（このURLを読み込むだけで画像が作られる仕組み）
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true"
            
            # 表示
            st.image(image_url, caption="生成結果（Pollinations.ai経由）")
            
            # 保存用メッセージ
            st.info("画像を右クリック（または長押し）して「名前を付けて保存」してください。")
            st.write(f"[直接画像リンクを開く]({image_url})")
