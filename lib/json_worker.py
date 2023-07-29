import json
from datetime import datetime
from os import path
from calculate_parser_time import caluculate_diapason
from pytz import timezone
from config import token
import requests


class Json_worker:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._validate_filename()

    def update_json(self, key: str, data: dict) -> None:
        try:
            with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
                py_dict = json.load(json_file)
        except FileNotFoundError:
            self.create_json_file()
            py_dict = {}

        py_dict[key] = data

        with open(path.join('orders', self.filename), 'w', encoding='utf-8') as updated_json_file:
            json.dump(py_dict, updated_json_file, indent=4, ensure_ascii=False)

    def load_to_dump(self) -> None:
        try:
            with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
                py_dict = json.load(json_file)
                return py_dict
        except FileNotFoundError:
            self.create_json_file()
            py_dict = []
            with open(path.join('orders', self.filename), 'w', encoding='utf-8') as updated_json_file:
                json.dump([], updated_json_file, indent=4, ensure_ascii=False)
            with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
                py_dict = json.load(json_file)
                return py_dict

    def dump_dict(self, data: dict) -> None:
        with open(path.join('orders', self.filename), 'w', encoding='utf-8') as updated_json_file:
            json.dump(data, updated_json_file, indent=4, ensure_ascii=False)

    def create_json_file(self) -> None:
        with open(path.join('orders', self.filename), 'w', encoding='utf-8') as new_json_file:
            json.dump({}, new_json_file, ensure_ascii=False)

    def _validate_filename(self) -> None:
        if not self.filename.endswith('.json'):
            self.filename += '.json'

    def price_with_strings(self, price) -> None:
        int_price = ''
        for string in price:
            if string in '0123456789':
                int_price += string
        return int(int_price) if int_price != '' else None

    def years_with_strings(self, string) -> None:
        arr_cr_data = []
        if string is not None:
            if 'лет' in string:
                arr_cr_data = string.split('лет')
            elif 'год' in string:
                arr_cr_data = string.split('год')
        years = ''

        if arr_cr_data != []:
            for register in arr_cr_data[0]:
                if register in '0123456789':
                    years += register
        return years
    
    def send_message_telegram(self, token: str, chat_id: int, filename=None) -> None:
        # requests.post(
        #     f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=test')
        # print('test')
        with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
                py_dict = json.load(json_file)
                for data in py_dict:
                    task_name = '<b>' + py_dict[data]['task_name'] + '</b>'
                    task_price =  py_dict[data]['price']
                    task_description= py_dict[data]['description'][:1000]
                    client_created_acc = py_dict[data]['client_info']['fr_created_acc'] if py_dict[data]['client_info'].get('fr_created_acc') is not None else py_dict[data]['client_info']['fl_created_acc']
                    client_created_acc = self.years_with_strings(client_created_acc)
                    if client_created_acc == '':
                        client_created_acc = '0'
                    feedback = py_dict[data]['client_info']['feedback']
                    client_username_info = 'Нет инфо' if py_dict[data]['client_info'].get('username_info') is None else py_dict[data]['client_info'].get('username_info')
                    client_avatar = ' - с фото' if py_dict[data]['client_info'].get('avatar') == True else ''
                    client_info = '<b>Клиент(лет/отзывов):</b>\n' + client_username_info + client_avatar + ' ' + client_created_acc + '/' + str(feedback)
                    tags_info = '<b>Тэги:</b>\n' + ' '.join(py_dict[data]['technologies'])
                    task_file_add = 'С приложением' if py_dict[data]['file_add'] else ''
                    task_link = py_dict[data]['task_link']
                    button_name = ''
                    if  'fl.ru' in task_link:
                        button_name = 'fl.ru'
                    elif 'freelance.ru' in task_link:
                        button_name = 'freelance.ru'
                    else:
                        button_name = 'freelance.habr.com'
                    rub_price = 0
                    
                    if 'руб' in task_price.lower() or 'Бюджет: ?' in task_price:
                        rub_price = task_price.split('руб') [0] if  'Бюджет: ?' not in task_price else 'Бюджет: 10 000 руб'
                        try:
                            task_price = task_price[:task_price.index('р')] + task_price[task_price.index('С'):] if task_price.count('?') != 2 else task_price
                        except ValueError:
                            task_price = task_price
                        task_price = task_price.replace('ССрок', 'Срок')
                    data = {"chat_id": chat_id,
                        "text": task_name+'\n' + task_price +'\n\n'+task_description+'\n\n' +tags_info +'\n\n'+ client_info+ '\n\n' + task_file_add,
                        "parse_mode": 'html',
                        "reply_markup": json.dumps({"inline_keyboard":[[{"text": button_name,"url": task_link}]]}),
                        "disable_web_page_preview": True
                        }
                    
                    if self.price_with_strings(rub_price) >= 10000:
                        requests.post(f'https://api.telegram.org/bot{token}/sendChatAction?chat_id={chat_id}&action=typing')
                        requests.post(
                            f'https://api.telegram.org/bot{token}/sendMessage', data=data
                        )

    def check_caluclate_parser_time(self, diaposon, sleep_time) -> None:
        zone = 'Europe/Moscow'
        start_diaposon, end_diaposon = caluculate_diapason(sleep_time(timezone(zone)), diaposon)
        data = {}
        with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
            data_json = json.load(json_file)
            for d in data_json:
                fl_true = data_json[d]['fl_true']
                if fl_true:
                    data[d]= data_json[d]
                else:
                    date_published = datetime.strptime(data_json[d]['date_publised'], "%Y-%m-%d %H:%M:%S")
                    # print(start_diaposon.minute, date_published.minute, end_diaposon.minute )
                    if start_diaposon.minute <= date_published.minute < end_diaposon.minute and start_diaposon.hour == date_published.hour:
                        data[d]= data_json[d]
                    elif date_published.minute >= 50 and start_diaposon.hour == date_published.hour:
                        data[d]= data_json[d]
                data_json[d].pop('fl_true', None) 
            self.dump_dict(data)
        
        #Отправка сообщений в telegram
        with open(path.join('orders', 'telegram_chat_id.json'), 'r', encoding='utf-8') as json_file:
                telegram_ids = json.load(json_file)
                for telegram_id in telegram_ids:
                    self.send_message_telegram(token, telegram_id['user_chat_id'], self.filename)