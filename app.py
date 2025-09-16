import streamlit as st
import random
import re

# Function to parse questions from the text file
def parse_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r"^(\d+)\.\s+(.*?),\s+\$P\s+=\s+([0-9.]+),\s+utregning:\s+\$(.*?)\$, (.*)$", line.strip())
            if match:
                q_id = int(match.group(1))
                text = match.group(2)
                prob = match.group(3)
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

# Load questions from file
question_file = "questions.txt"
questions = parse_questions(question_file)

# Streamlit UI setup
st.set_page_config(page_title="Borel-spill", page_icon="🎲", layout="centered")
st.title("🎲 Borel-spill om sannsynlighet")

# Nivåvalg
level_map = {"Barnetrinn": "B", "Mellomtrinn": "M", "Ungdomstrinn": "U"}
selected_level = st.selectbox("Velg nivå", list(level_map.keys()))
level_code = level_map[selected_level]

# Filtrer spørsmål basert på valgt nivå
filtered_questions = [q for q in questions if level_code in q["levels"]]

# Velg et tilfeldig spørsmål
if filtered_questions:
    question = random.choice(filtered_questions)
    with st.container():
        st.markdown(f"### Spørsmål {question['id']}")
        st.markdown(f"**{question['text']}**")
        if st.button("Vis svar"):
            st.latex(f"P = {question['probability']}")
            st.markdown("**Utregning:**")
            st.latex(question['calculation'])
else:
    st.warning("Ingen spørsmål tilgjengelig for valgt nivå.")
