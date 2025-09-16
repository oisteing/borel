
import streamlit as st
import random

# Function to parse questions from the text file
def parse_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ',' in line:
                parts = line.strip().split(',')
                question_text = parts[0].strip()
                levels = [p.strip() for p in parts[1:]]
                questions.append((question_text, levels))
    return questions

# Function to determine the answer (JA/NEI) and explanation
def evaluate_question(question_text):
    # Enkel heuristikk – kan byttes ut med ekte sannsynlighetsberegning
    answer = "JA" if "minst" in question_text.lower() or "få en" in question_text.lower() else "NEI"
    explanation = f"""
    Dette er en forenklet vurdering basert på nøkkelord i spørsmålet: '{question_text}'.

    For nøyaktig sannsynlighetsutregning må man analysere utfallsrommet og telle gunstige utfall.
    """
    return answer, explanation

# Load questions from file
question_file = "questions.txt"
questions = parse_questions(question_file)

# Streamlit UI
st.title("🎲 Borel-spørsmål om sannsynlighet")

# Select level
level_map = {"Barnetrinn": "B", "Mellomtrinn": "M", "Ungdomstrinn": "U"}
selected_level = st.selectbox("Velg nivå", list(level_map.keys()))
level_code = level_map[selected_level]

# Filter questions by selected level
filtered_questions = [q for q in questions if level_code in q[1]]

# Session state to store current question
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# Button to get a new question
if st.button("🆕 Still nytt spørsmål"):
    st.session_state.current_question = random.choice(filtered_questions)

# Display current question
if st.session_state.current_question:
    st.subheader("Spørsmål:")
    st.write(st.session_state.current_question[0])

    # Button to show answer
    if st.button("📢 Vis svar (JA/NEI)"):
        answer, _ = evaluate_question(st.session_state.current_question[0])
        st.success(f"Svar: {answer}")

    # Button to show explanation
    if st.button("🧮 Vis utregning"):
        _, explanation = evaluate_question(st.session_state.current_question[0])
        st.info(explanation)
else:
    st.write("Trykk på 'Still nytt spørsmål' for å starte.")
