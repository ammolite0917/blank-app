import streamlit as st
import random

# ページの設定
st.set_page_config(page_title="ハングル検定5級 単語クイズ", page_icon="🇰🇷", layout="centered")

# ハングル検定5級の代表的な必須単語データ (韓国語, 読み, 意味)
VOCAB_LIST = [
    {"kr": "가다", "read": "カダ", "meaning": "行く"},
    {"kr": "오다", "read": "オダ", "meaning": "来る"},
    {"kr": "먹다", "read": "モクタ", "meaning": "食べる"},
    {"kr": "마시다", "read": "マシダ", "meaning": "飲む"},
    {"kr": "보다", "read": "ポダ", "meaning": "見る"},
    {"kr": "사다", "read": "サダ", "meaning": "買う"},
    {"kr": "자다", "read": "ジャダ", "meaning": "寝る"},
    {"kr": "일하다", "read": "イラダ", "meaning": "働く"},
    {"kr": "쉬다", "read": "シュダ", "meaning": "休む"},
    {"kr": "만나다", "read": "マンナダ", "meaning": "会う"},
    {"kr": "책", "read": "チェク", "meaning": "本"},
    {"kr": "가사", "read": "カサ", "meaning": "歌詞"}, # 変更用プレースホルダー等
    {"kr": "연필", "read": "ヨンプル", "meaning": "鉛筆"},
    {"kr": "공책", "read": "ゴンチェク", "meaning": "ノート"},
    {"kr": "의자", "read": "ウィジャ", "meaning": "椅子"},
    {"kr": "책상", "read": "チェクサン", "meaning": "机"},
    {"kr": "학교", "read": "ハッキョ", "meaning": "学校"},
    {"kr": "선생님", "read": "ソンセンニム", "meaning": "先生"},
    {"kr": "학생", "read": "ハクセン", "meaning": "学生"},
    {"kr": "친구", "read": "チング", "meaning": "友達"},
    {"kr": "오늘", "read": "オヌル", "meaning": "今日"},
    {"kr": "내일", "read": "ネイル", "meaning": "明日"},
    {"kr": "어제", "read": "オジェ", "meaning": "昨日"},
    {"kr": "시간", "read": "シガン", "meaning": "時間"},
    {"kr": "돈", "read": "トン", "meaning": "お金"},
    {"kr": "물", "read": "ムル", "meaning": "水"},
    {"kr": "밥", "read": "パプ", "meaning": "ご飯"},
    {"kr": "김치", "read": "キムチ", "meaning": "キムチ"},
    {"kr": "고기", "read": "コギ", "meaning": "肉"},
    {"kr": "야채", "read": "ヤチェ", "meaning": "野菜"},
]

# セッションステートの初期化
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []  # 履歴: [{"kr":..., "meaning":..., "correct": True/False}]

if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = []   # 間違えた単語のリスト

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "通常モード"

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "options" not in st.session_state:
    st.session_state.options = []

if "answered" not in st.session_state:
    st.session_state.answered = False

# タイトル
st.title("🇰🇷 ハングル検定5級 単語クイズアプリ")
st.write("ハン検5級の必須単語をマスターしよう！")

# サイドバー：モード選択と成績確認
st.sidebar.header("メニュー")
mode = st.sidebar.radio("学習モードを選んでね", ["通常モード (全単語)", "復習モード (間違えた単語のみ)"])

if mode != st.session_state.current_mode:
    st.session_state.current_mode = mode
    st.session_state.current_question = None
    st.session_state.answered = False
    st.rerun()

# 成績・統計
total_answered = len(st.session_state.quiz_history)
correct_count = sum(1 for h in st.session_state.quiz_history if h["correct"])
accuracy = (correct_count / total_answered * 100) if total_answered > 0 else 0

st.sidebar.markdown("---")
st.sidebar.subheader("📊 あなたの学習記録")
st.sidebar.write(f"回答数: **{total_answered}** 問")
st.sidebar.write(f"正答率: **{accuracy:.1f}%**")
st.sidebar.write(f"間違えた単語の数: **{len(st.session_state.wrong_words)}** 個")

