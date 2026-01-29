"""
Import des fichiers JSON d'enquête dans la base de données SQLite
"""

import json
import os
import sqlite3
from datetime import datetime
from db_schema import create_database, get_connection

RAW_JSON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw_json')

def import_json_file(filepath, verbose=True):
    """Importe un fichier JSON dans la base de données"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Créer une nouvelle session
        cursor.execute(
            "INSERT INTO survey_sessions (timestamp) VALUES (?)",
            (data.get('timestamp', datetime.now().isoformat()),)
        )
        session_id = cursor.lastrowid
        
        # Importer chaque test
        for test in data.get('tests', []):
            selected_product = test.get('selectedProduct')
            
            if selected_product:
                cursor.execute("""
                    INSERT INTO test_results 
                    (session_id, phase, duration, product_title, product_price, 
                     product_seller, product_location, product_condition, product_days_ago)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    test.get('phase'),
                    test.get('duration'),
                    selected_product.get('title'),
                    selected_product.get('price'),
                    selected_product.get('seller'),
                    selected_product.get('location'),
                    selected_product.get('condition'),
                    selected_product.get('daysAgo')
                ))
                
                result_id = cursor.lastrowid
                
                # Importer les motivations
                for motivation in test.get('motivations', []):
                    cursor.execute(
                        "INSERT INTO motivations (result_id, motivation_type) VALUES (?, ?)",
                        (result_id, motivation)
                    )
        
        conn.commit()
        if verbose:
            print(f"✅ Importé : {os.path.basename(filepath)} (Session ID: {session_id})")
        return True
        
    except Exception as e:
        conn.rollback()
        if verbose:
            print(f"❌ Erreur lors de l'import de {filepath}: {e}")
        return False
        
    finally:
        conn.close()

def import_all_json():
    """Importe tous les fichiers JSON du dossier raw_json"""
    
    if not os.path.exists(RAW_JSON_DIR):
        print(f"⚠️ Le dossier {RAW_JSON_DIR} n'existe pas")
        return
    
    json_files = [f for f in os.listdir(RAW_JSON_DIR) if f.endswith('.json')]
    
    if not json_files:
        print(f"⚠️ Aucun fichier JSON trouvé dans {RAW_JSON_DIR}")
        return
    
    print(f"📂 {len(json_files)} fichier(s) JSON trouvé(s)\n")
    
    success_count = 0
    for filename in json_files:
        filepath = os.path.join(RAW_JSON_DIR, filename)
        if import_json_file(filepath):
            success_count += 1
    
    print(f"\n✅ Import terminé : {success_count}/{len(json_files)} fichier(s) importé(s)")

if __name__ == "__main__":
    print("🔧 Création/Vérification de la base de données...")
    create_database()
    print("\n📥 Import des fichiers JSON...")
    import_all_json()
