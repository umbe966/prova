#!/bin/bash

# Script automatico per caricare il bot su GitHub
# Uso: ./deploy_github.sh TUO_USERNAME_GITHUB

echo "🚀 Script Deploy GitHub - Bot Telegram YouTube AI"
echo "=================================================="

# Controlla se è stato fornito l'username
if [ -z "$1" ]; then
    echo "❌ Errore: Fornisci il tuo username GitHub"
    echo "Uso: ./deploy_github.sh TUO_USERNAME_GITHUB"
    echo "Esempio: ./deploy_github.sh mario_rossi"
    exit 1
fi

USERNAME=$1
REPO_NAME="telegram-youtube-ai-bot"

echo "👤 Username GitHub: $USERNAME"
echo "📁 Repository: $REPO_NAME"
echo ""

# Controlla se git è installato
if ! command -v git &> /dev/null; then
    echo "❌ Git non è installato. Installalo prima di continuare."
    exit 1
fi

# Controlla se siamo nella directory corretta
if [ ! -f "main.py" ]; then
    echo "❌ Errore: Esegui questo script nella cartella telegram_youtube_bot"
    echo "cd telegram_youtube_bot && ./deploy_github.sh $USERNAME"
    exit 1
fi

echo "🔧 Inizializzazione repository Git..."

# Inizializza git se non già fatto
if [ ! -d ".git" ]; then
    git init
    echo "✅ Repository Git inizializzato"
else
    echo "✅ Repository Git già esistente"
fi

# Aggiungi tutti i file
echo "📁 Aggiunta file al repository..."
git add .

# Commit
echo "💾 Creazione commit..."
git commit -m "Bot Telegram YouTube AI - Pronto per deploy su Railway

- Bot multi-utente con registrazione automatica
- Ricerca YouTube in italiano e inglese  
- Notifiche automatiche ogni 30 minuti
- Server Flask integrato per keep-alive
- Comandi admin per gestione utenti
- Configurazione pronta per Railway deploy"

# Configura remote
REPO_URL="https://github.com/$USERNAME/$REPO_NAME.git"
echo "🔗 Configurazione remote: $REPO_URL"

# Rimuovi remote esistente se presente
git remote remove origin 2>/dev/null || true

# Aggiungi nuovo remote
git remote add origin $REPO_URL

# Configura branch main
git branch -M main

echo ""
echo "🎯 PROSSIMI PASSI:"
echo "=================="
echo "1. Vai su GitHub: https://github.com"
echo "2. Crea nuovo repository chiamato: $REPO_NAME"
echo "3. NON aggiungere README, .gitignore o licenza"
echo "4. Torna qui e premi INVIO per continuare..."

read -p "Premi INVIO quando hai creato il repository su GitHub..."

echo ""
echo "📤 Caricamento su GitHub..."

# Push al repository
if git push -u origin main; then
    echo ""
    echo "🎉 SUCCESS! Bot caricato su GitHub!"
    echo "=================================="
    echo "📁 Repository: https://github.com/$USERNAME/$REPO_NAME"
    echo ""
    echo "🚀 PROSSIMO PASSO - DEPLOY SU RAILWAY:"
    echo "1. Vai su: https://railway.app"
    echo "2. Login con GitHub"
    echo "3. 'New Project' → 'Deploy from GitHub repo'"
    echo "4. Seleziona: $USERNAME/$REPO_NAME"
    echo "5. Deploy automatico!"
    echo ""
    echo "⚙️ Ricorda di aggiungere le variabili ambiente su Railway!"
    echo "Controlla il file .env per i valori da copiare."
else
    echo ""
    echo "❌ ERRORE nel caricamento!"
    echo "========================"
    echo "Possibili cause:"
    echo "1. Repository non creato su GitHub"
    echo "2. Nome repository diverso da: $REPO_NAME"
    echo "3. Repository non vuoto (ha README/licenza)"
    echo ""
    echo "🔧 SOLUZIONI:"
    echo "1. Verifica che il repository esista: https://github.com/$USERNAME/$REPO_NAME"
    echo "2. Assicurati che sia completamente vuoto"
    echo "3. Riprova con: ./deploy_github.sh $USERNAME"
fi

echo ""
echo "📞 Serve aiuto? Controlla le istruzioni dettagliate!"

