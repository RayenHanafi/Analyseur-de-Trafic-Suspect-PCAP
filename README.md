# 📊 Analyseur de Trafic Suspect PCAP

Outil d'analyse automatisée de fichiers PCAP pour détecter les flux réseau non désirables sur Android.

## 📁 Structure du Projet

```
projet_analyseur/
│
├── main.py                  # Point d'entrée principal
├── analyseur.py            # Logique d'analyse des paquets
├── rapport_generator.py    # Génération du rapport HTML
├── styles.py               # Styles CSS du rapport
├── template_html.py        # Templates HTML (optionnel)
└── README.md               # Cette documentation
```

## 🎯 Fonctionnalités

### Détection Automatique

- ✅ **Flux persistants** : Détecte les applications qui communiquent en arrière-plan (>50 paquets, >20s)
- ✅ **DNS suspects** : Identifie les domaines malveillants (.tk, .ml, .ga, etc.)
- ✅ **Ports malveillants** : Surveille les connexions vers des ports suspects (4444, 5555, 6666, etc.)
- ✅ **Trafic QUIC** : Détecte le protocole QUIC actif en arrière-plan (UDP 443)
- ✅ **Analyse des protocoles** : Statistiques complètes sur tous les protocoles utilisés

### Rapport HTML Interactif

- 📈 Statistiques globales en cartes visuelles
- 🚨 Liste détaillée des flux suspects avec niveaux de sévérité
- 📡 Tableau des flux persistants en arrière-plan
- 🔍 Graphiques de répartition des protocoles
- 📋 Évaluation automatique du niveau de risque

## 🚀 Installation

### Prérequis

1. **Python 3.8+**

```bash
python3 --version
```

2. **TShark/Wireshark** (requis par pyshark)

**Sur Ubuntu/Debian :**

```bash
sudo apt-get update
sudo apt-get install tshark
```

**Sur macOS :**

```bash
brew install wireshark
```

**Sur Windows :**

- Télécharger et installer Wireshark depuis : https://www.wireshark.org/download.html
- S'assurer que TShark est dans le PATH

3. **PyShark**

```bash
pip install pyshark
```

ou avec requirements.txt :

```bash
pip install -r requirements.txt
```

### Fichier requirements.txt

```
pyshark>=0.6
```

## 💻 Utilisation

### Commande de Base

```bash
python main.py capture.pcap
```

### Avec Nom de Rapport Personnalisé

```bash
python main.py capture.pcap mon_rapport.html
```

### Exemple Complet

```bash
# 1. Capturer le trafic avec tcpdump (Android avec root)
adb shell "tcpdump -i any -w /sdcard/capture.pcap"

# 2. Récupérer le fichier
adb pull /sdcard/capture.pcap

# 3. Analyser
python main.py capture.pcap rapport_facebook.html

# 4. Ouvrir le rapport
firefox rapport_facebook.html
```

## 📊 Sortie du Programme

### Terminal

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ANALYSEUR DE TRAFIC SUSPECT - DÉTECTION DE FLUX         ║
║                  NON DÉSIRABLES (PCAP)                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

[ÉTAPE 1/4] Analyse des paquets PCAP...
[*] Analyse du fichier: capture.pcap
[*] Chargement des paquets...
[*] 1000 paquets analysés...
[*] 2000 paquets analysés...
[✓] Analyse terminée: 2547 paquets traités

[ÉTAPE 2/4] Détection des flux persistants...
[*] Détection des flux persistants...
[✓] 3 flux persistants détectés

[ÉTAPE 3/4] Analyse des fréquences DNS...
[*] Analyse des requêtes DNS...
[✓] 142 requêtes DNS analysées, 2 domaines suspects

[ÉTAPE 4/4] Génération du rapport HTML...
[*] Génération du rapport HTML: rapport_analyse.html
[✓] Rapport généré: rapport_analyse.html

======================================================================
                  RÉSUMÉ DE L'ANALYSE
======================================================================

📊 Statistiques Globales:
   - Flux suspects détectés: 8
   - Flux persistants en arrière-plan: 3
   - Requêtes DNS: 142
   - Conversations IP: 47

🔴 Top 5 Flux Arrière-plan:
   - 192.168.1.45 → 157.240.13.35: 52 paquets en 27.3s
   - 192.168.1.45 → 142.250.185.106: 38 paquets en 22.1s
   - 192.168.1.45 → 172.217.16.195: 31 paquets en 20.5s

📡 Top 5 Protocoles:
   - TLS: 1,247 paquets
   - DNS: 284 paquets
   - QUIC: 156 paquets
   - TCP: 98 paquets
   - UDP: 42 paquets

