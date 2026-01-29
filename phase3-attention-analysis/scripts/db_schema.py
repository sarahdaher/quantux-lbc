"""
Schéma de la base de données SQLite pour l'analyse des tests d'attention
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'attention_results.db')

def create_database():
    """Crée la base de données et les tables si elles n'existent pas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table principale : Sessions d'enquête
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS survey_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table : Résultats de chaque phase
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            phase INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            product_title TEXT,
            product_price REAL,
            product_seller TEXT,
            product_location TEXT,
            product_condition TEXT,
            product_days_ago INTEGER,
            FOREIGN KEY (session_id) REFERENCES survey_sessions(session_id)
        )
    """)
    
    # Table : Motivations (relation many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motivations (
            motivation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            result_id INTEGER NOT NULL,
            motivation_type TEXT NOT NULL,
            FOREIGN KEY (result_id) REFERENCES test_results(result_id)
        )
    """)
    
    # Index pour optimiser les requêtes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON test_results(session_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_duration ON test_results(duration)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_motivation_type ON motivations(motivation_type)")
    
    conn.commit()
    conn.close()
    print(f"✅ Base de données créée : {DB_PATH}")

def get_connection():
    """Retourne une connexion à la base de données"""
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    create_database()
