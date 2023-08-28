import telebot, logging, time, os
from lib.json_worker import Json_worker
import subprocess
import psutil

processes = []

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')
logging.info('Start bot')

bot = telebot.TeleBot(os.environ.get('token'))

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def start_proccess_parsing(processes, stop=False):
    if len(processes) > 0 or stop:
        for pid in processes:
            kill(pid)
    if not stop:
        p = subprocess.Popen(['python', "main.py"])
        processes.append(p.pid)   

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет  <b>{message.from_user.first_name}!</b> Процесс парсинга запущен. Ознакомится с командами /help', parse_mode='html')
    user_chat_id = {'user_chat_id': message.chat.id}
    users_chat_ids = Json_worker('telegram_chat_id')
    tg_users = users_chat_ids.load_to_dump()
    if user_chat_id not in tg_users: 
        tg_users.append(user_chat_id)
        users_chat_ids.dump_dict(tg_users)
    global processes
    start_proccess_parsing(processes)

@bot.message_handler(commands=['restart_parser'])
def restart_parser(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, парсер перезапущен!')
    global processes
    start_proccess_parsing(processes)

@bot.message_handler(commands=['stop_parser'])
def stop_parser(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, парсер остановлен!')
    global processes
    start_proccess_parsing(processes, True)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/restart_parser - перезапустить парсер.\n/stop_parser - остановить парсер.\n/show_bot_log - получить логи бота и  логи парсера.')


@bot.message_handler(commands=['show_bot_log'])
def show_bot_log(message):
    bot.send_media_group(message.chat.id, [telebot.types.InputMediaDocument(open('bot.log', 'rb')), telebot.types.InputMediaDocument(open('main.log', 'rb'))])


while True:
    try:
        bot.polling(none_stop=True)  # Это нужно чтобы бот работал всё время
    except Exception as e:
        logging.error(e)
        time.sleep(5)  # если ошибка бот уходит в спящий режим на 5 секунд
