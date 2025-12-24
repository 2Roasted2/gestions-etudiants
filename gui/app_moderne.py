import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import json

from services.database import Database
from services.statistiques import (
    stats_par_matiere, stats_promotion, classement_etudiants,
    repartition_mentions, taux_reussite, etudiants_en_difficulte
)
from services.rapports import (
    generer_rapport_etudiant, generer_rapport_promotion,
    generer_rapport_global, generer_bulletin
)
from services.graphiques import Graphiques

# Configuration de CustomTkinter
ctk.set_appearance_mode("dark")  # "light" ou "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class ApplicationModerne:
    """Application de gestion des étudiants avec interface moderne"""
    
    def __init__(self):
        self.db = Database()
        self.etudiant_courant = None
        
        # Créer la fenêtre principale
        self.root = ctk.CTk()
        self.root.title("🎓 Système de Gestion des Étudiants - Version Professionnelle")
        self.root.geometry("1400x800")
        
        # Icône et configuration
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Créer l'interface
        self.creer_interface()
        
        # Charger les données initiales
        self.rafraichir_liste_etudiants()
    
    def creer_interface(self):
        """Crée l'interface principale avec sidebar et contenu"""
        
        # ========== SIDEBAR (Menu latéral) ==========
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo/Titre
        titre_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        titre_frame.pack(pady=30, padx=20)
        
        titre = ctk.CTkLabel(
            titre_frame,
            text="🎓 GESTION\nÉTUDIANTS",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("#2ecc71", "#2ecc71")
        )
        titre.pack()
        
        # Séparateur
        separateur = ctk.CTkFrame(self.sidebar, height=2, fg_color=("#3498db", "#3498db"))
        separateur.pack(fill="x", padx=20, pady=10)
        
        # Boutons de navigation
        self.boutons_nav = []
        
        nav_items = [
            ("👥 Étudiants", self.afficher_page_etudiants, "primary"),
            ("📝 Notes", self.afficher_page_notes, "success"),
            ("📊 Statistiques", self.afficher_page_statistiques, "warning"),
            ("📈 Graphiques", self.afficher_page_graphiques, "info"),
            ("📄 Rapports", self.afficher_page_rapports, "purple"),
        ]
        
        for texte, commande, _ in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=texte,
                command=commande,
                corner_radius=10,
                height=50,
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=("#34495e", "#2c3e50"),
                hover_color=("#3498db", "#2980b9"),
                anchor="w",
                text_color=("white", "white")
            )
            btn.pack(pady=8, padx=20, fill="x")
            self.boutons_nav.append(btn)
        
        # Séparateur
        separateur2 = ctk.CTkFrame(self.sidebar, height=2, fg_color=("#3498db", "#3498db"))
        separateur2.pack(fill="x", padx=20, pady=20)
        
        # Boutons d'action
        btn_backup = ctk.CTkButton(
            self.sidebar,
            text="💾 Backup",
            command=self.faire_backup,
            corner_radius=8,
            height=40,
            fg_color=("#7f8c8d", "#95a5a6"),
            hover_color=("#95a5a6", "#7f8c8d")
        )
        btn_backup.pack(pady=5, padx=20, fill="x")
        
        # Switch thème
        self.theme_var = ctk.StringVar(value="dark")
        theme_switch = ctk.CTkSwitch(
            self.sidebar,
            text="🌙 Mode Sombre",
            command=self.changer_theme,
            variable=self.theme_var,
            onvalue="dark",
            offvalue="light"
        )
        theme_switch.pack(pady=20, padx=20)
        
        # Info en bas
        info_label = ctk.CTkLabel(
            self.sidebar,
            text="Version 2.0 Pro\n© 2024",
            font=ctk.CTkFont(size=10),
            text_color=("#95a5a6", "#7f8c8d")
        )
        info_label.pack(side="bottom", pady=20)
        
        # ========== ZONE PRINCIPALE ==========
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Frame de contenu (changera selon la page)
        self.content_frame = None
        
        # Afficher la page d'accueil
        self.afficher_page_etudiants()
    
    def clear_content(self):
        """Efface le contenu actuel"""
        if self.content_frame:
            self.content_frame.destroy()
        
        self.content_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def afficher_page_etudiants(self):
        """Page de gestion des étudiants"""
        self.clear_content()
        
        # Titre de la page
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        titre = ctk.CTkLabel(
            header,
            text="👥 Gestion des Étudiants",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titre.pack(side="left")
        
        # Conteneur principal (2 colonnes)
        container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        # ===== COLONNE GAUCHE: Formulaire =====
        left_frame = ctk.CTkFrame(container, width=400)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        form_title = ctk.CTkLabel(
            left_frame,
            text="📝 Formulaire Étudiant",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.pack(pady=15)
        
        # Champs du formulaire
        self.nom_entry = self.create_form_field(left_frame, "Nom *")
        self.prenom_entry = self.create_form_field(left_frame, "Prénom *")
        self.promo_entry = self.create_form_field(left_frame, "Promotion * (ex: L1, M2)")
        self.email_entry = self.create_form_field(left_frame, "Email")
        
        # Boutons d'action
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=20)
        
        btn_create = ctk.CTkButton(
            btn_frame,
            text="➕ Créer",
            command=self.creer_etudiant,
            fg_color=("#2ecc71", "#27ae60"),
            hover_color=("#27ae60", "#2ecc71"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_create.pack(fill="x", pady=5)
        
        btn_update = ctk.CTkButton(
            btn_frame,
            text="✏️ Modifier",
            command=self.modifier_etudiant,
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#3498db"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_update.pack(fill="x", pady=5)
        
        btn_delete = ctk.CTkButton(
            btn_frame,
            text="🗑️ Supprimer",
            command=self.supprimer_etudiant,
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#e74c3c"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_delete.pack(fill="x", pady=5)
        
        # ===== COLONNE DROITE: Liste =====
        right_frame = ctk.CTkFrame(container)
        right_frame.pack(side="right", fill="both", expand=True)
        
        list_header = ctk.CTkFrame(right_frame, fg_color="transparent")
        list_header.pack(fill="x", pady=10, padx=10)
        
        list_title = ctk.CTkLabel(
            list_header,
            text="📋 Liste des Étudiants",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        list_title.pack(side="left")
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(list_header, fg_color="transparent")
        search_frame.pack(side="right")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher...",
            width=200
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.rechercher_temps_reel)
        
        btn_refresh = ctk.CTkButton(
            search_frame,
            text="🔄",
            command=self.rafraichir_liste_etudiants,
            width=40
        )
        btn_refresh.pack(side="left")
        
        # Frame pour le scrollable
        list_container = ctk.CTkFrame(right_frame)
        list_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollable frame pour la liste
        self.liste_frame = ctk.CTkScrollableFrame(
            list_container,
            label_text=f"Total: {self.db.nombre_total_etudiants()} étudiants"
        )
        self.liste_frame.pack(fill="both", expand=True)
        
        self.student_cards = []
    
    def create_form_field(self, parent, label_text):
        """Crée un champ de formulaire stylisé"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=8)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x")
        
        entry = ctk.CTkEntry(
            frame,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        entry.pack(fill="x", pady=(5, 0))
        
        return entry
    
    def rafraichir_liste_etudiants(self, etudiants=None):
        """Rafraîchit la liste des étudiants avec des cards modernes"""
        # Nettoyer les cards existantes
        for card in self.student_cards:
            card.destroy()
        self.student_cards.clear()
        
        # Obtenir les étudiants
        if etudiants is None:
            etudiants = self.db.obtenir_tous_etudiants()
        
        # Mettre à jour le titre
        if hasattr(self, 'liste_frame'):
            self.liste_frame.configure(label_text=f"Total: {len(etudiants)} étudiants")
        
        # Créer une card pour chaque étudiant
        for etudiant in etudiants:
            card = self.create_student_card(self.liste_frame, etudiant)
            self.student_cards.append(card)
    
    def create_student_card(self, parent, etudiant):
        """Crée une card moderne pour un étudiant"""
        # Couleur selon la mention
        mention = etudiant.get_mention()
        color_map = {
            "Très Bien": ("#2ecc71", "#27ae60"),
            "Bien": ("#3498db", "#2980b9"),
            "Assez Bien": ("#f39c12", "#e67e22"),
            "Passable": ("#e74c3c", "#c0392b"),
            "Insuffisant": ("#95a5a6", "#7f8c8d")
        }
        fg_color = color_map.get(mention, ("#34495e", "#2c3e50"))
        
        card = ctk.CTkFrame(
            parent,
            fg_color=fg_color,
            corner_radius=10,
            border_width=2,
            border_color=("#2c3e50", "#34495e")
        )
        card.pack(fill="x", pady=5, padx=5)
        
        # Contenu de la card
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Ligne 1: Nom et ID
        line1 = ctk.CTkFrame(content, fg_color="transparent")
        line1.pack(fill="x")
        
        nom_label = ctk.CTkLabel(
            line1,
            text=f"{etudiant.prenom} {etudiant.nom}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        nom_label.pack(side="left")
        
        id_badge = ctk.CTkLabel(
            line1,
            text=f"ID: {etudiant.id}",
            font=ctk.CTkFont(size=11),
            fg_color=("#34495e", "#2c3e50"),
            corner_radius=5,
            padx=10,
            pady=2
        )
        id_badge.pack(side="right")
        
        # Ligne 2: Promotion et Moyenne
        line2 = ctk.CTkFrame(content, fg_color="transparent")
        line2.pack(fill="x", pady=(5, 0))
        
        promo_label = ctk.CTkLabel(
            line2,
            text=f"🎓 {etudiant.promotion}",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        promo_label.pack(side="left")
        
        moyenne = etudiant.moyenne_generale()
        moyenne_label = ctk.CTkLabel(
            line2,
            text=f"📊 {moyenne:.2f}/20",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="e"
        )
        moyenne_label.pack(side="right")
        
        # Ligne 3: Mention
        mention_label = ctk.CTkLabel(
            content,
            text=f"🏆 {mention}",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        mention_label.pack(fill="x", pady=(5, 0))
        
        # Événement de clic
        for widget in [card, content, line1, line2, nom_label, promo_label, moyenne_label, mention_label]:
            widget.bind("<Button-1>", lambda e, etud=etudiant: self.selectionner_etudiant(etud))
        
        return card
    
    def selectionner_etudiant(self, etudiant):
        """Sélectionne un étudiant et remplit le formulaire"""
        self.etudiant_courant = etudiant
        
        # Remplir le formulaire
        self.nom_entry.delete(0, "end")
        self.nom_entry.insert(0, etudiant.nom)
        
        self.prenom_entry.delete(0, "end")
        self.prenom_entry.insert(0, etudiant.prenom)
        
        self.promo_entry.delete(0, "end")
        self.promo_entry.insert(0, etudiant.promotion)
        
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, etudiant.email)
        
        # Message de confirmation
        messagebox.showinfo("Sélection", f"Étudiant sélectionné: {etudiant.prenom} {etudiant.nom}")

    def creer_etudiant(self):
        """Crée un nouvel étudiant"""
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        promotion = self.promo_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not nom or not prenom or not promotion:
            messagebox.showwarning("Attention", "Nom, prénom et promotion sont obligatoires!")
            return
        
        try:
            etudiant_id = self.db.ajouter_etudiant(nom, prenom, promotion, email)
            messagebox.showinfo("Succès", f"Étudiant créé avec l'ID {etudiant_id}")
            self.vider_formulaire()
            self.rafraichir_liste_etudiants()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création: {str(e)}")
    
    def modifier_etudiant(self):
        """Modifie l'étudiant sélectionné"""
        if not self.etudiant_courant:
            messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant!")
            return
        
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        promotion = self.promo_entry.get().strip()
        email = self.email_entry.get().strip()
        
        try:
            self.db.modifier_etudiant(self.etudiant_courant.id, nom, prenom, promotion, email)
            messagebox.showinfo("Succès", "Étudiant modifié avec succès!")
            self.rafraichir_liste_etudiants()
            self.etudiant_courant = self.db.obtenir_etudiant(self.etudiant_courant.id)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")
    
    def supprimer_etudiant(self):
        """Supprime l'étudiant sélectionné"""
        if not self.etudiant_courant:
            messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant!")
            return
        
        reponse = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer {self.etudiant_courant.prenom} {self.etudiant_courant.nom}?"
        )
        
        if reponse:
            try:
                self.db.supprimer_etudiant(self.etudiant_courant.id)
                messagebox.showinfo("Succès", "Étudiant supprimé!")
                self.vider_formulaire()
                self.etudiant_courant = None
                self.rafraichir_liste_etudiants()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
    
    def vider_formulaire(self):
        """Vide tous les champs du formulaire"""
        self.nom_entry.delete(0, "end")
        self.prenom_entry.delete(0, "end")
        self.promo_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
    
    def rechercher_temps_reel(self, event=None):
        """Recherche en temps réel"""
        texte = self.search_entry.get().strip().upper()
        
        if not texte:
            self.rafraichir_liste_etudiants()
            return
        
        tous_etudiants = self.db.obtenir_tous_etudiants()
        resultats = [
            e for e in tous_etudiants
            if texte in e.nom or texte in e.prenom.upper() or texte in e.promotion
        ]
        
        self.rafraichir_liste_etudiants(resultats)
    
    def afficher_page_notes(self):
        """Page de gestion des notes"""
        self.clear_content()
        
        titre = ctk.CTkLabel(
            self.content_frame,
            text="📝 Gestion des Notes",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titre.pack(pady=20)
        
        # Message si aucun étudiant sélectionné
        if not self.etudiant_courant:
            msg = ctk.CTkLabel(
                self.content_frame,
                text="⚠️ Veuillez d'abord sélectionner un étudiant\ndans la page 'Étudiants'",
                font=ctk.CTkFont(size=16),
                text_color=("#e74c3c", "#c0392b")
            )
            msg.pack(pady=50)
            return
        
        # Info étudiant
        info_frame = ctk.CTkFrame(self.content_frame, fg_color=("#3498db", "#2980b9"))
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = ctk.CTkLabel(
            info_frame,
            text=f"👤 {self.etudiant_courant.prenom} {self.etudiant_courant.nom} - {self.etudiant_courant.promotion}\n" +
                 f"📊 Moyenne: {self.etudiant_courant.moyenne_generale():.2f}/20 | 🏆 {self.etudiant_courant.get_mention()}",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        info_text.pack(pady=15)
        
        # Formulaire ajout note
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        form_title = ctk.CTkLabel(
            form_frame,
            text="➕ Ajouter une Note",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.pack(pady=10)
        
        inputs_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        inputs_frame.pack(pady=10)
        
        self.matiere_entry = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Matière (ex: Mathématiques)",
            width=250
        )
        self.matiere_entry.pack(side="left", padx=5)
        
        self.note_entry = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Note (0-20)",
            width=100
        )
        self.note_entry.pack(side="left", padx=5)
        
        btn_add = ctk.CTkButton(
            inputs_frame,
            text="➕ Ajouter",
            command=self.ajouter_note,
            fg_color=("#2ecc71", "#27ae60"),
            width=120
        )
        btn_add.pack(side="left", padx=5)
        
        # Liste des notes
        notes_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            label_text=f"📚 Notes de {self.etudiant_courant.prenom}"
        )
        notes_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if not self.etudiant_courant.notes:
            no_notes = ctk.CTkLabel(
                notes_frame,
                text="Aucune note enregistrée pour cet étudiant.",
                font=ctk.CTkFont(size=14)
            )
            no_notes.pack(pady=20)
        else:
            for matiere, notes_list in sorted(self.etudiant_courant.notes.items()):
                self.creer_card_matiere(notes_frame, matiere, notes_list)
    
    def creer_card_matiere(self, parent, matiere, notes):
        """Crée une card pour une matière"""
        moyenne = sum(notes) / len(notes)
        
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.pack(fill="x", pady=8, padx=5)
        
        header = ctk.CTkFrame(card, fg_color=("#3498db", "#2980b9"))
        header.pack(fill="x", padx=2, pady=2)
        
        mat_label = ctk.CTkLabel(
            header,
            text=f"📖 {matiere}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        mat_label.pack(side="left", padx=15, pady=10)
        
        moy_label = ctk.CTkLabel(
            header,
            text=f"Moyenne: {moyenne:.2f}/20",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        moy_label.pack(side="right", padx=15, pady=10)
        
        notes_text = ctk.CTkLabel(
            card,
            text=f"Notes: {', '.join(str(n) for n in notes)}",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        notes_text.pack(fill="x", padx=15, pady=10)
    
    def ajouter_note(self):
        """Ajoute une note"""
        if not self.etudiant_courant:
            messagebox.showwarning("Attention", "Aucun étudiant sélectionné!")
            return
        
        matiere = self.matiere_entry.get().strip()
        note_str = self.note_entry.get().strip()
        
        if not matiere or not note_str:
            messagebox.showwarning("Attention", "Matière et note sont obligatoires!")
            return
        
        try:
            note = float(note_str)
            if not 0 <= note <= 20:
                raise ValueError("Note doit être entre 0 et 20")
            
            self.db.ajouter_note(self.etudiant_courant.id, matiere, note)
            messagebox.showinfo("Succès", f"Note ajoutée: {note}/20 en {matiere}")
            
            # Recharger l'étudiant
            self.etudiant_courant = self.db.obtenir_etudiant(self.etudiant_courant.id)
            
            # Rafraîchir l'affichage
            self.afficher_page_notes()
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
    
    def afficher_page_statistiques(self):
        """Page des statistiques"""
        self.clear_content()
        
        titre = ctk.CTkLabel(
            self.content_frame,
            text="📊 Statistiques",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titre.pack(pady=20)
        
        # Statistiques globales dans des cards
        cards_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        etudiants = self.db.obtenir_tous_etudiants()
        reussis, total, taux = taux_reussite(etudiants)
        mentions = repartition_mentions(etudiants)
        
        # Card 1: Nombre total
        self.create_stat_card(
            cards_frame,
            "👥 Total Étudiants",
            str(len(etudiants)),
            "#3498db"
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        # Card 2: Taux de réussite
        self.create_stat_card(
            cards_frame,
            "✅ Taux de Réussite",
            f"{taux:.1f}%",
            "#2ecc71" if taux >= 75 else "#e74c3c"
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        # Card 3: Moyenne générale
        if etudiants:
            moy_gen = sum(e.moyenne_generale() for e in etudiants) / len(etudiants)
            self.create_stat_card(
                cards_frame,
                "📈 Moyenne Générale",
                f"{moy_gen:.2f}/20",
                "#f39c12"
            ).pack(side="left", fill="both", expand=True, padx=5)
        
        # Texte détaillé
        details_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="📋 Détails")
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Répartition des mentions
        mentions_text = "🏆 RÉPARTITION DES MENTIONS\n" + "="*50 + "\n\n"
        for mention, count in mentions.items():
            pct = (count / len(etudiants) * 100) if etudiants else 0
            mentions_text += f"{mention}: {count} ({pct:.1f}%)\n"
        
        mentions_label = ctk.CTkLabel(
            details_frame,
            text=mentions_text,
            font=ctk.CTkFont(size=13),
            justify="left",
            anchor="w"
        )
        mentions_label.pack(fill="x", padx=10, pady=10)
    
    def create_stat_card(self, parent, titre, valeur, couleur):
        """Crée une card de statistique"""
        card = ctk.CTkFrame(parent, fg_color=(couleur, couleur), corner_radius=15)
        
        titre_label = ctk.CTkLabel(
            card,
            text=titre,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titre_label.pack(pady=(15, 5))
        
        valeur_label = ctk.CTkLabel(
            card,
            text=valeur,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        valeur_label.pack(pady=(5, 15))
        
        return card
    
    def afficher_page_graphiques(self):
        """Page des graphiques"""
        self.clear_content()
        
        titre = ctk.CTkLabel(
            self.content_frame,
            text="📈 Graphiques et Visualisations",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titre.pack(pady=20)
        
        # Boutons de sélection
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        graphiques = [
            ("📊 Mentions", self.afficher_graph_mentions),
            ("📈 Moyennes Promos", self.afficher_graph_promos),
            ("📉 Distribution", self.afficher_graph_distribution),
            ("🏆 Top 10", self.afficher_graph_top10),
        ]
        
        for texte, commande in graphiques:
            btn = ctk.CTkButton(
                btn_frame,
                text=texte,
                command=commande,
                fg_color=("#3498db", "#2980b9"),
                height=40,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # Zone d'affichage du graphique
        self.graph_frame = ctk.CTkFrame(self.content_frame)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Message initial
        msg = ctk.CTkLabel(
            self.graph_frame,
            text="Sélectionnez un graphique ci-dessus",
            font=ctk.CTkFont(size=16),
            text_color=("#95a5a6", "#7f8c8d")
        )
        msg.pack(expand=True)
    
    def afficher_graph_mentions(self):
        """Affiche le graphique des mentions"""
        self.clear_graph_frame()
        etudiants = self.db.obtenir_tous_etudiants()
        if etudiants:
            Graphiques.graphique_mentions(etudiants, self.graph_frame)
    
    def afficher_graph_promos(self):
        """Affiche le graphique des moyennes par promotion"""
        self.clear_graph_frame()
        etudiants = self.db.obtenir_tous_etudiants()
        if etudiants:
            Graphiques.graphique_moyennes_par_promotion(etudiants, self.graph_frame)
    
    def afficher_graph_distribution(self):
        """Affiche la distribution des moyennes"""
        self.clear_graph_frame()
        etudiants = self.db.obtenir_tous_etudiants()
        if etudiants:
            Graphiques.graphique_distribution_moyennes(etudiants, self.graph_frame)
    
    def afficher_graph_top10(self):
        """Affiche le top 10"""
        self.clear_graph_frame()
        etudiants = self.db.obtenir_tous_etudiants()
        if etudiants:
            Graphiques.graphique_top_etudiants(etudiants, 10, self.graph_frame)
    
    def clear_graph_frame(self):
        """Nettoie la zone de graphique"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
    
    def afficher_page_rapports(self):
        """Page des rapports"""
        self.clear_content()
        
        titre = ctk.CTkLabel(
            self.content_frame,
            text="📄 Rapports",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titre.pack(pady=20)
        
        msg = ctk.CTkLabel(
            self.content_frame,
            text="Génération de rapports en cours de développement...",
            font=ctk.CTkFont(size=16)
        )
        msg.pack(pady=50)
    
    def changer_theme(self):
        """Change le thème de l'application"""
        mode = self.theme_var.get()
        ctk.set_appearance_mode(mode)
    
    def faire_backup(self):
        """Fait un backup de la base"""
        fichier = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        
        if fichier:
            try:
                self.db.exporter_vers_json(fichier)
                messagebox.showinfo("Succès", f"Backup sauvegardé: {fichier}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du backup: {str(e)}")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()


def main():
    """Point d'entrée de l'application"""
    app = ApplicationModerne()
    app.run()


if __name__ == "__main__":
    main()
