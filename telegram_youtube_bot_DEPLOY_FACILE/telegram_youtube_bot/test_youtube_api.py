#!/usr/bin/env python3
"""
Test script per verificare la connessione all'API YouTube
"""

import sys
import json
from typing import Dict, Any, Optional

# Aggiungi il percorso del client API Manus
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

def test_youtube_search():
    """
    Testa la ricerca YouTube con parole chiave relative all'AI
    """
    print("🔍 Test API YouTube - Ricerca novità AI")
    print("=" * 50)
    
    # Parole chiave per testare la ricerca
    test_queries = [
        "intelligenza artificiale 2024",
        "AI tools coding",
        "machine learning platform",
        "AI video editing"
    ]
    
    client = ApiClient()
    
    for query in test_queries:
        print(f"\n🔎 Ricerca: '{query}'")
        print("-" * 30)
        
        try:
            # Parametri di ricerca
            query_params = {
                'q': query,
                'hl': 'it',  # Lingua italiana
                'gl': 'IT'   # Regione Italia
            }
            
            # Chiamata API
            response = client.call_api('Youtube/search', query=query_params)
            
            if response:
                contents = response.get('contents', [])
                estimated_results = response.get('estimatedResults', 0)
                
                print(f"✅ Risultati stimati: {estimated_results:,}")
                print(f"📄 Risultati in questa pagina: {len(contents)}")
                
                # Mostra i primi 2 risultati
                for i, content in enumerate(contents[:2], 1):
                    if content.get('type') == 'video':
                        video = content.get('video', {})
                        title = video.get('title', 'N/A')
                        channel = video.get('channelTitle', 'N/A')
                        published = video.get('publishedTimeText', 'N/A')
                        views = video.get('viewCountText', 'N/A')
                        
                        print(f"\n  🎥 Video {i}:")
                        print(f"     Titolo: {title[:60]}...")
                        print(f"     Canale: {channel}")
                        print(f"     Pubblicato: {published}")
                        print(f"     Visualizzazioni: {views}")
                
            else:
                print("❌ Nessun risultato ottenuto")
                
        except Exception as e:
            print(f"❌ Errore durante la ricerca: {str(e)}")
    
    print(f"\n{'='*50}")
    print("✅ Test completato!")

if __name__ == "__main__":
    test_youtube_search()

