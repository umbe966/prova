"""
Bot Telegram principale per le notifiche YouTube AI
"""

import asyncio
import logging
from datetime import datetime
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, logger
from src.user_manager import user_manager

class TelegramBot:
    """Classe principale del bot Telegram"""
    
    def __init__(self):
        self.application = None
        self.is_running = False
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Benvenuto e registrazione"""
        user = update.effective_user
        user_id = user.id
        
        # Aggiorna attività utente se già registrato
        if user_manager.is_user_registered(user_id):
            user_manager.update_user_activity(user_id)
            
            welcome_message = f"""
🤖 **Bentornato, {user.first_name}!**

Il Bot YouTube AI Monitor è attivo e ti sta già inviando notifiche sui nuovi video AI.

**Comandi disponibili:**
/status - Stato del bot e configurazione
/settings - Le tue impostazioni personali
/notifications - Attiva/disattiva notifiche
/test - Esegui una ricerca di test
/help - Aiuto completo

Il bot cerca automaticamente nuovi video ogni {Config.SEARCH_INTERVAL_MINUTES} minuti in italiano 🇮🇹 e inglese 🇺🇸!
            """
        else:
            # Nuovo utente - chiedi registrazione
            if Config.ALLOW_USER_REGISTRATION:
                welcome_message = f"""
🤖 **Benvenuto nel Bot YouTube AI Monitor!**

Ciao {user.first_name}! Questo bot ti terrà aggiornato sulle ultime novità nel mondo dell'intelligenza artificiale.

🔍 **Cosa fa il bot:**
• Cerca automaticamente nuovi video AI su YouTube
• Monitora contenuti in italiano 🇮🇹 e inglese 🇺🇸
• Ti invia notifiche sui video più interessanti
• Filtra contenuti su AI tools, coding, editing e molto altro

**Per iniziare, registrati con il comando:**
/register

**Altri comandi:**
/help - Aiuto completo
/test - Vedi un esempio di ricerca

🚀 Unisciti a {user_manager.get_user_stats()['total_users']} utenti che già ricevono aggiornamenti AI!
                """
            else:
                welcome_message = """
🤖 **Bot YouTube AI Monitor**

Ciao! Al momento le registrazioni sono chiuse.
Contatta un amministratore per maggiori informazioni.

