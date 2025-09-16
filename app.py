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
question_file = "questions.txt"
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

# Session
