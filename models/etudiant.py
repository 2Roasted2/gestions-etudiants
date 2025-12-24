from datetime import datetime

class Etudiant:
    """Classe représentant un étudiant avec ses informations et ses notes"""
    
    def __init__(self, id_, nom, prenom, promotion, email="", photo_path=""):
        self.id = id_
        self.nom = nom.strip().upper()
        self.prenom = prenom.strip().capitalize()
        self.promotion = promotion.strip().upper()
        self.email = email.strip().lower()
        self.photo_path = photo_path
        self.notes = {}  # {matiere: [notes]}
        self.coefficients = {}  # {matiere: coefficient}
    
    def ajouter_note(self, matiere, note):
        """Ajoute une note pour une matière donnée"""
        if not isinstance(note, (int, float)):
            raise ValueError("La note doit être un nombre")
        
        if not 0 <= note <= 20:
            raise ValueError("La note doit être entre 0 et 20")
        
        matiere = matiere.strip().capitalize()
        self.notes.setdefault(matiere, []).append(float(note))
    
    def set_coefficient(self, matiere, coefficient):
        """Définit le coefficient d'une matière"""
        matiere = matiere.strip().capitalize()
        if coefficient <= 0:
            raise ValueError("Le coefficient doit être positif")
        self.coefficients[matiere] = coefficient
    
    def supprimer_note(self, matiere, index):
        """Supprime une note à l'index donné pour une matière"""
        matiere = matiere.strip().capitalize()
        if matiere in self.notes and 0 <= index < len(self.notes[matiere]):
            del self.notes[matiere][index]
            if not self.notes[matiere]:
                del self.notes[matiere]
            return True
        return False
    
    def modifier_note(self, matiere, index, nouvelle_note):
        """Modifie une note existante"""
        if not 0 <= nouvelle_note <= 20:
            raise ValueError("La note doit être entre 0 et 20")
        
        matiere = matiere.strip().capitalize()
        if matiere in self.notes and 0 <= index < len(self.notes[matiere]):
            self.notes[matiere][index] = float(nouvelle_note)
            return True
        return False
    
    def moyenne_matiere(self, matiere):
        """Calcule la moyenne d'une matière"""
        matiere = matiere.strip().capitalize()
        notes = self.notes.get(matiere, [])
        return sum(notes) / len(notes) if notes else 0
    
    def moyenne_generale(self):
        """Calcule la moyenne générale de toutes les matières"""
        if not self.notes:
            return 0
        
        moyennes = [self.moyenne_matiere(mat) for mat in self.notes.keys()]
        return sum(moyennes) / len(moyennes) if moyennes else 0
    
    def moyenne_generale_ponderee(self):
        """Calcule la moyenne générale pondérée par les coefficients"""
        if not self.notes:
            return 0
        
        total = 0
        coef_total = 0
        
        for matiere in self.notes.keys():
            coef = self.coefficients.get(matiere, 1)
            total += self.moyenne_matiere(matiere) * coef
            coef_total += coef
        
        return total / coef_total if coef_total > 0 else 0
    
    def get_mention(self):
        """Retourne la mention en fonction de la moyenne générale"""
        moy = self.moyenne_generale()
        
        match moy:
            case m if m >= 16:
                return "Très Bien"
            case m if m >= 14:
                return "Bien"
            case m if m >= 12:
                return "Assez Bien"
            case m if m >= 10:
                return "Passable"
            case _:
                return "Insuffisant"
    
    def nombre_matieres(self):
        """Retourne le nombre de matières"""
        return len(self.notes)
    
    def nombre_notes(self):
        """Retourne le nombre total de notes"""
        return sum(len(notes) for notes in self.notes.values())
    
    def to_dict(self):
        """Convertit l'étudiant en dictionnaire"""
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "promotion": self.promotion,
            "email": self.email,
            "photo_path": self.photo_path,
            "notes": self.notes,
            "coefficients": self.coefficients
        }
    
    def __str__(self):
        return f"{self.id} - {self.nom} {self.prenom} ({self.promotion})"
    
    def __repr__(self):
        return f"Etudiant(id={self.id}, nom='{self.nom}', prenom='{self.prenom}', promotion='{self.promotion}')"
