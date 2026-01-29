#!/bin/bash

# 🚀 Script de démarrage rapide pour les contributeurs

echo "======================================================================"
echo "🎯 PHASE 3 - ATTENTION TEST - Configuration Contributeur"
echo "======================================================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python 3 détecté"

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Synchroniser la base de données
echo ""
echo "🔄 Synchronisation de la base de données..."
python3 scripts/sync_database.py

echo ""
echo "======================================================================"
echo "✅ Configuration terminée !"
echo "======================================================================"
echo ""
echo "📋 Prochaines étapes :"
echo ""
echo "1️⃣  Faire tester des participants :"
echo "   Ouvrez 'phase3-attention-test-v2.html' dans un navigateur"
echo ""
echo "2️⃣  Déplacez les JSON téléchargés dans :"
echo "   data/raw_json/"
echo ""
echo "3️⃣  Synchronisez :"
echo "   python3 scripts/sync_database.py"
echo ""
echo "4️⃣  Générez les graphiques (optionnel) :"
echo "   python3 scripts/generate_graphs.py"
echo ""
echo "5️⃣  Partagez vos données :"
echo "   git add data/raw_json/*.json"
echo "   git commit -m \"Ajout de X tests (contributeur: VotreNom)\""
echo "   git push origin main"
echo ""
echo "======================================================================"
