from services.statistiques import (
    stats_par_matiere, stats_promotion, classement_etudiants,
    repartition_mentions, taux_reussite, analyse_matiere
)
from datetime import datetime

def generer_rapport_etudiant(etudiant):
    """Génère un rapport détaillé pour un étudiant
    
    Returns:
        Dictionnaire imbriqué avec toutes les informations de l'étudiant
    """
    rapport = {
        "informations": {
            "id": etudiant.id,
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "promotion": etudiant.promotion,
            "email": etudiant.email
        },
        "statistiques": {
            "moyenne_generale": round(etudiant.moyenne_generale(), 2),
            "mention": etudiant.get_mention(),
            "nombre_matieres": etudiant.nombre_matieres(),
            "nombre_notes_total": etudiant.nombre_notes()
        },
        "notes_par_matiere": {},
        "date_generation": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    # Détails par matière
    for matiere, notes in sorted(etudiant.notes.items()):
        rapport["notes_par_matiere"][matiere] = {
            "notes": notes,
            "nombre_notes": len(notes),
            "moyenne": round(etudiant.moyenne_matiere(matiere), 2),
            "meilleure_note": max(notes),
            "moins_bonne_note": min(notes)
        }
    
    return rapport

def generer_rapport_promotion(etudiants, promotion):
    """Génère un rapport complet pour une promotion
    
    Returns:
        Dictionnaire imbriqué avec statistiques et classement
    """
    stats = stats_promotion(etudiants, promotion)
    
    if not stats:
        return {"erreur": f"Aucun étudiant dans la promotion {promotion}"}
    
    etudiants_promo = [e for e in etudiants if e.promotion == promotion]
    classement = classement_etudiants(etudiants_promo)
    mentions = repartition_mentions(etudiants_promo)
    reussis, total, taux = taux_reussite(etudiants_promo)
    
    rapport = {
        "promotion": promotion,
        "date_generation": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "effectif": {
            "nombre_etudiants": stats["nombre_etudiants"],
            "nombre_reussis": reussis,
            "nombre_echecs": total - reussis,
            "taux_reussite": round(taux, 2)
        },
        "statistiques_globales": stats.get("global", {}),
        "statistiques_par_matiere": stats.get("matieres", {}),
        "repartition_mentions": mentions,
        "classement": classement[:20],  # Top 20
        "major_promotion": classement[0] if classement else None
    }
    
    return rapport

def generer_rapport_global(etudiants):
    """Génère un rapport global de tous les étudiants
    
    Returns:
        Dictionnaire imbriqué avec vue d'ensemble complète
    """
    if not etudiants:
        return {"erreur": "Aucun étudiant dans la base de données"}
    
    promotions = set(e.promotion for e in etudiants)
    stats_matieres = stats_par_matiere(etudiants)
    classement_global = classement_etudiants(etudiants)
    mentions = repartition_mentions(etudiants)
    reussis, total, taux = taux_reussite(etudiants)
    
    rapport = {
        "date_generation": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "vue_ensemble": {
            "nombre_total_etudiants": len(etudiants),
            "nombre_promotions": len(promotions),
            "nombre_matieres": len(stats_matieres),
            "taux_reussite_global": round(taux, 2)
        },
        "promotions": list(promotions),
        "statistiques_par_matiere": stats_matieres,
        "repartition_mentions": mentions,
        "top_10_etudiants": classement_global[:10],
        "statistiques_par_promotion": {}
    }
    
    # Stats détaillées par promotion
    for promo in promotions:
        rapport["statistiques_par_promotion"][promo] = stats_promotion(etudiants, promo)
    
    return rapport

def generer_rapport_matiere(etudiants, matiere):
    """Génère un rapport détaillé pour une matière spécifique
    
    Returns:
        Dictionnaire avec analyse complète de la matière
    """
    analyse = analyse_matiere(etudiants, matiere)
    
    if not analyse:
        return {"erreur": f"Aucune donnée pour la matière {matiere}"}
    
    rapport = {
        "matiere": matiere,
        "date_generation": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "vue_ensemble": {
            "nombre_etudiants_inscrits": analyse["nombre_etudiants"],
            "nombre_notes_total": analyse["nombre_notes_total"],
            "moyenne_classe": round(analyse["statistiques"]["moyenne"], 2)
        },
        "statistiques": analyse["statistiques"],
        "top_10_etudiants": analyse["etudiants"][:10],
        "etudiants_en_difficulte": [
            e for e in analyse["etudiants"] 
            if e["moyenne_matiere"] < 10
        ]
    }
    
    return rapport

def generer_bulletin(etudiant, format_texte=False):
    """Génère un bulletin de notes pour un étudiant
    
    Args:
        etudiant: L'étudiant concerné
        format_texte: Si True, retourne un texte formaté, sinon un dictionnaire
    
    Returns:
        Bulletin sous forme de dictionnaire ou texte
    """
    bulletin = generer_rapport_etudiant(etudiant)
    
    if not format_texte:
        return bulletin
    
    # Format texte pour impression
    texte = f"""
{'='*60}
                    BULLETIN DE NOTES
{'='*60}

Étudiant : {etudiant.nom} {etudiant.prenom}
ID : {etudiant.id}
Promotion : {etudiant.promotion}
Email : {etudiant.email}

{'-'*60}
                    NOTES PAR MATIÈRE
{'-'*60}
"""
    
    for matiere, details in sorted(bulletin["notes_par_matiere"].items()):
        texte += f"\n{matiere}:\n"
        texte += f"  Notes : {', '.join(map(str, details['notes']))}\n"
        texte += f"  Moyenne : {details['moyenne']}/20\n"
        texte += f"  Meilleure note : {details['meilleure_note']}/20\n"
        texte += f"  Moins bonne note : {details['moins_bonne_note']}/20\n"
    
    texte += f"""
{'-'*60}
                    RÉSULTATS GÉNÉRAUX
{'-'*60}

Moyenne générale : {bulletin['statistiques']['moyenne_generale']}/20
Mention : {bulletin['statistiques']['mention']}
Nombre de matières : {bulletin['statistiques']['nombre_matieres']}
Nombre total de notes : {bulletin['statistiques']['nombre_notes_total']}

{'-'*60}
Date d'édition : {bulletin['date_generation']}
{'='*60}
"""
    
    return texte

def exporter_rapport_txt(rapport, nom_fichier):
    """Exporte un rapport au format texte
    
    Args:
        rapport: Le rapport à exporter (dictionnaire)
        nom_fichier: Nom du fichier de sortie
    """
    import json
    
    try:
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write("RAPPORT DÉTAILLÉ\n")
            f.write("=" * 80 + "\n\n")
            f.write(json.dumps(rapport, indent=4, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"Erreur lors de l'export : {e}")
        return False

def comparer_promotions(etudiants, promo1, promo2):
    """Compare deux promotions
    
    Returns:
        Dictionnaire avec comparaison détaillée
    """
    stats1 = stats_promotion(etudiants, promo1)
    stats2 = stats_promotion(etudiants, promo2)
    
    if not stats1 or not stats2:
        return {"erreur": "Une ou les deux promotions n'existent pas"}
    
    comparaison = {
        "promotion_1": promo1,
        "promotion_2": promo2,
        "effectifs": {
            promo1: stats1["nombre_etudiants"],
            promo2: stats2["nombre_etudiants"]
        },
        "moyennes_generales": {
            promo1: round(stats1["global"]["moyenne_generale"], 2),
            promo2: round(stats2["global"]["moyenne_generale"], 2)
        },
        "taux_reussite": {
            promo1: round(taux_reussite([e for e in etudiants if e.promotion == promo1])[2], 2),
            promo2: round(taux_reussite([e for e in etudiants if e.promotion == promo2])[2], 2)
        },
        "meilleure_promotion": promo1 if stats1["global"]["moyenne_generale"] > stats2["global"]["moyenne_generale"] else promo2
    }
    
    return comparaison
