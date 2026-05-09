import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy

def calculate_metrics(tokens):
    counts = tokens.value_counts()
    freqs = counts / counts.sum()
    ent = entropy(freqs, base=2)
    unique_words = []
    total_words = []
    seen = set()
    for i, word in enumerate(tokens):
        seen.add(word)
        if (i + 1) % 10 == 0:
            total_words.append(i + 1)
            unique_words.append(len(seen))
    return ent, total_words, unique_words

def run_signature_analysis(csv_path):
    try:
        df = pd.read_csv(csv_path)
        tokens = df['token'].dropna().astype(str)
        ent_orig, x_heaps, y_heaps = calculate_metrics(tokens)
        shuffled_tokens = tokens.sample(frac=1).reset_index(drop=True)
        ent_shuff, _, _ = calculate_metrics(shuffled_tokens)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        ax1.plot(x_heaps, y_heaps, label='Folio 88r', color='blue')
        ax1.set_title("Heaps' Law: Crescita Vocabolario")
        ax1.set_xlabel("Token Totali")
        ax1.set_ylabel("Token Unici")
        ax1.grid(True)
        ax2.bar(['Originale', 'Randomizzato'], [ent_orig, ent_shuff], color=['blue', 'gray'])
        ax2.set_title("Entropia di Shannon (H)")
        ax2.set_ylabel("Bits")
        plt.tight_layout()
        plt.savefig('results/statistical_signature.png')
        print(f"--- FIRMA STATISTICA ---")
        print(f"Entropia Unigrammi: {ent_orig:.3f} bits")
        print(f"Differenza con Random: {ent_shuff - ent_orig:.3f} bits")
        print(f"Rapporto Vocabolario/Testo: {len(tokens.unique())/len(tokens):.3f}")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/data_88r.csv'
    run_signature_analysis(path)
