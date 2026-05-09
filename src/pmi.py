import pandas as pd
import numpy as np
from collections import Counter
import math

def calculate_pmi(df, window=1):
    tokens = df['token'].tolist()
    total_tokens = len(tokens)
    
    # Frequenza singola
    unigram_counts = Counter(tokens)
    
    # Frequenza coppie (bigrammi)
    bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    bigram_counts = Counter(bigrams)
    
    pmi_results = []
    
    for (a, b), count_ab in bigram_counts.items():
        # Probabilità p(a), p(b), p(a,b)
        pa = unigram_counts[a] / total_tokens
        pb = unigram_counts[b] / total_tokens
        pab = count_ab / (total_tokens - 1)
        
        # Formula PMI: log2( p(a,b) / (p(a)*p(b)) )
        pmi = math.log2(pab / (pa * pb))
        
        pmi_results.append({"word_a": a, "word_b": b, "pmi": pmi, "count": count_ab})
    
    return pd.DataFrame(pmi_results).sort_values(by="pmi", ascending=False)

if __name__ == "__main__":
    df = pd.read_csv("data/raw/folio88r.csv")
    results = calculate_pmi(df)
    results.to_csv("results/pmi_matrix.csv", index=False)
    print("Analisi PMI completata. Top 5 attrazioni trovate:")
    print(results.head(5))
