#!/bin/bash
# Script di installazione per Bot Telegram YouTube AI Monitor

set -e

echo "🚀 Installazione Bot Telegram YouTube AI Monitor"
echo "================================================="

# Controlla se Python 3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✅ Python 3 trovato: $(python3 --version)"

# Controlla se pip è installato
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✅ pip3 trovato"

# Installa le dipendenze Python
echo "📦 Installazione dipendenze Python..."
pip3 install python-telegram-bot apscheduler python-dotenv --upgrade

echo "✅ Dipendenze installate"

# Crea le directory necessarie
echo "📁 Creazione directory..."
mkdir -p data logs

echo "✅ Directory create"

# Copia il file di configurazione se non esiste
if [ ! -f ".env" ]; then
    echo "⚙️ Creazione file di configurazione..."
    cp config/.env.example .env
    echo "✅ File .env creato da .env.example"
    echo ""
    echo "🔧 IMPORTANTE: Modifica il file .env con le tue configurazioni:"
    echo "   - TELEGRAM_BOT_TOKEN (ottieni da @BotFather)"
    echo "   - TELEGRAM_CHAT_ID (il tuo ID chat Telegram)"
    echo ""
else
    echo "✅ File .env già esistente"
fi

# Inizializza il file dei video inviati se non esiste
if [ ! -f "data/sent_videos.json" ]; then
    echo '{"last_update": "", "videos": []}' > data/sent_videos.json
    echo "✅ File sent_videos.json inizializzato"
fi

# Rende eseguibili gli script
chmod +x install.sh
chmod +x start.sh
chmod +x stop.sh
chmod +x main.py
chmod +x test_bot.py

echo "✅ Script resi eseguibili"

# Esegue i test
echo "🧪 Esecuzione test..."
if python3 test_bot.py; then
    echo "✅ Test completati con successo"
else
    echo "⚠️ Alcuni test sono falliti. Controlla la configurazione."
fi

echo ""
echo "🎉 Installazione completata!"
echo ""
echo "📋 Prossimi passi:"
echo "1. Modifica il file .env con le tue configurazioni"
echo "2. Avvia il bot con: ./start.sh"
echo "3. Ferma il bot con: ./stop.sh"
echo ""
echo "📚 Comandi utili:"
echo "   ./start.sh    - Avvia il bot"
echo "   ./stop.sh     - Ferma il bot"
echo "   python3 test_bot.py - Esegui test"
echo "   python3 main.py     - Avvia manualmente"
echo ""

