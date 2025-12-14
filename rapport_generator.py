#!/usr/bin/env python3
"""
Module de génération de rapports HTML
Crée le rapport d'analyse avec les styles CSS
"""

from datetime import datetime
from styles import get_css_styles
from template_html import get_html_template

def generer_rapport_html(analyseur, fichier_sortie='rapport_analyse.html'):
    """
    Génère un rapport HTML complet avec les résultats de l'analyse
    
    Args:
        analyseur: Instance de AnalyseurTraficSuspect
        fichier_sortie: Nom du fichier HTML à créer
    """
    
    # Récupérer les styles CSS
    css = get_css_styles()
    
    # Construire le contenu HTML
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Analyse de Trafic Suspect</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Rapport d'Analyse de Trafic Suspect</h1>
            <p>Analyse PCAP - Détection de flux non désirables</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
        </div>
        
        <div class="content">
"""
    
    # Section Statistiques Globales
    html += generer_section_statistiques(analyseur)
    
    # Section Flux Suspects
    html += generer_section_flux_suspects(analyseur)
    
    # Section Flux Arrière-plan
    html += generer_section_flux_arriere_plan(analyseur)
    
    # Section Protocoles
    html += generer_section_protocoles(analyseur)
    
    # Section Conclusion
    html += generer_section_conclusion(analyseur)
    
    # Fermer le HTML
    html += f"""
        </div>
        
        <div class="footer">
            <p>Rapport généré automatiquement par l'Analyseur de Trafic Suspect</p>
            <p style="margin-top: 5px; font-size: 0.9em;">Fichier analysé: {analyseur.fichier_pcap}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Écrire le fichier
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        f.write(html)


def generer_section_statistiques(analyseur):
    """Génère la section des statistiques globales"""
    return f"""
            <div class="section">
                <h2>Statistiques Globales</h2>
                <div class="stat-grid">
                <div class="stat-grid">
                    <div class="stat-card">
                        <h3>{len(analyseur.flux_suspects)}</h3>
                        <p>Flux Suspects Détectés</p>
                    </div>
                    <div class="stat-card">
                        <h3>{len(analyseur.flux_arriere_plan)}</h3>
                        <p>Flux en Arrière-plan</p>
                    </div>
                    <div class="stat-card">
                        <h3>{len(analyseur.requetes_dns)}</h3>
                        <p>Requêtes DNS</p>
                    </div>
                    <div class="stat-card">
                        <h3>{len(analyseur.conversations)}</h3>
                        <p>Conversations IP</p>
                    </div>
                </div>
            </div>
"""


def generer_section_flux_suspects(analyseur):
    """Génère la section des flux suspects"""
    html = """
            <div class="section">
                <h2>Flux Suspects Détectés</h2>
"""
    
    if analyseur.flux_suspects:
        html += """
                <table>
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Détail</th>
                            <th>Sévérité</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for flux in analyseur.flux_suspects[:50]:  # Limiter à 50 entrées
            severite_class = flux['severite'].lower().replace('é', 'e')
            html += f"""
                        <tr>
                            <td><strong>{flux['type']}</strong></td>
                            <td>{flux['detail']}</td>
                            <td><span class="badge {severite_class}">{flux['severite']}</span></td>
                        </tr>
"""
        html += """
                    </tbody>
                </table>
"""
    else:
        html += '<p style="color: #6bcf7f; font-size: 1.2em;">✓ Aucun flux suspect détecté</p>'
    
    html += '</div>'
    return html


def generer_section_flux_arriere_plan(analyseur):
    """Génère la section des flux en arrière-plan"""
    html = """
            <div class="section">
                <h2>Flux Persistants en Arrière-plan</h2>
                <div class="alert">
                    <strong>⚠️ Attention:</strong> Ces flux continuent de communiquer alors que l'application est supposée inactive.
                </div>
"""
    
    if analyseur.flux_arriere_plan:
        html += """
                <table>
                    <thead>
                        <tr>
                            <th>Conversation</th>
                            <th>Paquets</th>
                            <th>Données (bytes)</th>
                            <th>Durée (s)</th>
                            <th>Débit (bytes/s)</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for flux in sorted(analyseur.flux_arriere_plan, key=lambda x: x['paquets'], reverse=True)[:20]:
            html += f"""
                        <tr>
                            <td><code>{flux['conversation']}</code></td>
                            <td>{flux['paquets']}</td>
                            <td>{flux['bytes']:,}</td>
                            <td>{flux['duree']}</td>
                            <td>{flux['debit']:,.2f}</td>
                        </tr>
"""
        html += """
                    </tbody>
                </table>
"""
    else:
        html += '<p style="color: #6bcf7f; font-size: 1.2em;">✓ Aucun flux persistant anormal détecté</p>'
    
    html += '</div>'
    return html


def generer_section_protocoles(analyseur):
    """Génère la section de répartition des protocoles"""
    html = """
            <div class="section">
                <h2>Répartition des Protocoles</h2>
"""
    
    total_paquets = sum(analyseur.stats_protocoles.values())
    for proto, count in sorted(analyseur.stats_protocoles.items(), key=lambda x: x[1], reverse=True)[:10]:
        pourcentage = (count / total_paquets * 100) if total_paquets > 0 else 0
        html += f"""
                <div style="margin: 10px 0;">
                    <p><strong>{proto}</strong> - {count:,} paquets ({pourcentage:.1f}%)</p>
                    <div class="protocole-bar" style="width: {pourcentage}%;">
                        <span>{count:,}</span>
                    </div>
                </div>
"""
    
    html += '</div>'
    return html


def generer_section_conclusion(analyseur):
    """Génère la section de conclusion"""
    html = """
            <div class="section">
                <h2>Conclusion de l'Analyse</h2>
                <p style="line-height: 1.8; font-size: 1.1em;">
"""
    
    if len(analyseur.flux_suspects) > 10 or len(analyseur.flux_arriere_plan) > 5:
        html += """
                    <strong style="color: #ff6b6b;">⚠️ Niveau de risque: ÉLEVÉ</strong><br><br>
                    Plusieurs flux suspects et activités en arrière-plan ont été détectés. 
                    Il est recommandé d'examiner en détail les applications concernées et de vérifier 
                    leurs permissions d'accès réseau.
"""
    elif len(analyseur.flux_suspects) > 0:
        html += """
                    <strong style="color: #ff9800;">⚠️ Niveau de risque: MODÉRÉ</strong><br><br>
                    Quelques flux suspects ont été identifiés. Une vérification des applications 
                    en arrière-plan est conseillée.
"""
    else:
        html += """
                    <strong style="color: #6bcf7f;">✓ Niveau de risque: FAIBLE</strong><br><br>
                    Aucun flux suspect majeur n'a été détecté. Le trafic analysé semble globalement légitime.
"""
    
    html += """
                </p>
            </div>
"""
    return html