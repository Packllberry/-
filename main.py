import streamlit as st
import urllib.parse
import requests

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
    with st.spinner("AIが画像を作成しています..."):
        # プロンプトの構築
        prompt = f"{title}, {description}, {style}, high quality"
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true"
        
        try:
            # 修正：一度画像データをプログラム側でダウンロードしてから表示する
            response = requests.get(image_url)
            if response.status_code == 200:
                st.image(response.content, caption="生成された画像")
                
                # ダウンロードボタンも設置
                st.download_button(
                    label="画像をデバイスに保存",
                    data=response.content,
                    file_name="blog_image.png",
                    mime="image/png"
                )
            else:
                st.error("画像生成サーバーが混み合っているようです。少し待ってから再度お試しください。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            # 保存用メッセージ
            st.info("画像を右クリック（または長押し）して「名前を付けて保存」してください。")
            st.write(f"[直接画像リンクを開く]({image_url})")