/help - Informazioni sul bot
                """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        logger.info(f"Comando /start ricevuto da {user.username} (ID: {user_id})")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - Mostra stato del bot"""
        status_message = f"""
📊 **Stato Bot YouTube AI Monitor**

🟢 **Bot Status:** Attivo
⏰ **Intervallo ricerca:** {Config.SEARCH_INTERVAL_MINUTES} minuti
🔍 **Parole chiave:** {len(Config.SEARCH_KEYWORDS)} configurate
🌍 **Lingue:** {', '.join(Config.YOUTUBE_LANGUAGES)}
🗺️ **Regioni:** {', '.join(Config.YOUTUBE_REGIONS)}
📺 **Max video per ricerca:** {Config.MAX_VIDEOS_PER_SEARCH}
🔇 **Ore silenzio:** {Config.QUIET_HOURS}

⚙️ **Debug mode:** {'Attivo' if Config.DEBUG_MODE else 'Disattivo'}
📅 **Ultimo aggiornamento:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        await update.message.reply_text(status_message, parse_mode='Markdown')
        logger.info(f"Comando /status ricevuto da {update.effective_user.username}")
    
    async def keywords_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /keywords - Mostra parole chiave di ricerca"""
        keywords_list = "\n".join([f"• {keyword.strip()}" for keyword in Config.SEARCH_KEYWORDS])
        
        keywords_message = f"""
🔍 **Parole chiave monitorate:**

{keywords_list}

Queste parole chiave vengono utilizzate per cercare nuovi video su YouTube.
Il bot cerca contenuti recenti che contengono questi termini.
        """
        
        await update.message.reply_text(keywords_message, parse_mode='Markdown')
        logger.info(f"Comando /keywords ricevuto da {update.effective_user.username}")
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /test - Esegui ricerca di test"""
        await update.message.reply_text("🔍 Eseguendo ricerca di test...")
        
        try:
            # Importa il modulo di ricerca YouTube
            from src.youtube_searcher import YouTubeSearcher
            
            searcher = YouTubeSearcher()
            test_keyword = Config.SEARCH_KEYWORDS[0] if Config.SEARCH_KEYWORDS else "intelligenza artificiale"
            
            results = await searcher.search_videos(test_keyword, max_results=3)
            
            if results:
                test_message = f"✅ **Test completato!**\n\nTrovati {len(results)} video per '{test_keyword}':\n\n"
                
                for i, video in enumerate(results[:3], 1):
                    test_message += f"{i}. **{video.get('title', 'N/A')[:50]}...**\n"
                    test_message += f"   📺 {video.get('channel', 'N/A')}\n"
                    test_message += f"   📅 {video.get('published', 'N/A')}\n\n"
                
                await update.message.reply_text(test_message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Nessun risultato trovato nel test.")
                
        except Exception as e:
            logger.error(f"Errore durante il test: {e}")
            await update.message.reply_text(f"❌ Errore durante il test: {str(e)}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Aiuto e informazioni"""
        help_message = """
🆘 **Aiuto Bot YouTube AI Monitor**

**Cosa fa questo bot:**
Il bot monitora automaticamente YouTube per trovare nuovi video sull'intelligenza artificiale e tecnologie correlate. Ti invia notifiche quando trova contenuti interessanti.

**Comandi disponibili:**
/start - Avvia il bot e mostra il benvenuto
/status - Mostra lo stato attuale del bot
/keywords - Elenca le parole chiave monitorate
/test - Esegue una ricerca di prova
/help - Mostra questo messaggio di aiuto

**Come funziona:**
1. Il bot cerca automaticamente ogni {} minuti
2. Utilizza parole chiave specifiche per l'AI
3. Filtra i video già inviati per evitare duplicati
4. Ti invia notifiche solo per contenuti nuovi e rilevanti

**Supporto:**
Se riscontri problemi, controlla i log del bot o contatta l'amministratore.

**Configurazione:**
Le impostazioni possono essere modificate nel file .env del progetto.
        """.format(Config.SEARCH_INTERVAL_MINUTES)
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
        logger.info(f"Comando /help ricevuto da {update.effective_user.username}")
    
    # Comandi Gestione Utenti
    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /register - Registrazione utente"""
        user = update.effective_user
        user_id = user.id
        
        # Controlla se le registrazioni sono abilitate
        if not Config.ALLOW_USER_REGISTRATION:
            await update.message.reply_text(
                "❌ Le registrazioni sono attualmente disabilitate.",
                parse_mode='Markdown'
            )
            return
        
        # Controlla se l'utente è già registrato
        if user_manager.is_user_registered(user_id):
            await update.message.reply_text(
                "✅ Sei già registrato! Ricevi già le notifiche AI.",
                parse_mode='Markdown'
            )
            return
        
        # Registra l'utente
        success = user_manager.register_user(
            user_id=user_id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
        
        if success:
            # Notifica admin della nuova registrazione
            await self._notify_admins_new_user(user)
            
            message = f"""
✅ **Registrazione completata!**

Benvenuto {user.first_name}! Ora riceverai notifiche automatiche sui nuovi video AI.

**Cosa succede ora:**
• Il bot cerca nuovi video ogni {Config.SEARCH_INTERVAL_MINUTES} minuti
• Riceverai notifiche sui contenuti più interessanti
• Puoi gestire le tue preferenze con /settings

**Comandi utili:**
/notifications - Attiva/disattiva notifiche
/settings - Le tue impostazioni
/help - Aiuto completo

