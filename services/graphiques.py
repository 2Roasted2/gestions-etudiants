import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import defaultdict
import numpy as np

# Configuration de matplotlib pour un rendu moderne
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

class Graphiques:
    """Gestionnaire de création de graphiques pour l'application"""
    
    # Palette de couleurs moderne
    COLORS = {
        'primary': '#3498db',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#1abc9c',
        'purple': '#9b59b6',
        'gray': '#95a5a6'
    }
    
    @staticmethod
    def graphique_mentions(etudiants, parent_widget=None):
        """Crée un graphique en camembert des mentions"""
        mentions = {
            "Très Bien": 0,
            "Bien": 0,
            "Assez Bien": 0,
            "Passable": 0,
            "Insuffisant": 0
        }
        
        for e in etudiants:
            mentions[e.get_mention()] += 1
        
        # Filtrer les mentions à 0
        mentions_filtered = {k: v for k, v in mentions.items() if v > 0}
        
        fig, ax = plt.subplots(figsize=(7, 6))
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']
        
        wedges, texts, autotexts = ax.pie(
            mentions_filtered.values(),
            labels=mentions_filtered.keys(),
            colors=colors[:len(mentions_filtered)],
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.05] * len(mentions_filtered),
            shadow=True
        )
        
        # Améliorer le style du texte
        for text in texts:
            text.set_fontsize(11)
            text.set_weight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title('Répartition des Mentions', fontsize=14, fontweight='bold', pad=20)
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
    
    @staticmethod
    def graphique_moyennes_par_promotion(etudiants, parent_widget=None):
        """Crée un histogramme des moyennes par promotion"""
        promos = defaultdict(list)
        
        for e in etudiants:
            promos[e.promotion].append(e.moyenne_generale())
        
        if not promos:
            return None
        
        promotions = sorted(promos.keys())
        moyennes = [sum(promos[p])/len(promos[p]) for p in promotions]
        
        fig, ax = plt.subplots(figsize=(9, 6))
        
        bars = ax.bar(
            range(len(promotions)),
            moyennes,
            color=Graphiques.COLORS['primary'],
            alpha=0.8,
            edgecolor='black',
            linewidth=1.2
        )
        
        # Gradient de couleur selon la moyenne
        for i, bar in enumerate(bars):
            if moyennes[i] >= 14:
                bar.set_color(Graphiques.COLORS['success'])
            elif moyennes[i] >= 10:
                bar.set_color(Graphiques.COLORS['primary'])
            else:
                bar.set_color(Graphiques.COLORS['danger'])
        
        ax.set_xticks(range(len(promotions)))
        ax.set_xticklabels(promotions, fontweight='bold')
        ax.set_ylabel('Moyenne Générale', fontsize=12, fontweight='bold')
        ax.set_xlabel('Promotion', fontsize=12, fontweight='bold')
        ax.set_title('Moyennes par Promotion', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Ajouter les valeurs sur les barres
        for i, (bar, moy) in enumerate(zip(bars, moyennes)):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.3,
                f'{moy:.2f}',
                ha='center',
                va='bottom',
                fontweight='bold',
                fontsize=10
            )
        
        plt.tight_layout()
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
    
    @staticmethod
    def graphique_evolution_notes(etudiant, matiere, parent_widget=None):
        """Crée une courbe d'évolution des notes dans une matière"""
        if matiere not in etudiant.notes or not etudiant.notes[matiere]:
            return None
        
        notes = etudiant.notes[matiere]
        x = list(range(1, len(notes) + 1))
        
        fig, ax = plt.subplots(figsize=(9, 6))
        
        # Courbe principale
        ax.plot(
            x, notes,
            marker='o',
            color=Graphiques.COLORS['primary'],
            linewidth=2.5,
            markersize=10,
            markerfacecolor=Graphiques.COLORS['success'],
            markeredgecolor='white',
            markeredgewidth=2,
            label='Notes'
        )
        
        # Ligne de moyenne
        moyenne = sum(notes) / len(notes)
        ax.axhline(
            y=moyenne,
            color=Graphiques.COLORS['warning'],
            linestyle='--',
            linewidth=2,
            label=f'Moyenne: {moyenne:.2f}/20'
        )
        
        # Ligne de passage (10/20)
        ax.axhline(
            y=10,
            color=Graphiques.COLORS['danger'],
            linestyle=':',
            linewidth=1.5,
            alpha=0.7,
            label='Seuil de passage (10/20)'
        )
        
        ax.set_xlabel('Numéro de contrôle', fontsize=12, fontweight='bold')
        ax.set_ylabel('Note (/20)', fontsize=12, fontweight='bold')
        ax.set_title(
            f'Évolution des notes en {matiere}\n{etudiant.prenom} {etudiant.nom}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.set_ylim(0, 21)
        ax.set_xlim(0.5, len(notes) + 0.5)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='best', framealpha=0.9)
        
        # Ajouter les valeurs sur les points
        for i, note in enumerate(notes):
            ax.annotate(
                f'{note:.1f}',
                (x[i], note),
                textcoords="offset points",
                xytext=(0, 10),
                ha='center',
                fontsize=9,
                fontweight='bold'
            )
        
        plt.tight_layout()
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
    
    @staticmethod
    def graphique_comparaison_matieres(etudiant, parent_widget=None):
        """Crée un graphique en barres des moyennes par matière"""
        if not etudiant.notes:
            return None
        
        matieres = sorted(etudiant.notes.keys())
        moyennes = [etudiant.moyenne_matiere(m) for m in matieres]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Créer les barres avec couleurs selon la moyenne
        colors = []
        for moy in moyennes:
            if moy >= 14:
                colors.append(Graphiques.COLORS['success'])
            elif moy >= 10:
                colors.append(Graphiques.COLORS['primary'])
            else:
                colors.append(Graphiques.COLORS['danger'])
        
        bars = ax.barh(matieres, moyennes, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
        
        ax.set_xlabel('Moyenne (/20)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Matière', fontsize=12, fontweight='bold')
        ax.set_title(
            f'Moyennes par matière - {etudiant.prenom} {etudiant.nom}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.set_xlim(0, 20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Ajouter les valeurs
        for i, (bar, moy) in enumerate(zip(bars, moyennes)):
            width = bar.get_width()
            ax.text(
                width + 0.3,
                bar.get_y() + bar.get_height()/2,
                f'{moy:.2f}',
                ha='left',
                va='center',
                fontweight='bold',
                fontsize=10
            )
        
        plt.tight_layout()
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
    
    @staticmethod
    def graphique_distribution_moyennes(etudiants, parent_widget=None):
        """Crée un histogramme de distribution des moyennes générales"""
        if not etudiants:
            return None
        
        moyennes = [e.moyenne_generale() for e in etudiants]
        
        fig, ax = plt.subplots(figsize=(9, 6))
        
        # Histogramme
        n, bins, patches = ax.hist(
            moyennes,
            bins=20,
            color=Graphiques.COLORS['primary'],
            alpha=0.7,
            edgecolor='black',
            linewidth=1.2
        )
        
        # Colorer selon les tranches de notes
        for i, patch in enumerate(patches):
            bin_center = (bins[i] + bins[i+1]) / 2
            if bin_center >= 14:
                patch.set_facecolor(Graphiques.COLORS['success'])
            elif bin_center >= 10:
                patch.set_facecolor(Graphiques.COLORS['primary'])
            else:
                patch.set_facecolor(Graphiques.COLORS['danger'])
        
        # Ligne de moyenne
        moyenne_globale = sum(moyennes) / len(moyennes)
        ax.axvline(
            x=moyenne_globale,
            color=Graphiques.COLORS['warning'],
            linestyle='--',
            linewidth=2,
            label=f'Moyenne: {moyenne_globale:.2f}'
        )
        
        ax.set_xlabel('Moyenne Générale', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre d\'étudiants', fontsize=12, fontweight='bold')
        ax.set_title('Distribution des Moyennes Générales', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.legend(loc='best', framealpha=0.9)
        
        plt.tight_layout()
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
    
    @staticmethod
    def graphique_radar_competences(etudiant, parent_widget=None):
        """Crée un graphique radar des compétences par matière"""
        if not etudiant.notes or len(etudiant.notes) < 3:
            return None
        
        matieres = list(etudiant.notes.keys())
        moyennes = [etudiant.moyenne_matiere(m) for m in matieres]
        
        # Nombre d'axes
        N = len(matieres)
        
        # Angles pour chaque axe
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        moyennes += moyennes[:1]  # Fermer le polygone
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        # Tracer
        ax.plot(angles, moyennes, 'o-', linewidth=2, color=Graphiques.COLORS['primary'])
        ax.fill(angles, moyennes, alpha=0.25, color=Graphiques.COLORS['primary'])
        
        # Labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(matieres, fontsize=10, fontweight='bold')
        
        ax.set_ylim(0, 20)
        ax.set_yticks([5, 10, 15, 20])
        ax.set_yticklabels(['5', '10', '15', '20'], fontsize=9)
        ax.set_title(
            f'Profil de compétences - {etudiant.prenom} {etudiant.nom}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.grid(True)
        
        plt.tight_layout()
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
    
    @staticmethod
    def graphique_top_etudiants(etudiants, n=10, parent_widget=None):
        """Crée un graphique des top N étudiants"""
        if not etudiants:
            return None
        
        # Trier par moyenne décroissante
        etudiants_tries = sorted(
            etudiants,
            key=lambda e: e.moyenne_generale(),
            reverse=True
        )[:n]
        
        noms = [f"{e.prenom} {e.nom[0]}." for e in etudiants_tries]
        moyennes = [e.moyenne_generale() for e in etudiants_tries]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.barh(noms, moyennes, color=Graphiques.COLORS['success'], alpha=0.8, edgecolor='black')
        
        ax.set_xlabel('Moyenne Générale', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {n} des Meilleurs Étudiants', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Ajouter médailles
        medals = ['🥇', '🥈', '🥉']
        for i, (bar, moy) in enumerate(zip(bars, moyennes)):
            width = bar.get_width()
            medal = medals[i] if i < 3 else ''
            ax.text(
                width + 0.3,
                bar.get_y() + bar.get_height()/2,
                f'{medal} {moy:.2f}',
                ha='left',
                va='center',
                fontweight='bold',
                fontsize=10
            )
        
        plt.tight_layout()
        
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, parent_widget)
            canvas.draw()
            return canvas.get_tk_widget()
        
        return fig
