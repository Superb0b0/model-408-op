import pandas as pd
import matplotlib.pyplot as plt

def analyze_zipf(csv_path):
    # Carica i dati del Folio 88r
    df = pd.read_csv(csv_path)
    
    # Conta quante volte appare ogni parola (token)
    counts = df['token'].value_counts()
    
    # Crea un grafico della distribuzione
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(counts) + 1), counts.values, marker='o')
    plt.title('Distribuzione di Zipf - Folio 88r')
    plt.xlabel('Rango della parola (dalla più comune alla più rara)')
    plt.ylabel('Frequenza')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    
    # Salva il grafico
    plt.savefig('results/zipf_distribution.png')
    print("Analisi completata! Il grafico è in results/zipf_distribution.png")

if __name__ == "__main__":
    analyze_zipf('data/data_88r.csv')
