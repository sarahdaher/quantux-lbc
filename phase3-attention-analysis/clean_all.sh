#!/bin/bash

# 🧹 Script de nettoyage COMPLET (JSON + DB + Graphiques)
# ATTENTION : Supprime TOUT - À utiliser pour repartir de zéro

echo "======================================================================"
echo "🧹 NETTOYAGE COMPLET - SUPPRESSION TOTALE"
echo "======================================================================"
echo ""
echo "⚠️⚠️⚠️  ATTENTION ⚠️⚠️⚠️"
echo ""
echo "Ce script va supprimer TOUTES les données :"
echo "   - La base de données (data/attention_results.db)"
echo "   - Tous les fichiers JSON (data/raw_json/*.json)"
echo "   - Tous les graphiques (outputs/*)"
echo ""
echo "⚠️  CETTE ACTION EST IRRÉVERSIBLE ⚠️"
echo ""
read -p "Tapez 'SUPPRIMER TOUT' pour confirmer : " confirmation

if [ "$confirmation" != "SUPPRIMER TOUT" ]; then
    echo "❌ Annulé"
    exit 0
fi

echo ""
echo "🗑️  Suppression en cours..."

# Supprimer la base de données
if [ -f "data/attention_results.db" ]; then
    rm data/attention_results.db
    echo "✅ Base de données supprimée"
fi

# Supprimer tous les JSON sauf .gitkeep
if [ -d "data/raw_json" ]; then
    find data/raw_json -type f -name "*.json" -delete
    echo "✅ Fichiers JSON supprimés"
fi

# Supprimer les graphiques
if [ -d "outputs" ]; then
    rm -f outputs/*.png outputs/*.jpg outputs/*.pdf outputs/*.txt
    echo "✅ Graphiques supprimés"
fi

echo ""
echo "======================================================================"
echo "✅ Nettoyage complet terminé !"
echo "======================================================================"
echo ""
echo "Le système est maintenant vierge."
echo "Vous pouvez recommencer à collecter des données."
echo ""
