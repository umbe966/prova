#!/bin/bash
# Script di avvio per Bot Telegram YouTube AI Monitor

set -e

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BOT_DIR/bot.pid"
LOG_FILE="$BOT_DIR/logs/bot.log"

echo "🚀 Avvio Bot Telegram YouTube AI Monitor"
echo "========================================"

# Controlla se il bot è già in esecuzione
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️ Il bot è già in esecuzione (PID: $PID)"
        echo "   Usa ./stop.sh per fermarlo prima"
        exit 1
    else
        echo "🧹 Rimozione file PID obsoleto"
        rm -f "$PID_FILE"
    fi
fi

# Controlla se il file .env esiste
if [ ! -f "$BOT_DIR/.env" ]; then
    echo "❌ File .env non trovato!"
    echo "   Copia config/.env.example in .env e configuralo"
    exit 1
fi

# Controlla se le directory esistono
mkdir -p "$BOT_DIR/data" "$BOT_DIR/logs"

# Avvia il bot in background
echo "🔄 Avvio del bot..."
cd "$BOT_DIR"

nohup python3 main.py > "$LOG_FILE" 2>&1 &
BOT_PID=$!

# Salva il PID
echo $BOT_PID > "$PID_FILE"

# Aspetta un momento per verificare che il bot si sia avviato
sleep 3

if ps -p $BOT_PID > /dev/null 2>&1; then
    echo "✅ Bot avviato con successo!"
    echo "   PID: $BOT_PID"
    echo "   Log: $LOG_FILE"
    echo ""
    echo "📋 Comandi utili:"
    echo "   ./stop.sh           - Ferma il bot"
    echo "   tail -f $LOG_FILE   - Mostra log in tempo reale"
    echo "   python3 test_bot.py - Esegui test"
else
    echo "❌ Errore nell'avvio del bot"
    echo "   Controlla il log: $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi

