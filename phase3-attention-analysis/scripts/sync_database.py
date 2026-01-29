"""
Script de synchronisation : reconstruit la base de données depuis TOUS les JSON
À utiliser après un git pull ou après avoir ajouté de nouveaux JSON
"""

import os
import sqlite3
from db_schema import create_database, DB_PATH
from import_json_to_db import import_json_file, RAW_JSON_DIR

def clear_database():
    """Vide complètement la base de données"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🗑️  Ancienne base de données supprimée")

def sync_database():
    """Reconstruit la base de données depuis tous les JSON"""
    
    print("=" * 70)
    print("🔄 SYNCHRONISATION DE LA BASE DE DONNÉES")
    print("=" * 70)
    print()
    
    # 1. Supprimer l'ancienne DB
    clear_database()
    
    # 2. Créer une nouvelle DB vide
    print("🔧 Création d'une nouvelle base de données...")
    create_database()
    print()
    
    # 3. Importer TOUS les JSON
    if not os.path.exists(RAW_JSON_DIR):
        print(f"⚠️  Le dossier {RAW_JSON_DIR} n'existe pas")
        return
    
    json_files = sorted([f for f in os.listdir(RAW_JSON_DIR) if f.endswith('.json')])
    
    if not json_files:
        print(f"⚠️  Aucun fichier JSON trouvé dans {RAW_JSON_DIR}")
        print("   Effectuez des tests avec phase3-attention-test-v2.html")
        print("   et placez les JSON dans data/raw_json/")
        return
    
    print(f"📂 {len(json_files)} fichier(s) JSON trouvé(s)")
    print()
    
    success_count = 0
    for i, filename in enumerate(json_files, 1):
        filepath = os.path.join(RAW_JSON_DIR, filename)
        print(f"[{i}/{len(json_files)}] Import de {filename}...", end=" ")
        
        if import_json_file(filepath):
            success_count += 1
            print("✅")
        else:
            print("❌")
    
    print()
    print("=" * 70)
    print(f"✅ Synchronisation terminée : {success_count}/{len(json_files)} fichier(s) importé(s)")
    print("=" * 70)
    print()
    
    # Afficher les statistiques
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM survey_sessions")
    session_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM test_results")
    test_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM motivations")
    motivation_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"📊 Statistiques de la base de données :")
    print(f"   - Sessions d'enquête : {session_count}")
    print(f"   - Tests enregistrés : {test_count}")
    print(f"   - Motivations collectées : {motivation_count}")
    print()
    print("💡 Prochaines étapes :")
    print("   1. Lancez : python3 scripts/generate_graphs.py")
    print("   2. Consultez les graphiques dans outputs/")
    print()

if __name__ == "__main__":
    sync_database()
