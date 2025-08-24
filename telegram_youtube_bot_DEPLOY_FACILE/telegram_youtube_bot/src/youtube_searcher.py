"""
Modulo per la ricerca automatica di video YouTube sull'intelligenza artificiale
"""

import sys
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os

# Aggiungi il percorso del client API Manus
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# Aggiungi il percorso del progetto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import Config, logger

class YouTubeSearcher:
    """Classe per gestire le ricerche YouTube automatiche"""
    
    def __init__(self):
        self.api_client = ApiClient()
        self.sent_videos_file = Config.SENT_VIDEOS_FILE
        self.sent_videos = self._load_sent_videos()
        
    def _load_sent_videos(self) -> Dict[str, Any]:
        """Carica l'elenco dei video già inviati"""
        try:
            if os.path.exists(self.sent_videos_file):
                with open(self.sent_videos_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Caricati {len(data.get('videos', []))} video già inviati")
                    return data
        except Exception as e:
            logger.error(f"Errore nel caricamento video inviati: {e}")
        
        # Struttura di default
        return {
            "last_update": datetime.now().isoformat(),
            "videos": []
        }
    
    def _save_sent_videos(self):
        """Salva l'elenco dei video già inviati"""
        try:
            # Crea la directory se non esiste
            os.makedirs(os.path.dirname(self.sent_videos_file), exist_ok=True)
            
            self.sent_videos["last_update"] = datetime.now().isoformat()
            
            with open(self.sent_videos_file, 'w', encoding='utf-8') as f:
                json.dump(self.sent_videos, f, ensure_ascii=False, indent=2)
                
            logger.debug("File video inviati salvato")
        except Exception as e:
            logger.error(f"Errore nel salvataggio video inviati: {e}")
    
    def _is_video_sent(self, video_id: str) -> bool:
        """Controlla se un video è già stato inviato"""
        return any(video.get('video_id') == video_id for video in self.sent_videos.get('videos', []))
    
    def _add_sent_video(self, video_data: Dict[str, Any]):
        """Aggiunge un video all'elenco di quelli inviati"""
        if 'videos' not in self.sent_videos:
            self.sent_videos['videos'] = []
        
        video_record = {
            "video_id": video_data.get('video_id'),
            "title": video_data.get('title'),
            "channel": video_data.get('channel'),
            "sent_at": datetime.now().isoformat(),
            "url": f"https://www.youtube.com/watch?v={video_data.get('video_id')}"
        }
        
        self.sent_videos['videos'].append(video_record)
        
        # Mantieni solo gli ultimi 1000 video per evitare file troppo grandi
        if len(self.sent_videos['videos']) > 1000:
            self.sent_videos['videos'] = self.sent_videos['videos'][-1000:]
        
        self._save_sent_videos()
        logger.debug(f"Video aggiunto ai già inviati: {video_data.get('title')}")
    
    def _parse_video_data(self, content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Estrae i dati rilevanti da un risultato di ricerca YouTube"""
        if content.get('type') != 'video':
            return None
        
        video = content.get('video', {})
        
        # Estrai i dati principali
        video_data = {
            'video_id': video.get('videoId'),
            'title': video.get('title', 'N/A'),
            'channel': video.get('channelTitle', 'N/A'),
            'channel_id': video.get('channelId'),
            'published': video.get('publishedTimeText', 'N/A'),
            'duration': video.get('lengthText', 'N/A'),
            'views': video.get('viewCountText', 'N/A'),
            'description': video.get('descriptionSnippet', ''),
            'thumbnail': video.get('thumbnail', {}).get('url') if video.get('thumbnail') else None,
            'url': f"https://www.youtube.com/watch?v={video.get('videoId')}" if video.get('videoId') else None
        }
        
        return video_data if video_data['video_id'] else None
    
    def _is_recent_video(self, published_text: str, max_days: int = 7) -> bool:
        """Controlla se un video è stato pubblicato di recente"""
        if not published_text or published_text == 'N/A':
            return False
        
        published_lower = published_text.lower()
        
        # Video pubblicati oggi o ieri
        if any(keyword in published_lower for keyword in ['oggi', 'today', 'ieri', 'yesterday']):
            return True
        
        # Video pubblicati nelle ultime ore
        if any(keyword in published_lower for keyword in ['ore fa', 'hours ago', 'hour ago']):
            return True
        
        # Video pubblicati nei giorni scorsi
        if 'giorni fa' in published_lower or 'days ago' in published_lower:
            try:
                # Estrai il numero di giorni
                words = published_lower.split()
                for i, word in enumerate(words):
                    if word.isdigit():
                        days = int(word)
                        return days <= max_days
            except:
                pass
        
        # Video pubblicati nelle settimane scorse (considera solo 1 settimana)
        if 'settimana fa' in published_lower or 'week ago' in published_lower:
            return True
        
        return False
    
    def _filter_relevant_videos(self, videos: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
        """Filtra i video più rilevanti per le notifiche"""
        relevant_videos = []
        
        for video in videos:
            # Salta video già inviati
            if self._is_video_sent(video['video_id']):
                continue
            
            # Controlla rilevanza nel titolo e descrizione
            title_lower = video['title'].lower()
            desc_lower = video['description'].lower()
            keyword_lower = keyword.lower()
            
            # Parole chiave che indicano contenuti rilevanti
            ai_keywords = [
                'ai', 'artificial intelligence', 'intelligenza artificiale',
                'machine learning', 'deep learning', 'neural network',
                'chatgpt', 'gpt', 'llm', 'transformer',
                'coding', 'programming', 'development',
                'tool', 'platform', 'software',
                'editing', 'video editing', 'automation'
            ]
            
            # Controlla se il video contiene parole chiave rilevanti
            relevance_score = 0
            
            # Punteggio per keyword principale nel titolo
            if keyword_lower in title_lower:
                relevance_score += 3
            
            # Punteggio per parole chiave AI
            for ai_keyword in ai_keywords:
                if ai_keyword in title_lower:
                    relevance_score += 2
                if ai_keyword in desc_lower:
                    relevance_score += 1
            
            # Bonus per video recenti (ma non obbligatorio)
            if self._is_recent_video(video['published'], max_days=7):
                relevance_score += 2
            
            # Considera video con punteggio di rilevanza sufficiente
            if relevance_score >= 1:  # Soglia più bassa
                video['relevance_score'] = relevance_score
                relevant_videos.append(video)
        
        # Ordina per punteggio di rilevanza (decrescente)
        relevant_videos.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return relevant_videos
    
    async def search_videos(self, keyword: str, language: str = None, region: str = None, max_results: int = None) -> List[Dict[str, Any]]:
        """Cerca video su YouTube per una specifica parola chiave in una lingua/regione"""
        if max_results is None:
            max_results = Config.MAX_VIDEOS_PER_SEARCH
        
        if language is None:
            language = Config.YOUTUBE_LANGUAGES[0] if Config.YOUTUBE_LANGUAGES else 'it'
        
        if region is None:
            region = Config.YOUTUBE_REGIONS[0] if Config.YOUTUBE_REGIONS else 'IT'
        
        try:
            logger.info(f"Ricerca YouTube per: '{keyword}' (lingua: {language}, regione: {region})")
            
            # Parametri di ricerca
            query_params = {
                'q': keyword,
                'hl': language,
                'gl': region
            }
            
            # Chiamata API
            response = self.api_client.call_api('Youtube/search', query=query_params)
            
            if not response:
                logger.warning(f"Nessuna risposta dall'API per '{keyword}' ({language}/{region})")
                return []
            
            contents = response.get('contents', [])
            logger.info(f"Trovati {len(contents)} risultati per '{keyword}' ({language}/{region})")
            
            # Estrai e filtra i video
            videos = []
            for content in contents[:max_results * 2]:  # Prendi più risultati per filtrare meglio
                video_data = self._parse_video_data(content)
                if video_data:
                    # Aggiungi informazioni sulla lingua/regione
                    video_data['search_language'] = language
                    video_data['search_region'] = region
                    videos.append(video_data)
            
            # Filtra per rilevanza e novità
            relevant_videos = self._filter_relevant_videos(videos, keyword)
            
            logger.info(f"Trovati {len(relevant_videos)} video rilevanti per '{keyword}' ({language}/{region})")
            return relevant_videos[:max_results]
            
        except Exception as e:
            logger.error(f"Errore nella ricerca YouTube per '{keyword}' ({language}/{region}): {e}")
            return []
    
    async def search_all_keywords(self) -> List[Dict[str, Any]]:
        """Cerca video per tutte le parole chiave configurate in tutte le lingue/regioni"""
        all_videos = []
        
        # Calcola il numero totale di ricerche
        total_searches = len(Config.SEARCH_KEYWORDS) * len(Config.YOUTUBE_LANGUAGES) * len(Config.YOUTUBE_REGIONS)
        logger.info(f"Inizio ricerca per {len(Config.SEARCH_KEYWORDS)} parole chiave in {len(Config.YOUTUBE_LANGUAGES)} lingue e {len(Config.YOUTUBE_REGIONS)} regioni (totale: {total_searches} ricerche)")
        
        search_count = 0
        
        for keyword in Config.SEARCH_KEYWORDS:
            keyword = keyword.strip()
            if not keyword:
                continue
            
            # Cerca in tutte le combinazioni lingua/regione
            for language in Config.YOUTUBE_LANGUAGES:
                language = language.strip()
                for region in Config.YOUTUBE_REGIONS:
                    region = region.strip()
                    
                    try:
                        search_count += 1
                        logger.info(f"Ricerca {search_count}/{total_searches}: '{keyword}' ({language}/{region})")
                        
                        videos = await self.search_videos(keyword, language, region)
                        all_videos.extend(videos)
                        
                        # Pausa tra le ricerche per evitare rate limiting
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.error(f"Errore nella ricerca per '{keyword}' ({language}/{region}): {e}")
                        continue
        
        # Rimuovi duplicati basandosi sul video_id
        unique_videos = []
        seen_ids = set()
        
        for video in all_videos:
            if video['video_id'] not in seen_ids:
                unique_videos.append(video)
                seen_ids.add(video['video_id'])
        
        # Ordina per punteggio di rilevanza
        unique_videos.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        logger.info(f"Trovati {len(unique_videos)} video unici da tutte le ricerche multilingua")
        return unique_videos
    
    def mark_video_as_sent(self, video_data: Dict[str, Any]):
        """Marca un video come già inviato"""
        self._add_sent_video(video_data)
    
    def get_sent_videos_count(self) -> int:
        """Restituisce il numero di video già inviati"""
        return len(self.sent_videos.get('videos', []))
    
    def cleanup_old_records(self, days: int = 30):
        """Rimuove i record di video inviati più vecchi di X giorni"""
        if 'videos' not in self.sent_videos:
            return
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        original_count = len(self.sent_videos['videos'])
        self.sent_videos['videos'] = [
            video for video in self.sent_videos['videos']
            if datetime.fromisoformat(video.get('sent_at', '1970-01-01')) > cutoff_date
        ]
        
        removed_count = original_count - len(self.sent_videos['videos'])
        if removed_count > 0:
            self._save_sent_videos()
            logger.info(f"Rimossi {removed_count} record di video vecchi")

# Funzione di test
async def test_youtube_searcher():
    """Funzione di test per il modulo di ricerca"""
    searcher = YouTubeSearcher()
    
    print("🔍 Test YouTube Searcher")
    print("=" * 40)
    
    # Test ricerca singola parola chiave
    results = await searcher.search_videos("intelligenza artificiale", max_results=3)
    
    print(f"\n✅ Trovati {len(results)} video per 'intelligenza artificiale':")
    for i, video in enumerate(results, 1):
        print(f"\n{i}. {video['title'][:60]}...")
        print(f"   📺 {video['channel']}")
        print(f"   📅 {video['published']}")
        print(f"   🔗 {video['url']}")
        print(f"   ⭐ Rilevanza: {video.get('relevance_score', 0)}")

if __name__ == "__main__":
    asyncio.run(test_youtube_searcher())

