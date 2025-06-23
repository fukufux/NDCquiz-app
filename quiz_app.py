import streamlit as st
import random

# ページタイトル
st.title("NDCランダムクイズ(第2区分)")

# 問題を読み込む
quiz = []
with open("questions.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(",")
        if len(parts) == 2:
            quiz.append({"question": parts[0], "answer": parts[1]})

# 問題15問をランダムに選ぶ（セッションに保存）
if "selected_quiz" not in st.session_state:
    st.session_state.selected_quiz = random.sample(quiz, min(15, len(quiz)))
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.answers = []
# --- 出題中 ---
if st.session_state.current < len(st.session_state.selected_quiz):
    q = st.session_state.selected_quiz[st.session_state.current]
    st.subheader(f"Q{st.session_state.current + 1}: {q['question']}")

    with st.form(key="quiz_form"):
        user_input = st.text_input("答えを入力してね", key="answer_input")
        submitted = st.form_submit_button("答える")

    if submitted:
        correct = q["answer"].strip()
        st.session_state.answers.append({
            "question": q["question"],
            "your_answer": user_input.strip(),
            "correct_answer": correct,
            "is_correct": user_input.strip() == correct
        })
        if user_input.strip() == correct:
            st.success("正解！")
            st.session_state.score += 1
        else:
            st.error(f"不正解！正解は {correct}")
        
        # 入力欄をリセット
        del st.session_state["answer_input"]
        st.session_state.current += 1
        st.rerun()
else:
   else:
    st.success(f"クイズ終了！スコア：{st.session_state.score} / {len(st.session_state.selected_quiz)}")

    # 回答一覧表示
    st.subheader("あなたの回答一覧")
    for i, ans in enumerate(st.session_state.answers, 1):
        st.markdown(f"**Q{i}：{ans['question']}**")
        st.markdown(f"- あなたの答え：`{ans['your_answer']}`")
        st.markdown(f"- 正解：`{ans['correct_answer']}`")
        if ans["is_correct"]:
            st.markdown(":white_check_mark: 正解！")
        else:
            st.markdown(":x: 不正解")
        st.markdown("---")

    if st.button("もう一度やる"):
        for key in ["selected_quiz", "score", "current", "answers"]:
            del st.session_state[key]
        st.rerun()

