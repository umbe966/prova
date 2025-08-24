# Bot Telegram YouTube AI Monitor

Un bot Telegram che monitora automaticamente YouTube per le novità sull'intelligenza artificiale, nuovi tool, piattaforme per coding ed editing, inviando notifiche costanti.

## 🚀 Caratteristiche

- **Monitoraggio automatico**: Cerca nuovi video su YouTube ogni 30 minuti (configurabile)
- **Supporto multilingua**: Ricerca video in italiano e inglese simultaneamente
- **Filtri intelligenti**: Identifica contenuti rilevanti sull'AI e tecnologie correlate
- **Anti-duplicati**: Non invia mai lo stesso video due volte
- **Ore di silenzio**: Configura quando non ricevere notifiche
- **Comandi interattivi**: Controlla il bot tramite comandi Telegram
- **Logging completo**: Traccia tutte le attività per debugging

## 📋 Requisiti

- Python 3.9 o superiore
- Account Telegram
- Accesso all'API YouTube (tramite Manus API Hub)

## 🛠️ Installazione

### 1. Clona o scarica il progetto

```bash
git clone <repository-url>
cd telegram_youtube_bot
```

### 2. Esegui l'installazione automatica

```bash
chmod +x install.sh
./install.sh
```

### 3. Crea un bot Telegram

1. Apri Telegram e cerca `@BotFather`
2. Invia `/newbot` e segui le istruzioni
3. Scegli un nome (es. "AI News Monitor")
4. Scegli un username che finisca con "bot" (es. "ai_news_monitor_bot")
5. Copia il token fornito da BotFather

### 4. Ottieni il tuo Chat ID

1. Invia un messaggio al tuo bot
2. Visita: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Cerca il campo `"chat":{"id":123456789}` e copia l'ID

### 5. Configura il bot

Modifica il file `.env`:

```bash
nano .env
```

Inserisci le tue configurazioni:

```env
# Token del bot Telegram (ottenuto da @BotFather)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# ID chat Telegram dove inviare le notifiche
TELEGRAM_CHAT_ID=123456789

# Intervallo di ricerca in minuti (default: 30 minuti)
SEARCH_INTERVAL_MINUTES=30

# Parole chiave per la ricerca YouTube (separate da virgola)
SEARCH_KEYWORDS=intelligenza artificiale,AI tools,machine learning,coding AI,AI platform,video editing AI,AI development,artificial intelligence 2024,neural networks,deep learning,strumenti AI,piattaforme AI,editing video AI,sviluppo AI

# Lingue per la ricerca YouTube (separate da virgola: it,en per italiano e inglese)
YOUTUBE_LANGUAGES=it,en

# Regioni per la ricerca YouTube (separate da virgola: IT,US per Italia e USA)
YOUTUBE_REGIONS=IT,US

# Numero massimo di video da controllare per ricerca per lingua
MAX_VIDEOS_PER_SEARCH=10

# Ore di silenzio (formato: HH:MM-HH:MM, esempio: 23:00-07:00)
QUIET_HOURS=23:00-07:00

# Abilitare logging debug (true/false)
DEBUG_MODE=false
```

## 🎮 Utilizzo

### Avvio del bot

```bash
./start.sh
```

### Arresto del bot

```bash
./stop.sh
```

### Test del bot

```bash
python3 test_bot.py
```

### Visualizzazione log in tempo reale

```bash
tail -f logs/bot.log
```

## 🤖 Comandi Telegram

Una volta avviato il bot, puoi utilizzare questi comandi:

- `/start` - Mostra messaggio di benvenuto
- `/status` - Stato del bot e configurazione
- `/keywords` - Mostra parole chiave monitorate
- `/test` - Esegui una ricerca di test
- `/help` - Aiuto e informazioni

## 📁 Struttura del progetto

```
telegram_youtube_bot/
├── config/
│   ├── settings.py          # Configurazioni del bot
│   └── .env.example         # Template configurazione
├── src/
│   ├── bot.py              # Bot Telegram principale
│   ├── youtube_searcher.py # Modulo ricerca YouTube
│   └── scheduler.py        # Sistema di scheduling
├── data/
│   └── sent_videos.json    # Database video già inviati
├── logs/
│   └── bot.log            # File di log
├── main.py                # File principale
├── test_bot.py           # Script di test
├── install.sh            # Script di installazione
├── start.sh              # Script di avvio
├── stop.sh               # Script di arresto
└── README.md             # Questa documentazione
```

## ⚙️ Configurazione avanzata

### Personalizzazione parole chiave

Modifica `SEARCH_KEYWORDS` nel file `.env` per aggiungere o rimuovere parole chiave:

```env
SEARCH_KEYWORDS=AI,machine learning,deep learning,neural networks,chatgpt,coding tools,AI platform,video editing AI,intelligenza artificiale,strumenti AI
```

### Configurazione lingue e regioni

Configura le lingue e regioni di ricerca:

```env
YOUTUBE_LANGUAGES=it,en,fr    # Italiano, inglese, francese
YOUTUBE_REGIONS=IT,US,FR      # Italia, USA, Francia
```

### Modifica intervallo di ricerca

Cambia `SEARCH_INTERVAL_MINUTES` per ricerche più o meno frequenti:

```env
SEARCH_INTERVAL_MINUTES=15  # Ricerca ogni 15 minuti
```

### Ore di silenzio

Configura quando non ricevere notifiche:

```env
QUIET_HOURS=22:00-08:00  # Silenzio dalle 22:00 alle 08:00
```

## 🔧 Risoluzione problemi

### Il bot non si avvia

1. Controlla che il file `.env` sia configurato correttamente
2. Verifica che il token Telegram sia valido
3. Controlla i log: `tail -f logs/bot.log`

### Non ricevo notifiche

1. Verifica che il `TELEGRAM_CHAT_ID` sia corretto
2. Controlla se sei nelle ore di silenzio
3. Esegui `/test` per verificare la ricerca

### Errori di connessione

1. Verifica la connessione internet
2. Controlla che l'API YouTube sia accessibile
3. Riavvia il bot: `./stop.sh && ./start.sh`

## 📊 Monitoraggio

### Visualizzare statistiche

Usa il comando `/status` nel bot per vedere:
- Stato del bot
- Numero di video già inviati
- Configurazione attuale
- Prossima ricerca programmata

### Log dettagliati

I log sono salvati in `logs/bot.log` e includono:
- Ricerche eseguite
- Video trovati e inviati
- Errori e warning
- Statistiche di utilizzo

## 🔄 Aggiornamenti

Per aggiornare il bot:

1. Ferma il bot: `./stop.sh`
2. Aggiorna i file del progetto
3. Riavvia: `./start.sh`

## 🐛 Debug

Per abilitare il debug dettagliato:

```env
DEBUG_MODE=true
```

Questo mostrerà informazioni aggiuntive nei log.

## 📝 Note

- Il bot mantiene un database locale dei video già inviati per evitare duplicati
- I record vengono puliti automaticamente dopo 30 giorni
- Il bot rispetta le ore di silenzio configurate
- Ogni ricerca è limitata a un numero massimo di video per evitare spam

## 🆘 Supporto

Se riscontri problemi:

1. Controlla i log: `tail -f logs/bot.log`
2. Esegui i test: `python3 test_bot.py`
3. Verifica la configurazione nel file `.env`
4. Riavvia il bot: `./stop.sh && ./start.sh`

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file LICENSE per i dettagli.