if st.sidebar.button("🧹 記録をリセット"):
    st.session_state.quiz_history = []
    st.session_state.wrong_words = []
    st.session_state.current_question = None
    st.session_state.answered = False
    st.rerun()

# 問題生成関数
def generate_question():
    target_pool = VOCAB_LIST
    if st.session_state.current_mode == "復習モード (間違えた単語のみ)":
        if len(st.session_state.wrong_words) > 0:
            target_pool = st.session_state.wrong_words
        else:
            st.warning("復習する単語がありません！通常モードでたくさん問題を解いてみましょう。")
            return

    # ランダムに問題を選ぶ
    q = random.choice(target_pool)
    st.session_state.current_question = q

    # 選択肢を作成 (正解1つ + ダミー3つ)
    other_pool = [v["meaning"] for v in VOCAB_LIST if v["meaning"] != q["meaning"]]
    dummies = random.sample(other_pool, min(3, len(other_pool)))
    options = dummies + [q["meaning"]]
    random.shuffle(options)
    st.session_state.options = options
    st.session_state.answered = False

# 問題がまだない、または次の問題に進む場合
if st.session_state.current_question is None:
    if st.session_state.current_mode == "復習モード (間違えた単語のみ)" and len(st.session_state.wrong_words) == 0:
        st.info("現在、復習すべき間違えた単語はありません。")
    else:
        generate_question()
        st.rerun()

# クイズ出題画面
if st.session_state.current_question:
    q = st.session_state.current_question
    
    st.subheader(f"📝 問題 ({st.session_state.current_mode})")
    st.markdown(f"次の韓国語の意味として正しいものはどれでしょう？")
    
    # 単語を大きく表示
    st.markdown(f"<h1 style='text-align: center; color: #4A90E2;'>{q['kr']}</h1>", unsafe_allow_html=True)
    
    # 解答フォーム
    with st.form(key="quiz_form"):
        selected_option = st.radio("選択肢:", st.session_state.options, index=None)
        submit_button = st.form_submit_button(label="回答する")

    if submit_button:
        if selected_option is None:
            st.warning("選択肢を一つ選んでください。")
        else:
            st.session_state.answered = True
            is_correct = (selected_option == q["meaning"])
            
            # 履歴に追加
            st.session_state.quiz_history.append({
                "kr": q["kr"],
                "read": q["read"],
                "meaning": q["meaning"],
                "correct": is_correct
            })

            # 間違えた単語リストの管理
            # 既にリストになければ追加、正解したらリストから削除
            existing_words = [w["kr"] for w in st.session_state.wrong_words]
            if not is_correct:
                if q["kr"] not in existing_words:
                    st.session_state.wrong_words.append(q)
            else:
                # 正解できたら復習リストから外す
                st.session_state.wrong_words = [w for w in st.session_state.wrong_words if w["kr"] != q["kr"]]

            if is_correct:
                st.success("🎉 正解です！素晴らしい！")
            else:
                st.error(f"❌ 残念！正解は **{q['meaning']}** （読み：{q['read']}）でした。")
            
            st.rerun()

    if st.session_state.answered:
        if st.button("▶️ 次の問題へ"):
            generate_question()
            st.rerun()

# 탭切り替えで「間違えた単語一覧」を表示
st.markdown("---")
st.subheader("📚 間違えた単語の一覧・復習用リスト")
if len(st.session_state.wrong_words) == 0:
    st.info("現在、覚えるべき間違えた単語はありません。この調子で頑張りましょう！")
else:
    st.write(f"現在 **{len(st.session_state.wrong_words)}個** の単語が登録されています。")
    for idx, w in enumerate(st.session_state.wrong_words, 1):
        st.write(f"{idx}. **{w['kr']}** （読み: {w['read']}） - 意味: **{w['meaning']}**")
```

### アプリの特徴
1. **通常モードと復習モードの切り替え**: サイドバーからワンクリックで切り替え可能です。
2. **自動リスト更新**: 間違えた問題は自動で「間違えた単語の一覧」にストックされ、復習モードで出題されます。見事正解すると自動的にそのリストから外れていくため、効率よく苦手を克服できます。
3. **解答履歴の保持**: セッション中、解いた問題の履歴と正答率がリアルタイムでサイドバーに表示されます。
