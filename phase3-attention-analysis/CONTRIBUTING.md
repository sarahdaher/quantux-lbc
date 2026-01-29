# 🤝 Guide de Contribution Collaborative

## 🎯 Objectif
Chaque contributeur clone le dépôt, fait tester plusieurs personnes, et partage les résultats via Git. Tous les résultats s'accumulent sans conflit.

---

## 📋 Workflow Contributeur

### 1️⃣ **Cloner le dépôt**
```bash
git clone https://github.com/sarahdaher/quantux-lbc.git
cd quantux-lbc/phase3-attention-analysis
```

### 2️⃣ **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Faire réaliser les tests**
1. Ouvrir `phase3-attention-test-v2.html` dans un navigateur
2. Chaque participant complète le test (6s, 15s, 30s)
3. À la fin, cliquer sur "📥 Télécharger résultats"
4. Un fichier JSON est téléchargé (ex: `survey_2026-01-29_14-30-45_1738163445123.json`)
5. **Déplacer** ce fichier dans `data/raw_json/`

**Répéter pour chaque participant** (faites tester 5-10 personnes minimum)

### 4️⃣ **Synchroniser la base de données locale**
```bash
python3 scripts/sync_database.py
```
Cela reconstruit la DB depuis tous les JSON (les vôtres + ceux déjà dans Git)

### 5️⃣ **Vérifier les données (optionnel)**
```bash
python3 scripts/generate_graphs.py
```
Les graphiques sont générés dans `outputs/` pour vérifier vos contributions

### 6️⃣ **Committer et pusher vos résultats**
```bash
git add data/raw_json/*.json
git commit -m "Ajout de X tests d'attention (contributeur: VotreNom)"
git push origin main
```

---

## 🔄 Workflow Mise à Jour (après un pull)

Quand vous récupérez les contributions des autres :

```bash
# Récupérer les nouveaux JSON
git pull origin main

# Reconstruire la DB avec TOUS les JSON (anciens + nouveaux)
python3 scripts/sync_database.py

# Générer les graphiques à jour
python3 scripts/generate_graphs.py
```

---

## 🗂️ Architecture des Données

```
data/
├── raw_json/                          # SOURCE DE VÉRITÉ (versionnée sur Git)
│   ├── survey_2026-01-29_10-00-00.json
│   ├── survey_2026-01-29_11-30-00.json
│   └── ...
└── attention_results.db               # Base de données (NON versionnée, reconstruite)
```

### 🔑 Principes Clés
- **Les JSON sont la source de vérité** : versionnés sur Git
- **La DB est reconstruite** : générée à la demande depuis les JSON
- **Pas de conflit possible** : chaque JSON a un nom unique (timestamp)
- **Accumulation automatique** : `sync_database.py` intègre TOUS les JSON

---

## 🎨 Génération des Graphiques

Après une synchronisation :

```bash
python3 scripts/generate_graphs.py
```

Graphiques générés dans `outputs/` :
- `duration_vs_motivation.png` : Motivations par durée
- `price_distribution.png` : Distribution des prix
- `condition_distribution.png` : États préférés
- `top_motivations.png` : Motivations les plus fréquentes
- `time_vs_price.png` : Corrélation temps/prix
- `summary_stats.txt` : Statistiques textuelles

---

## 🚨 Résolution de Conflits

### Si un conflit Git sur un JSON :
**C'est impossible !** Chaque JSON a un nom unique avec timestamp.

### Si la base de données est corrompue :
```bash
rm data/attention_results.db
python3 scripts/sync_database.py
```

### Si des JSON sont manquants après un pull :
```bash
git pull --rebase origin main
python3 scripts/sync_database.py
```

---

## 📊 Exemple de Contribution

**Marie** clone le dépôt :
```bash
git clone ...
cd phase3-attention-analysis
```

Elle fait tester **8 personnes** :
- 8 fichiers JSON dans `data/raw_json/`

Elle synchronise et push :
```bash
python3 scripts/sync_database.py
git add data/raw_json/*.json
git commit -m "Ajout de 8 tests (contributeur: Marie)"
git push
```

**Thomas** récupère les données de Marie :
```bash
git pull
python3 scripts/sync_database.py  # Reconstruit la DB avec les 8 tests de Marie
```

Il fait tester **5 personnes** supplémentaires :
- 5 nouveaux JSON
- La DB contiendra 8 + 5 = 13 tests

Il push :
```bash
git add data/raw_json/*.json
git commit -m "Ajout de 5 tests (contributeur: Thomas)"
git push
```

**Résultat** : Base de données collaborative avec 13 tests sans conflit !

---

## 💡 Bonnes Pratiques

1. **Avant de commencer** : `git pull` + `python3 scripts/sync_database.py`
2. **Faire tester plusieurs personnes** : minimum 5-10 tests par contributeur
3. **Nommer vos commits** : mentionnez votre nom et le nombre de tests
4. **Synchroniser régulièrement** : pour avoir les analyses à jour
5. **Ne jamais modifier les JSON existants** : seulement en ajouter
6. **Ne jamais committer la DB** : elle est dans `.gitignore`

---

## 🆘 Support

En cas de problème :
1. Vérifier que tous les JSON sont bien dans `data/raw_json/`
2. Relancer `python3 scripts/sync_database.py`
3. Vérifier les logs d'erreur dans le terminal
4. Contacter le mainteneur du projet

---

## 📈 Objectif de Collecte

**Cible** : 100+ tests d'attention pour une analyse statistique robuste

**Contributions actuelles** : Voir `python3 scripts/sync_database.py` pour le nombre total de tests
