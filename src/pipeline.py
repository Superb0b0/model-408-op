import os

def load_data(filepath):
    """Carica il file di testo gestendo i percorsi relativi."""
    if not os.path.exists(filepath):
        # Prova a risalire se chiamato da un notebook
        alt_path = os.path.join("..", filepath)
        if os.path.exists(alt_path):
            filepath = alt_path
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_clean_tokens(text):
    """Pulisce il testo e restituisce token e righe."""
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#")]
    tokens = (" ".join(lines)).split()
    return tokens, lines

if __name__ == "__main__":
    # Test rapido se eseguito come script
    try:
        text = load_data("data/voynich_source.txt")
        tokens, lines = get_clean_tokens(text)
        print(f"Successo: {len(tokens)} token trovati.")
    except Exception as e:
        print(f"Errore: {e}")
