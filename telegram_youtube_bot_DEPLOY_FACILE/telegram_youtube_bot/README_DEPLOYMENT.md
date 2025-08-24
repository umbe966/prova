# 🚀 Bot Telegram YouTube AI Monitor - Deployment Gratuito

Un bot Telegram che monitora automaticamente YouTube per le novità sull'intelligenza artificiale e invia notifiche a più utenti.

## ⚡ Deploy Rapido su Railway (Gratuito)

### 1. Fork questo repository
- Clicca "Fork" in alto a destra
- Crea la tua copia del repository

### 2. Deploy su Railway
1. Vai su [Railway.app](https://railway.app)
2. Registrati con GitHub
3. Clicca "New Project" → "Deploy from GitHub repo"
4. Seleziona il tuo fork del repository
5. Railway farà il deploy automaticamente!

### 3. Configura le variabili ambiente
Nel dashboard Railway, vai su "Variables" e aggiungi:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_IDS=your_telegram_user_id
ALLOW_USER_REGISTRATION=true
MAX_USERS=100
SEARCH_INTERVAL_MINUTES=30
SEARCH_KEYWORDS=intelligenza artificiale,AI tools,machine learning,coding AI,AI platform,video editing AI
YOUTUBE_LANGUAGES=it,en
YOUTUBE_REGIONS=IT,US
MAX_VIDEOS_PER_SEARCH=10
QUIET_HOURS=23:00-07:00
DEBUG_MODE=false
```

### 4. Ottieni il token del bot
1. Apri Telegram e cerca `@BotFather`
2. Invia `/newbot`
3. Scegli nome e username per il bot
4. Copia il token fornito
5. Incollalo in `TELEGRAM_BOT_TOKEN`

### 5. Ottieni il tuo ID Telegram
1. Cerca `@userinfobot` su Telegram
2. Invia `/start`
3. Copia il tuo ID
4. Incollalo in `TELEGRAM_ADMIN_IDS`

## 🎯 Funzionalità

- **Multi-utente**: Supporta registrazione di più utenti
- **Multilingua**: Cerca video in italiano e inglese
- **Notifiche smart**: Filtra contenuti rilevanti sull'AI
- **Comandi admin**: Gestione utenti e broadcast
- **Keep-alive**: Rimane sempre attivo sui servizi gratuiti

## 👥 Comandi Bot

### Utenti:
- `/start` - Benvenuto e registrazione
- `/register` - Registrati al servizio
- `/settings` - Le tue impostazioni
- `/notifications` - Gestisci notifiche

### Admin:
- `/admin_stats` - Statistiche utenti
- `/admin_broadcast` - Messaggio a tutti
- `/admin_users` - Lista utenti

## 🔧 Configurazione Avanzata

### Personalizza parole chiave:
```env
SEARCH_KEYWORDS=AI,machine learning,ChatGPT,coding tools,video editing AI
```

### Cambia lingue di ricerca:
```env
YOUTUBE_LANGUAGES=it,en,fr,es
YOUTUBE_REGIONS=IT,US,FR,ES
```

### Limita utenti:
```env
MAX_USERS=50
ALLOW_USER_REGISTRATION=false
```

## 📊 Monitoraggio

Il bot include un server web per monitoraggio:
- `https://your-app.railway.app/` - Pagina principale
- `https://your-app.railway.app/health` - Stato bot
- `https://your-app.railway.app/stats` - Statistiche

## 🆘 Risoluzione Problemi

### Bot non risponde:
1. Controlla i log su Railway
2. Verifica token bot valido
3. Controlla variabili ambiente

### Bot si spegne:
1. Configura UptimeRobot per ping automatico
2. Verifica di avere ore gratuite disponibili
3. Considera upgrade a Railway Pro

## 💰 Costi

- **Railway Gratuito**: 500 ore/mese (≈20 giorni)
- **Railway Pro**: $5/mese per uso illimitato
- **Render Gratuito**: 750 ore/mese ma si spegne

## 🔗 Link Utili

- [Railway](https://railway.app) - Hosting gratuito
- [UptimeRobot](https://uptimerobot.com) - Keep-alive gratuito
- [BotFather](https://t.me/BotFather) - Crea bot Telegram

---

**Il bot è pronto per essere condiviso pubblicamente!** 🎉

Dopo il deployment, condividi il link del tuo bot: `https://t.me/YOUR_BOT_USERNAME`

