"""
Modulo per la gestione dello scheduling delle ricerche YouTube automatiche
"""

import asyncio
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from typing import Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, logger
from src.youtube_searcher import YouTubeSearcher

class NotificationScheduler:
    """Classe per gestire lo scheduling delle notifiche YouTube AI"""
    
    def __init__(self, telegram_bot=None):
        self.scheduler = AsyncIOScheduler()
        self.telegram_bot = telegram_bot
        self.youtube_searcher = YouTubeSearcher()
        self.is_running = False
        
    def _is_quiet_hours(self) -> bool:
        """Controlla se siamo nelle ore di silenzio"""
        try:
            start_time_str, end_time_str = Config.parse_quiet_hours()
            
            # Converte le stringhe in oggetti time
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            current_time = datetime.now().time()
            
            # Gestisce il caso in cui le ore di silenzio attraversano la mezzanotte
            if start_time <= end_time:
                # Caso normale: 22:00-06:00 non attraversa mezzanotte
                return start_time <= current_time <= end_time
            else:
                # Caso che attraversa mezzanotte: 23:00-07:00
                return current_time >= start_time or current_time <= end_time
                
        except Exception as e:
            logger.error(f"Errore nel controllo ore silenzio: {e}")
            return False
    
    async def search_and_notify(self):
        """Esegue la ricerca YouTube e invia notifiche per nuovi video"""
        try:
            # Controlla se siamo nelle ore di silenzio
            if self._is_quiet_hours():
                logger.info("Ricerca saltata: ore di silenzio attive")
                return
            
            logger.info("Inizio ricerca automatica YouTube...")
            
            # Esegui ricerca per tutte le parole chiave
            new_videos = await self.youtube_searcher.search_all_keywords()
            
            if not new_videos:
                logger.info("Nessun nuovo video trovato")
                return
            
            logger.info(f"Trovati {len(new_videos)} nuovi video da notificare")
            
            # Invia notifiche per i video trovati
            for video in new_videos[:5]:  # Limita a 5 video per volta
                await self._send_video_notification(video)
                
                # Marca il video come inviato
                self.youtube_searcher.mark_video_as_sent(video)
                
                # Pausa tra le notifiche
                await asyncio.sleep(2)
            
            # Cleanup periodico dei record vecchi
            self.youtube_searcher.cleanup_old_records(days=30)
            
            logger.info(f"Ricerca completata: {len(new_videos)} notifiche inviate")
            
        except Exception as e:
            logger.error(f"Errore durante ricerca e notifica: {e}")
    
    async def _send_video_notification(self, video: dict):
        """Invia una notifica per un singolo video"""
        try:
            # Formatta il messaggio di notifica
            message = self._format_video_message(video)
            
            # Invia la notifica tramite il bot Telegram
            if self.telegram_bot:
                success = await self.telegram_bot.send_notification(message)
                if success:
                    logger.info(f"Notifica inviata per: {video['title'][:50]}...")
                else:
                    logger.error(f"Errore nell'invio notifica per: {video['title'][:50]}...")
            else:
                logger.warning("Bot Telegram non configurato per le notifiche")
                
        except Exception as e:
            logger.error(f"Errore nell'invio notifica video: {e}")
    
    def _format_video_message(self, video: dict) -> str:
        """Formatta il messaggio di notifica per un video"""
        # Emoji basati sul punteggio di rilevanza
        relevance_score = video.get('relevance_score', 0)
        if relevance_score >= 6:
            emoji = "🔥"
        elif relevance_score >= 4:
            emoji = "⭐"
        else:
            emoji = "🆕"
        
        # Emoji per la lingua
        language = video.get('search_language', 'unknown')
        if language == 'it':
            lang_emoji = "🇮🇹"
        elif language == 'en':
            lang_emoji = "🇺🇸"
        else:
            lang_emoji = "🌍"
        
        # Formatta il titolo (massimo 80 caratteri)
        title = video.get('title', 'N/A')
        if len(title) > 80:
            title = title[:77] + "..."
        
        # Crea il messaggio
        message = f"""
{emoji} **Nuovo video AI trovato!** {lang_emoji}

**{title}**

📺 **Canale:** {video.get('channel', 'N/A')}
📅 **Pubblicato:** {video.get('published', 'N/A')}
👀 **Visualizzazioni:** {video.get('views', 'N/A')}
⏱️ **Durata:** {video.get('duration', 'N/A')}
🌍 **Lingua:** {language.upper()}
⭐ **Rilevanza:** {relevance_score}/10

🔗 **Guarda ora:** {video.get('url', 'N/A')}

---
🤖 *Bot YouTube AI Monitor*
        """.strip()
        
        return message
    
    def start_scheduler(self):
        """Avvia lo scheduler"""
        if self.is_running:
            logger.warning("Scheduler già in esecuzione")
            return
        
        try:
            # Aggiungi il job di ricerca periodica
            self.scheduler.add_job(
                self.search_and_notify,
                trigger=IntervalTrigger(minutes=Config.SEARCH_INTERVAL_MINUTES),
                id='youtube_search',
                name='Ricerca YouTube AI',
                replace_existing=True,
                max_instances=1  # Evita sovrapposizioni
            )
            
            # Aggiungi job di cleanup giornaliero (alle 3:00)
            self.scheduler.add_job(
                self._daily_cleanup,
                trigger=CronTrigger(hour=3, minute=0),
                id='daily_cleanup',
                name='Cleanup giornaliero',
                replace_existing=True
            )
            
            # Avvia lo scheduler
            self.scheduler.start()
            self.is_running = True
            
            logger.info(f"Scheduler avviato - ricerca ogni {Config.SEARCH_INTERVAL_MINUTES} minuti")
            
        except Exception as e:
            logger.error(f"Errore nell'avvio dello scheduler: {e}")
            raise
    
    def stop_scheduler(self):
        """Ferma lo scheduler"""
        if not self.is_running:
            return
        
        try:
            self.scheduler.shutdown(wait=True)
            self.is_running = False
            logger.info("Scheduler fermato")
        except Exception as e:
            logger.error(f"Errore nel fermare lo scheduler: {e}")
    
    async def _daily_cleanup(self):
        """Cleanup giornaliero dei dati"""
        try:
            logger.info("Esecuzione cleanup giornaliero...")
            
            # Cleanup record video vecchi
            self.youtube_searcher.cleanup_old_records(days=30)
            
            # Log statistiche
            sent_count = self.youtube_searcher.get_sent_videos_count()
            logger.info(f"Cleanup completato - {sent_count} video in archivio")
            
        except Exception as e:
            logger.error(f"Errore durante cleanup giornaliero: {e}")
    
    async def run_immediate_search(self):
        """Esegue una ricerca immediata (per test)"""
        logger.info("Esecuzione ricerca immediata...")
        await self.search_and_notify()
    
    def get_scheduler_status(self) -> dict:
        """Restituisce lo stato dello scheduler"""
        jobs = []
        if self.is_running:
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
        
        return {
            'running': self.is_running,
            'jobs': jobs,
            'quiet_hours': Config.QUIET_HOURS,
            'search_interval': Config.SEARCH_INTERVAL_MINUTES,
            'sent_videos_count': self.youtube_searcher.get_sent_videos_count()
        }

# Funzione di test
async def test_scheduler():
    """Test del modulo scheduler"""
    print("🕐 Test Notification Scheduler")
    print("=" * 40)
    
    scheduler = NotificationScheduler()
    
    # Test ricerca immediata
    await scheduler.run_immediate_search()
    
    # Mostra stato
    status = scheduler.get_scheduler_status()
    print(f"\n📊 Stato scheduler:")
    print(f"   Running: {status['running']}")
    print(f"   Video inviati: {status['sent_videos_count']}")
    print(f"   Intervallo: {status['search_interval']} minuti")

if __name__ == "__main__":
    asyncio.run(test_scheduler())

