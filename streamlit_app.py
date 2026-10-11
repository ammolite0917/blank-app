import random
import streamlit as st

# ハングル検定5級の必須単語・活用例文データ (すべて韓国語の正しい自然な例文)
WORDS_DB = [
    {
        "word": "가다",
        "meaning": "行く",
        "sentence": "내일 학교에 **가요**.",
    },
    {
        "word": "오다",
        "meaning": "来る",
        "sentence": "친구가 집에 **왔어요**.",
    },
    {
        "word": "먹다",
        "meaning": "食べる",
        "sentence": "아침 밥을 **먹습니다**.",
    },
    {
        "word": "마시다",
        "meaning": "飲む",
        "sentence": "커피를 **안 마셔요**.",
    },
    {
        "word": "보다",
        "meaning": "見る",
        "sentence": "영화를 **봐요**.",
    },
    {
        "word": "사다",
        "meaning": "買う",
        "sentence": "새 옷을 **샀어요**.",
    },
    {
        "word": "자다",
        "meaning": "寝る",
        "sentence": "지금 **안 자요**.",
    },
    {
        "word": "읽다",
        "meaning": "読む",
        "sentence": "한국어 책을 **읽습니다**.",
    },
    {
        "word": "쓰다",
        "meaning": "書く / 使う",
        "sentence": "편지를 **써요**.",
    },
    {
        "word": "말하다",
        "meaning": "話す",
        "sentence": "천천히 **말해 주세요**.",
    },
    {
        "word": "사람",
        "meaning": "人",
        "sentence": "저 **사람**은 누구예요?",
    },
    {
        "word": "친구",
        "meaning": "友達",
        "sentence": "한국 **친구**가 있어요.",
    },
    {
        "word": "선생님",
        "meaning": "先生",
        "sentence": "우리 **선생님**은 친절해요.",
    },
    {
        "word": "학교",
        "meaning": "学校",
        "sentence": "오늘 **학교**에 갑니다.",
    },
    {
        "word": "집",
        "meaning": "家",
        "sentence": "지금 **집**에 가요.",
    },
    {
        "word": "물",
        "meaning": "水",
        "sentence": "시원한 **물**을 주세요.",
    },
    {
        "word": "밥",
        "meaning": "ご飯",
        "sentence": "맛있는 **밥**을 먹어요.",
    },
    {
        "word": "책",
        "meaning": "本",
        "sentence": "이 **책**은 재미있어요.",
    },
    {
        "word": "돈",
        "meaning": "お金",
        "sentence": "지금 **돈**이 없어요.",
    },
    {
        "word": "시간",
        "meaning": "時間",
        "sentence": "지금 **시간**이 있어요?",
    },
]

ALL_MEANINGS = [item["meaning"] for item in WORDS_DB]

st.set_page_config(page_title="ハングル検定5級 活用例文クイズ", page_icon="🇰🇷", layout="centered")

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

st.title("🇰🇷 ハングル検定5級 活用例文クイズ")
st.write("活用された例文（**가요, 갑니다, 안 가요** など）の中から、元の単語の意味を当てよう！")

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

# 問題を新しく生成する関数
def generate_new_question(mode_type):
    if mode_type == "復習モード (間違えた単語のみ)":
        available_pool = [w for w in WORDS_DB if w["word"] in st.session_state.wrong_words]
        if not available_pool:
            return None
    else:
        available_pool = WORDS_DB

    item = random.choice(available_pool)
    
    other_meanings = [m for m in ALL_MEANINGS if m != item["meaning"]]
    wrong_choices = random.sample(other_meanings, min(3, len(other_meanings)))
    options = [item["meaning"]] + wrong_choices
    random.shuffle(options)

    return {
        "word": item["word"],
        "meaning": item["meaning"],
        "sentence": item["sentence"],
        "options": options
    }

# 初回、または問題がない場合に問題を設定
if st.session_state.current_question is None:
    st.session_state.current_question = generate_new_question(mode)

# 復習モードで単語がない場合のハンドリング
if mode == "復習モード (間違えた単語のみ)" and len(st.session_state.wrong_words) == 0:
    st.info("🎉 現在、復習が必要な単語はありません！「通常モード」でクイズを進めてみましょう。")
else:
    q = st.session_state.current_question

    st.subheader("Q. 例文内の太字の部分（活用形）の元となる単語の意味は？")
    
    # 例文の表示
    st.info(f"### 例文： {q['sentence']}")
    st.write(f"対象の原形単語: **{q['word']}**")

    # まだ回答していない場合
    if not st.session_state.answered:
        with st.form(key="quiz_form"):
            selected_answer = st.radio("選択肢を選んでください：", q["options"])
            submit_button = st.form_submit_button(label="
