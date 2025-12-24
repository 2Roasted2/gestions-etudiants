# 🎓 Système de Gestion des Étudiants - Version Professionnelle 2.0

**Application complète avec SQLite, Graphiques et Interface Moderne**

---

## ✨ NOUVEAUTÉS VERSION 2.0

### 🗄️ Base de Données SQLite
- ✅ Performance optimale avec requêtes SQL
- ✅ Intégrité des données garantie
- ✅ Support de milliers d'étudiants sans ralentissement
- ✅ Relations entre tables (étudiants, notes, coefficients)
- ✅ Index pour recherches rapides

### 📊 Graphiques Professionnels
- ✅ **7 types de graphiques** intégrés
- ✅ Camembert des mentions
- ✅ Histogramme des moyennes par promotion
- ✅ Courbe d'évolution des notes
- ✅ Distribution des moyennes
- ✅ Graphique radar des compétences
- ✅ Top 10 des meilleurs étudiants
- ✅ Comparaison par matière

### 🎨 Interface Moderne
- ✅ **CustomTkinter** - Design moderne et élégant
- ✅ Mode sombre/clair
- ✅ Animations fluides
- ✅ Cards interactives pour chaque étudiant
- ✅ Sidebar de navigation
- ✅ Recherche en temps réel
- ✅ Interface responsive

---

## 📦 INSTALLATION

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étape 1: Installer les dépendances
```bash
pip install customtkinter matplotlib pillow
```

**Note:** SQLite est inclus avec Python, pas besoin de l'installer !

### Étape 2: Lancer l'application
```bash
python main.py
# ou
./main.py  # Linux/Mac
```

---

## 🚀 GUIDE D'UTILISATION

### 1️⃣ Page Étudiants 👥
**Créer un étudiant:**
1. Remplir le formulaire (Nom, Prénom, Promotion, Email)
2. Cliquer sur "➕ Créer"

**Modifier un étudiant:**
1. Cliquer sur la card de l'étudiant dans la liste
2. Modifier les informations
3. Cliquer sur "✏️ Modifier"

**Supprimer un étudiant:**
1. Sélectionner l'étudiant
2. Cliquer sur "🗑️ Supprimer"
3. Confirmer

**Recherche:**
- Utiliser la barre de recherche en haut à droite
- Recherche en temps réel sur nom/prénom/promotion

### 2️⃣ Page Notes 📝
1. Sélectionner un étudiant dans la page "Étudiants"
2. Aller dans "Notes"
3. Entrer la matière et la note (0-20)
4. Cliquer sur "➕ Ajouter"

Les notes s'affichent par matière avec:
- Liste des notes
- Moyenne par matière
- Nombre de notes

### 3️⃣ Page Statistiques 📊
Affiche en temps réel:
- **Nombre total** d'étudiants
- **Taux de réussite** (%)
- **Moyenne générale** de l'école
- **Répartition des mentions** (détails)

### 4️⃣ Page Graphiques 📈
Cliquer sur un bouton pour afficher:
- **📊 Mentions**: Camembert coloré
- **📈 Moyennes Promos**: Barres par promotion
- **📉 Distribution**: Histogramme des moyennes
- **🏆 Top 10**: Meilleurs étudiants avec médailles

### 5️⃣ Fonctionnalités Supplémentaires
- **💾 Backup**: Exporter toute la base en JSON
- **🌙 Mode Sombre/Clair**: Switch en bas du menu
- **🔄 Actualiser**: Recharge les données

---

## 🏗️ ARCHITECTURE

```
Gestion_etudiant_COMPLET/
├── main.py                     # Point d'entrée
│
├── models/                     # Modèles de données
│   ├── __init__.py
│   └── etudiant.py             # Classe Etudiant
│
├── services/                   # Logique métier
│   ├── __init__.py
│   ├── database.py             # Gestion SQLite ⭐ NOUVEAU
│   ├── graphiques.py           # Génération graphiques ⭐ NOUVEAU
│   ├── statistiques.py         # Calculs statistiques
│   └── rapports.py             # Génération rapports
│
├── gui/                        # Interface graphique
│   ├── __init__.py
│   └── app_moderne.py          # Interface CustomTkinter ⭐ NOUVEAU
│
├── data/                       # Données (créé auto)
│   └── etudiants.db            # Base SQLite ⭐ NOUVEAU
│
└── README.md                   # Cette documentation
```

---

## 💡 TECHNOLOGIES UTILISÉES

| Technologie | Usage | Version |
|-------------|-------|---------|
| **Python** | Langage principal | 3.8+ |
| **SQLite** | Base de données | Inclus |
| **CustomTkinter** | Interface moderne | 5.2+ |
| **Matplotlib** | Graphiques | 3.5+ |
| **Pillow (PIL)** | Images | 9.0+ |

---

## 🔧 PERSONNALISATION

### Changer les couleurs
Modifier dans `gui/app_moderne.py`:
```python
# Ligne 15-16
ctk.set_appearance_mode("dark")  # "light" ou "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

### Ajouter un graphique
Dans `services/graphiques.py`, créer une méthode:
```python
@staticmethod
def mon_nouveau_graphique(etudiants, parent_widget=None):
    fig, ax = plt.subplots()
    # ... votre code
    return fig
```

### Modifier les seuils de mentions
Dans `models/etudiant.py`, méthode `get_mention()`:
```python
match moy:
    case m if m >= 16:  # Modifier ici
        return "Très Bien"
```

---

## 🐛 DÉPANNAGE

### Erreur: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Erreur: "No module named 'matplotlib'"
```bash
pip install matplotlib
```

### La base de données ne se crée pas
- Vérifier les permissions du dossier
- Le dossier `data/` sera créé automatiquement

### Les graphiques ne s'affichent pas
```bash
pip install --upgrade matplotlib pillow
```

---

## 💻 EXEMPLES DE CODE

### Créer un étudiant (code)
```python
from services.database import Database

db = Database()
etudiant_id = db.ajouter_etudiant("DUPONT", "Jean", "L3", "jean@email.com")
print(f"Étudiant créé avec l'ID: {etudiant_id}")
```

### Ajouter des notes (code)
```python
db.ajouter_note(etudiant_id, "Mathématiques", 15.5)
db.ajouter_note(etudiant_id, "Informatique", 18.0)
```

### Générer un graphique (code)
```python
from services.graphiques import Graphiques

etudiants = db.obtenir_tous_etudiants()
fig = Graphiques.graphique_mentions(etudiants)
fig.savefig("graphique_mentions.png")
```

---

## 📞 SUPPORT

En cas de problème:
1. Vérifier que toutes les dépendances sont installées
2. Consulter la section Dépannage ci-dessus
3. Vérifier les permissions du dossier `data/`

---

## 📄 LICENCE

Projet éducatif - Libre d'utilisation et de modification

---

🎉 **Profitez de votre nouveau système de gestion ultra-professionnel !** 🎉
