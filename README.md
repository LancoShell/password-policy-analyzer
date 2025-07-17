# Password Policy Analyzer Avanzato

Tool Python per analizzare e migliorare le policy delle password aziendali a partire da un dataset CSV.

---

## Funzionalità

- Analisi di lunghezza, complessità e presenza di pattern comuni nelle password
- Stima dell'entropia delle password (bit di sicurezza)
- Visualizzazione grafica delle statistiche (distribuzione lunghezza, entropia, caratteristiche, top password)
- Suggerimenti automatici per migliorare la policy di sicurezza
- Salvataggio report analizzato in CSV opzionale

---

## Requisiti

- Python 3.7+
- Pandas
- Matplotlib

Puoi installare le librerie con:

```bash
pip install requirements.txt
```

Esegui lo script:
```bash
python password_policy_analyzer.py passwords_example.csv
```

Per salvare il report analizzato in un file CSV:
```bash
python password_policy_analyzer.py passwords_example.csv --save
```

Esempio di output console:
```bash
=== REPORT PASSWORD POLICY ===

Totale password analizzate: 14
Lunghezza media: 9.43
Lunghezza min/max: 5 / 15
Entropia media stimata (bit): 54.82
Entropia min/max: 26.00 / 93.97

Percentuale con has_upper: 64.3%
Percentuale con has_lower: 100.0%
Percentuale con has_digit: 50.0%
Percentuale con has_symbol: 35.7%
Percentuale con common_pattern: 42.9%

Percentili lunghezza password:
0.25     7.00
0.50     8.00
0.75    11.75
0.90    15.00
Name: length, dtype: float64

Percentili entropia stimata:
0.25    45.53
0.50    56.28
0.75    65.02
0.90    87.53
Name: entropy, dtype: float64

--- Suggerimenti ---
- Migliorare la lunghezza minima consigliata a 12+ caratteri.
- Inserire obbligo di almeno una cifra.
- Considerare l'obbligo di simboli speciali.
- Eliminare pattern comuni facilmente indovinabili.
- Promuovere password con maggiore entropia (più casualità).
```

Autore: https://lancohacker.com | info@lancohacker.com


