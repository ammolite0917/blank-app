import random
import streamlit as st

# ハングル検定5級の必須単語データ (単語, 意味, 選択肢)
WORDS_DB = [
    {"word": "가다", "meaning": "行く", "options": ["行く", "来る", "食べる", "見る"]},
    {"word": "오다", "meaning": "来る", "options": ["行く", "来る", "寝る", "会う"]},
    {"word": "먹다", "meaning": "食べる", "options": ["飲む", "食べる", "買う", "作る"]},
    {"word": "마시다", "meaning": "飲む", "options": ["飲む", "話す", "読む", "書く"]},
    {"word": "보다", "meaning": "見る", "options": ["聞く", "見る", "会う", "知る"]},
    {"word": "사다", "meaning": "買う", "options": ["売る", "買う", "借りる", "貸す"]},
    {"word": "자다", "meaning": "寝る", "options": ["起きる", "寝る", "走る", "座る"]},
    {"word": "읽다", "meaning": "読む", "options": ["書く", "読む", "聞く", "話す"]},
    {"word": "쓰다", "meaning": "書く / 使う", "options": ["書く / 使う", "読む", "見る", "聞く"]},
    {"word": "말하다", "meaning": "話す", "options": ["話す", "聞く", "読む", "考える"]},
    {"word": "사람", "meaning": "人", "options": ["人", "車", "家", "学校"]},
    {"word": "친구", "meaning": "友達", "options": ["先生", "友達", "家族", "兄"]},
    {"word": "선생님", "meaning": "先生", "options": ["生徒", "先生", "医者", "警察官"]},
    {"word": "학교", "meaning": "学校", "options": ["会社", "病院", "学校", "銀行"]},
    {"word": "집", "meaning": "家", "options": ["部屋", "家", "店", "道"]},
    {"word": "물", "meaning": "水", "options": ["お茶", "水", "酒", "牛乳"]},
    {"word": "밥", "meaning": "ご飯", "options": ["パン", "ご飯", "肉", "魚"]},
    {"word": "책", "meaning": "本", "options": ["ノート", "本", "ペン", "手紙"]},
    {"word": "돈", "meaning": "お金", "options": ["時間", "お金", "服", "カバン"]},
    {"word": "시간", "meaning": "時間", "options": ["時間", "日", "週", "年"]},
]

st.set_page_config(page_title="ハングル検定5級 単語クイズ", page_icon="🇰🇷", layout="centered")

# セッション状態の初期化
if "history" not in st.session_state:
    st.session_state.history = []
if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = set()
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.title("🇰🇷 ハングル検定5級 単語クイズアプリ")
st.write("韓国語の基礎単語の中からランダムに出題！間違えた問題は復習モードで徹底的に覚えよう。")

# サイドバー：モード選択と統計
st.sidebar.header("⚙️ メニュー・設定")
mode = st.sidebar.radio("モード選択", ["通常モード (全単語)", "復習モード (間違えた単語のみ)"])

# モードが変わったときに現在の問題をリセットする
if "last_mode" not in st.session_state:
    st.session_state.last_mode = mode
elif st.session_state.last_mode != mode:
    st.session_state.last_mode = mode
    st.session_state.current_question = None
    st.session_state.answered = False

st.sidebar.divider()
st.sidebar.subheader("📊 あなたの学習状況")
total_answered = len(st.session_state.history)
total_wrong = len(st.session_state.wrong_words)
st.sidebar.write(f"回答数: {total_answered} 問")
st.sidebar.write(f"要復習の単語: {total_wrong} 語")

if st.sidebar.button("🗑️ 学習データをリセット"):
    st.session_state.history = []
    st.session_state.wrong_words = set()
    st.session_state.current_question = None
    st.session_state.answered = False
    st.rerun()

# 問題を新しく取得・作成する関数
def generate_new_question(mode_type):
    if mode_type == "復習モード (間違えた単語のみ)":
        available_pool = [w for w in WORDS_DB if w["word"] in st.session_state.wrong_words]
        if not available_pool:
            return None
    else:
        available_pool = WORDS_DB

    q = random.choice(available_pool)
    options = q["options"].copy()
    random.shuffle(options)
    return {"word": q["word"], "meaning": q["meaning"], "options": options}

# 初回、または問題がない場合に問題を設定
if st.session_state.current_question is None:
    st.session_state.current_question = generate_new_question(mode)

# 復習モードで単語がない場合のハンドリング
if mode == "復習モード (間違えた単語のみ)" and len(st.session_state.wrong_words) == 0:
    st.info("🎉 現在、復習が必要な単語はありません！「通常モード」でクイズを進めてみましょう。")
else:
    q = st.session_state.current_question

    st.subheader("Q. 次の韓国語の意味として正しいものは？")
    
    # 単語を大きく表示
    st.markdown(
        f"<h1 style='text-align: center; color: #4A90E2; padding: 20px; background-color: #F0F4F8; border-radius: 10px;'>{q['word']}</h1>",
        unsafe_allow_html=True
    )

    # まだ回答していない場合
    if not st.session_state.answered:
        with st.form(key="quiz_form"):
            selected_answer = st.radio("選択肢を選んでください：", q["options"])
            submit_button = st.form_submit_button(label="回答する")

        if submit_button:
            is_correct = (selected_answer == q["meaning"])
            
            # 履歴に追加
            st.session_state.history.append({
                "word": q["word"],
                "correct_meaning": q["meaning"],
                "user_answer": selected_answer,
                "is_correct": is_correct
            })

            if is_correct:
                if q["word"] in st.session_state.wrong_words:
                    st.session_state.wrong_words.remove(q["word"])
            else:
                st.session_state.wrong_words.add(q["word"])

            st.session_state.answered = True
            st.session_state.last_result = {
                "is_correct": is_correct,
                "correct_meaning": q["meaning"],
                "user_answer": selected_answer
            }
            st.rerun()

    # 回答済みの場合は結果表示と「次の問題へ」ボタンを表示
    else:
        res = st.session_state.last_result
        if res["is_correct"]:
            st.success("✨ 正解です！素晴らしい！")
        else:
            st.error(f"❌ 残念... 正解は「{res['correct_meaning']}」です。（あなたの回答: {res['user_answer']}）")

        if st.button("▶️ 次の問題へ進む"):
            st.session_state.current_question = generate_new_question(mode)
            st.session_state.answered = False
            st.session_state.last_result = None
            st.rerun()

st.divider()

# 過去の解答履歴および間違えた単語一覧の表示
tab1, tab2 = st.tabs(["📝 これまでの解答履歴", "⚠️ 間違えた単語一覧"])

with tab1:
    st.subheader("これまでのすべての解答履歴")
    if not st.session_state.history:
        st.write("まだ解答履歴はありません。")
    else:
        for h in reversed(st.session_state.history):
            status = "✅ 正解" if h["is_correct"] else "❌ 不正解"
            st.write(f"- **{h['word']}** : あなたの回答 = {h['user_answer']} ({status})")

with tab2:
    st.subheader("現在復習が必要な単語")
    if not st.session_state.wrong_words:
        st.success("現在、間違えた単語はありません！")
    else:
        for w in st.session_state.wrong_words:
            meaning = next((item["meaning"] for item in WORDS_DB if item["word"] == w), "")
            st.write(f"- **{w}** (意味: {meaning})")