======================================================================

[✓] ANALYSE TERMINÉE AVEC SUCCÈS!
[✓] Rapport disponible: rapport_analyse.html
```

### Rapport HTML

Le rapport généré contient :

1. **En-tête** : Titre, date de génération
2. **Statistiques Globales** : 4 cartes avec les métriques principales
3. **Flux Suspects** : Tableau détaillé avec badges de sévérité
   - 🔴 CRITIQUE : Ports malveillants
   - 🟠 HAUTE : DNS suspects
   - 🟡 MOYENNE : QUIC arrière-plan, DNS fréquents
4. **Flux Persistants** : Liste des communications en arrière-plan
5. **Répartition Protocoles** : Barres de progression visuelles
6. **Conclusion** : Évaluation automatique du risque

## 🎨 Architecture du Code

### main.py

Point d'entrée principal qui :

- Parse les arguments
- Crée l'analyseur
- Orchestre les 4 étapes d'analyse
- Affiche le résumé

### analyseur.py

Logique métier contenant :

- Classe `AnalyseurTraficSuspect`
- Analyse paquet par paquet
- Détection des flux suspects
- Algorithmes de détection

### rapport_generator.py

Génération du rapport avec :

- Fonction principale `generer_rapport_html()`
- Fonctions pour chaque section
- Assemblage du HTML final

### styles.py

Styles CSS incluant :

- Design moderne et responsive
- Animations CSS
- Codes couleurs pour les sévérités
- Support impression

## 📖 Critères de Détection

### Flux Persistants (MOYENNE-HAUTE)

```python
if paquets > 50 and duree > 20:
    # Flux suspect détecté
```

### DNS Suspects (HAUTE)

```python
tlds_suspects = ['.tk', '.ml', '.ga', '.cf', '.gq']
mots_suspects = ['temp', 'tmp', 'test', 'malware', 'c2', 'cmd']
```

### Ports Malveillants (CRITIQUE)

```python
ports_malveillants = [4444, 5555, 6666, 7777, 8080, 9999, 31337]
```

### DNS Fréquents (MOYENNE)

```python
if requetes_vers_domaine > 10:
    # Possible DNS tunneling
```

## 🔧 Personnalisation

### Modifier les Seuils de Détection

Dans `analyseur.py`, ligne 158 :

```python
# Changer le seuil de paquets
if stats['paquets'] > 50:  # Modifier cette valeur

# Changer le seuil de durée
if duree > 20:  # Modifier cette valeur
```

### Ajouter des Ports Suspects

Dans `analyseur.py`, ligne 115 :

```python
ports_malveillants = [4444, 5555, 6666, 7777, 8080, 9999, 31337,
                      8888, 1337]  # Ajouter vos ports
```

### Modifier les Couleurs du Rapport

Dans `styles.py`, lignes 62-81 :

```python
.critique { background: #ff6b6b; }  # Rouge
.haute { background: #ff9800; }     # Orange
.moyenne { background: #ffd93d; }   # Jaune
```

## 🐛 Dépannage

### Erreur : "Module pyshark not found"

```bash
pip install --upgrade pyshark
```

### Erreur : "TShark not found"

Installer Wireshark/TShark et vérifier le PATH :

```bash
which tshark  # Linux/Mac
where tshark  # Windows
```

### Erreur : "Permission denied"

Sur Linux, donner les permissions à TShark :

```bash
sudo dpkg-reconfigure wireshark-common
sudo usermod -a -G wireshark $USER
```

### Le rapport HTML est vide

Vérifier que le fichier PCAP est valide :

```bash
tshark -r capture.pcap -c 10
```

## 📝 Intégration dans un Rapport LaTeX

Voir la section LaTeX fournie séparément pour intégrer cette analyse dans votre rapport académique.

## 🤝 Contribution

Contributions bienvenues ! Pour ajouter des fonctionnalités :

1. Créer une nouvelle méthode de détection dans `analyseur.py`
2. Ajouter la section correspondante dans `rapport_generator.py`
3. Mettre à jour les styles si nécessaire dans `styles.py`

## 📄 Licence

Ce projet est fourni à des fins éducatives.

## 👨‍💻 Auteur

Développé pour l'analyse de sécurité réseau Android.

## 🔗 Ressources

- [Documentation PyShark](https://github.com/KimiNewt/pyshark)
- [Wireshark Display Filters](https://wiki.wireshark.org/DisplayFilters)
- [PCAP Analysis Guide](https://www.wireshark.org/docs/)

---

**Note**: Assurez-vous d'avoir l'autorisation légale avant de capturer et analyser le trafic réseau.
