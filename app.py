import telebot
import os
import time
import threading
from flask import Flask

# === CONFIGURAZIONE ===
API_TOKEN = os.environ.get('TELEGRAM_TOKEN')  # Prende il token da Render
if not API_TOKEN:
    raise ValueError("TELEGRAM_TOKEN non trovato! Aggiungilo come Environment Variable su Render.")

bot = telebot.TeleBot(API_TOKEN)

# === FILE ID IMMAGINI ===
ID_FOTO1 = 'AgACAgQAAxkBAAFKD_FqDHJdz1o9gE_ltSClnXWf2LFFngAC-Q1rG7h2aVCdN-PAYCQZQwEAAwIAA3cAAzsE'
ID_FOTO2 = 'AgACAgQAAxkBAAFKEAtqDHM7GV6ZCg_QSU-W44hoZtwa3QAC9g1rG7h2aVC36DG-5I2mAgEAAwIAA3cAAzsE'
ID_FOTO3 = 'AgACAgQAAxkBAAFKEBVqDHN2ByiEIQs--lEDsBGJnW3H3QAC-A1rG7h2aVBOWhamtMY-iAEAAwIAA3cAAzsE'
ID_FOTO4 = 'AgACAgQAAxkBAAFKECZqDHP7NM99_am293dIpHJUxYq-NwACCg5rG34BYVAiJC_oYE5YQgEAAwIAA3cAAzsE'

# === COMANDI DEL BOT ===
@bot.message_handler(commands=['start'])
def invia_guida(message):
    chat_id = message.chat.id
    
    bot.send_message(chat_id, "CIAO! Ti aiuterò a guadagnare il tuo BONUS!")
    
    testo_funzionamento = (
        "Per guadagnare il bonus dovrai iscriverti a BUDDYBANK (la banca online "
        "di Unicredit 100% legit dal loro sito), effettuare una transazione da "
        "minimo 10€ dopo qualche giorno (1-2 sett.) il bonus verrà accreditato sul "
        "tuo conto buddy."
    )
    bot.send_message(chat_id, testo_funzionamento)
    
    bot.send_message(chat_id, "IMPORTANTE:")
    
    testo_codice = (
        "SE NON SI INSERISCE IL CODICE AMICO **B2601MH40CSSN4** durante la procedura "
        "IL BONUS 50€ NON VERRA' ACCREDITATO!"
    )
    bot.send_message(chat_id, testo_codice, parse_mode='Markdown')
    
    bot.send_message(chat_id, "GUIDA step by step per farsi accreditare il bonus:")
    
    # STEP 1
    bot.send_message(chat_id, "STEP 1: ISCRIZIONE")
    bot.send_photo(chat_id, ID_FOTO1, caption="Cerca su Google Buddybank e clicca sul link \"apertura conto Genius Buddy\"")
    bot.send_message(chat_id, "Clicca sul tasto \"APRI CONTO GENIUS BUDDY\"")
    bot.send_photo(chat_id, ID_FOTO2, caption="• Controlla di soddisfare i requisiti")
    bot.send_photo(chat_id, ID_FOTO3, caption="• Prosegui nella registrazione ed INSERISCI IL CODICE AMICO **B2601MH40CSSN4** quando richiesto", parse_mode='Markdown')
    bot.send_message(chat_id, "Inserisci i tuoi dati e prosegui nella fase di IDENTIFICAZIONE scegliendo il tuo metodo di identificazione")
    bot.send_message(chat_id, "PER QUALSIASI PROBLEMA CON L'ISCRIZIONE POTETE SCRIVERE ALL'ASSISTENZA SE INERENTE ALL'APP O A ME SE INERENTE AL BONUS!")
    
    # STEP 2
    bot.send_message(chat_id, "STEP 2: ACCESSO IN APP")
    bot.send_photo(chat_id, ID_FOTO4, caption="Dopo aver effettuato l'accesso dal web SCARICA l'app BUDDYBANK")
    bot.send_message(chat_id, "• Attiva il conto accedendo all'app, puoi trovare il MOBILE CODE nella posta dell'E-mail utilizzata per l'iscrizione e il PIN negli SMS")
    bot.send_message(chat_id, "Collega la carta a Google o Apple Wallet per poter effettuare la transazione di 10€ (vai nella sezione carte e poi in gestione carta per aggiungere la carta)")
    
    # STEP 3
    bot.send_message(chat_id, "STEP 3: RICEZIONE BONUS")
    bot.send_message(chat_id, "Carica 10€ e spendili nelle modalità consentite (NO INVIO DI DENARO A TERZI, GIOCO D'AZZARDO...chiedi ad assistenza in App Buddybank se non le trovi)")
    bot.send_message(chat_id, "• Aspetta che ti arrivi il Bonus!")
    bot.send_message(chat_id, "(1-2 settimane)")

@bot.message_handler(func=lambda message: True)
def risposte_utente(message):
    testo_utente = message.text.strip().lower()
    chat_id = message.chat.id

    if testo_utente in ['fatto', 'fatto!']:
        bot.send_message(
            chat_id, 
            "🎉 Se sei riuscito a completare tutti gli step scrivi in chat \"FATTO!\" Se hai seguito correttamente tutti i passaggi e inserito il codice amico, il tuo bonus verrà accreditato entro 1-2 settimane direttamente sul tuo conto!"
        )
    elif testo_utente == 'aiuto':
        bot.send_message(
            chat_id, 
            "⚠️ SE HAI PROBLEMI CON LA PROCEDURA DI ISCRIZIONE SCRIVI \"AIUTO\" in chat e un OPERATORE UMANO TI RISPONDERA' A BREVE!"
        )
        bot.send_message(
            chat_id,
            "💬 Nel frattempo, descrivi pure qui sotto il tuo problema in modo dettagliato, così l'operatore saprà già come aiutarti appena legge!"
        )
    else:
        bot.reply_to(
            message, 
            "Se hai completato la procedura scrivi *FATTO!*, se invece hai riscontrato problemi scrivi *AIUTO*.",
            parse_mode='Markdown'
        )

# === SERVER FLASK PER TENERE IL BOT ATTIVO ===
app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health_check():
    return "Bot is running!", 200

# === AVVIO DEL BOT IN UN THREAD SEPARATO ===
def run_bot():
    print("🤖 Bot avviato!")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"❌ Errore: {e}")
            time.sleep(15)

if __name__ == '__main__':
    # Avvia il bot in un thread separato
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Avvia il server Flask per Render
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Flask server in ascolto sulla porta {port}")
    app.run(host='0.0.0.0', port=port)