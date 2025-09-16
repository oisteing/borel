# streamlit_app.py
import os
import streamlit as st

st.set_page_config(page_title="Borel som spel", page_icon="🎲", layout="centered")
st.title("🎲 Borel som spel")

st.markdown(
    """
Vel ei tekstfil **eller** legg `borel.txt` i same mappe.  
Kvar linje skal ha: `tekst før komma, LaTeX-uttrykk etter komma`
"""
)

# ---------- Robust helpers ----------
def clean_latex(s: str) -> str:
    # fjern BOM, CR og rare/usynlege teikn
    for bad in ("\ufeff", "\r", "\u200b", "\u200e", "\u200f"):
        s = s.replace(bad, "")
    s = s.strip()
    # fjern leiiande/etterfølgjande $
    while s.startswith("$"):
        s = s[1:].lstrip()
    while s.endswith("$"):
        s = s[:-1].rstrip()
    return s

def parse_lines(raw_text: str):
    items = []
    bad = []
    for lineno, raw in enumerate(raw_text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith(("#", "//", "---")):
            continue
        if "," not in line:
            bad.append((lineno, line, "Manglar komma"))
            continue
        left, right = line.split(",", 1)  # del berre på første komma
        oppg = left.strip()
        latex = clean_latex(right)
        if not oppg or not latex:
            bad.append((lineno, line, "Tom tekst eller tom LaTeX"))
            continue
        items.append((oppg, latex))
    return items, bad

def load_tasks():
    uploaded = st.file_uploader("Last opp .txt med Borel-oppgåver", type=["txt"])
    if uploaded is not None:
        try:
            text = uploaded.read().decode("utf-8", errors="replace")
            items, bad = parse_lines(text)
            return items, bad, "opplasta fil"
        except Exception as e:
            st.error(f"Klarte ikkje lese opplasta fil: {e}")
            return [], [], None

    if os.path.exists("borel.txt"):
        try:
            with open("borel.txt", "r", encoding="utf-8-sig", newline="") as f:
                items, bad = parse_lines(f.read())
            return items, bad, "borel.txt"
        except Exception as e:
            st.error(f"Klarte ikkje lese borel.txt: {e}")
            return [], [], None
    return [], [], None

# ---------- Hent oppgåver ----------
items, bad_lines, source = load_tasks()

# init state
if "idx" not in st.session_state: st.session_state.idx = 0
if "revealed" not in st.session_state: st.session_state.revealed = {}  # {idx: bool}

# feilrapport (men ikkje blokker appen)
if bad_lines:
    with st.expander("⚠️ Linjer som vart hoppa over (klikk for detaljer)"):
        for lineno, line, why in bad_lines:
            st.write(f"Linje {lineno}: {why}")
            st.code(line)

# ingen oppgåver enno
if not items:
    st.info("Ingen oppgåver funne. Last opp fil eller legg `borel.txt` i mappa.")
    st.stop()

st.success(f"Fant {len(items)} oppgåver frå {source}.")

# ---------- Navigasjon ----------
c1, c2, _ = st.columns([1,1,2])
with c1:
    if st.button("⬅️ Forrige", use_container_width=True):
        st.session_state.idx = (st.session_state.idx - 1) % len(items)
with c2:
    if st.button("Neste ➡️", use_container_width=True):
        st.session_state.idx = (st.session_state.idx + 1) % len(items)

idx = st.session_state.idx
oppg, latex = items[idx]
st.caption(f"Oppgåve {idx+1} av {len(items)}")

# ---------- Kort ----------
st.markdown(
    """
    <div style="border:1px solid #e6e6e6;border-radius:14px;padding:18px 20px;
                box-shadow:0 4px 14px rgba(0,0,0,0.06);background:white;">
      <h3 style="margin:0 0 6px 0;">Oppgåve</h3>
      <p style="margin:0;font-size:1.05rem;">{}</p>
    </div>
    """.format(oppg),
    unsafe_allow_html=True,
)

# ---------- Vis utrekning ----------
show = st.session_state.revealed.get(idx, False)
mid = st.columns([1,2,1])[1]
with mid:
    if not show:
        if st.button("👀 Vis utregning", key=f"reveal_{idx}", use_container_width=True):
            st.session_state.revealed[idx] = True
            show = True
    else:
        st.button("✅ Utregning vist", key=f"shown_{idx}", disabled=True, use_container_width=True)

if show:
    st.markdown("**Utregning:**")
    try:
        st.latex(latex)
    except Exception as e:
        st.warning(f"Klarte ikkje å rendre LaTeX ({e}). Viser råtekst:")
        st.code(latex, language="latex")

# ---------- Bunnknappar ----------
b1, b2, _ = st.columns([1,1,2])
with b1:
    if st.button("🔁 Start på nytt", use_container_width=True):
        st.session_state.idx = 0
        st.session_state.revealed = {}
with b2:
    if st.button("Neste oppgåve ➡️", key="next_bottom", use_container_width=True):
        st.session_state.idx = (st.session_state.idx + 1) % len(items)

# Liten debug (frivillig)
with st.expander("🔧 Debug for gjeldande oppgåve"):
    st.write("repr(latex):")
    st.code(repr(latex))