🎉 Benvenuto nella community AI!
            """
        else:
            message = "❌ Errore nella registrazione. Potrebbe essere raggiunto il limite massimo di utenti."
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /register da {user.username} (ID: {user_id}) - {'OK' if success else 'FAIL'}")
    
    async def unregister_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /unregister - Cancellazione utente"""
        user = update.effective_user
        user_id = user.id
        
        if not user_manager.is_user_registered(user_id):
            await update.message.reply_text(
                "❌ Non sei registrato al servizio.",
                parse_mode='Markdown'
            )
            return
        
        # Rimuovi l'utente
        success = user_manager.unregister_user(user_id)
        
        if success:
            message = """
✅ **Cancellazione completata**

Ti sei cancellato dal servizio. Non riceverai più notifiche.

Puoi registrarti nuovamente in qualsiasi momento con /register.

Grazie per aver utilizzato il Bot YouTube AI Monitor! 👋
            """
        else:
            message = "❌ Errore nella cancellazione. Riprova più tardi."
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /unregister da {user.username} (ID: {user_id}) - {'OK' if success else 'FAIL'}")
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /settings - Impostazioni utente"""
        user = update.effective_user
        user_id = user.id
        
        if not user_manager.is_user_registered(user_id):
            await update.message.reply_text(
                "❌ Devi essere registrato per vedere le impostazioni. Usa /register",
                parse_mode='Markdown'
            )
            return
        
        user_data = user_manager.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Errore nel recupero delle impostazioni.")
            return
        
        # Aggiorna attività
        user_manager.update_user_activity(user_id)
        
        message = f"""
⚙️ **Le tue impostazioni**

👤 **Profilo:**
• Nome: {user_data.first_name} {user_data.last_name}
• Username: @{user_data.username}
• Registrato: {user_data.registered_at[:10]}

🔔 **Notifiche:**
• Stato: {'🟢 Attive' if user_data.notifications_enabled else '🔴 Disattivate'}
• Comando: /notifications per cambiare

📊 **Statistiche:**
• Ultima attività: {user_data.last_activity[:10] if user_data.last_activity else 'N/A'}
• Stato account: {'🟢 Attivo' if user_data.is_active else '🔴 Inattivo'}

**Comandi utili:**
/notifications - Gestisci notifiche
/unregister - Cancellati dal servizio
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /settings da {user.username} (ID: {user_id})")
    
    async def notifications_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /notifications - Gestione notifiche"""
        user = update.effective_user
        user_id = user.id
        
        if not user_manager.is_user_registered(user_id):
            await update.message.reply_text(
                "❌ Devi essere registrato per gestire le notifiche. Usa /register",
                parse_mode='Markdown'
            )
            return
        
        # Toggle notifiche
        notifications_enabled = user_manager.toggle_user_notifications(user_id)
        
        status = "🟢 attivate" if notifications_enabled else "🔴 disattivate"
        message = f"""
🔔 **Notifiche {status}**

{'Riceverai' if notifications_enabled else 'Non riceverai più'} notifiche sui nuovi video AI.

