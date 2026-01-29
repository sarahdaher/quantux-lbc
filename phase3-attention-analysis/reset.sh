#!/bin/bash

# 🗑️  Script de réinitialisation pour la phase de test
# ATTENTION : Supprime la DB et les graphiques (pas les JSON)

echo "======================================================================"
echo "🗑️  RÉINITIALISATION - MODE TEST"
echo "======================================================================"
echo ""
echo "⚠️  Ce script va supprimer :"
echo "   - La base de données (data/attention_results.db)"
echo "   - Tous les graphiques (outputs/*.png, outputs/*.txt)"
echo ""
echo "✅ Les fichiers JSON dans data/raw_json/ seront CONSERVÉS"
echo ""
read -p "Êtes-vous sûr de vouloir continuer ? (oui/non) : " confirmation

if [ "$confirmation" != "oui" ]; then
    echo "❌ Annulé"
    exit 0
fi

echo ""
echo "🗑️  Suppression en cours..."

# Supprimer la base de données
if [ -f "data/attention_results.db" ]; then
    rm data/attention_results.db
    echo "✅ Base de données supprimée"
else
    echo "ℹ️  Pas de base de données à supprimer"
fi

# Supprimer les graphiques
if [ -d "outputs" ]; then
    rm -f outputs/*.png outputs/*.jpg outputs/*.pdf outputs/*.txt
    echo "✅ Graphiques supprimés"
else
    echo "ℹ️  Pas de graphiques à supprimer"
fi

echo ""
echo "======================================================================"
echo "✅ Réinitialisation terminée !"
echo "======================================================================"
echo ""
echo "💡 Pour reconstruire avec les JSON existants :"
echo "   python3 scripts/sync_database.py"
echo "   python3 scripts/generate_graphs.py"
echo ""
