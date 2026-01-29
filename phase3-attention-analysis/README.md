# 📊 Phase 3 - Test d'Attention Le Bon Coin

## 🎯 Objectif du Projet

Ce projet permet d'**analyser le comportement d'attention visuelle** des utilisateurs sur des annonces Le Bon Coin en fonction du **temps d'observation** (6s, 15s, 30s). 

L'objectif est de comprendre :
- 🕒 **Comment le temps influence les choix** (prix, état, marque, localisation)
- 🧠 **Quelles motivations dominent** selon la durée d'observation
- 💰 **La corrélation entre temps et prix sélectionné**

---

## 📖 Table des Matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Installation](#-installation)
3. [Utilisation du Test](#-utilisation-du-test)
4. [Architecture Technique](#-architecture-technique)
5. [Workflow Collaboratif](#-workflow-collaboratif)
6. [Génération des Analyses](#-génération-des-analyses)
7. [Scripts Utiles](#-scripts-utiles)
8. [Troubleshooting](#-troubleshooting)

---

## 🔍 Vue d'ensemble

### Comment ça marche ?

1. **Test d'Attention** : Les participants voient 10 annonces Le Bon Coin pendant 6s, puis 15s, puis 30s
2. **Sélection** : Après chaque durée, ils cliquent sur l'annonce qui les a le plus intéressés
3. **Motivations** : Ils indiquent pourquoi (prix, état, marque, localisation, etc.)
4. **Export JSON** : Les résultats sont sauvegardés dans un fichier JSON
5. **Analyse** : Les JSON sont importés dans une base SQLite pour générer des graphiques

### Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│         phase3-attention-test-v2.html                       │
│         (Interface de test web)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Télécharge JSON
                     ▼
         ┌───────────────────────┐
         │   data/raw_json/      │ ◄── SOURCE DE VÉRITÉ (Git)
         │   survey_*.json       │
         └───────────┬───────────┘
                     │
                     │ sync_database.py
                     ▼
         ┌───────────────────────┐
         │ attention_results.db  │ ◄── Base SQLite (locale)
         └───────────┬───────────┘
                     │
                     │ generate_graphs.py
                     ▼
         ┌───────────────────────┐
         │    outputs/           │
         │    - Graphiques       │
         │    - Statistiques     │
         └───────────────────────┘
```

---

## 🚀 Installation

### Prérequis

- Python 3.8+ installé
- Git installé
- Navigateur web moderne (Chrome, Firefox, Safari)

### Étapes d'installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/sarahdaher/quantux-lbc.git
cd quantux-lbc/phase3-attention-analysis

# 2. Installer les dépendances Python
pip install -r requirements.txt

# OU utiliser le script automatique
./setup.sh
```

### Contenu de `requirements.txt`

```txt
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## 🧪 Utilisation du Test

### Pour les Participants

#### Étape 1 : Ouvrir le Test

```bash
# Démarrer un serveur local (optionnel mais recommandé)
python3 -m http.server 9999
```

Puis ouvrir dans un navigateur :
```
http://localhost:9999/phase3-attention-test-v2.html
```

Ou simplement double-cliquer sur `phase3-attention-test-v2.html`

#### Étape 2 : Réaliser le Test

1. **Écran d'intro** : Lire les instructions, cliquer sur "Commencer le test"
2. **Phase 1 (6 secondes)** :
   - Observer les 10 annonces pendant 6 secondes
   - Possibilité de scroller
   - ⏱️ Compte à rebours visible
3. **Sélection** :
   - La liste devient cliquable
   - Cliquer sur l'annonce qui vous a le plus intéressé
   - Confirmer votre choix
4. **Motivations** :
   - Cocher les raisons de votre choix (plusieurs possibles)
   - Options : Prix bas, Prix élevé, Bon état, Vendeur, Localisation, Marque, Annonce récente
5. **Phases 2 & 3** : Répéter pour 15s et 30s

#### Étape 3 : Télécharger les Résultats

- À la fin, cliquer sur "📥 Télécharger résultats"
- Un fichier JSON est téléchargé : `survey_2026-01-29_14-30-45_1738163445123.json`
- **Important** : Déplacer ce fichier dans `data/raw_json/`

---

## 🏗️ Architecture Technique

### 📁 Structure du Projet

```
phase3-attention-analysis/
│
├── 📄 README.md                          # Ce fichier (documentation complète)
├── 🤝 CONTRIBUTING.md                    # Guide de contribution collaborative
├── 🏗️ ARCHITECTURE.txt                   # Schéma visuel du système
├── 📦 requirements.txt                   # Dépendances Python
│
├── 🌐 phase3-attention-test-v2.html      # Interface de test web
│
├── 🚀 setup.sh                           # Script d'installation automatique
├── 🗑️ reset.sh                           # Réinitialise DB + graphiques (garde JSON)
├── 🧹 clean_all.sh                       # Supprime TOUT (DB + JSON + graphiques)
│
├── data/
│   ├── raw_json/                         # 📂 Fichiers JSON (SOURCE DE VÉRITÉ)
│   │   ├── .gitkeep                      # Assure l'existence du dossier
│   │   ├── example-survey-1.json         # Exemple de données
│   │   ├── example-survey-2.json
│   │   └── survey_*.json                 # Vos données collectées
│   │
│   └── attention_results.db              # 🗄️ Base SQLite (générée, NON versionnée)
│
├── scripts/
│   ├── db_schema.py                      # Définit le schéma SQLite
│   ├── import_json_to_db.py             # Importe un JSON dans la DB
│   ├── sync_database.py                  # 🔄 Reconstruit la DB depuis TOUS les JSON
│   └── generate_graphs.py                # 📊 Génère les graphiques d'analyse
│
└── outputs/                              # 📈 Résultats d'analyse (générés)
    ├── duration_vs_motivation.png        # Motivations par durée
    ├── price_distribution.png            # Distribution des prix
    ├── condition_distribution.png        # États préférés
    ├── top_motivations.png               # Motivations les plus fréquentes
    ├── time_vs_price.png                 # Corrélation temps/prix
    └── summary_stats.txt                 # Statistiques textuelles
```

### 🗄️ Base de Données SQLite

#### Tables

**1. `survey_sessions`** : Une session = un participant complet
```sql
- session_id (PK)
- timestamp (ISO 8601)
- created_at
```

**2. `test_results`** : Un résultat = une phase (6s, 15s ou 30s)
```sql
- result_id (PK)
- session_id (FK)
- phase (1, 2 ou 3)
- duration (6, 15 ou 30)
- product_title
- product_price
- product_seller
- product_location
- product_condition
- product_days_ago
```

**3. `motivations`** : Les raisons du choix (relation many-to-many)
```sql
- motivation_id (PK)
- result_id (FK)
- motivation_type (prix-bas, condition, marque, etc.)
```

---

## 🤝 Workflow Collaboratif

### Principe Clé

Les **fichiers JSON sont la source de vérité**, pas la base de données. Cela permet à plusieurs personnes de contribuer sans conflit Git.

### Mode Contributeur (Vous collectez des données)

#### 1. Premier lancement

```bash
git clone https://github.com/sarahdaher/quantux-lbc.git
cd quantux-lbc/phase3-attention-analysis
./setup.sh
```

#### 2. Faire tester des participants

- Ouvrir `phase3-attention-test-v2.html`
- Faire tester **5-10 personnes minimum**
- Récupérer tous les JSON téléchargés
- Les déplacer dans `data/raw_json/`

#### 3. Synchroniser localement

```bash
python3 scripts/sync_database.py
```

Cela reconstruit la DB avec vos nouveaux JSON + ceux déjà présents.

#### 4. Partager sur Git

```bash
git add data/raw_json/*.json
git commit -m "Ajout de 8 tests (contributeur: Marie)"
git push origin main
```

### Mode Analyste (Vous consultez les données)

#### 1. Récupérer les contributions

```bash
git pull origin main
python3 scripts/sync_database.py
```

#### 2. Générer les analyses

```bash
python3 scripts/generate_graphs.py
```

Les graphiques sont créés dans `outputs/`

### Pourquoi ce workflow fonctionne ?

✅ **Pas de conflit Git** : Chaque JSON a un nom unique (timestamp)  
✅ **Accumulation automatique** : `sync_database.py` intègre TOUS les JSON  
✅ **Source de vérité** : Les JSON sont versionnés, pas la DB  
✅ **DB reconstruite** : À chaque `sync_database.py`, la DB est régénérée  
✅ **Collaboration simple** : Push/Pull des JSON uniquement

---

## 📊 Génération des Analyses

### Commande

```bash
python3 scripts/generate_graphs.py
```

### Graphiques Générés

#### 1. `duration_vs_motivation.png`
**Motivations de choix par durée d'observation**
- Graphique en barres groupées
- X : Durée (6s, 15s, 30s)
- Y : Nombre de sélections
- Groupes : Motivations (Prix bas, Condition, Marque, etc.)

#### 2. `price_distribution.png`
**Distribution des prix sélectionnés**
- Histogramme + Box plot
- Histogramme : Distribution globale des prix
- Box plot : Prix par durée d'observation

#### 3. `condition_distribution.png`
**Répartition des conditions sélectionnées**
- Diagramme circulaire (pie chart)
- Montre la proportion de "Bon état", "Très bon état", "Excellent état"

#### 4. `top_motivations.png`
**Motivations les plus fréquentes**
- Graphique en barres horizontales
- Affiche le nombre total de sélections par motivation

#### 5. `time_vs_price.png`
**Prix moyen sélectionné selon la durée**
- Graphique linéaire
- X : Durée d'observation
- Y : Prix moyen en euros

#### 6. `summary_stats.txt`
**Statistiques textuelles**
```txt
============================================================
STATISTIQUES RÉSUMÉES - TEST D'ATTENTION PHASE 3
============================================================

📊 Nombre total de sessions : 2
📊 Nombre total de tests : 6

💰 PRIX
   - Prix moyen sélectionné : 684.00€
   - Prix minimum : 299.00€
   - Prix maximum : 1099.00€
   - Médiane : 724.00€

⏱️ DURÉES
   - 6s : 2 tests (prix moyen : 329.00€)
   - 15s : 2 tests (prix moyen : 949.00€)
   - 30s : 2 tests (prix moyen : 774.00€)

✨ CONDITIONS PRÉFÉRÉES
   - Bon état : 4 (66.7%)
   - Excellent état : 1 (16.7%)
   - Très bon état : 1 (16.7%)
```

---

## 🛠️ Scripts Utiles

### `setup.sh` - Installation Automatique

```bash
./setup.sh
```

- Vérifie Python 3
- Installe les dépendances (`requirements.txt`)
- Synchronise la base de données
- Affiche les prochaines étapes

### `sync_database.py` - Synchronisation

```bash
python3 scripts/sync_database.py
```

**Fonction** : Reconstruit la base de données depuis TOUS les JSON

**Étapes** :
1. Supprime l'ancienne DB
2. Crée une nouvelle DB vide
3. Importe tous les JSON de `data/raw_json/`
4. Affiche les statistiques

**Quand l'utiliser** :
- Après un `git pull`
- Après avoir ajouté de nouveaux JSON
- Quand la DB est corrompue

### `generate_graphs.py` - Analyse

```bash
python3 scripts/generate_graphs.py
```

**Fonction** : Génère tous les graphiques et statistiques

**Prérequis** : La base de données doit exister (lancer `sync_database.py` avant)

### `reset.sh` - Réinitialisation (Mode Test)

```bash
./reset.sh
```

**Fonction** : Supprime la DB et les graphiques (garde les JSON)

**Utilisation** : Phase de test/développement

**Supprime** :
- ❌ `data/attention_results.db`
- ❌ `outputs/*.png`
- ❌ `outputs/*.txt`

**Conserve** :
- ✅ `data/raw_json/*.json`

### `clean_all.sh` - Nettoyage Complet

```bash
./clean_all.sh
```

**⚠️ ATTENTION : Supprime TOUTES les données**

**Confirmation requise** : Taper `SUPPRIMER TOUT`

**Supprime** :
- ❌ `data/attention_results.db`
- ❌ `data/raw_json/*.json` (sauf `.gitkeep`)
- ❌ `outputs/*`

**Utilisation** : Repartir complètement de zéro

---

## 🧪 Phase de Test vs Déploiement

### En Phase de Test (Actuellement)

- Utiliser `reset.sh` pour nettoyer entre les tests
- Les JSON d'exemple sont conservés
- Tester différents scénarios

```bash
# Cycle de test typique
./reset.sh                          # Nettoyer
# Faire des tests manuels
python3 scripts/sync_database.py   # Reconstruire
python3 scripts/generate_graphs.py  # Analyser
```

### En Phase de Déploiement

- Ne plus utiliser `reset.sh` ni `clean_all.sh`
- Tous les JSON sont précieux
- Workflow Git strict :

```bash
git pull                            # Récupérer les contributions
python3 scripts/sync_database.py   # Synchroniser
python3 scripts/generate_graphs.py  # Analyser
# Faire tester de nouveaux participants
git add data/raw_json/*.json
git commit -m "Ajout de X tests"
git push
```

---

## 🎯 Objectif de Collecte

### Cible Statistique

**Minimum** : 30 tests (10 participants × 3 phases)  
**Optimal** : 100+ tests (33+ participants)  
**Idéal** : 300+ tests (100+ participants)

### Vérifier la Progression

```bash
python3 scripts/sync_database.py
```

Affiche :
```
📊 Statistiques de la base de données :
   - Sessions d'enquête : 2
   - Tests enregistrés : 6
   - Motivations collectées : 14
```

---

## 🆘 Troubleshooting

### Problème : `ModuleNotFoundError: No module named 'pandas'`

**Solution** :
```bash
pip install -r requirements.txt
```

### Problème : La DB est corrompue

**Solution** :
```bash
rm data/attention_results.db
python3 scripts/sync_database.py
```

### Problème : Pas de JSON trouvés

**Vérifier** :
```bash
ls data/raw_json/*.json
```

**Solution** : Faire des tests et déplacer les JSON téléchargés dans `data/raw_json/`

### Problème : Conflit Git sur un JSON

**Cause** : Impossible normalement (noms uniques avec timestamp)

**Solution** :
```bash
git pull --rebase origin main
```

### Problème : Graphiques vides

**Cause** : Pas assez de données

**Solution** : Faire plus de tests (minimum 3-5 sessions)

### Problème : Le test HTML ne fonctionne pas

**Vérifier** :
- Navigateur moderne (Chrome/Firefox/Safari)
- Pas de bloqueur de JavaScript
- Ouvrir depuis un serveur local si possible :
  ```bash
  python3 -m http.server 9999
  ```

---

## 📚 Documentation Complémentaire

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** : Guide détaillé de contribution collaborative
- **[ARCHITECTURE.txt](./ARCHITECTURE.txt)** : Schéma visuel du système
- **Scripts Python** : Commentés en détail dans chaque fichier

---

## 🎓 Comprendre les Résultats

### Interprétation des Graphiques

#### Durée vs Motivations

**Question** : Les motivations changent-elles avec le temps ?

**Analyse** :
- **6s** : Réactions impulsives, probablement dominées par prix/marque
- **15s** : Temps de comparer, condition et vendeur deviennent importants
- **30s** : Analyse approfondie, tous les critères pris en compte

#### Prix vs Temps

**Question** : Plus de temps = choix plus chers ou moins chers ?

**Hypothèses** :
- **Si prix ↑** : Plus de temps = meilleure appréciation de la valeur
- **Si prix ↓** : Plus de temps = meilleure détection des bonnes affaires

---

## 🤝 Contribution

Vous voulez améliorer ce projet ?

1. Fork le dépôt
2. Créer une branche : `git checkout -b feature/amelioration`
3. Committer : `git commit -m "Ajout de X"`
4. Pusher : `git push origin feature/amelioration`
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet fait partie de l'étude UX Quantux - Le Bon Coin

---

## 📞 Contact

**Mainteneur** : Sarah Daher  
**Dépôt** : https://github.com/sarahdaher/quantux-lbc

---

**Dernière mise à jour** : 29 janvier 2026
