#!/bin/bash
# Script per configurare cron jobs per il bot

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "⏰ Configurazione Cron Jobs per Bot Telegram YouTube AI"
echo "======================================================"

# Crea script di monitoraggio
MONITOR_SCRIPT="$BOT_DIR/monitor_bot.sh"

echo "📝 Creazione script di monitoraggio..."

cat > "$MONITOR_SCRIPT" << 'EOF'
#!/bin/bash
# Script di monitoraggio per il bot

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BOT_DIR/bot.pid"
LOG_FILE="$BOT_DIR/logs/monitor.log"

# Funzione di log
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Controlla se il bot è in esecuzione
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        log_message "Bot in esecuzione (PID: $PID)"
        exit 0
    else
        log_message "Bot non in esecuzione, riavvio..."
        rm -f "$PID_FILE"
    fi
else
    log_message "File PID non trovato, riavvio bot..."
fi

# Riavvia il bot
cd "$BOT_DIR"
if ./start.sh >> "$LOG_FILE" 2>&1; then
    log_message "Bot riavviato con successo"
else
    log_message "ERRORE: Impossibile riavviare il bot"
fi
EOF

chmod +x "$MONITOR_SCRIPT"
echo "✅ Script di monitoraggio creato: $MONITOR_SCRIPT"

# Crea script di backup
BACKUP_SCRIPT="$BOT_DIR/backup_data.sh"

echo "📝 Creazione script di backup..."

cat > "$BACKUP_SCRIPT" << 'EOF'
#!/bin/bash
# Script di backup per i dati del bot

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$BOT_DIR/backups"
DATE=$(date '+%Y%m%d_%H%M%S')

# Crea directory backup se non esiste
mkdir -p "$BACKUP_DIR"

# Backup dei dati
tar -czf "$BACKUP_DIR/bot_data_$DATE.tar.gz" \
    -C "$BOT_DIR" \
    data/ logs/ .env 2>/dev/null || true

# Mantieni solo gli ultimi 7 backup
find "$BACKUP_DIR" -name "bot_data_*.tar.gz" -type f -mtime +7 -delete

echo "$(date '+%Y-%m-%d %H:%M:%S') - Backup completato: bot_data_$DATE.tar.gz" >> "$BOT_DIR/logs/backup.log"
EOF

chmod +x "$BACKUP_SCRIPT"
echo "✅ Script di backup creato: $BACKUP_SCRIPT"

# Mostra i cron jobs proposti
echo ""
echo "📋 Cron jobs consigliati:"
echo ""
echo "# Monitoraggio bot ogni 5 minuti"
echo "*/5 * * * * $MONITOR_SCRIPT"
echo ""
echo "# Backup giornaliero alle 2:00"
echo "0 2 * * * $BACKUP_SCRIPT"
echo ""
echo "# Riavvio settimanale (domenica alle 3:00)"
echo "0 3 * * 0 $BOT_DIR/stop.sh && sleep 10 && $BOT_DIR/start.sh"
echo ""

# Chiedi se aggiungere i cron jobs
read -p "Vuoi aggiungere questi cron jobs? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⏰ Aggiunta cron jobs..."
    
    # Backup del crontab esistente
    crontab -l > /tmp/crontab_backup_$(date +%s) 2>/dev/null || true
    
    # Aggiungi i nuovi cron jobs
    (crontab -l 2>/dev/null || true; cat << EOF

# Bot Telegram YouTube AI Monitor
# Monitoraggio ogni 5 minuti
*/5 * * * * $MONITOR_SCRIPT
# Backup giornaliero alle 2:00
0 2 * * * $BACKUP_SCRIPT
# Riavvio settimanale domenica alle 3:00
0 3 * * 0 $BOT_DIR/stop.sh && sleep 10 && $BOT_DIR/start.sh
EOF
    ) | crontab -
    
    echo "✅ Cron jobs aggiunti con successo!"
    echo ""
    echo "📋 Cron jobs attivi:"
    crontab -l | grep -E "(monitor_bot|backup_data|telegram_youtube_bot)" || echo "   Nessun cron job trovato"
else
    echo "⏭️ Cron jobs non aggiunti. Puoi configurarli manualmente con:"
    echo "   crontab -e"
fi

echo ""
echo "🎉 Configurazione cron completata!"
echo ""
echo "📁 File creati:"
echo "   $MONITOR_SCRIPT - Script di monitoraggio"
echo "   $BACKUP_SCRIPT - Script di backup"
echo ""
echo "📋 Comandi utili:"
echo "   crontab -l                    - Mostra cron jobs attivi"
echo "   crontab -e                    - Modifica cron jobs"
echo "   tail -f logs/monitor.log      - Log monitoraggio"
echo "   tail -f logs/backup.log       - Log backup"
echo ""

