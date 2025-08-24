# 🚀 Guida Deployment Gratuito - Bot Telegram YouTube AI

## 🌟 Opzioni di Deployment Gratuito

### 1. Railway (Raccomandato) ⭐
- **500 ore/mese gratis**
- **Facile da usare**
- **Deploy automatico da GitHub**
- **Supporto Python nativo**

### 2. Render
- **750 ore/mese gratis**
- **Si spegne dopo 15 min di inattività**
- **Riavvio automatico**

### 3. Heroku (Non più gratuito)
- **Solo piani a pagamento**

---

## 🚀 Deployment su Railway (Raccomandato)

### Passo 1: Preparazione Repository GitHub

1. **Crea account GitHub** (se non ce l'hai): https://github.com
2. **Crea nuovo repository**:
   - Nome: `telegram-youtube-ai-bot`
   - Pubblico o privato
   - Non aggiungere README, .gitignore, licenza

3. **Carica il bot su GitHub**:
```bash
# Estrai il bot
tar -xzf telegram_youtube_bot_multiuser.tar.gz
cd telegram_youtube_bot

# Inizializza Git
git init
git add .
git commit -m "Initial commit - Telegram YouTube AI Bot"

# Collega a GitHub (sostituisci USERNAME)
git remote add origin https://github.com/USERNAME/telegram-youtube-ai-bot.git
git branch -M main
git push -u origin main
```

### Passo 2: Deploy su Railway

1. **Vai su Railway**: https://railway.app
2. **Registrati** con GitHub
3. **Crea nuovo progetto**:
   - Click "New Project"
   - Seleziona "Deploy from GitHub repo"
   - Scegli il tuo repository `telegram-youtube-ai-bot`

4. **Configura variabili ambiente**:
   - Vai su "Variables" nel dashboard
   - Aggiungi tutte le variabili dal file `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_IDS=your_admin_id_here
ALLOW_USER_REGISTRATION=true
MAX_USERS=100
SEARCH_INTERVAL_MINUTES=30
SEARCH_KEYWORDS=intelligenza artificiale,AI tools,machine learning,coding AI
YOUTUBE_LANGUAGES=it,en
YOUTUBE_REGIONS=IT,US
MAX_VIDEOS_PER_SEARCH=10
QUIET_HOURS=23:00-07:00
DEBUG_MODE=false
```

5. **Deploy automatico**:
   - Railway rileverà automaticamente Python
   - Installerà le dipendenze da `requirements.txt`
   - Avvierà il bot con `python3 main.py`

### Passo 3: Verifica Deployment

1. **Controlla log**:
   - Vai su "Deployments" nel dashboard Railway
   - Clicca sull'ultimo deployment
   - Visualizza i log per verificare che il bot si avvii

2. **Testa il bot**:
   - Invia `/start` al tuo bot Telegram
   - Dovrebbe rispondere immediatamente

---

## 🔄 Deployment su Render (Alternativa)

### Passo 1: Preparazione

1. **Repository GitHub** (stesso del Railway)
2. **Vai su Render**: https://render.com
3. **Registrati** con GitHub

### Passo 2: Crea Web Service

1. **New Web Service**:
   - Connetti repository GitHub
   - Nome: `telegram-youtube-ai-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python3 main.py`

2. **Configura variabili ambiente**:
   - Aggiungi tutte le variabili `.env` nella sezione "Environment"

3. **Deploy**:
   - Render farà il deploy automaticamente
   - Il bot sarà online in pochi minuti

---

## ⚙️ Configurazione Avanzata

### Mantenere il Bot Sempre Attivo

**Problema**: I servizi gratuiti si spengono dopo inattività.

**Soluzione**: Crea un "keep-alive" service:

1. **Aggiungi al main.py**:
```python
# Aggiungi all'inizio del file
from flask import Flask
import threading

# Crea app Flask semplice
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Telegram YouTube AI is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "bot_running": True}

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Nel main(), aggiungi:
if __name__ == "__main__":
    # Avvia Flask in thread separato
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Avvia il bot normalmente
    asyncio.run(main())
```

2. **Aggiungi Flask ai requirements**:
```txt
flask==2.3.3
```

3. **Servizio di ping esterno**:
   - Usa UptimeRobot (gratuito): https://uptimerobot.com
   - Configura ping ogni 5 minuti al tuo URL Railway/Render
   - Questo mantiene il bot sempre attivo

### Monitoraggio e Log

1. **Log su Railway/Render**:
   - Visualizza log in tempo reale dal dashboard
   - Configura alert per errori

2. **Notifiche admin**:
   - Il bot invia notifiche agli admin per errori critici
   - Statistiche giornaliere automatiche

---

## 🔧 Risoluzione Problemi

### Bot non si avvia

1. **Controlla log deployment**
2. **Verifica variabili ambiente**
3. **Controlla token bot valido**

### Bot si spegne spesso

1. **Configura keep-alive** (vedi sopra)
2. **Usa UptimeRobot** per ping automatico
3. **Considera upgrade a piano a pagamento**

### Errori di memoria

1. **Riduci `MAX_VIDEOS_PER_SEARCH`**
2. **Aumenta `SEARCH_INTERVAL_MINUTES`**
3. **Limita `MAX_USERS`**

---

## 💰 Costi e Limiti

### Railway (Gratuito)
- **500 ore/mese** (≈20 giorni)
- **1GB RAM**
- **1GB storage**
- **Upgrade**: $5/mese per uso illimitato

### Render (Gratuito)
- **750 ore/mese** (≈31 giorni)
- **512MB RAM**
- **Si spegne dopo 15 min inattività**
- **Upgrade**: $7/mese per sempre attivo

---

## 🎯 Raccomandazioni

### Per uso personale/test:
- **Railway** con keep-alive
- Sufficiente per 50-100 utenti

### Per uso pubblico serio:
- **Railway Pro** ($5/mese)
- **VPS economico** ($3-5/mese)
- Maggiore affidabilità e controllo

---

## 📞 Supporto

Se hai problemi:
1. Controlla i log del deployment
2. Verifica la configurazione
3. Testa localmente prima
4. Controlla la documentazione Railway/Render

**Il bot è ora pronto per essere lanciato gratuitamente online!** 🚀

