#!/usr/bin/env python3
"""
Bot Telegram YouTube AI Monitor - File principale
Monitora automaticamente YouTube per novità sull'intelligenza artificiale
"""

import asyncio
import signal
import sys
import os
import threading
from flask import Flask, jsonify

# Aggiungi il percorso del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config, logger
from src.bot import TelegramBot
from src.scheduler import NotificationScheduler

# Flask app per keep-alive sui servizi cloud gratuiti
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>🤖 Bot Telegram YouTube AI Monitor</h1>
    <p>Il bot è attivo e funzionante!</p>
    <p><a href="/health">Controlla stato</a></p>
    <p><a href="/stats">Statistiche</a></p>
    """

@app.route('/health')
def health():
    """Endpoint per controllo stato bot"""
    try:
        from src.user_manager import user_manager
        stats = user_manager.get_user_stats()
        
        return jsonify({
            "status": "healthy",
            "bot_running": True,
            "total_users": stats.get('total_users', 0),
            "active_users": stats.get('active_users', 0),
            "timestamp": str(asyncio.get_event_loop().time()) if asyncio.get_event_loop().is_running() else "N/A"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "bot_running": False
        }), 500

@app.route('/stats')
def stats():
    """Endpoint per statistiche dettagliate"""
    try:
        from src.user_manager import user_manager
        stats = user_manager.get_user_stats()
        
        return jsonify({
            "bot_stats": stats,
            "config": {
                "search_interval": Config.SEARCH_INTERVAL_MINUTES,
                "languages": Config.YOUTUBE_LANGUAGES,
                "regions": Config.YOUTUBE_REGIONS,
                "max_users": Config.MAX_USERS,
                "registration_enabled": Config.ALLOW_USER_REGISTRATION
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask():
    """Avvia il server Flask in thread separato"""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

class YouTubeAIBot:
    """Classe principale che coordina bot Telegram e scheduler"""
    
    def __init__(self):
        self.telegram_bot = None
        self.scheduler = None
        self.is_running = False
        
    async def initialize(self):
        """Inizializza tutti i componenti del bot"""
        try:
            logger.info("Inizializzazione Bot YouTube AI Monitor...")
            
            # Valida la configurazione
            if not Config.validate_config():
                raise ValueError("Configurazione non valida. Controlla il file .env")
            
            # Inizializza il bot Telegram
            self.telegram_bot = TelegramBot()
            await self.telegram_bot.initialize()
            
            # Inizializza lo scheduler con riferimento al bot
            self.scheduler = NotificationScheduler(telegram_bot=self.telegram_bot)
            
            logger.info("Inizializzazione completata con successo")
            
        except Exception as e:
            logger.error(f"Errore durante l'inizializzazione: {e}")
            raise
    
    async def start(self):
        """Avvia il bot e tutti i suoi componenti"""
        if self.is_running:
            logger.warning("Bot già in esecuzione")
            return
        
        try:
            logger.info("Avvio Bot YouTube AI Monitor...")
            
            # Avvia il bot Telegram
            await self.telegram_bot.start()
            
            # Avvia lo scheduler
            self.scheduler.start_scheduler()
            
            # Invia messaggio di avvio
            await self._send_startup_message()
            
            self.is_running = True
            logger.info("🚀 Bot YouTube AI Monitor avviato con successo!")
            
            # Esegui una ricerca iniziale dopo 30 secondi
            await asyncio.sleep(30)
            await self.scheduler.run_immediate_search()
            
        except Exception as e:
            logger.error(f"Errore durante l'avvio: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Ferma il bot e tutti i suoi componenti"""
        if not self.is_running:
            return
        
        try:
            logger.info("Arresto Bot YouTube AI Monitor...")
            
            # Invia messaggio di arresto
            await self._send_shutdown_message()
            
            # Ferma lo scheduler
            if self.scheduler:
                self.scheduler.stop_scheduler()
            
            # Ferma il bot Telegram
            if self.telegram_bot:
                await self.telegram_bot.stop()
            
            self.is_running = False
            logger.info("Bot YouTube AI Monitor arrestato")
            
        except Exception as e:
            logger.error(f"Errore durante l'arresto: {e}")
    
    async def _send_startup_message(self):
        """Invia messaggio di avvio"""
        try:
            startup_message = f"""
🚀 **Bot YouTube AI Monitor avviato!**

Il bot è ora attivo e monitorerà YouTube per le novità sull'intelligenza artificiale.

⚙️ **Configurazione:**
• Ricerca ogni {Config.SEARCH_INTERVAL_MINUTES} minuti
• {len(Config.SEARCH_KEYWORDS)} parole chiave monitorate
• Ore silenzio: {Config.QUIET_HOURS}

Usa /help per vedere tutti i comandi disponibili.

🔍 Prima ricerca in corso...
            """.strip()
            
            await self.telegram_bot.send_notification(startup_message)
            
        except Exception as e:
            logger.error(f"Errore nell'invio messaggio di avvio: {e}")
    
    async def _send_shutdown_message(self):
        """Invia messaggio di arresto"""
        try:
            shutdown_message = """
🛑 **Bot YouTube AI Monitor in arresto**

Il bot si sta spegnendo. Riavvialo per continuare il monitoraggio.

Grazie per aver utilizzato il servizio! 👋
            """.strip()
            
            await self.telegram_bot.send_notification(shutdown_message)
            
        except Exception as e:
            logger.error(f"Errore nell'invio messaggio di arresto: {e}")
    
    async def run_forever(self):
        """Mantiene il bot in esecuzione indefinitamente"""
        try:
            while self.is_running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Ricevuto segnale di cancellazione")
        except Exception as e:
            logger.error(f"Errore nel loop principale: {e}")
        finally:
            await self.stop()

# Gestione segnali per arresto pulito
def signal_handler(bot_instance):
    """Gestore per i segnali di sistema"""
    def handler(signum, frame):
        logger.info(f"Ricevuto segnale {signum}, arresto in corso...")
        asyncio.create_task(bot_instance.stop())
    return handler

async def main():
    """Funzione principale"""
    bot = None
    
    try:
        # Avvia Flask in thread separato per keep-alive
        logger.info("Avvio server Flask per keep-alive...")
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Crea l'istanza del bot
        bot = YouTubeAIBot()
        
        # Configura gestione segnali
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler(bot))
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, signal_handler(bot))
        
        # Inizializza e avvia il bot
        await bot.initialize()
        await bot.start()
        
        logger.info("🚀 Bot e server Flask avviati con successo!")
        logger.info(f"🌐 Server accessibile su porta {os.environ.get('PORT', 8080)}")
        
        # Mantieni il bot in esecuzione
        await bot.run_forever()
        
    except KeyboardInterrupt:
        logger.info("Interruzione da tastiera ricevuta")
    except Exception as e:
        logger.error(f"Errore critico: {e}")
        sys.exit(1)
    finally:
        if bot:
            await bot.stop()

if __name__ == "__main__":
    # Configura il loop degli eventi per Windows se necessario
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Avvia il bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Arresto forzato del bot")
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        sys.exit(1)

