# streamlit_app.py
import streamlit as st
from io import StringIO
import os

st.set_page_config(page_title="Borel som spel", page_icon="🎲", layout="centered")

st.title("🎲 Borel som spel")

st.markdown(
    """
    Last opp ei tekstfil **eller** legg ei fil kalt `borel.txt` i samme mappe som denne appen.
    Hver linje skal ha formatet:  
    `tekst før komma, LaTeX-uttrykk etter komma`
    """,
)

# ---------- Hjelpefunksjoner ----------
def parse_lines(raw_text: str):
    """Returnerer liste av (oppgavetekst, latex) fra rå tekst. Hopper over tomme linjer og kommentarer (#...)."""
    items = []
    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//") or line.startswith("---"):
            continue
        if "," not in line:
            # linjer uten komma ignoreres
            continue
        left, right = line.split(",", 1)
        oppgave = left.strip()
        latex = right.strip()

        # Fjern omsluttende $ ... $ hvis brukeren allerede har satt det
        if latex.startswith("$") and latex.endswith("$") and latex.count("$") == 2:
            latex = latex[1:-1].strip()

        items.append((oppgave, latex))
    return items

def load_tasks():
    """Prøv først opplasting, ellers prøv 'borel.txt' i arbeidsmappa."""
    uploaded = st.file_uploader("Last opp tekstfila med Borel-oppgåver (.txt)", type=["txt"])
    if uploaded is not None:
        text = uploaded.read().decode("utf-8")
        return parse_lines(text), "opplasta fil"

    # Fallback: lokal fil borel.txt hvis den finnes
    if os.path.exists("borel.txt"):
        with open("borel.txt", "r", encoding="utf-8") as f:
            return parse_lines(f.read()), "borel.txt"
    return [], None

# ---------- Last opp/les oppgåver ----------
items, source = load_tasks()

if "idx" not in st.sess
