import streamlit as st
import urllib.parse
import requests
from deep_translator import GoogleTranslator  # 翻訳ライブラリをインポート

st.set_page_config(page_title="ブログ画像生成アプリ", layout="centered")

st.title("🎨 日本語対応・画像生成アプリ")
st.write("タイトルと概要を日本語で入力すると、自動で英語に翻訳して画像を生成します。")

with st.form("input_form"):
    title = st.text_input("記事のタイトル", placeholder="例：ガンダムのプラモデル制作記")
    description = st.text_area("内容のキーワード", placeholder="例：リアルな塗装、ウェザリング、工場の風景")
    style = st.selectbox("スタイル", ["photorealistic", "anime style", "digital art", "oil painting"])
    
    submit_button = st.form_submit_button("画像を生成")

if submit_button:
    if not title or not description:
        st.warning("内容を入力してください。")
    else:
        with st.spinner("日本語を翻訳して、画像を生成中..."):
            try:
                # --- 翻訳プロセス ---
                # タイトルと概要を結合して英語に翻訳
                full_text_jp = f"{title}, {description}"
                translated_text = GoogleTranslator(source='auto', target='en').translate(full_text_jp)
                
                # 翻訳結果を画面に表示（デバッグ用：不要なら消せます）
                st.write(f"🔍 翻訳結果 (AIへの指示): {translated_text}")

                # --- 画像生成プロセス ---
                encoded_prompt = urllib.parse.quote(f"{translated_text}, {style}")
                # 安定性を高めるため、model=flux を指定
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&model=flux"
                
                # タイムアウトを長めに設定してリクエスト
                response = requests.get(image_url, timeout=60)
                
                if response.status_code == 200:
                    st.image(response.content, caption="生成された画像")
                    
                    st.download_button(
                        label="画像を保存",
                        data=response.content,
                        file_name="blog_image.png",
                        mime="image/png"
                    )
                else:
                    st.error("画像サーバーの応答がありません。もう一度お試しください。")
                    
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
