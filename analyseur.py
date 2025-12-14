#!/usr/bin/env python3
"""
Module d'analyse de trafic PCAP
Contient toute la logique de détection des flux suspects
"""

import pyshark
from collections import defaultdict
from datetime import datetime
import sys
from rapport_generator import generer_rapport_html

class AnalyseurTraficSuspect:
    """Classe principale pour l'analyse de fichiers PCAP"""
    
    def __init__(self, fichier_pcap):
        self.fichier_pcap = fichier_pcap
        self.flux_suspects = []
        self.stats_protocoles = defaultdict(int)
        self.conversations = defaultdict(lambda: {'paquets': 0, 'bytes': 0, 'timestamps': []})
        self.requetes_dns = []
        self.flux_arriere_plan = []
        
    def analyser(self):
        """Analyse principale du fichier PCAP"""
        print(f"[*] Analyse du fichier: {self.fichier_pcap}")
        print("[*] Chargement des paquets...")
        
        try:
            capture = pyshark.FileCapture(self.fichier_pcap, keep_packets=False)
            
            compteur = 0
            for paquet in capture:
                compteur += 1
                if compteur % 1000 == 0:
                    print(f"[*] {compteur} paquets analysés...")
                
                self._analyser_paquet(paquet)
            
            capture.close()
            print(f"[✓] Analyse terminée: {compteur} paquets traités")
            
        except FileNotFoundError:
            print(f"[!] Erreur: Fichier '{self.fichier_pcap}' introuvable")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Erreur lors de l'analyse: {e}")
            sys.exit(1)
    
    def _analyser_paquet(self, paquet):
        """Analyse un paquet individuel"""
        try:
            # Statistiques des protocoles
            if hasattr(paquet, 'highest_layer'):
                self.stats_protocoles[paquet.highest_layer] += 1
            
            # Analyse TCP/UDP
            if hasattr(paquet, 'ip'):
                self._analyser_conversation(paquet)
            
            # Analyse DNS
            if hasattr(paquet, 'dns') and hasattr(paquet.dns, 'qry_name'):
                self._analyser_dns(paquet)
            
            # Détection QUIC
            if hasattr(paquet, 'udp') and hasattr(paquet.udp, 'dstport'):
                if paquet.udp.dstport == '443':
                    self._detecter_quic(paquet)
            
            # Détection ports suspects
            if hasattr(paquet, 'tcp'):
                self._detecter_ports_suspects(paquet)
                
        except AttributeError:
            pass
    
    def _analyser_conversation(self, paquet):
        """Analyse les conversations IP"""
        try:
            src = paquet.ip.src
            dst = paquet.ip.dst
            cle = f"{src} → {dst}"
            
            self.conversations[cle]['paquets'] += 1
            if hasattr(paquet, 'length'):
                self.conversations[cle]['bytes'] += int(paquet.length)
            
            if hasattr(paquet, 'sniff_timestamp'):
                self.conversations[cle]['timestamps'].append(float(paquet.sniff_timestamp))
                
        except AttributeError:
            pass
    
    def _analyser_dns(self, paquet):
        """Analyse les requêtes DNS"""
        try:
            domaine = paquet.dns.qry_name
            timestamp = float(paquet.sniff_timestamp) if hasattr(paquet, 'sniff_timestamp') else 0
            
            self.requetes_dns.append({
                'domaine': domaine,
                'timestamp': timestamp,
                'src': paquet.ip.src if hasattr(paquet, 'ip') else 'Unknown'
            })
            
            # Domaines suspects
            tlds_suspects = ['.tk', '.ml', '.ga', '.cf', '.gq']
            mots_suspects = ['temp', 'tmp', 'test', 'malware', 'c2', 'cmd']
            
            if any(tld in domaine for tld in tlds_suspects) or \
               any(mot in domaine.lower() for mot in mots_suspects):
                self.flux_suspects.append({
                    'type': 'DNS Suspect',
                    'detail': f"Domaine suspect: {domaine}",
                    'severite': 'HAUTE',
                    'timestamp': timestamp
                })
                
        except AttributeError:
            pass
    
    def _detecter_quic(self, paquet):
        """Détecte le trafic QUIC"""
        try:
            src = paquet.ip.src
            dst = paquet.ip.dst
            
            # QUIC utilise UDP port 443
            self.flux_suspects.append({
                'type': 'QUIC en arrière-plan',
                'detail': f"{src} → {dst} (UDP 443)",
                'severite': 'MOYENNE',
                'timestamp': float(paquet.sniff_timestamp) if hasattr(paquet, 'sniff_timestamp') else 0
            })
            
        except AttributeError:
            pass
    
    def _detecter_ports_suspects(self, paquet):
        """Détecte les ports suspects"""
        ports_malveillants = [4444, 5555, 6666, 7777, 8080, 9999, 31337]
        
        try:
            dstport = int(paquet.tcp.dstport)
            if dstport in ports_malveillants:
                self.flux_suspects.append({
                    'type': 'Port Malveillant',
                    'detail': f"Connexion vers port {dstport} ({paquet.ip.src} → {paquet.ip.dst})",
                    'severite': 'CRITIQUE',
                    'timestamp': float(paquet.sniff_timestamp) if hasattr(paquet, 'sniff_timestamp') else 0
                })
        except (AttributeError, ValueError):
            pass
    
    def detecter_flux_persistants(self):
        """Détecte les flux persistants en arrière-plan"""
        print("[*] Détection des flux persistants...")
        
        count = 0
        for conv, stats in self.conversations.items():
            # Flux avec plus de 50 paquets
            if stats['paquets'] > 50:
                # Calculer la durée
                if len(stats['timestamps']) > 1:
                    duree = stats['timestamps'][-1] - stats['timestamps'][0]
                    
                    # Flux persistant > 20 secondes
                    if duree > 20:
                        self.flux_arriere_plan.append({
                            'conversation': conv,
                            'paquets': stats['paquets'],
                            'bytes': stats['bytes'],
                            'duree': round(duree, 2),
                            'debit': round(stats['bytes'] / duree, 2) if duree > 0 else 0
                        })
                        count += 1
        
        print(f"[✓] {count} flux persistants détectés")
    
    def analyser_frequence_dns(self):
        """Analyse la fréquence des requêtes DNS"""
        print("[*] Analyse des requêtes DNS...")
        
        domaines = defaultdict(int)
        for req in self.requetes_dns:
            domaines[req['domaine']] += 1
        
        count = 0
        # Domaines contactés plus de 10 fois
        for domaine, freq in domaines.items():
            if freq > 10:
                self.flux_suspects.append({
                    'type': 'DNS Fréquent',
                    'detail': f"{domaine} contacté {freq} fois (possible DNS tunneling)",
                    'severite': 'MOYENNE',
                    'timestamp': 0
                })
                count += 1
        
        print(f"[✓] {len(self.requetes_dns)} requêtes DNS analysées, {count} domaines suspects")
    
    def generer_rapport_html(self, fichier_sortie='rapport_analyse.html'):
        """Génère un rapport HTML détaillé"""
        print(f"[*] Génération du rapport HTML: {fichier_sortie}")
        
        # Appeler la fonction du module rapport_generator
        generer_rapport_html(self, fichier_sortie)
        
        print(f"[✓] Rapport généré: {fichier_sortie}")
    
    def afficher_resume(self):
        """Affiche un résumé dans le terminal"""
        print("\n" + "="*70)
        print("                  RÉSUMÉ DE L'ANALYSE")
        print("="*70)
        print(f"\n📊 Statistiques Globales:")
        print(f"   - Flux suspects détectés: {len(self.flux_suspects)}")
        print(f"   - Flux persistants en arrière-plan: {len(self.flux_arriere_plan)}")
        print(f"   - Requêtes DNS: {len(self.requetes_dns)}")
        print(f"   - Conversations IP: {len(self.conversations)}")
        
        if self.flux_arriere_plan:
            print(f"\n🔴 Top 5 Flux Arrière-plan:")
            for flux in sorted(self.flux_arriere_plan, key=lambda x: x['paquets'], reverse=True)[:5]:
                print(f"   - {flux['conversation']}: {flux['paquets']} paquets en {flux['duree']}s")
        
        if self.stats_protocoles:
            print(f"\n📡 Top 5 Protocoles:")
            for proto, count in sorted(self.stats_protocoles.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   - {proto}: {count:,} paquets")
        
        print("\n" + "="*70 + "\n")