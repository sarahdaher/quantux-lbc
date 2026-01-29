"""
Génération de graphiques d'analyse à partir de la base de données
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from db_schema import get_connection

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')

# Configuration du style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def ensure_output_dir():
    """Crée le dossier outputs s'il n'existe pas"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def load_data():
    """Charge les données depuis la base de données"""
    conn = get_connection()
    
    # Requête principale avec jointure
    query = """
        SELECT 
            tr.result_id,
            tr.session_id,
            tr.phase,
            tr.duration,
            tr.product_title,
            tr.product_price,
            tr.product_seller,
            tr.product_location,
            tr.product_condition,
            tr.product_days_ago,
            GROUP_CONCAT(m.motivation_type, ', ') as motivations
        FROM test_results tr
        LEFT JOIN motivations m ON tr.result_id = m.result_id
        GROUP BY tr.result_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def plot_duration_vs_motivation(df):
    """Graphique : Corrélation durée vs motivations"""
    
    # Exploser les motivations (une ligne par motivation)
    df_exploded = df.copy()
    df_exploded['motivations'] = df_exploded['motivations'].fillna('Aucune')
    df_exploded['motivation_list'] = df_exploded['motivations'].str.split(', ')
    df_exploded = df_exploded.explode('motivation_list')
    
    # Labels français pour les motivations
    motivation_labels = {
        'prix-bas': 'Prix bas',
        'prix-eleve': 'Prix élevé',
        'condition': 'Bon état',
        'vendeur': 'Vendeur fiable',
        'localisation': 'Localisation',
        'marque': 'Marque/Modèle',
        'recente': 'Annonce récente',
        'Aucune': 'Aucune motivation'
    }
    
    df_exploded['motivation_label'] = df_exploded['motivation_list'].map(motivation_labels)
    
    # Compter les occurrences par durée et motivation
    pivot_data = df_exploded.groupby(['duration', 'motivation_label']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    pivot_data.plot(kind='bar', ax=ax, width=0.8)
    
    ax.set_title('Motivations de choix par durée d\'observation', fontsize=16, fontweight='bold')
    ax.set_xlabel('Durée (secondes)', fontsize=12)
    ax.set_ylabel('Nombre de sélections', fontsize=12)
    ax.legend(title='Motivations', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticklabels([f'{int(x)}s' for x in pivot_data.index], rotation=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'duration_vs_motivation.png'), dpi=300, bbox_inches='tight')
    print("✅ Graphique créé : duration_vs_motivation.png")
    plt.close()

def plot_price_distribution(df):
    """Graphique : Distribution des prix sélectionnés"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histogramme des prix
    ax1.hist(df['product_price'].dropna(), bins=15, color='#ff6e14', edgecolor='black', alpha=0.7)
    ax1.set_title('Distribution des prix sélectionnés', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Prix (€)', fontsize=12)
    ax1.set_ylabel('Fréquence', fontsize=12)
    ax1.axvline(df['product_price'].mean(), color='red', linestyle='--', linewidth=2, label=f'Moyenne: {df["product_price"].mean():.2f}€')
    ax1.legend()
    
    # Box plot par durée
    df_boxplot = df.dropna(subset=['product_price'])
    df_boxplot['duration_label'] = df_boxplot['duration'].apply(lambda x: f'{x}s')
    
    sns.boxplot(data=df_boxplot, x='duration_label', y='product_price', ax=ax2, palette='Set2')
    ax2.set_title('Prix sélectionnés par durée d\'observation', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Durée', fontsize=12)
    ax2.set_ylabel('Prix (€)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'price_distribution.png'), dpi=300, bbox_inches='tight')
    print("✅ Graphique créé : price_distribution.png")
    plt.close()

def plot_condition_distribution(df):
    """Graphique : Répartition par condition"""
    
    condition_counts = df['product_condition'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = sns.color_palette('pastel')[0:len(condition_counts)]
    
    wedges, texts, autotexts = ax.pie(
        condition_counts.values, 
        labels=condition_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    ax.set_title('Répartition des conditions sélectionnées', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'condition_distribution.png'), dpi=300, bbox_inches='tight')
    print("✅ Graphique créé : condition_distribution.png")
    plt.close()

def plot_top_motivations(df):
    """Graphique : Top motivations globales"""
    
    # Exploser les motivations
    df_exploded = df.copy()
    df_exploded['motivations'] = df_exploded['motivations'].fillna('Aucune')
    df_exploded['motivation_list'] = df_exploded['motivations'].str.split(', ')
    df_exploded = df_exploded.explode('motivation_list')
    
    motivation_labels = {
        'prix-bas': 'Prix bas',
        'prix-eleve': 'Prix élevé',
        'condition': 'Bon état',
        'vendeur': 'Vendeur fiable',
        'localisation': 'Localisation',
        'marque': 'Marque/Modèle',
        'recente': 'Annonce récente',
        'Aucune': 'Aucune'
    }
    
    df_exploded['motivation_label'] = df_exploded['motivation_list'].map(motivation_labels)
    
    motivation_counts = df_exploded['motivation_label'].value_counts()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = sns.color_palette('viridis', len(motivation_counts))
    
    motivation_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_title('Motivations de choix les plus fréquentes', fontsize=16, fontweight='bold')
    ax.set_xlabel('Nombre de sélections', fontsize=12)
    ax.set_ylabel('Motivation', fontsize=12)
    
    # Ajouter les valeurs sur les barres
    for i, v in enumerate(motivation_counts.values):
        ax.text(v + 0.1, i, str(v), va='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'top_motivations.png'), dpi=300, bbox_inches='tight')
    print("✅ Graphique créé : top_motivations.png")
    plt.close()

def plot_time_correlation(df):
    """Graphique : Corrélation temps vs prix moyen sélectionné"""
    
    avg_price_by_duration = df.groupby('duration')['product_price'].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(avg_price_by_duration.index, avg_price_by_duration.values, 
            marker='o', linewidth=3, markersize=10, color='#ff6e14')
    
    ax.set_title('Prix moyen sélectionné selon la durée d\'observation', fontsize=16, fontweight='bold')
    ax.set_xlabel('Durée d\'observation (secondes)', fontsize=12)
    ax.set_ylabel('Prix moyen (€)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(avg_price_by_duration.index)
    ax.set_xticklabels([f'{int(x)}s' for x in avg_price_by_duration.index])
    
    # Ajouter les valeurs
    for x, y in zip(avg_price_by_duration.index, avg_price_by_duration.values):
        ax.text(x, y + 20, f'{y:.0f}€', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'time_vs_price.png'), dpi=300, bbox_inches='tight')
    print("✅ Graphique créé : time_vs_price.png")
    plt.close()

def generate_summary_stats(df):
    """Génère un fichier texte avec les statistiques résumées"""
    
    with open(os.path.join(OUTPUT_DIR, 'summary_stats.txt'), 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("STATISTIQUES RÉSUMÉES - TEST D'ATTENTION PHASE 3\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"📊 Nombre total de sessions : {df['session_id'].nunique()}\n")
        f.write(f"📊 Nombre total de tests : {len(df)}\n\n")
        
        f.write("💰 PRIX\n")
        f.write(f"   - Prix moyen sélectionné : {df['product_price'].mean():.2f}€\n")
        f.write(f"   - Prix minimum : {df['product_price'].min():.2f}€\n")
        f.write(f"   - Prix maximum : {df['product_price'].max():.2f}€\n")
        f.write(f"   - Médiane : {df['product_price'].median():.2f}€\n\n")
        
        f.write("⏱️ DURÉES\n")
        for duration in sorted(df['duration'].unique()):
            count = len(df[df['duration'] == duration])
            avg_price = df[df['duration'] == duration]['product_price'].mean()
            f.write(f"   - {duration}s : {count} tests (prix moyen : {avg_price:.2f}€)\n")
        
        f.write("\n✨ CONDITIONS PRÉFÉRÉES\n")
        for condition, count in df['product_condition'].value_counts().items():
            percentage = (count / len(df)) * 100
            f.write(f"   - {condition} : {count} ({percentage:.1f}%)\n")
        
    print("✅ Statistiques créées : summary_stats.txt")

def main():
    """Fonction principale"""
    print("📊 Génération des graphiques d'analyse...\n")
    
    ensure_output_dir()
    
    # Charger les données
    print("📂 Chargement des données...")
    df = load_data()
    
    if df.empty:
        print("⚠️ Aucune donnée trouvée dans la base de données")
        print("   Veuillez d'abord importer des fichiers JSON avec import_json_to_db.py")
        return
    
    print(f"✅ {len(df)} résultats chargés\n")
    
    # Générer les graphiques
    print("🎨 Création des graphiques...\n")
    plot_duration_vs_motivation(df)
    plot_price_distribution(df)
    plot_condition_distribution(df)
    plot_top_motivations(df)
    plot_time_correlation(df)
    generate_summary_stats(df)
    
    print(f"\n✅ Tous les graphiques ont été générés dans : {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
