# Changelog - Phase 3 Attention Test

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [1.0.0] - 2026-01-29

### ✨ Fonctionnalités Initiales

#### Interface de Test
- Interface web `phase3-attention-test-v2.html`
- Test d'attention en 3 phases (6s, 15s, 30s)
- 10 annonces Le Bon Coin avec vrais produits (smartphones)
- Images Unsplash pour illustrations réalistes
- Prix répartis de 299€ à 1099€
- Scroll activé pendant observation et sélection
- Modal de sélection des motivations (7 options multi-choix)
- Export JSON automatique avec timestamp unique

#### Base de Données
- SQLite avec 3 tables (survey_sessions, test_results, motivations)
- Schéma relationnel complet
- Index pour optimisation des requêtes

#### Scripts Python
- `db_schema.py` : Définition du schéma
- `import_json_to_db.py` : Import individuel de JSON
- `sync_database.py` : Reconstruction complète de la DB
- `generate_graphs.py` : 5 graphiques + statistiques textuelles

#### Graphiques d'Analyse
- Motivations par durée (barres groupées)
- Distribution des prix (histogramme + boxplot)
- Conditions préférées (pie chart)
- Top motivations (barres horizontales)
- Corrélation temps/prix (graphique linéaire)
- Statistiques résumées (fichier texte)

#### Scripts Shell
- `setup.sh` : Installation automatique
- `reset.sh` : Réinitialisation (mode test)
- `clean_all.sh` : Nettoyage complet

#### Documentation
- `README.md` : Documentation exhaustive (10+ sections)
- `CONTRIBUTING.md` : Guide de contribution collaborative
- `ARCHITECTURE.txt` : Schéma visuel du système
- `QUICKSTART.txt` : Guide de démarrage rapide
- `requirements.txt` : Dépendances Python commentées

### 🏗️ Architecture Collaborative

- Workflow Git-friendly (JSON = source de vérité)
- Pas de conflit possible (noms uniques avec timestamp)
- Accumulation automatique des contributions
- DB reconstruite à la demande

### 🎯 Objectifs de Collecte

- Minimum : 30 tests
- Optimal : 100+ tests
- Idéal : 300+ tests

### 📦 Fichiers d'Exemple

- 2 JSON d'exemple pour tester le système
- Génération automatique de 6 résultats de test

---

## [Prochaines Versions Possibles]

### [1.1.0] - Améliorations UX (À venir)

**Propositions** :
- [ ] Eye-tracking avec WebGazer.js (déjà implémenté dans phase2)
- [ ] Heatmap des zones regardées
- [ ] Export des données de gaze
- [ ] Replay des sessions

### [1.2.0] - Analyses Avancées (À venir)

**Propositions** :
- [ ] Analyse de corrélation statistique (p-values)
- [ ] Clustering des comportements
- [ ] Prédiction des choix (ML)
- [ ] Dashboard interactif (Streamlit/Dash)

### [1.3.0] - Scalabilité (À venir)

**Propositions** :
- [ ] Support PostgreSQL pour grandes volumétries
- [ ] API REST pour import automatique
- [ ] Interface web d'administration
- [ ] Export PDF des rapports

---

## Notes de Version

### Standards de Versionnement

Ce projet suit [Semantic Versioning](https://semver.org/) :
- **MAJOR** : Changements incompatibles avec versions précédentes
- **MINOR** : Nouvelles fonctionnalités rétrocompatibles
- **PATCH** : Corrections de bugs rétrocompatibles

### Types de Changements

- ✨ **Ajouté** : Nouvelles fonctionnalités
- 🔄 **Modifié** : Changements dans fonctionnalités existantes
- 🗑️ **Supprimé** : Fonctionnalités retirées
- 🐛 **Corrigé** : Corrections de bugs
- 🔒 **Sécurité** : Corrections de vulnérabilités

---

**Dernière mise à jour** : 29 janvier 2026
