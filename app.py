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

if "idx" not in st.session_state:
    st.session_state.idx = 0
if "revealed_for" not in st.session_state:
    # lagrer hvilket indeksnummer som har fått "Vis utregning" trykket
    st.session_state.revealed_for = set()

if not items:
    st.info("Ingen oppgåver funnet ennå. Last opp ei fil, eller legg `borel.txt` i mappe sammen med appen.")
    st.stop()

st.success(f"Fant {len(items)} oppgåver fra {source}.")

# ---------- Navigasjon ----------
cols_top = st.columns([1, 1, 2])
with cols_top[0]:
    if st.button("⬅️ Forrige", use_container_width=True):
        st.session_state.idx = (st.session_state.idx - 1) % len(items)
with cols_top[1]:
    if st.button("Neste ➡️", use_container_width=True):
        st.session_state.idx = (st.session_state.idx + 1) % len(items)

idx = st.session_state.idx
oppgave, latex = items[idx]

st.caption(f"Oppgåve {idx+1} av {len(items)}")

# ---------- "Kort" for oppgåva ----------
card_css = """
<style>
.card {
  border: 1px solid #e6e6e6;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  background: white;
}
.card h3 { margin: 0 0 6px 0; }
.card p { margin: 0; font-size: 1.05rem; }
</style>
"""
st.markdown(card_css, unsafe_allow_html=True)

with st.container():
    st.markdown(
        f"""
        <div class="card">
          <h3>Oppgåve</h3>
          <p>{oppgave}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Knapp for å vise utrekning ----------
btn_key = f"reveal_{idx}"
show = idx in st.session_state.revealed_for

cols = st.columns([1, 2, 1])
with cols[1]:
    if not show:
        if st.button("👀 Vis utregning", key=btn_key, use_container_width=True):
            st.session_state.revealed_for.add(idx)
            show = True
    else:
        st.button("✅ Utregning vist", key=btn_key + "_shown", disabled=True, use_container_width=True)

# ---------- Vis LaTeX-utrekning (hvis avslørt) ----------
if show:
    st.markdown("**Utregning:**")
    try:
        st.latex(latex)
    except Exception:
        # Hvis latex ikke rendres, vis som kode så brukeren kan feilsøke
        st.warning("Klarte ikke å rendre LaTeX. Viser rå tekst i stedet:")
        st.code(latex, language="latex")

# ---------- Bunnnavigasjon ----------
cols_bottom = st.columns([1, 1, 2])
with cols_bottom[0]:
    if st.button("🔁 Start på nytt", use_container_width=True):
        st.session_state.idx = 0
        st.session_state.revealed_for = set()
with cols_bottom[1]:
    if st.button("Neste oppgåve ➡️", key="next_bottom", use_container_width=True):
        st.session_state.idx = (st.session_state.idx + 1) % len(items)
