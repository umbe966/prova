#!/usr/bin/env python3
"""
Script di test per il Bot Telegram YouTube AI Monitor
"""

import asyncio
import sys
import os

# Aggiungi il percorso del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config, logger
from src.youtube_searcher import YouTubeSearcher
from src.scheduler import NotificationScheduler

async def test_youtube_api():
    """Test dell'API YouTube"""
    print("🔍 Test API YouTube")
    print("=" * 50)
    
    searcher = YouTubeSearcher()
    
    # Test ricerca in italiano
    print("🇮🇹 Test ricerca in italiano...")
    results_it = await searcher.search_videos("intelligenza artificiale", "it", "IT", max_results=2)
    
    print(f"✅ Trovati {len(results_it)} video italiani:")
    for i, video in enumerate(results_it, 1):
        print(f"\n{i}. {video['title'][:60]}...")
        print(f"   📺 {video['channel']}")
        print(f"   📅 {video['published']}")
        print(f"   🌍 {video.get('search_language', 'N/A')}")
        print(f"   ⭐ Rilevanza: {video.get('relevance_score', 0)}")
    
    # Test ricerca in inglese
    print("\n🇺🇸 Test ricerca in inglese...")
    results_en = await searcher.search_videos("AI tools", "en", "US", max_results=2)
    
    print(f"✅ Trovati {len(results_en)} video inglesi:")
    for i, video in enumerate(results_en, 1):
        print(f"\n{i}. {video['title'][:60]}...")
        print(f"   📺 {video['channel']}")
        print(f"   📅 {video['published']}")
        print(f"   🌍 {video.get('search_language', 'N/A')}")
        print(f"   ⭐ Rilevanza: {video.get('relevance_score', 0)}")
    
    return len(results_it) > 0 or len(results_en) > 0

async def test_scheduler():
    """Test dello scheduler"""
    print("\n🕐 Test Scheduler")
    print("=" * 50)
    
    scheduler = NotificationScheduler()
    
    # Test ricerca immediata
    print("Esecuzione ricerca immediata...")
    await scheduler.run_immediate_search()
    
    # Mostra stato
    status = scheduler.get_scheduler_status()
    print(f"\n📊 Stato scheduler:")
    print(f"   Video inviati: {status['sent_videos_count']}")
    print(f"   Intervallo: {status['search_interval']} minuti")
    print(f"   Ore silenzio: {status['quiet_hours']}")
    
    return True

def test_configuration():
    """Test della configurazione"""
    print("\n⚙️ Test Configurazione")
    print("=" * 50)
    
    print(f"📁 Directory progetto: {Config.PROJECT_ROOT}")
    print(f"🔍 Parole chiave: {len(Config.SEARCH_KEYWORDS)}")
    print(f"⏰ Intervallo ricerca: {Config.SEARCH_INTERVAL_MINUTES} minuti")
    print(f"🌍 Lingue YouTube: {', '.join(Config.YOUTUBE_LANGUAGES)}")
    print(f"🗺️ Regioni YouTube: {', '.join(Config.YOUTUBE_REGIONS)}")
    print(f"📺 Max video per ricerca: {Config.MAX_VIDEOS_PER_SEARCH}")
    print(f"🔇 Ore silenzio: {Config.QUIET_HOURS}")
    print(f"🐛 Debug mode: {Config.DEBUG_MODE}")
    
    # Controlla file necessari
    files_to_check = [
        Config.SENT_VIDEOS_FILE,
        Config.LOG_FILE
    ]
    
    print(f"\n📂 File di sistema:")
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}")
    
    return True

async def test_all():
    """Esegue tutti i test"""
    print("🧪 Test Completo Bot YouTube AI Monitor")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    try:
        # Test configurazione
        if test_configuration():
            tests_passed += 1
            print("✅ Test configurazione: PASSATO")
        else:
            print("❌ Test configurazione: FALLITO")
    except Exception as e:
        print(f"❌ Test configurazione: ERRORE - {e}")
    
    try:
        # Test API YouTube
        if await test_youtube_api():
            tests_passed += 1
            print("✅ Test API YouTube: PASSATO")
        else:
            print("❌ Test API YouTube: FALLITO")
    except Exception as e:
        print(f"❌ Test API YouTube: ERRORE - {e}")
    
    try:
        # Test scheduler
        if await test_scheduler():
            tests_passed += 1
            print("✅ Test scheduler: PASSATO")
        else:
            print("❌ Test scheduler: FALLITO")
    except Exception as e:
        print(f"❌ Test scheduler: ERRORE - {e}")
    
    # Risultato finale
    print(f"\n{'='*60}")
    print(f"🏁 Risultato test: {tests_passed}/{total_tests} passati")
    
    if tests_passed == total_tests:
        print("🎉 Tutti i test sono passati! Il bot è pronto per l'uso.")
        return True
    else:
        print("⚠️ Alcuni test sono falliti. Controlla la configurazione.")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_all())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Errore durante i test: {e}")
        sys.exit(1)

