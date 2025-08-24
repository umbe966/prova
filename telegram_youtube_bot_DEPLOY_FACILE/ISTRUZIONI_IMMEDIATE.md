# 🚀 Bot Telegram YouTube AI - PRONTO ALL'USO!

## ✅ **Configurazione Completata**

Il tuo bot è **già configurato** e pronto per l'uso con:
- **Token Bot**: `8203686038:AAE2TxfGbuG5x3XhrbF5vHl1D5jllqJ4EKg`
- **Admin ID**: `7101469364`
- **Username Bot**: Cerca il tuo bot su Telegram!

---

## 🧪 **Test Immediato (Locale)**

### 1. Avvia il bot localmente:
```bash
# Estrai l'archivio
tar -xzf telegram_youtube_bot_PRONTO.tar.gz
cd telegram_youtube_bot

# Avvia il bot
python3 main.py
```

### 2. Testa su Telegram:
1. **Cerca il tuo bot** su Telegram (username che hai scelto)
2. **Invia `/start`** - Dovrebbe rispondere immediatamente
3. **Invia `/register`** - Ti registri come utente
4. **Invia `/test`** - Testa la ricerca YouTube

---

## 🌐 **Deploy Online (Railway)**

### Passo 1: Carica su GitHub
```bash
# Nella cartella telegram_youtube_bot
git init
git add .
git commit -m "Bot YouTube AI pronto"

# Crea repository su GitHub e poi:
git remote add origin https://github.com/TUO_USERNAME/telegram-ai-bot.git
git push -u origin main
```

### Passo 2: Deploy su Railway
1. **Vai su**: https://railway.app
2. **Login** con GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Seleziona** il tuo repository
5. **Deploy automatico** - Railway rileva tutto automaticamente!

### Passo 3: Verifica
- Il bot sarà online in 2-3 minuti
- Controlla i log su Railway
- Testa con `/start` su Telegram

---

## 🎯 **Comandi Disponibili**

### Per tutti gli utenti:
- `/start` - Benvenuto e info
- `/register` - Registrati al servizio
- `/settings` - Le tue impostazioni
- `/notifications` - Attiva/disattiva notifiche
- `/help` - Aiuto completo

### Per te (Admin):
- `/admin_stats` - Statistiche utenti
- `/admin_users` - Lista utenti registrati
- `/admin_broadcast Messaggio` - Invia a tutti
- `/test` - Test ricerca YouTube

---

## 📊 **Monitoraggio Web**

Dopo il deploy su Railway, avrai:
- **URL principale**: `https://tuo-app.railway.app/`
- **Stato bot**: `https://tuo-app.railway.app/health`
- **Statistiche**: `https://tuo-app.railway.app/stats`

---

## 🔄 **Keep-Alive Automatico**

Per mantenere il bot sempre attivo:

### 1. UptimeRobot (Gratuito):
1. Vai su: https://uptimerobot.com
2. Crea account gratuito
3. **Add New Monitor**:
   - Type: HTTP(s)
   - URL: `https://tuo-app.railway.app/health`
   - Interval: 5 minutes
4. **Risultato**: Bot sempre online 24/7!

---

## 🎉 **Condivisione Pubblica**

Una volta online:
1. **Trova username bot**: Cerca nelle impostazioni Telegram
2. **Link pubblico**: `https://t.me/TUO_BOT_USERNAME`
3. **Condividi**: Chiunque può registrarsi con `/register`

---

## 🔧 **Personalizzazione**

### Cambia parole chiave:
Modifica nel file `.env`:
```env
SEARCH_KEYWORDS=AI,ChatGPT,machine learning,coding tools
```

### Cambia intervallo ricerca:
```env
SEARCH_INTERVAL_MINUTES=15  # Ogni 15 minuti
```

### Limita utenti:
```env
MAX_USERS=50  # Massimo 50 utenti
```

---

## 🆘 **Risoluzione Problemi**

### "Chat not found":
- **Normale** se non hai mai scritto al bot
- **Soluzione**: Invia `/start` al bot su Telegram

### Bot non risponde:
1. Controlla che sia online (Railway logs)
2. Verifica token bot valido
3. Assicurati di aver fatto `/start`

### Bot si spegne:
1. Configura UptimeRobot (vedi sopra)
2. Controlla ore gratuite Railway (500/mese)

---

## 💰 **Costi**

- **Railway Gratuito**: 500 ore/mese (≈20 giorni)
- **UptimeRobot**: Gratuito per sempre
- **Upgrade Railway**: $5/mese per uso illimitato

---

## 🎯 **Prossimi Passi**

1. ✅ **Testa localmente** (5 min)
2. ✅ **Deploy su Railway** (5 min)
3. ✅ **Configura UptimeRobot** (5 min)
4. ✅ **Condividi il bot** pubblicamente!

**Il tuo bot YouTube AI è pronto per monitorare e notificare automaticamente le novità AI!** 🚀

