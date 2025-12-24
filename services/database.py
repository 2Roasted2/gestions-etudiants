import sqlite3
import json
import os
from datetime import datetime
from models.etudiant import Etudiant

class Database:
    """Gestionnaire de base de données SQLite pour les étudiants"""
    
    def __init__(self, db_path="data/etudiants.db"):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        self.creer_tables()
    
    def creer_tables(self):
        """Crée les tables si elles n'existent pas"""
        cursor = self.conn.cursor()
        
        # Table des étudiants
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS etudiants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                promotion TEXT NOT NULL,
                email TEXT,
                photo_path TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des notes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                etudiant_id INTEGER NOT NULL,
                matiere TEXT NOT NULL,
                note REAL NOT NULL CHECK(note >= 0 AND note <= 20),
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE
            )
        ''')
        
        # Table des coefficients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coefficients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                etudiant_id INTEGER NOT NULL,
                matiere TEXT NOT NULL,
                coefficient REAL NOT NULL CHECK(coefficient > 0),
                FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
                UNIQUE(etudiant_id, matiere)
            )
        ''')
        
        # Index pour améliorer les performances
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_notes_etudiant 
            ON notes(etudiant_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_etudiants_promotion 
            ON etudiants(promotion)
        ''')
        
        self.conn.commit()
    
    def ajouter_etudiant(self, nom, prenom, promotion, email="", photo_path=""):
        """Ajoute un nouvel étudiant dans la base"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO etudiants (nom, prenom, promotion, email, photo_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (nom.upper(), prenom.capitalize(), promotion.upper(), email.lower(), photo_path))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def modifier_etudiant(self, id_, nom=None, prenom=None, promotion=None, email=None, photo_path=None):
        """Modifie les informations d'un étudiant"""
        cursor = self.conn.cursor()
        
        updates = []
        params = []
        
        if nom is not None:
            updates.append("nom = ?")
            params.append(nom.upper())
        if prenom is not None:
            updates.append("prenom = ?")
            params.append(prenom.capitalize())
        if promotion is not None:
            updates.append("promotion = ?")
            params.append(promotion.upper())
        if email is not None:
            updates.append("email = ?")
            params.append(email.lower())
        if photo_path is not None:
            updates.append("photo_path = ?")
            params.append(photo_path)
        
        if updates:
            params.append(id_)
            query = f"UPDATE etudiants SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount > 0
        
        return False
    
    def supprimer_etudiant(self, id_):
        """Supprime un étudiant et toutes ses notes"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM etudiants WHERE id = ?", (id_,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def obtenir_etudiant(self, id_):
        """Récupère un étudiant par son ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM etudiants WHERE id = ?", (id_,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_etudiant(row)
        return None
    
    def obtenir_tous_etudiants(self):
        """Récupère tous les étudiants"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM etudiants ORDER BY nom, prenom")
        rows = cursor.fetchall()
        
        return [self._row_to_etudiant(row) for row in rows]
    
    def obtenir_etudiants_par_promotion(self, promotion):
        """Récupère les étudiants d'une promotion"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM etudiants WHERE promotion = ? ORDER BY nom, prenom",
            (promotion.upper(),)
        )
        rows = cursor.fetchall()
        
        return [self._row_to_etudiant(row) for row in rows]
    
    def rechercher_etudiants(self, critere, valeur):
        """Recherche des étudiants selon un critère"""
        cursor = self.conn.cursor()
        
        match critere.lower():
            case "nom":
                cursor.execute(
                    "SELECT * FROM etudiants WHERE nom LIKE ? ORDER BY nom",
                    (f"%{valeur.upper()}%",)
                )
            case "prenom":
                cursor.execute(
                    "SELECT * FROM etudiants WHERE prenom LIKE ? ORDER BY prenom",
                    (f"%{valeur.capitalize()}%",)
                )
            case "promotion":
                cursor.execute(
                    "SELECT * FROM etudiants WHERE promotion = ? ORDER BY nom",
                    (valeur.upper(),)
                )
            case "id":
                cursor.execute("SELECT * FROM etudiants WHERE id = ?", (int(valeur),))
            case _:
                return []
        
        rows = cursor.fetchall()
        return [self._row_to_etudiant(row) for row in rows]
    
    def ajouter_note(self, etudiant_id, matiere, note):
        """Ajoute une note pour un étudiant"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notes (etudiant_id, matiere, note)
            VALUES (?, ?, ?)
        ''', (etudiant_id, matiere.capitalize(), float(note)))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def obtenir_notes_etudiant(self, etudiant_id):
        """Récupère toutes les notes d'un étudiant"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT matiere, note FROM notes WHERE etudiant_id = ? ORDER BY matiere, date_ajout",
            (etudiant_id,)
        )
        rows = cursor.fetchall()
        
        # Organiser par matière
        notes = {}
        for row in rows:
            matiere = row['matiere']
            note = row['note']
            notes.setdefault(matiere, []).append(note)
        
        return notes
    
    def supprimer_note(self, etudiant_id, matiere, index):
        """Supprime une note spécifique"""
        cursor = self.conn.cursor()
        
        # Récupérer toutes les notes de cette matière
        cursor.execute('''
            SELECT id FROM notes 
            WHERE etudiant_id = ? AND matiere = ?
            ORDER BY date_ajout
        ''', (etudiant_id, matiere.capitalize()))
        
        rows = cursor.fetchall()
        
        if 0 <= index < len(rows):
            note_id = rows[index]['id']
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self.conn.commit()
            return True
        
        return False
    
    def set_coefficient(self, etudiant_id, matiere, coefficient):
        """Définit le coefficient d'une matière pour un étudiant"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO coefficients (etudiant_id, matiere, coefficient)
            VALUES (?, ?, ?)
        ''', (etudiant_id, matiere.capitalize(), float(coefficient)))
        
        self.conn.commit()
    
    def obtenir_coefficients(self, etudiant_id):
        """Récupère les coefficients d'un étudiant"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT matiere, coefficient FROM coefficients WHERE etudiant_id = ?",
            (etudiant_id,)
        )
        rows = cursor.fetchall()
        
        return {row['matiere']: row['coefficient'] for row in rows}
    
    def obtenir_promotions(self):
        """Récupère la liste des promotions"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT promotion FROM etudiants ORDER BY promotion")
        rows = cursor.fetchall()
        
        return [row['promotion'] for row in rows]
    
    def obtenir_matieres(self):
        """Récupère la liste des matières"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT matiere FROM notes ORDER BY matiere")
        rows = cursor.fetchall()
        
        return [row['matiere'] for row in rows]
    
    def nombre_total_etudiants(self):
        """Retourne le nombre total d'étudiants"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM etudiants")
        return cursor.fetchone()['count']
    
    def _row_to_etudiant(self, row):
        """Convertit une ligne SQL en objet Etudiant"""
        etudiant = Etudiant(
            row['id'],
            row['nom'],
            row['prenom'],
            row['promotion'],
            row['email'] or "",
            row['photo_path'] or ""
        )
        
        # Charger les notes
        etudiant.notes = self.obtenir_notes_etudiant(row['id'])
        
        # Charger les coefficients
        etudiant.coefficients = self.obtenir_coefficients(row['id'])
        
        return etudiant
    
    def exporter_vers_json(self, fichier="data/backup.json"):
        """Exporte toute la base vers JSON (backup)"""
        etudiants = self.obtenir_tous_etudiants()
        data = [e.to_dict() for e in etudiants]
        
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        return True
    
    def importer_depuis_json(self, fichier):
        """Importe des données depuis JSON"""
        with open(fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            etudiant_id = self.ajouter_etudiant(
                item['nom'],
                item['prenom'],
                item['promotion'],
                item.get('email', ''),
                item.get('photo_path', '')
            )
            
            # Ajouter les notes
            for matiere, notes in item.get('notes', {}).items():
                for note in notes:
                    self.ajouter_note(etudiant_id, matiere, note)
            
            # Ajouter les coefficients
            for matiere, coef in item.get('coefficients', {}).items():
                self.set_coefficient(etudiant_id, matiere, coef)
        
        return True
    
    def fermer(self):
        """Ferme la connexion à la base de données"""
        self.conn.close()
    
    def __del__(self):
        """Ferme automatiquement la connexion"""
        if hasattr(self, 'conn'):
            self.conn.close()
