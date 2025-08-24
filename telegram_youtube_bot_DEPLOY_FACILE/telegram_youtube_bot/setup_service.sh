#!/bin/bash
# Script per configurare il bot come servizio systemd

set -e

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="telegram-youtube-bot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "🔧 Configurazione servizio systemd per Bot Telegram YouTube AI"
echo "============================================================="

# Controlla se lo script viene eseguito come root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Questo script deve essere eseguito come root"
    echo "   Usa: sudo ./setup_service.sh"
    exit 1
fi

# Controlla se il file .env esiste
if [ ! -f "$BOT_DIR/.env" ]; then
    echo "❌ File .env non trovato!"
    echo "   Configura prima il bot con ./install.sh"
    exit 1
fi

# Ottieni l'utente che ha eseguito sudo
REAL_USER=${SUDO_USER:-$USER}
REAL_HOME=$(eval echo ~$REAL_USER)

echo "📝 Creazione file di servizio systemd..."

# Crea il file di servizio
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Telegram YouTube AI Monitor Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$REAL_USER
Group=$REAL_USER
WorkingDirectory=$BOT_DIR
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 $BOT_DIR/main.py
ExecStop=/bin/kill -TERM \$MAINPID
Restart=always
RestartSec=10
StandardOutput=append:$BOT_DIR/logs/bot.log
StandardError=append:$BOT_DIR/logs/bot.log

# Limiti di sicurezza
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$BOT_DIR

[Install]
WantedBy=multi-user.target
EOF

echo "✅ File di servizio creato: $SERVICE_FILE"

# Ricarica systemd
echo "🔄 Ricaricamento configurazione systemd..."
systemctl daemon-reload

# Abilita il servizio per l'avvio automatico
echo "🚀 Abilitazione avvio automatico..."
systemctl enable "$SERVICE_NAME"

echo "✅ Servizio configurato con successo!"
echo ""
echo "📋 Comandi per gestire il servizio:"
echo "   sudo systemctl start $SERVICE_NAME     - Avvia il servizio"
echo "   sudo systemctl stop $SERVICE_NAME      - Ferma il servizio"
echo "   sudo systemctl restart $SERVICE_NAME   - Riavvia il servizio"
echo "   sudo systemctl status $SERVICE_NAME    - Stato del servizio"
echo "   sudo systemctl disable $SERVICE_NAME   - Disabilita avvio automatico"
echo ""
echo "📊 Log del servizio:"
echo "   sudo journalctl -u $SERVICE_NAME -f   - Log in tempo reale"
echo "   sudo journalctl -u $SERVICE_NAME       - Tutti i log"
echo ""

# Chiedi se avviare il servizio ora
read -p "Vuoi avviare il servizio ora? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Avvio del servizio..."
    systemctl start "$SERVICE_NAME"
    
    # Aspetta un momento e controlla lo stato
    sleep 3
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "✅ Servizio avviato con successo!"
        systemctl status "$SERVICE_NAME" --no-pager
    else
        echo "❌ Errore nell'avvio del servizio"
        echo "   Controlla i log: sudo journalctl -u $SERVICE_NAME"
    fi
fi

