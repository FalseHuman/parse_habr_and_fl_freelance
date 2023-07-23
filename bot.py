import telebot, logging, time
from lib.json_worker import Json_worker
from config import token

# from config import token

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет  <b>{message.from_user.first_name}!</b> Процесс парсинга запущен', parse_mode='html')
    user_chat_id = {'user_chat_id': message.chat.id}
    users_chat_ids = Json_worker('telegram_chat_id')
    test = users_chat_ids.load_to_dump()
    test.append(user_chat_id)
    # users_chat_ids.save_tg_user_date(user_chat_id)
    users_chat_ids.dump_dict(test)
    



while True:
    try:
        bot.polling(none_stop=True)  # Это нужно чтобы бот работал всё время
    except:
        time.sleep(5)  # если ошибка бот уходит в спящий режим на 5 секунд
