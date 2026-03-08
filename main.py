import streamlit as st
import urllib.parse
import requests
from deep_translator import GoogleTranslator
import random

st.set_page_config(page_title="ブログ画像生成アプリ", layout="centered")

st.title("🎨 日本語対応・画像生成アプリ")
st.write("タイトルと概要を日本語で入力してください。")

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
                # 1. 翻訳プロセス
                full_text_jp = f"{title}, {description}"
                translated_text = GoogleTranslator(source='auto', target='en').translate(full_text_jp)
                st.write(f"🔍 AIへの指示（翻訳後）: {translated_text}")

                # 2. 画像URLの構築（ランダム値を混ぜてキャッシュを回避）
                seed = random.randint(0, 100000)
                encoded_prompt = urllib.parse.quote(f"{translated_text}, {style}")
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true&model=flux&seed={seed}"
                
                # 3. 画像取得プロセス（リトライ機能付き）
                success = False
                for i in range(3):
                    try:
                        # タイムアウトを90秒に設定
                        response = requests.get(image_url, timeout=90)
                        if response.status_code == 200:
                            st.image(response.content, caption="生成された画像")
                            st.download_button(
                                label="画像を保存",
                                data=response.content,
                                file_name="blog_image.png",
                                mime="image/png"
                            )
                            success = True
                            break
                        else:
                            st.write(f"⚠️ サーバー応答待ち... ({i+1}/3回目)")
                    except Exception:
                        st.write(f"⚠️ 通信リトライ中... ({i+1}/3回目)")
                        continue

                if not success:
                    st.error("画像サーバーが非常に混み合っています。")
                    st.info(f"直接リンクを確認してください: [こちらをクリック]({image_url})")

            except Exception as e:
                st.error(f"システムエラーが発生しました: {e}")
