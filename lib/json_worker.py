import json
from datetime import datetime
from os import path
from calculate_parser_time import caluculate_diapason
from pytz import timezone


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