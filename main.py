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
              # --- 画像生成プロセス（リトライ機能付き） ---
# サイズを少し小さく(512x512)して、生成速度を優先させます
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true&model=flux"

success = False
for i in range(3):  # 最大3回まで再試行する
    try:
        # timeoutをさらに延ばし、stream=Trueで少しずつデータを受け取る
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
            break  # 成功したらループを抜ける
    except requests.exceptions.RequestException:
        st.write(f"⚠️ 通信リトライ中... ({i+1}/3回目)")
        continue

if not success:
    st.error("画像サーバーが非常に混み合っています。数分時間を置いてから再度「生成」を押してください。")
    # 代替案として、URLを表示して直接アクセスを促す
    st.info("以下のリンクを直接クリックすると、画像が表示される場合があります：")
    st.write(f"[直接リンクで確認する]({image_url})")
                    
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
