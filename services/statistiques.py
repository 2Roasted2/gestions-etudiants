from statistics import median, stdev

def moyenne(liste):
    """Calcule la moyenne d'une liste de nombres"""
    return sum(liste) / len(liste) if liste else 0

def moyenne_generale(etudiant):
    """Calcule la moyenne générale d'un étudiant"""
    if not etudiant.notes:
        return 0
    
    moyennes = [moyenne(notes) for notes in etudiant.notes.values()]
    return moyenne(moyennes)

def stats_par_matiere(etudiants):
    """Calcule les statistiques par matière pour tous les étudiants
    
    Returns:
        Dictionnaire imbriqué avec statistiques détaillées par matière
    """
    stats = {}
    
    # Collecte des notes par matière
    for e in etudiants:
        for matiere, notes in e.notes.items():
            stats.setdefault(matiere, []).extend(notes)
    
    # Calcul des statistiques
    resultats = {}
    for matiere, notes in stats.items():
        if notes:
            resultats[matiere] = {
                "nombre_notes": len(notes),
                "moyenne": moyenne(notes),
                "mediane": median(notes),
                "max": max(notes),
                "min": min(notes),
                "ecart_type": stdev(notes) if len(notes) > 1 else 0,
                "notes": sorted(notes, reverse=True)
            }
    
    return resultats

def stats_promotion(etudiants, promotion):
    """Calcule les statistiques d'une promotion spécifique
    
    Returns:
        Dictionnaire avec statistiques par matière et globales
    """
    etudiants_promo = [e for e in etudiants if e.promotion == promotion]
    
    if not etudiants_promo:
        return {}
    
    stats = {}
    moyennes_generales = []
    
    # Stats par matière
    for e in etudiants_promo:
        moyennes_generales.append(e.moyenne_generale())
        for matiere, notes in e.notes.items():
            stats.setdefault(matiere, []).extend(notes)
    
    # Calcul des statistiques
    resultats = {
        "promotion": promotion,
        "nombre_etudiants": len(etudiants_promo),
        "matieres": {},
        "global": {}
    }
    
    for matiere, notes in stats.items():
        if notes:
            resultats["matieres"][matiere] = {
                "nombre_notes": len(notes),
                "moyenne": moyenne(notes),
                "mediane": median(notes),
                "max": max(notes),
                "min": min(notes),
                "ecart_type": stdev(notes) if len(notes) > 1 else 0
            }
    
    # Statistiques globales de la promotion
    if moyennes_generales:
        resultats["global"] = {
            "moyenne_generale": moyenne(moyennes_generales),
            "mediane": median(moyennes_generales),
            "meilleure_moyenne": max(moyennes_generales),
            "moins_bonne_moyenne": min(moyennes_generales),
            "ecart_type": stdev(moyennes_generales) if len(moyennes_generales) > 1 else 0
        }
    
    return resultats

def classement_etudiants(etudiants, par_promotion=False):
    """Classe les étudiants par moyenne générale
    
    Returns:
        Liste de tuples (rang, etudiant, moyenne, mention)
    """
    if par_promotion:
        classements = {}
        promotions = set(e.promotion for e in etudiants)
        
        for promo in promotions:
            etudiants_promo = [e for e in etudiants if e.promotion == promo]
            classements[promo] = _classement_helper(etudiants_promo)
        
        return classements
    else:
        return _classement_helper(etudiants)

def _classement_helper(etudiants):
    """Fonction helper pour le classement"""
    if not etudiants:
        return []
    
    # Trier par moyenne décroissante
    etudiants_tries = sorted(
        etudiants,
        key=lambda e: e.moyenne_generale(),
        reverse=True
    )
    
    classement = []
    for rang, e in enumerate(etudiants_tries, 1):
        classement.append({
            "rang": rang,
            "id": e.id,
            "nom": e.nom,
            "prenom": e.prenom,
            "promotion": e.promotion,
            "moyenne": e.moyenne_generale(),
            "mention": e.get_mention(),
            "nombre_matieres": e.nombre_matieres()
        })
    
    return classement

def repartition_mentions(etudiants):
    """Calcule la répartition des mentions
    
    Returns:
        Dictionnaire avec le nombre d'étudiants par mention
    """
    mentions = {
        "Très Bien": 0,
        "Bien": 0,
        "Assez Bien": 0,
        "Passable": 0,
        "Insuffisant": 0
    }
    
    for e in etudiants:
        mention = e.get_mention()
        mentions[mention] += 1
    
    return mentions

def taux_reussite(etudiants, seuil=10):
    """Calcule le taux de réussite (moyenne >= seuil)
    
    Returns:
        Tuple (nombre_reussis, nombre_total, taux_pourcentage)
    """
    if not etudiants:
        return (0, 0, 0)
    
    reussis = sum(1 for e in etudiants if e.moyenne_generale() >= seuil)
    total = len(etudiants)
    taux = (reussis / total) * 100 if total > 0 else 0
    
    return (reussis, total, taux)

def meilleurs_etudiants(etudiants, n=10):
    """Retourne les n meilleurs étudiants
    
    Returns:
        Liste des n meilleurs étudiants triés par moyenne
    """
    classement = classement_etudiants(etudiants)
    return classement[:n]

def etudiants_en_difficulte(etudiants, seuil=10):
    """Retourne les étudiants ayant une moyenne < seuil
    
    Returns:
        Liste des étudiants en difficulté
    """
    return [
        {
            "id": e.id,
            "nom": e.nom,
            "prenom": e.prenom,
            "promotion": e.promotion,
            "moyenne": e.moyenne_generale()
        }
        for e in etudiants if e.moyenne_generale() < seuil
    ]

def analyse_matiere(etudiants, matiere):
    """Analyse détaillée d'une matière spécifique
    
    Returns:
        Dictionnaire avec statistiques et liste des étudiants
    """
    notes_collectees = []
    etudiants_matiere = []
    
    for e in etudiants:
        if matiere in e.notes:
            moy_mat = e.moyenne_matiere(matiere)
            notes_collectees.extend(e.notes[matiere])
            etudiants_matiere.append({
                "id": e.id,
                "nom": e.nom,
                "prenom": e.prenom,
                "moyenne_matiere": moy_mat,
                "nombre_notes": len(e.notes[matiere]),
                "notes": e.notes[matiere]
            })
    
    if not notes_collectees:
        return None
    
    # Tri par moyenne décroissante
    etudiants_matiere.sort(key=lambda x: x["moyenne_matiere"], reverse=True)
    
    return {
        "matiere": matiere,
        "nombre_etudiants": len(etudiants_matiere),
        "nombre_notes_total": len(notes_collectees),
        "statistiques": {
            "moyenne": moyenne(notes_collectees),
            "mediane": median(notes_collectees),
            "max": max(notes_collectees),
            "min": min(notes_collectees),
            "ecart_type": stdev(notes_collectees) if len(notes_collectees) > 1 else 0
        },
        "etudiants": etudiants_matiere
    }
