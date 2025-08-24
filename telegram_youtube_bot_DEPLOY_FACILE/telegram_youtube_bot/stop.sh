#!/bin/bash
# Script di arresto per Bot Telegram YouTube AI Monitor

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BOT_DIR/bot.pid"

echo "🛑 Arresto Bot Telegram YouTube AI Monitor"
echo "========================================="

# Controlla se il file PID esiste
if [ ! -f "$PID_FILE" ]; then
    echo "⚠️ File PID non trovato. Il bot potrebbe non essere in esecuzione."
    
    # Cerca processi Python che potrebbero essere il bot
    PYTHON_PIDS=$(pgrep -f "python3.*main.py" || true)
    if [ -n "$PYTHON_PIDS" ]; then
        echo "🔍 Trovati processi Python che potrebbero essere il bot:"
        ps -p $PYTHON_PIDS -o pid,cmd
        echo ""
        read -p "Vuoi terminarli? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill $PYTHON_PIDS
            echo "✅ Processi terminati"
        fi
    fi
    exit 0
fi

# Leggi il PID
PID=$(cat "$PID_FILE")

# Controlla se il processo è in esecuzione
if ! ps -p $PID > /dev/null 2>&1; then
    echo "⚠️ Il processo con PID $PID non è in esecuzione"
    rm -f "$PID_FILE"
    exit 0
fi

echo "🔄 Arresto del bot (PID: $PID)..."

# Prova prima con SIGTERM (arresto pulito)
kill -TERM $PID

# Aspetta fino a 10 secondi per l'arresto pulito
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "✅ Bot arrestato correttamente"
        rm -f "$PID_FILE"
        exit 0
    fi
    echo "   Attesa arresto... ($i/10)"
    sleep 1
done

# Se non si è fermato, usa SIGKILL
echo "⚠️ Arresto forzato del bot..."
kill -KILL $PID

# Verifica che sia stato terminato
sleep 2
if ! ps -p $PID > /dev/null 2>&1; then
    echo "✅ Bot arrestato forzatamente"
    rm -f "$PID_FILE"
else
    echo "❌ Impossibile arrestare il bot"
    exit 1
fi