Puoi cambiare questa impostazione in qualsiasi momento con /notifications
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /notifications da {user.username} (ID: {user_id}) - {status}")
    
    async def _notify_admins_new_user(self, user):
        """Notifica gli admin di una nuova registrazione"""
        try:
            message = f"""
👤 **Nuovo utente registrato**

• Nome: {user.first_name} {user.last_name or ''}
• Username: @{user.username or 'N/A'}
• ID: `{user.id}`
• Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Totale utenti: {user_manager.get_user_stats()['total_users']}
            """
            
            for admin_id in Config.TELEGRAM_ADMIN_IDS:
                try:
                    await self.application.bot.send_message(
                        chat_id=admin_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.warning(f"Errore notifica admin {admin_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Errore notifica admin nuova registrazione: {e}")
    
    async def unknown_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestisce messaggi non riconosciuti"""
        user_id = update.effective_user.id
        
        # Aggiorna attività se registrato
        if user_manager.is_user_registered(user_id):
            user_manager.update_user_activity(user_id)
        
        message = """
❓ **Comando non riconosciuto**

Usa /help per vedere tutti i comandi disponibili.

**Comandi principali:**
/start - Informazioni e registrazione
/register - Registrati al servizio
/status - Stato del bot
/help - Aiuto completo
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    # Comandi Admin
    async def admin_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /admin_stats - Statistiche per admin"""
        user_id = update.effective_user.id
        
        if not user_manager.is_admin(user_id):
            await update.message.reply_text("❌ Comando riservato agli amministratori.")
            return
        
        stats = user_manager.get_user_stats()
        
        message = f"""
📊 **Statistiche Bot (Admin)**

👥 **Utenti:**
• Totali: {stats['total_users']}/{stats['max_users']}
• Attivi: {stats['active_users']}
• Con notifiche: {stats['users_with_notifications']}

⚙️ **Configurazione:**
• Registrazioni: {'🟢 Aperte' if stats['registration_enabled'] else '🔴 Chiuse'}
• Intervallo ricerca: {Config.SEARCH_INTERVAL_MINUTES} min
• Lingue: {', '.join(Config.YOUTUBE_LANGUAGES)}

**Comandi admin:**
/admin_users - Lista utenti
/admin_broadcast - Messaggio a tutti
/admin_add_user - Aggiungi utente
/admin_remove_user - Rimuovi utente
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /admin_stats da admin {user_id}")
    
    async def admin_users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /admin_users - Lista utenti per admin"""
        user_id = update.effective_user.id
        
        if not user_manager.is_admin(user_id):
            await update.message.reply_text("❌ Comando riservato agli amministratori.")
            return
        
        users = user_manager.get_all_users()
        
        if not users:
            await update.message.reply_text("📭 Nessun utente registrato.")
            return
        
        message = "👥 **Lista Utenti Registrati:**\n\n"
        
        for i, user in enumerate(users[:20], 1):  # Limita a 20 utenti per messaggio
            status = "🟢" if user.is_active else "🔴"
            notifications = "🔔" if user.notifications_enabled else "🔕"
            
            message += f"{i}. {status}{notifications} {user.first_name} (@{user.username})\n"
            message += f"   ID: `{user.user_id}` | {user.registered_at[:10]}\n\n"
        
        if len(users) > 20:
            message += f"... e altri {len(users) - 20} utenti"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /admin_users da admin {user_id}")
    
    async def admin_broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /admin_broadcast - Messaggio a tutti gli utenti"""
        user_id = update.effective_user.id
        
        if not user_manager.is_admin(user_id):
            await update.message.reply_text("❌ Comando riservato agli amministratori.")
            return
        
        # Ottieni il messaggio da inviare
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /admin_broadcast <messaggio>\n\nEsempio: /admin_broadcast Ciao a tutti!"
            )
            return
        
        broadcast_message = " ".join(context.args)
        
        # Invia a tutti gli utenti attivi
        user_ids = user_manager.get_users_for_notifications()
        sent_count = 0
        failed_count = 0
        
        for target_user_id in user_ids:
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📢 **Messaggio dall'amministratore:**\n\n{broadcast_message}",
                    parse_mode='Markdown'
                )
                sent_count += 1
                await asyncio.sleep(0.1)  # Pausa per evitare rate limiting
            except Exception as e:
                failed_count += 1
                logger.warning(f"Errore invio broadcast a {target_user_id}: {e}")
        
        result_message = f"""
📢 **Broadcast completato**

✅ Inviato a: {sent_count} utenti
❌ Falliti: {failed_count} utenti

Messaggio: "{broadcast_message[:100]}{'...' if len(broadcast_message) > 100 else ''}"
        """
        
        await update.message.reply_text(result_message, parse_mode='Markdown')
        logger.info(f"Broadcast da admin {user_id}: {sent_count} inviati, {failed_count} falliti")
        
        response = """
Ciao! 👋 

Sono il bot per monitorare le novità AI su YouTube.
Usa /help per vedere tutti i comandi disponibili.

Il monitoraggio automatico è già attivo! 🚀
        """
        
        await update.message.reply_text(response)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestisce gli errori del bot"""
        logger.error(f"Errore nel bot: {context.error}")
        
        if update and update.message:
            await update.message.reply_text(
                "❌ Si è verificato un errore. Riprova più tardi."
            )
    
    async def send_notification(self, message: str, parse_mode: str = 'Markdown'):
        """Invia una notifica a tutti gli utenti registrati"""
        try:
            if not self.application:
                logger.error("Bot non inizializzato per l'invio notifiche")
                return False
            
            # Ottieni tutti gli utenti che devono ricevere notifiche
            user_ids = user_manager.get_users_for_notifications()
            
            if not user_ids:
                logger.warning("Nessun utente configurato per le notifiche")
                return False
            
            sent_count = 0
            failed_count = 0
            
            for user_id in user_ids:
                try:
                    await self.application.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode=parse_mode
                    )
                    sent_count += 1
                    
                    # Pausa per evitare rate limiting
                    await asyncio.sleep(0.1)
                    
                except TelegramError as e:
                    failed_count += 1
                    logger.warning(f"Errore invio notifica a {user_id}: {e}")
                    
                    # Se l'utente ha bloccato il bot, disattivalo
                    if "blocked" in str(e).lower():
                        user_manager.set_user_active(user_id, False)
                        logger.info(f"Utente {user_id} disattivato (bot bloccato)")
            
            logger.info(f"Notifica inviata: {sent_count} successi, {failed_count} fallimenti")
            return sent_count > 0
            
        except Exception as e:
            logger.error(f"Errore nell'invio notifiche: {e}")
            return False
    
    async def setup_commands(self):
        """Configura i comandi del bot"""
        commands = [
            BotCommand("start", "Avvia il bot"),
            BotCommand("status", "Stato del bot"),
            BotCommand("keywords", "Parole chiave monitorate"),
            BotCommand("test", "Esegui test ricerca"),
            BotCommand("help", "Aiuto e informazioni")
        ]
        
        await self.application.bot.set_my_commands(commands)
        logger.info("Comandi del bot configurati")
    
    async def initialize(self):
        """Inizializza il bot"""
        if not Config.validate_config():
            raise ValueError("Configurazione non valida")
        
        # Crea l'applicazione
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Aggiungi i gestori dei comandi base
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("keywords", self.keywords_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Comandi gestione utenti
        self.application.add_handler(CommandHandler("register", self.register_command))
        self.application.add_handler(CommandHandler("unregister", self.unregister_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        self.application.add_handler(CommandHandler("notifications", self.notifications_command))
        
        # Comandi admin
        self.application.add_handler(CommandHandler("admin_stats", self.admin_stats_command))
        self.application.add_handler(CommandHandler("admin_users", self.admin_users_command))
        self.application.add_handler(CommandHandler("admin_broadcast", self.admin_broadcast_command))
        
        # Gestore per messaggi di testo
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.unknown_message))
        
        # Gestore errori
        self.application.add_error_handler(self.error_handler)
        
        # Configura i comandi
        await self.setup_commands()
        
        logger.info("Bot Telegram inizializzato con successo")
    
    async def start(self):
        """Avvia il bot"""
        if not self.application:
            await self.initialize()
        
        self.is_running = True
        logger.info("Avvio del bot Telegram...")
        
        # Avvia il bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("Bot Telegram avviato e in ascolto")
    
    async def stop(self):
        """Ferma il bot"""
        if self.application and self.is_running:
            self.is_running = False
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("Bot Telegram fermato")

# Funzione principale per testare il bot
async def main():
    """Funzione principale per test"""
    bot = TelegramBot()
    
    try:
        await bot.start()
        
        # Mantieni il bot in esecuzione
        while bot.is_running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Interruzione da tastiera ricevuta")
    except Exception as e:
        logger.error(f"Errore nel bot: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())

