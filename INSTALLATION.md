# 🚀 INSTALLATION RAPIDE - 3 ÉTAPES

## Étape 1️⃣ : Vérifier Python
```bash
python --version
# Doit afficher Python 3.8 ou supérieur
```

## Étape 2️⃣ : Installer les dépendances
```bash
cd Gestion_etudiant_COMPLET/
pip install -r requirements.txt
```

**Dépendances installées:**
- ✅ customtkinter (interface moderne)
- ✅ matplotlib (graphiques)
- ✅ pillow (images)

## Étape 3️⃣ : Lancer l'application
```bash
python main.py
```

---

## 💡 PREMIÈRE UTILISATION

### Créer votre premier étudiant
1. Dans l'onglet "👥 Étudiants"
2. Remplir: Nom, Prénom, Promotion (ex: L1)
3. Cliquer "➕ Créer"

### Ajouter des notes
1. Sélectionner l'étudiant (cliquer sur sa card)
2. Aller dans "📝 Notes"
3. Entrer matière et note
4. Cliquer "➕ Ajouter"

### Voir les statistiques
1. Aller dans "📊 Statistiques"
2. Voir le taux de réussite et les mentions

### Voir les graphiques
1. Aller dans "📈 Graphiques"
2. Cliquer sur un type de graphique

---

## 🎨 PERSONNALISATION

### Changer le thème
- Utiliser le switch "🌙 Mode Sombre" en bas du menu

### Thème par défaut
Modifier dans `main.py` ligne 25:
```python
ctk.set_appearance_mode("dark")  # ou "light"
```

---

## ❓ PROBLÈMES FRÉQUENTS

### "ModuleNotFoundError: No module named 'customtkinter'"
**Solution:**
```bash
pip install customtkinter
```

### "ModuleNotFoundError: No module named 'matplotlib'"
**Solution:**
```bash
pip install matplotlib
```

### L'application ne démarre pas
**Solution:**
```bash
# Réinstaller toutes les dépendances
pip install --upgrade customtkinter matplotlib pillow
```

### Permission denied (Linux/Mac)
**Solution:**
```bash
chmod +x main.py
./main.py
```

---

## ✅ CHECKLIST D'INSTALLATION

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Application lance sans erreur
- [ ] Peut créer un étudiant
- [ ] Peut ajouter une note
- [ ] Les graphiques s'affichent
- [ ] Mode sombre/clair fonctionne

**Tout fonctionne ? Bravo ! 🎉**

---

## 📚 RESSOURCES

- **Documentation complète**: Voir `README.md`
- **Exemples de code**: Dans `README.md` section "Exemples"
- **Architecture**: Dans `README.md` section "Architecture"

---

**Besoin d'aide ?** Consultez le `README.md` complet ! 📖
