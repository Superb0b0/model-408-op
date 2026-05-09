import pandas as pd
from src.pmi import calculate_pmi
import json
from datetime import datetime

def run():
    df = pd.read_csv("data/raw/folio88r.csv")
    pmi_df = calculate_pmi(df)

    # Salviamo i risultati migliori nella traccia
    top_5 = pmi_df.head(5).to_dict(orient='records')

    trace = {
        "timestamp": datetime.utcnow().isoformat(),
        "top_pmi_attractions": top_5
    }

    with open("results/execution_trace.json", "w") as f:
        json.dump(trace, f, indent=2)

    pmi_df.to_csv("results/pmi_matrix.csv", index=False)
    print("Pipeline aggiornata con successo!")

if __name__ == "__main__":
    run()
