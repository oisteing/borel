# --- HJELP: robust LaTeX-rens ---
def clean_latex(s: str) -> str:
    # fjern BOM, \r og null-width/rare whitespace
    s = s.replace("\ufeff", "").replace("\r", "")
    s = s.replace("\u200b", "").replace("\u200e", "").replace("\u200f", "")
    s = s.strip()
    # fjern $ i start/slutt (også hvis bare én side har $)
    while s.startswith("$"):
        s = s[1:].lstrip()
    while s.endswith("$"):
        s = s[:-1].rstrip()
    return s

def parse_lines(raw_text: str):
    """Returnerer liste av (oppgavetekst, latex). Hopper over tomme/kommentar-linjer."""
    items = []
    for raw in raw_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//") or line.startswith("---"):
            continue
        if "," not in line:
            continue
        left, right = line.split(",", 1)  # del kun på første komma
        oppgave = left.strip()
        latex = clean_latex(right)
        if latex:
            items.append((oppgave, latex))
    return items

def load_tasks():
    uploaded = st.file_uploader("Last opp tekstfila med Borel-oppgåver (.txt)", type=["txt"])
    if uploaded is not None:
        text = uploaded.read().decode("utf-8", errors="replace")
        return parse_lines(text), "opplasta fil"

    if os.path.exists("borel.txt"):
        with open("borel.txt", "r", encoding="utf-8-sig", newline="") as f:
            return parse_lines(f.read()), "borel.txt"
    return [], None
