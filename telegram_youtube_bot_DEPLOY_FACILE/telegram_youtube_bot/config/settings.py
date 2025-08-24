"""
Modulo di configurazione per il bot Telegram YouTube AI
"""

import os
from dotenv import load_dotenv
from typing import List, Tuple
import logging

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class Config:
    """Classe per gestire tutte le configurazioni del bot"""
    
    # Configurazioni Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Chat ID singolo (compatibilità)
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Admin IDs (per gestione bot)
    admin_ids_str = os.getenv('TELEGRAM_ADMIN_IDS', '')
    TELEGRAM_ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip().isdigit()]
    
    # Se non ci sono admin configurati, usa il chat ID come admin
    if not TELEGRAM_ADMIN_IDS and TELEGRAM_CHAT_ID:
        try:
            TELEGRAM_ADMIN_IDS = [int(TELEGRAM_CHAT_ID)]
        except (ValueError, TypeError):
            TELEGRAM_ADMIN_IDS = []
    
    # Configurazioni multi-utente
    ALLOW_USER_REGISTRATION = os.getenv('ALLOW_USER_REGISTRATION', 'true').lower() == 'true'
    MAX_USERS = int(os.getenv('MAX_USERS', 100))
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')  # Canale pubblico opzionale
    
    # Configurazioni ricerca YouTube
    SEARCH_INTERVAL_MINUTES = int(os.getenv('SEARCH_INTERVAL_MINUTES', 30))
    SEARCH_KEYWORDS = os.getenv('SEARCH_KEYWORDS', 
        'intelligenza artificiale,AI tools,machine learning,coding AI').split(',')
    YOUTUBE_LANGUAGES = os.getenv('YOUTUBE_LANGUAGES', 'it,en').split(',')
    YOUTUBE_REGIONS = os.getenv('YOUTUBE_REGIONS', 'IT,US').split(',')
    MAX_VIDEOS_PER_SEARCH = int(os.getenv('MAX_VIDEOS_PER_SEARCH', 10))
    
    # Configurazioni comportamento
    QUIET_HOURS = os.getenv('QUIET_HOURS', '23:00-07:00')
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
       # Percorsi file
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
    
    SENT_VIDEOS_FILE = os.path.join(DATA_DIR, 'sent_videos.json')
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    LOG_FILE = os.path.join(LOG_DIR, 'bot.log')    
    @classmethod
    def validate_config(cls) -> bool:
        """Valida la configurazione e restituisce True se tutto è OK"""
        errors = []
        
        if not cls.TELEGRAM_BOT_TOKEN or cls.TELEGRAM_BOT_TOKEN == 'your_bot_token_here':
            errors.append("TELEGRAM_BOT_TOKEN non configurato")
        
        if not cls.TELEGRAM_CHAT_ID or cls.TELEGRAM_CHAT_ID == 'your_chat_id_here':
            errors.append("TELEGRAM_CHAT_ID non configurato")
        
        if cls.SEARCH_INTERVAL_MINUTES < 1:
            errors.append("SEARCH_INTERVAL_MINUTES deve essere almeno 1")
        
        if not cls.SEARCH_KEYWORDS:
            errors.append("SEARCH_KEYWORDS non può essere vuoto")
        
        if errors:
            print("❌ Errori di configurazione:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        return True
    
    @classmethod
    def parse_quiet_hours(cls) -> Tuple[str, str]:
        """Analizza le ore di silenzio e restituisce (ora_inizio, ora_fine)"""
        try:
            start_time, end_time = cls.QUIET_HOURS.split('-')
            return start_time.strip(), end_time.strip()
        except ValueError:
            return "23:00", "07:00"  # Default
    
    @classmethod
    def setup_logging(cls):
        """Configura il sistema di logging"""
        # Crea la directory logs se non esiste
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        
        # Configura il logging
        log_level = logging.DEBUG if cls.DEBUG_MODE else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Riduci il livello di logging per le librerie esterne
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('telegram').setLevel(logging.WARNING)
        
        return logging.getLogger(__name__)

# Inizializza il logger
logger = Config.setup_logging()

