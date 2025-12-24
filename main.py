#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de Gestion des Étudiants - Version Professionnelle Complète
====================================================================

Version 2.0 avec:
- Base de données SQLite
- Graphiques Matplotlib
- Interface CustomTkinter moderne

Auteur: Votre Nom
Date: Décembre 2024
"""

import sys
import os

# Vérifier les dépendances
try:
    import customtkinter
    import matplotlib
    print("✓ Toutes les dépendances sont installées")
except ImportError as e:
    print("❌ Erreur: Dépendances manquantes!")
    print("\nInstallez-les avec:")
    print("pip install customtkinter matplotlib pillow")
    sys.exit(1)

from gui.app_moderne import main

if __name__ == "__main__":
    print("=" * 70)
    print("  SYSTÈME DE GESTION DES ÉTUDIANTS - VERSION PROFESSIONNELLE")
    print("=" * 70)
    print("\n📊 Fonctionnalités:")
    print("  ✅ Base de données SQLite")
    print("  ✅ Interface moderne CustomTkinter")
    print("  ✅ Graphiques et statistiques avancées")
    print("  ✅ Gestion complète CRUD")
    print("\n🚀 Démarrage de l'application...\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application fermée par l'utilisateur.")
    except Exception as e:
        print(f"\n\n❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")
