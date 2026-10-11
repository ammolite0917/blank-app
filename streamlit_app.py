import random
import streamlit as st

# ハングル検定5級の必須単語・例文データ
WORDS_DB = [
    {
        "word": "가다",
        "meaning": "行く",
        "sentence": "학교에 **가다**.",
    },
    {
        "word": "오다",
        "meaning": "来る",
        "sentence": "친구가 **오다**.",
    },
    {
        "word": "먹다",
        "meaning": "食べる",
        "sentence": "밥을 **먹다**.",
    },
    {
        "word": "마시다",
        "meaning": "飲む",
        "sentence": "물을 **마시다**.",
    },
    {
        "word": "보다",
        "meaning": "見る",
        "sentence": "책을 **보다**.",
    },
    {
        "word": "사다",
        "meaning": "買う",
        "sentence": "옷을 **사다**.",
    },
    {
        "word": "자다",
        "meaning": "寝る",
        "sentence": "집에서 **자다**.",
    },
    {
        "word": "읽다",
        "meaning": "読む",
        "sentence": "신문을 **읽다**.",
    },
    {
        "word": "쓰다",
        "meaning": "書く / 使う",
        "sentence": "편지를 **쓰다**.",
    },
    {
        "word": "말하다",
        "meaning": "話す",
        "sentence": "한국어로 **말하다**.",
    },
    {
        "word": "사람",
        "meaning": "人",
        "sentence": "좋은 **사람**.",
    },
    {
        "word": "친구",
        "meaning": "友達",
        "sentence": "친한 **친구**.",
    },
    {
        "word": "선생님",
        "meaning": "先生",
        "sentence": "한국어 **선생님**.",
    },
    {
        "word": "학교",
        "meaning": "学校",
        "sentence": "즐거운 **학교**.",
    },
    {
        "word": "집",
        "meaning": "家",
        "sentence": "나의 **집**.",
    },
    {
        "word": "물",
        "meaning": "水",
        "sentence": "차가운 **물**.",
    },
    {
        "word": "밥",
        "meaning": "ご飯",
        "sentence": "따뜻한 **밥**.",
    },
    {
        "word": "책",
        "meaning": "本",
        "sentence": "재미있는 **책**.",
    },
    {
        "word": "돈",
        "meaning": "お金",
        "sentence": "많은 **돈**.",
    },
    {
        "word": "시간",
        "meaning": "時間",
        "sentence": "남은 **시간**.",
    },
]

ALL_MEANINGS = [item["meaning"] for item in WORDS_DB]

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

# 問題を新しく生成する関数
def generate_new_question(mode_type):
    if mode_type == "復習モード (間違えた単語のみ)":
        available_pool = [w for w in WORDS_DB if w["word"] in st.session_state.wrong_words]
        if not available_pool:
            return None
    else:
        available_pool = WORDS_DB

    item = random.choice(available_pool)
    
    # 選択肢の作成
    other_meanings = [m for m in ALL_MEANINGS if m != item["meaning"]]
    wrong_choices = random.sample(other_meanings, min(3, len(other_meanings)))
    options = [item["meaning"]] + wrong_choices
    random.shuffle(options)

    return {
        "word": item["word"],
        "meaning": item["meaning"],
        "
