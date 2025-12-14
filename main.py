#!/usr/bin/env python3
"""
Point d'entrée principal pour l'analyseur de trafic PCAP
"""

import sys
from analyseur import AnalyseurTraficSuspect

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <fichier.pcap> [rapport_sortie.html]")
        print("\nExemple:")
        print("  python main.py capture.pcap")
        print("  python main.py capture.pcap mon_rapport.html")
        sys.exit(1)
    
    fichier_pcap = sys.argv[1]
    fichier_rapport = sys.argv[2] if len(sys.argv) > 2 else 'rapport_analyse.html'
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ANALYSEUR DE TRAFIC SUSPECT - DÉTECTION DE FLUX           ║
║                  NON DÉSIRABLES (PCAP)                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Créer l'analyseur
    analyseur = AnalyseurTraficSuspect(fichier_pcap)
    
    # Étape 1: Analyse principale du fichier PCAP
    print("\n[ÉTAPE 1/4] Analyse des paquets PCAP...")
    analyseur.analyser()
    
    # Étape 2: Détection des flux persistants
    print("\n[ÉTAPE 2/4] Détection des flux persistants...")
    analyseur.detecter_flux_persistants()
    
    # Étape 3: Analyse des requêtes DNS
    print("\n[ÉTAPE 3/4] Analyse des fréquences DNS...")
    analyseur.analyser_frequence_dns()
    
    # Étape 4: Génération du rapport HTML
    print("\n[ÉTAPE 4/4] Génération du rapport HTML...")
    analyseur.generer_rapport_html(fichier_rapport)
    
    # Affichage du résumé
    analyseur.afficher_resume()
    
    print(f"\n{'='*70}")
    print(f"[✓] ANALYSE TERMINÉE AVEC SUCCÈS!")
    print(f"[✓] Rapport disponible: {fichier_rapport}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()