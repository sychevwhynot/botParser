import imaplib
import email
from email.header import decode_header
import time
from telegram import Bot

# Настройки для проверки электронной почты
EMAIL = ''
PASSWORD = ''
IMAP_SERVER = 'imap.mail.ru'
IMAP_PORT = 993

# Настройки для Telegram
TELEGRAM_TOKEN = ''
CHAT_ID = ''

# Функция для подключения к почтовому серверу
def connect_to_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    return mail

# Функция для проверки новых сообщений
def check_new_emails(mail):
    status, messages = mail.search(None, '(UNSEEN)')
    if status != 'OK':
        print("Ошибка поиска писем:", status)
        return []
    email_ids = messages[0].split()
    return email_ids

# Функция для чтения содержимого письма
def read_email(mail, email_id):
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    if status != 'OK':
        print(f"Ошибка чтения письма {email_id}: {status}")
        return None, None
    msg = email.message_from_bytes(msg_data[0][1])
    subject, encoding = decode_header(msg['Subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else 'utf-8')
    from_ = msg.get('From')
    return subject, from_

# Функция для отправки уведомлений в Telegram
def send_telegram_message(bot, chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    otvet = ''
    while True:
        try:
            mail = connect_to_email()
            email_ids = check_new_emails(mail)
            for email_id in email_ids:
                subject, from_ = read_email(mail, email_id)
                if subject and from_:
                    message = f'Новый отзыв 2GIS \nТема: {subject}\nОт кого: {from_}\nОтветить: {otvet}'
                    send_telegram_message(bot, CHAT_ID, message)
            mail.logout()
        except imaplib.IMAP4.abort as e:
            print(f"Соединение с сервером потеряно, повторное подключение через минуту... Ошибка: {e}")
            time.sleep(60)
        except Exception as e:
            print(f"Произошла ошибка 2ГИС: {e}")
            time.sleep(3600)
        time.sleep(3600)  # Проверка почты каждый час

if __name__ == '__main__':
    main()