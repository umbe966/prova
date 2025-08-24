"""
Modulo per la gestione degli utenti registrati al bot
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, logger

@dataclass
class User:
    """Classe per rappresentare un utente"""
    user_id: int
    username: str
    first_name: str
    last_name: str
    registered_at: str
    is_active: bool = True
    notifications_enabled: bool = True
    language_preference: str = "it"
    last_activity: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte l'utente in dizionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Crea un utente da dizionario"""
        return cls(**data)

class UserManager:
    """Classe per gestire gli utenti registrati"""
    
    def __init__(self):
        self.users_file = Config.USERS_FILE
        self.users: Dict[int, User] = {}
        self.load_users()
    
    def load_users(self):
        """Carica gli utenti dal file JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Converte i dati in oggetti User
                for user_id_str, user_data in data.get('users', {}).items():
                    user_id = int(user_id_str)
                    self.users[user_id] = User.from_dict(user_data)
                
                logger.info(f"Caricati {len(self.users)} utenti registrati")
            else:
                logger.info("File utenti non trovato, inizializzazione vuota")
                self.save_users()
                
        except Exception as e:
            logger.error(f"Errore nel caricamento utenti: {e}")
            self.users = {}
    
    def save_users(self):
        """Salva gli utenti nel file JSON"""
        try:
            # Assicurati che la directory esista
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            
            # Prepara i dati per il salvataggio
            data = {
                'last_update': datetime.now().isoformat(),
                'total_users': len(self.users),
                'users': {
                    str(user_id): user.to_dict() 
                    for user_id, user in self.users.items()
                }
            }
            
            # Salva nel file
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.debug(f"Salvati {len(self.users)} utenti nel file")
            
        except Exception as e:
            logger.error(f"Errore nel salvataggio utenti: {e}")
    
    def register_user(self, user_id: int, username: str = "", first_name: str = "", 
                     last_name: str = "") -> bool:
        """Registra un nuovo utente"""
        try:
            # Controlla se l'utente è già registrato
            if user_id in self.users:
                logger.info(f"Utente {user_id} già registrato")
                return False
            
            # Controlla il limite massimo di utenti
            if len(self.users) >= Config.MAX_USERS:
                logger.warning(f"Raggiunto limite massimo utenti ({Config.MAX_USERS})")
                return False
            
            # Crea nuovo utente
            new_user = User(
                user_id=user_id,
                username=username or "",
                first_name=first_name or "",
                last_name=last_name or "",
                registered_at=datetime.now().isoformat(),
                last_activity=datetime.now().isoformat()
            )
            
            # Aggiungi alla lista
            self.users[user_id] = new_user
            self.save_users()
            
            logger.info(f"Nuovo utente registrato: {user_id} (@{username})")
            return True
            
        except Exception as e:
            logger.error(f"Errore nella registrazione utente {user_id}: {e}")
            return False
    
    def unregister_user(self, user_id: int) -> bool:
        """Rimuove un utente dalla registrazione"""
        try:
            if user_id in self.users:
                user = self.users[user_id]
                del self.users[user_id]
                self.save_users()
                
                logger.info(f"Utente rimosso: {user_id} (@{user.username})")
                return True
            else:
                logger.warning(f"Tentativo di rimozione utente non registrato: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Errore nella rimozione utente {user_id}: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Ottiene un utente specifico"""
        return self.users.get(user_id)
    
    def is_user_registered(self, user_id: int) -> bool:
        """Controlla se un utente è registrato"""
        return user_id in self.users
    
    def is_admin(self, user_id: int) -> bool:
        """Controlla se un utente è admin"""
        return user_id in Config.TELEGRAM_ADMIN_IDS
    
    def get_all_users(self) -> List[User]:
        """Ottiene tutti gli utenti registrati"""
        return list(self.users.values())
    
    def get_active_users(self) -> List[User]:
        """Ottiene solo gli utenti attivi"""
        return [user for user in self.users.values() if user.is_active]
    
    def get_users_for_notifications(self) -> List[int]:
        """Ottiene gli ID degli utenti che ricevono notifiche"""
        user_ids = []
        
        # Aggiungi utenti registrati con notifiche attive
        for user in self.users.values():
            if user.is_active and user.notifications_enabled:
                user_ids.append(user.user_id)
        
        # Aggiungi admin se non già inclusi
        for admin_id in Config.TELEGRAM_ADMIN_IDS:
            if admin_id not in user_ids:
                user_ids.append(admin_id)
        
        # Aggiungi chat ID legacy se configurato
        if Config.TELEGRAM_CHAT_ID:
            try:
                legacy_id = int(Config.TELEGRAM_CHAT_ID)
                if legacy_id not in user_ids:
                    user_ids.append(legacy_id)
            except (ValueError, TypeError):
                pass
        
        return user_ids
    
    def update_user_activity(self, user_id: int):
        """Aggiorna l'ultima attività dell'utente"""
        if user_id in self.users:
            self.users[user_id].last_activity = datetime.now().isoformat()
            # Salva solo ogni 10 aggiornamenti per performance
            if len(self.users) % 10 == 0:
                self.save_users()
    
    def toggle_user_notifications(self, user_id: int) -> bool:
        """Attiva/disattiva le notifiche per un utente"""
        if user_id in self.users:
            user = self.users[user_id]
            user.notifications_enabled = not user.notifications_enabled
            self.save_users()
            return user.notifications_enabled
        return False
    
    def set_user_active(self, user_id: int, active: bool):
        """Imposta lo stato attivo di un utente"""
        if user_id in self.users:
            self.users[user_id].is_active = active
            self.save_users()
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Ottiene statistiche sugli utenti"""
        total_users = len(self.users)
        active_users = len(self.get_active_users())
        users_with_notifications = len([u for u in self.users.values() 
                                      if u.notifications_enabled and u.is_active])
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'users_with_notifications': users_with_notifications,
            'max_users': Config.MAX_USERS,
            'registration_enabled': Config.ALLOW_USER_REGISTRATION
        }
    
    def cleanup_inactive_users(self, days: int = 90):
        """Rimuove utenti inattivi da più di X giorni"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            inactive_users = []
            for user_id, user in self.users.items():
                try:
                    last_activity = datetime.fromisoformat(user.last_activity)
                    if last_activity < cutoff_date:
                        inactive_users.append(user_id)
                except (ValueError, TypeError):
                    # Se non c'è data di attività valida, considera inattivo
                    inactive_users.append(user_id)
            
            # Rimuovi utenti inattivi (ma non gli admin)
            removed_count = 0
            for user_id in inactive_users:
                if not self.is_admin(user_id):
                    del self.users[user_id]
                    removed_count += 1
            
            if removed_count > 0:
                self.save_users()
                logger.info(f"Rimossi {removed_count} utenti inattivi")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Errore nel cleanup utenti inattivi: {e}")
            return 0

# Istanza globale del manager utenti
user_manager = UserManager()

# Funzioni di test
def test_user_manager():
    """Test del modulo gestione utenti"""
    print("🧪 Test User Manager")
    print("=" * 40)
    
    # Test registrazione
    success = user_manager.register_user(12345, "testuser", "Test", "User")
    print(f"✅ Registrazione utente: {'OK' if success else 'FAIL'}")
    
    # Test verifica registrazione
    is_registered = user_manager.is_user_registered(12345)
    print(f"✅ Verifica registrazione: {'OK' if is_registered else 'FAIL'}")
    
    # Test ottenimento utente
    user = user_manager.get_user(12345)
    print(f"✅ Ottenimento utente: {'OK' if user else 'FAIL'}")
    
    # Test statistiche
    stats = user_manager.get_user_stats()
    print(f"✅ Statistiche: {stats}")
    
    # Test rimozione
    removed = user_manager.unregister_user(12345)
    print(f"✅ Rimozione utente: {'OK' if removed else 'FAIL'}")

if __name__ == "__main__":
    test_user_manager()

