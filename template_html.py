#!/usr/bin/env python3
"""
Module contenant les templates HTML réutilisables
(Optionnel - utilisé si besoin de templates supplémentaires)
"""

def get_html_template():
    """
    Retourne le template HTML de base
    Ce fichier est optionnel et peut être utilisé pour des extensions futures
    """
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
    {content}
</body>
</html>
"""


def get_section_template():
    """Template pour une section générique"""
    return """
<div class="section">
    <h2>{icon} {title}</h2>
    {content}
</div>
"""


def get_table_template():
    """Template pour un tableau"""
    return """
<table>
    <thead>
        <tr>{headers}</tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""


def get_stat_card_template():
    """Template pour une carte statistique"""
    return """
<div class="stat-card">
    <h3>{value}</h3>
    <p>{label}</p>
</div>
"""


def get_badge_template(severite):
    """Retourne un badge selon la sévérité"""
    severite_map = {
        'CRITIQUE': 'critique',
        'HAUTE': 'haute',
        'MOYENNE': 'moyenne',
        'BASSE': 'basse'
    }
    
    css_class = severite_map.get(severite, 'moyenne')
    
    return f'<span class="badge {css_class}">{severite}</span>'


def get_alert_template(message, level='warning'):
    """Template pour une alerte"""
    icons = {
        'warning': '⚠️',
        'error': '❌',
        'success': '✅',
        'info': 'ℹ️'
    }
    
    icon = icons.get(level, '⚠️')
    
    return f"""
<div class="alert">
    <strong>{icon} Attention:</strong> {message}
</div>
"""


def get_progress_bar_template(label, value, max_value):
    """Template pour une barre de progression"""
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    return f"""
<div style="margin: 10px 0;">
    <p><strong>{label}</strong> - {value:,} ({percentage:.1f}%)</p>
    <div class="protocole-bar" style="width: {percentage}%;">
        <span>{value:,}</span>
    </div>
</div>
"""


# Fonctions utilitaires supplémentaires

def format_bytes(bytes_value):
    """Formate une valeur en bytes de manière lisible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"


def format_duration(seconds):
    """Formate une durée en secondes de manière lisible"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def get_risk_level_html(flux_suspects_count, flux_arriere_plan_count):
    """Génère le HTML pour le niveau de risque"""
    if flux_suspects_count > 10 or flux_arriere_plan_count > 5:
        return """
<strong style="color: #ff6b6b;">⚠️ Niveau de risque: ÉLEVÉ</strong><br><br>
Plusieurs flux suspects et activités en arrière-plan ont été détectés. 
Il est recommandé d'examiner en détail les applications concernées et de vérifier 
leurs permissions d'accès réseau.
"""
    elif flux_suspects_count > 0:
        return """
<strong style="color: #ff9800;">⚠️ Niveau de risque: MODÉRÉ</strong><br><br>
Quelques flux suspects ont été identifiés. Une vérification des applications 
en arrière-plan est conseillée.
"""
    else:
        return """
<strong style="color: #6bcf7f;">✅ Niveau de risque: FAIBLE</strong><br><br>
Aucun flux suspect majeur n'a été détecté. Le trafic analysé semble globalement légitime.
"""


def get_footer_template(fichier_pcap):
    """Template pour le footer"""
    from datetime import datetime
    
    return f"""
<div class="footer">
    <p>Rapport généré automatiquement par l'Analyseur de Trafic Suspect</p>
    <p style="margin-top: 5px; font-size: 0.9em;">Fichier analysé: {fichier_pcap}</p>
    <p style="margin-top: 5px; font-size: 0.85em; opacity: 0.8;">
        Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
    </p>
</div>
"""


# Export des templates si nécessaire
__all__ = [
    'get_html_template',
    'get_section_template',
    'get_table_template',
    'get_stat_card_template',
    'get_badge_template',
    'get_alert_template',
    'get_progress_bar_template',
    'format_bytes',
    'format_duration',
    'get_risk_level_html',
    'get_footer_template'
]