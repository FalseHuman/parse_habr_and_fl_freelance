import asyncio
import datetime
import time
import json

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse #python-dateutil

from lib.validate_url import Validation
from lib.pagination import Pagination
from lib.json_worker import Json_worker
from lib.req import get_response
from fl_parser import fl_parser_link


class Parser():
    def __init__(self, url: str, filter_url: str = '', diapason: int = 10) -> None:
        self.url = url
        self.filter_url = filter_url
        self.ready_orders_dict = {}
        self.diapason = diapason
        self.pag = Pagination(self.url, self.filter_url)

        super().__init__()

        # self._main(self.diapason)

    def _main(self, diaposon) -> None:
        Validation(self.url)
        ready_dict = self._parse()
        json_result = Json_worker('result')
        json_result.dump_dict(ready_dict)
        json_result.check_caluclate_parser_time(diaposon)

    def _parse(self) -> None:
        counter = 0
        ready_dict = {}
        url_client = 'https://freelance.habr.com'

        for resp in self.pag.pagination_pages:
            temp_parser = BeautifulSoup(resp.text, 'html.parser')
            default_avatar = 'https://freelance.habr.com/assets/default/users/avatar_r100-510ec240a9384f321c7075c46962f4fad15dd58cd22cd41d7f1ca9b2e1732c00.png'
            orders = temp_parser.find_all('li', class_=['content-list__item', 'content-list__item content-list__item_marked'])

            for order in orders:
                date_published_str = order.findAll('span', class_='params__published-at icon_task_publish_at')[0].text
                description = []
                if 'минут' in date_published_str:
                    task = order.findAll('a')[0].text
                    task_link = url_client + order.findAll('a')[0]['href']
                    price = order.findAll('span', class_=['count', 'negotiated_price'])[0].text
                    # order_responses = order.findAll('span', class_='params__responses icon_task_responses')[0].text if order.findAll('span', class_='params__responses icon_task_responses') else '0 откликов'
                    technologies = list(map(lambda t: t.text, order.findAll('a', class_='tags__item_link')))
                    task_page  =  BeautifulSoup(get_response(task_link).text, 'html.parser')
                    description = task_page.find_all('div', class_='task__description')[0].text.replace('\n', ' ') if task_page.find_all('div', class_='task__description') else ''
                    meta_tags = ' '.join(task_page.find_all('div', class_='task__meta')[0].text.replace('\n', ' ').split())
                    avatar = url_client + task_page.find('img', class_='avatario')['src'] if 'https' not in task_page.find('img', class_='avatario')['src'] else task_page.find('img', class_='avatario')['src']
                    true_avatar = False if avatar == default_avatar else True
                    username = task_page.find_all('div', class_='fullname')[0]
                    username_link = url_client + username.find_all('a')[0]['href']
                    username_info = task_page.find_all('div', class_='specialization')[0].text \
                                     + task_page.find_all('div', class_='meta')[0].text
                    verification = True if task_page.find('span', 'verified') else False
                    static_emploer = task_page.find_all('div', 'row')
                    active_emploer = static_emploer[1].find('div', class_='value').text
                    find_freelance = static_emploer[2].find('div', class_='value').text
                    arbitage_emploer = static_emploer[3].find('div', class_='value').text.replace(' ', '').replace('\n', '')
                    feedback = int(static_emploer[4].find('div', class_='value').text.split('/')[0]) - int(static_emploer[4].find('div', class_='value').text.split('/')[1])
                    
                    file_add =  True if task_page.find_all('dl', class_='user-params') else False
                    date_published = parse(meta_tags.split('•')[0].split(',')[1])

                    counter += 1

                    ready_order = {
                        'task_name': task,
                        'task_link': task_link,
                        'description': description,
                        'fl_true': False,
                        'price': price,
                        'date_publised': str(date_published),
                        'date_published_str': date_published_str,
                        'technologies': technologies,
                        # 'order_responses': order_responses,
                        'file_add': file_add,
                        'client_info': {
                            'client_name': username.text.replace('\n', ''),
                            'avatar': true_avatar,
                            'username_link': username_link,
                            'username_info': username_info.replace('\n', ' '),
                            'verification': verification,
                            'orders': int(active_emploer) + int(find_freelance.replace('\n', '')) + int(arbitage_emploer),
                            'feedback': feedback
                        }
                    }

                    ready_dict[counter] = ready_order
        fl_tasks = fl_parser_link()
        for fl_task in fl_tasks:
            fl_task_page = BeautifulSoup(get_response(fl_task).text, 'html.parser')
            fl_title = fl_task_page.find('h1', class_='text-1 d-flex align-items-center')
            fl_description = fl_task_page.find('div', class_='b-layout__txt_padbot_20')
            fl_date_published = fl_task_page.find('div', class_='b-layout__txt b-layout__txt_padbot_30 mt-32')
            fl_created_acc = fl_task_page.find('div', class_='mt-8 text-7')
            fl_price = ' '.join(fl_task_page.find('div', class_='py-32 text-right unmobile flex-shrink-0 ml-auto').text.replace('\n', '').split()) if fl_task_page.find('div', class_='py-32 text-right unmobile flex-shrink-0 ml-auto') else None
            fl_file_add = True if len(fl_task_page.find_all('span', class_='text-gray-dark text-7')) > 0 else False
            positive_feedback = int(''.join(fl_task_page.find('span', class_='text-8 b-layout__txt_color_6db335').text.split())) if fl_task_page.find('span', class_='text-8 b-layout__txt_color_6db335') else 0
            negative_feedback = int(''.join(fl_task_page.find('span', class_='text-8 b-layout__txt_color_c10600').text.split())) if fl_task_page.find('span', class_='text-8 b-layout__txt_color_c10600') else 0
            fl_technologies =[tech.text.replace('\n', '').split('/') for tech in fl_task_page.find_all('div', class_='text-5 mb-4 b-layout__txt_padbot_20')]
            ready_order = {
                        'task_name': fl_title.text.replace('\n', '').strip(),
                        'task_link': fl_task,
                        'description': fl_description.text.replace('\n', '').strip(),
                        'price': fl_price,
                        'fl_true': True,
                        'fl_created_acc': fl_created_acc.text.replace('\n', '').strip(),
                        'date_publised': ' '.join(fl_date_published.text.replace('\n', '').split()),
                        'technologies': fl_technologies,
                        'file_add': fl_file_add,
                        'client_info': {
                            'client_name': None,
                            'avatar': False,
                            'username_link': None,
                            'username_info': None,
                            'verification': None,
                            'orders': None,
                            'feedback': positive_feedback - negative_feedback
                        }
                    }

            ready_dict[counter] = ready_order
        return ready_dict


    def start_parse(self) -> None:
        diaposon_second = 600 # Нужно чтобы корректно работал sleep 10 минут
        while True:
            self._main(self.diapason)
            print('sleep', datetime.datetime.now())
            time.sleep(diaposon_second)
