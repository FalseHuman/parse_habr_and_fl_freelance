import json
from datetime import datetime
from os import path
from calculate_parser_time import caluculate_diapason
from pytz import timezone
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

    def dump_dict(self, data: dict) -> None:
        with open(path.join('orders', self.filename), 'w', encoding='utf-8') as updated_json_file:
            json.dump(data, updated_json_file, indent=4, ensure_ascii=False)

    def create_json_file(self) -> None:
        with open(path.join('orders', self.filename), 'w', encoding='utf-8') as new_json_file:
            json.dump({}, new_json_file, ensure_ascii=False)

    def _validate_filename(self) -> None:
        if not self.filename.endswith('.json'):
            self.filename += '.json'
    
    def send_message_telegram(self, token: str, chat_id: str, filename=None) -> None:
        # requests.post(
        #     f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=test')
        # print('test')
        with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
                py_dict = json.load(json_file)
                for data in py_dict:
                    task_name = '<b>' + py_dict[data]['task_name'] + '</b>'
                    task_description= py_dict[data]['description'][:1000]
                    client_created_acc = py_dict[data]['client_info']['fr_created_acc'] if py_dict[data]['client_info'].get('fr_created_acc') is not None else py_dict[data]['client_info']['fl_created_acc']
                    feedback = py_dict[data]['client_info']['feedback']
                    client_name = 'Нет информации о имени' if py_dict[data]['client_info'].get('client_name') is None else py_dict[data]['client_info'].get('client_name')
                    client_info = '<b>Клиент(лет/отзывов):</b>\n' + client_name + ' ' + client_created_acc + '/' + str(feedback)
                    task_file_add = 'С приложением' if py_dict[data]['file_add'] else 'Без приложения'
                    task_link = py_dict[data]['task_link']
                    data = {"chat_id": chat_id,
                        "text": task_name+'\n\n'+task_description+'\n\n'+ client_info+ '\n\n' + task_file_add,
                        "parse_mode": 'html',
                        "reply_markup": json.dumps({"inline_keyboard":[[{"text":"Перейти","url": task_link}]]})
                        }
                    requests.post(f'https://api.telegram.org/bot{token}/sendChatAction?chat_id={chat_id}&action=typing')
                    requests.post(
                        f'https://api.telegram.org/bot{token}/sendMessage', data=data
                    )

    def check_caluclate_parser_time(self, diaposon) -> None:
        zone = 'Europe/Moscow'
        start_diaposon, end_diaposon = caluculate_diapason(datetime.now(timezone(zone)), diaposon)
        data = {}
        with open(path.join('orders', self.filename), 'r', encoding='utf-8') as json_file:
            data_json = json.load(json_file)
            for d in data_json:
                fl_true = data_json[d]['fl_true']
                if fl_true:
                    data[d]= data_json[d]
                else:
                    date_published = datetime.strptime(data_json[d]['date_publised'], "%Y-%m-%d %H:%M:%S")
                    if start_diaposon.minute <= date_published.minute <=end_diaposon.minute and start_diaposon.hour == date_published.hour:
                        data[d]= data_json[d]
                    elif date_published.minute > 50 and start_diaposon.hour == date_published.hour:
                        data[d]= data_json[d]
                data_json[d].pop('fl_true', None) 
            self.dump_dict(data)
        self.send_message_telegram('6386900425:AAGXK-TufHnCtOscI6T5vijRrBw44wBzLMw', '741541899', self.filename)