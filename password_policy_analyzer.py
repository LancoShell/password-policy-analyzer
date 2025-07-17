import pandas as pd
import matplotlib.pyplot as plt
import re
import math
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

COMMON_PATTERNS = [
    '123', 'password', 'qwerty', 'admin', 'letmein', 'abc', 'welcome', 'login',
    'user', 'test', 'guest', 'root', 'pass', '111', '000'
]

def estimate_entropy(pw):
    """Stima semplificata dell'entropia in bit della password."""
    pool_size = 0
    if re.search(r'[a-z]', pw): pool_size += 26
    if re.search(r'[A-Z]', pw): pool_size += 26
    if re.search(r'\d', pw): pool_size += 10
    if re.search(r'[\W_]', pw): pool_size += 32  # simboli comuni
    
    if pool_size == 0:
        return 0
    entropy = len(pw) * math.log2(pool_size)
    return entropy

def check_common_patterns(pw, patterns=COMMON_PATTERNS):
    for pat in patterns:
        if pat.lower() in pw.lower():
            return True
    return False

def analyze_password(pw):
    analysis = {}
    analysis['length'] = len(pw)
    analysis['has_upper'] = bool(re.search(r'[A-Z]', pw))
    analysis['has_lower'] = bool(re.search(r'[a-z]', pw))
    analysis['has_digit'] = bool(re.search(r'\d', pw))
    analysis['has_symbol'] = bool(re.search(r'[\W_]', pw))
    analysis['common_pattern'] = check_common_patterns(pw)
    analysis['entropy'] = estimate_entropy(pw)
    return analysis

def load_passwords(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'password' not in df.columns:
            raise ValueError("Il file CSV deve contenere una colonna 'password'")
        return df
    except Exception as e:
        logging.error(f"Errore caricamento file: {e}")
        raise

def analyze_dataset(df):
    logging.info("Inizio analisi dataset")
    results = df['password'].apply(analyze_password)
    analysis_df = pd.DataFrame(results.tolist())
    combined = pd.concat([df, analysis_df], axis=1)
    logging.info("Analisi completata")
    return combined

def generate_report(df, save_csv=False, csv_name='password_policy_report.csv'):
    total = len(df)
    if total == 0:
        logging.warning("Dataset vuoto!")
        return
    
    print(f"\n=== REPORT PASSWORD POLICY ===\n")
    print(f"Totale password analizzate: {total}")
    print(f"Lunghezza media: {df['length'].mean():.2f}")
    print(f"Lunghezza min/max: {df['length'].min()} / {df['length'].max()}")
    print(f"Entropia media stimata (bit): {df['entropy'].mean():.2f}")
    print(f"Entropia min/max: {df['entropy'].min():.2f} / {df['entropy'].max():.2f}\n")
    
    for col in ['has_upper', 'has_lower', 'has_digit', 'has_symbol', 'common_pattern']:
        perc = df[col].mean() * 100
        print(f"Percentuale con {col}: {perc:.1f}%")
    
    # Percentili lunghezza e entropia
    print("\nPercentili lunghezza password:")
    print(df['length'].quantile([0.25, 0.5, 0.75, 0.9]))
    print("\nPercentili entropia stimata:")
    print(df['entropy'].quantile([0.25, 0.5, 0.75, 0.9]))
    
    # Suggerimenti
    print("\n--- Suggerimenti ---")
    if df['length'].mean() < 12:
        print("- Migliorare la lunghezza minima consigliata a 12+ caratteri.")
    if df['has_upper'].mean() < 0.8:
        print("- Incentivare l'uso di lettere maiuscole.")
    if df['has_digit'].mean() < 0.8:
        print("- Inserire obbligo di almeno una cifra.")
    if df['has_symbol'].mean() < 0.5:
        print("- Considerare l'obbligo di simboli speciali.")
    if df['common_pattern'].mean() > 5:
        print("- Eliminare pattern comuni facilmente indovinabili.")
    if df['entropy'].mean() < 50:
        print("- Promuovere password con maggiore entropia (più casualità).")
    
    if save_csv:
        try:
            df.to_csv(csv_name, index=False)
            logging.info(f"Report salvato in {csv_name}")
        except Exception as e:
            logging.error(f"Errore salvataggio CSV: {e}")
    
    plot_statistics(df)

def plot_statistics(df):
    plt.style.use('ggplot')
    fig, axs = plt.subplots(2, 2, figsize=(14,10))
    
    # Distribuzione lunghezza
    axs[0,0].hist(df['length'], bins=range(df['length'].min(), df['length'].max()+2), color='skyblue')
    axs[0,0].set_title('Distribuzione lunghezza password')
    axs[0,0].set_xlabel('Lunghezza')
    axs[0,0].set_ylabel('Conteggio')
    
    # Distribuzione entropia
    axs[0,1].hist(df['entropy'], bins=30, color='lightgreen')
    axs[0,1].set_title('Distribuzione entropia stimata (bit)')
    axs[0,1].set_xlabel('Entropia')
    axs[0,1].set_ylabel('Conteggio')
    
    # Percentuale caratteristiche
    features = ['has_upper', 'has_lower', 'has_digit', 'has_symbol', 'common_pattern']
    percents = [df[f].mean()*100 for f in features]
    labels = ['Maiuscole', 'Minuscole', 'Cifre', 'Simboli', 'Pattern comuni']
    colors = ['green', 'blue', 'orange', 'red', 'gray']
    axs[1,0].bar(labels, percents, color=colors)
    axs[1,0].set_title('Percentuale caratteristiche password')
    axs[1,0].set_ylim(0, 100)
    
    # Top 10 password più frequenti
    top_pw = df['password'].value_counts().head(10)
    axs[1,1].barh(top_pw.index, top_pw.values, color='purple')
    axs[1,1].set_title('Top 10 password più usate')
    axs[1,1].invert_yaxis()
    
    plt.tight_layout()
    plt.show()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Password Policy Analyzer Avanzato")
    parser.add_argument("csv_file", help="File CSV contenente la colonna 'password'")
    parser.add_argument("--save", action="store_true", help="Salva il report analizzato in CSV")
    args = parser.parse_args()
    
    try:
        df = load_passwords(args.csv_file)
        analyzed_df = analyze_dataset(df)
        generate_report(analyzed_df, save_csv=args.save)
    except Exception as e:
        logging.error(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    main()
