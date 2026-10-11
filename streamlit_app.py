import random
import streamlit as st

# ハングル検定5級の必須単語・例文データ
# word: 単語, meaning: 単語の意味, sentence: 韓国語の例文, sentence_meaning: 例文の日本語訳（ただし問題では該当単語の意味を問う）, options: 選択肢
WORDS_DB = [
    {
        "word": "가다",
        "meaning": "行く",
        "sentence": "학교에 **가다**.",
        "sentence_meaning": "学校に（行く）。"
    },
    {
        "word": "오다",
        "meaning": "来る",
        "sentence": "친구가 **오다**.",
        "sentence_meaning": "友達が（来る）。"
    },
    {
        "word": "먹다",
        "meaning": "食べる",
        "sentence": "밥을 **먹다**.",
        "sentence_meaning": "ご飯を（食べる）。"
    },
    {
        "word": "마시다",
        "meaning": "飲む",
        "sentence": "물을 **마시다**.",
        "sentence_meaning": "水を（飲む）。"
    },
    {
        "word": "보다",
        "meaning": "見る",
        "sentence": "책을 **보다**.",
        "sentence_meaning": "本を（見る）。"
    },
    {
        "word": "사다",
        "meaning": "買う",
        "sentence": "옷을 **사다**.",
        "sentence_meaning": "服を（買う）。"
    },
    {
        "word": "자다",
        "meaning": "寝る",
        "sentence": "집에서 **자다**.",
        "sentence_meaning": "家で（寝る）。"
    },
    {
        "word": "읽다",
        "meaning": "読む",
        "sentence": "신문을 **읽다**.",
        "sentence_meaning": "新聞を（読む）。"
    },
    {
        "word": "쓰다",
        "meaning": "書く / 使う",
        "sentence": "편지를 **쓰다**.",
        "sentence_meaning": "手紙を（書く / 使う）。"
    },
    {
        "word": "말하다",
        "meaning": "話す",
        "sentence": "한국어로 **말하다**.",
        "sentence_meaning": "韓国語で（話す）。"
    },
    {
        "word": "사람",
        "meaning": "人",
        "sentence": "좋은 **사람**.",
        "sentence_meaning": "良い（人）。"
    },
    {
        "word": "친구",
        "meaning": "友達",
        "sentence": "친한 **친구**.",
        "sentence_meaning": "親しい（友達）。"
    },
    {
        "word": "선생님",
        "meaning": "先生",
        "sentence": "한국어 **선생님**.",
        "sentence_meaning": "韓国語の（先生）。"
    },
    {
        "word": "학교",
        "meaning": "学校",
        "sentence": "즐거운 **학교**.",
        "sentence_meaning": "楽しい（学校）。"
    },
    {
        "word": "집",
        "meaning": "家",
        "sentence": "나의 **집**.",
        "sentence_meaning": "私の（家）。"
    },
    {
        "word": "물",
        "meaning": "水",
        "sentence": "차가운 **물**.",
        "sentence_meaning": "冷たい（水）。"
    },
    {
        "word": "밥",
        "meaning": "ご飯",
        "sentence": "따뜻한 **밥**.",
        "sentence_meaning": "温かい（ご飯）。"
    },
    {
        "word": "책",
        "meaning": "本",
        "sentence": "재미있는 **책**.",
        "sentence_meaning": "面白い（本）。"
    },
    {
        "word": "돈",
        "meaning": "お金",
        "sentence": "많은 **돈**.",
        "sentence_meaning": "たくさんのお（金）。"
    },
    {
        "word": "시간",
        "meaning": "時間",
        "sentence": "남은 **시간**.",
        "sentence_meaning": "残りの（時間）。"
    },
]

# 各単語にダミーの選択肢（四択用）を自動設定
ALL_MEANINGS = [item["meaning"] for item in WORDS_DB]

for item in WORDS_DB:
    # 正解以外の意味から3つ選ぶ
    other_meanings = [m for m in ALL_MEANINGS if m != item["meaning"]]
    wrong_choices = random.sample(other_meanings, min(3, len(other_meanings)))
    options = [item["meaning"]] + wrong_choices
    random.shuffle(options)
    item["options"] = options

st.set_page_config(page_title="ハングル検定5級 例文付き単語クイズ", page_icon="🇰🇷", layout="centered")

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

st.title("🇰🇷 ハングル検定5級 例文クイズアプリ")
st.write("簡単な例文の中で使われている韓国語（**太字**）の意味を当てよう！間違えた問題は復習モードで再挑戦できます。")

# サイドバー：モード選択と統計
st.sidebar.header("⚙️ メニュー・設定")
mode = st.sidebar.radio("モード選択", ["通常モード (全単語)", "復習モード (間違えた単語のみ)"])

# モードが変わったときに現在の問題をリセット
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

# 問題を生成・取得する関数
def generate_new_question(mode_type):
    if mode_type == "復習モード (間違えた単語のみ)":
        available_pool = [w for w in WORDS_DB if w["word"] in st.session_state.wrong_words]
        if not available_pool:
            return None
    else:
        available_pool = WORDS_DB

    q = random.choice(available_pool)
    return q

# 初回、または問題がない場合に問題を設定
if st.session_state.current_question is None:
    st.session_state.current_question = generate_new_question(mode)

# 復習モードで単語がない場合のハンドリング
if mode == "復習モード (間違えた単語のみ)" and len(st.session_state.wrong_words) == 0:
    st.info("🎉 現在、復習が必要な単語はありません！「通常モード」でクイズを進めてみましょう。")
else:
    q = st.session_state.current_question

    st.subheader("Q. 次の例文の太字の部分（**単語**）の意味として正しいものは？")
    
    # 例文を大きく表示
    st.markdown(
        f"<h2 style='text-align: center; color: #2C3E50; padding: 20px; background-color: #F0F4F8; border-radius: 10px;'>{q['sentence']}</h2>",
        unsafe_allow_html=True
    )
    
    # ターゲットの単語を補足表示
    st.write(f"対象の単語: **{q['word']}**")

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
                "sentence": q["sentence"],
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
            st.write(f"- **{h['sentence']}** ({h['word']}) : あなたの回答 = {h['user_answer']} ({status})")

with tab2:
    st.subheader("現在復習が必要な単語")
    if not st.session_state.wrong_words:
        st.success("現在、間違えた単語はありません！")
    else:
        for w in st.session_state.wrong_words:
            meaning = next((item["meaning"] for item in WORDS_DB if item["word"] == w), "")
