import streamlit as st
import random
import re

# Function to parse questions from the text file
def parse_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r"^(\d+)\. (.*?), \$P = ([0-9.]+)\$, utregning: \$(.*?)\$, (.*)$", line.strip())
            if match:
                q_id = int(match.group(1))
                text = match.group(2)
                prob = float(match.group(3))
                calc = match.group(4)
                levels = [lvl.strip() for lvl in match.group(5).split(',')]
                questions.append({
                    "id": q_id,
                    "text": text,
                    "probability": prob,
                    "calculation": calc,
                    "levels": levels
                })
    return questions

# Load questions
question_file = "questions_with_probabilities.txt"
questions = parse_questions(question_file)

# UI setup
st.set_page_config(page_title="Borel-spørsmål", page_icon="🎲", layout="centered")
st.title("🎲 Borel-spørsmål om sannsynlighet")

# Nivåvalg
level_map = {"Barnetrinn": "B", "Mellomtrinn": "M", "Ungdomstrinn": "U"}
selected_level = st.selectbox("Velg nivå", list(level_map.keys()))
level_code = level_map[selected_level]

# Filtrer spørsmål
filtered_questions = [q for q in questions if level_code in q["levels"]]

# Session state
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# Nytt spørsmål
if st.button("🆕 Still nytt spørsmål") and filtered_questions:
    st.session_state.current_question = random.choice(filtered_questions)

# Vis spørsmål som kort
if st.session_state.current_question:
    q = st.session_state.current_question
    st.markdown(
        f"""
        <div style="
            background-color: #f0f8ff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
            margin-top: 30px;
            margin-bottom: 30px;
            text-align: center;
        ">
            <h2 style="color: #222; font-size: 28px;">{q['text']}</h2>
        </div>
        """, unsafe_allow_html=True
    )

    # Vis svar
    if st.button("📢 Vis svar (JA/NEI)"):
        svar = "JA" if q["probability"] > 0.05 else "NEI"  # Juster terskel etter behov
        st.success(f"Svar: {svar} (P = {q['probability']:.4f})")

    # Vis utregning
    if st.button("🧮 Vis utregning"):
        st.latex(q["calculation"])
else:
    st.write("Trykk på 'Still nytt spørsmål' for å starte.")
