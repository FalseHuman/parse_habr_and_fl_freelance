import asyncio
import datetime
import time
import json

from bs4 import BeautifulSoup
from dateutil.parser import parse #python-dateutil

from lib.validate_url import Validation
from lib.pagination import Pagination
from lib.json_worker import Json_worker
from lib.req import get_response
from fl_parser import fl_parser_link
from freelance_parser import freelance_ru_parser_link


class Parser():
    def __init__(self, url: str, sleep_time, filter_url: str = '', diapason: int = 10) -> None:
        self.url = url
        self.sleep_time = sleep_time
        self.filter_url = filter_url
        self.ready_orders_dict = {}
        self.diapason = diapason
        self.pag = Pagination(self.url, self.filter_url, pagination=False)

        super().__init__()

        # self._main(self.diapason)

    def _main(self) -> None:
        Validation(self.url)
        ready_dict = self._parse()
        json_result = Json_worker('result')
        json_result.dump_dict(ready_dict)
        json_result.check_caluclate_parser_time(self.diapason, self.sleep_time)

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
                    fr_created_acc = task_page.find_all('div', class_='divider row')[-1].text.replace('\n', ' ') if task_page.find_all('div', class_='divider row') else "Нет информации о регистрации"
                    feedback = int(static_emploer[4].find('div', class_='value').text.split('/')[0]) - int(static_emploer[4].find('div', class_='value').text.split('/')[1])
                    
                    file_add =  True if task_page.find_all('dl', class_='user-params') else False
                    date_published = parse(meta_tags.split('•')[0].split(',')[1])

                    counter += 1

                    ready_order = {
                        'task_name': task,
                        'task_link': task_link,
                        'description': description,
                        'fl_true': False,
                        'price': 'Бюджет: ' + price.replace('договорная', '?') + ' Срок: ?',
                        'date_publised': str(date_published),
                        'date_published_str': date_published_str,
                        'technologies': technologies,
                        # 'order_responses': order_responses,
                        'file_add': file_add,
                        'client_info': {
                            'client_name': username.text.replace('\n', ''),
                            'avatar': true_avatar,
                            'username_link': username_link,
                            'username_info': username_info.replace('\n', ' ') if len(username_info) > 1 else None,
                            'fr_created_acc': fr_created_acc,
                            'verification': verification,
                            'orders': int(active_emploer) + int(find_freelance.replace('\n', '')) + int(arbitage_emploer),
                            'feedback': feedback
                        }
                    }

                    if 'час' not in price:
                        ready_dict[counter] = ready_order
        last_count_fl = list(ready_dict.keys())[-1]
        fl_tasks = fl_parser_link(self.sleep_time)
        fl_file_add = False
        for fl_task in fl_tasks:
            fl_task_page = BeautifulSoup(get_response(fl_task, fl_page=True).text, 'html.parser')
            fl_title = fl_task_page.find('h1', class_='text-1 d-flex align-items-center')
            fl_description = fl_task_page.find('div', class_='b-layout__txt_padbot_20')
            fl_date_published = fl_task_page.find('div', class_='b-layout__txt b-layout__txt_padbot_30 mt-32')
            fl_created_acc = fl_task_page.find('div', class_='mt-8 text-7')
            fl_price = ' '.join(fl_task_page.find('div', class_='py-32 text-right unmobile flex-shrink-0 ml-auto').text.replace('\n', '').split()) if fl_task_page.find('div', class_='py-32 text-right unmobile flex-shrink-0 ml-auto') else 'Бюджет: ? Срок: ?'
            if fl_task_page.find('div', class_='b-layout mt-22 base-attach-class') is not None:
                fl_file_add = True
            positive_feedback = int(''.join(fl_task_page.find('span', class_='text-8 b-layout__txt_color_6db335').text.split())) if fl_task_page.find('span', class_='text-8 b-layout__txt_color_6db335') else 0
            negative_feedback = int(''.join(fl_task_page.find('span', class_='text-8 b-layout__txt_color_c10600').text.split())) if fl_task_page.find('span', class_='text-8 b-layout__txt_color_c10600') else 0
            fl_technologies =[' '.join(tech.text.replace('\n', '').split('/')) for tech in fl_task_page.find_all('div', class_='text-5 mb-4 b-layout__txt_padbot_20')]
            if fl_technologies == []:
                fl_technologies =[' '.join(tech.text.replace('\n', '').split('/')) for tech in fl_task_page.find_all('div', class_='text-5 mb-4')]
            ready_order = {
                        'task_name': fl_title.text.replace('\n', '').strip() if fl_title else 'Нет информации',
                        'task_link': fl_task,
                        'description': fl_description.text.replace('\n', '').strip() if fl_description else 'Нет информации',
                        'price': fl_price.replace('ожидает предложений', '?').replace('по договоренности', '?').replace('Дедлайн', 'Срок').replace('дня', '').replace('день', '').replace('дней', ''),
                        'fl_true': True,
                        'date_publised': ' '.join(fl_date_published.text.replace('\n', '').split()) if fl_date_published else 'Нет информации',
                        'technologies': fl_technologies,
                        'file_add': fl_file_add,
                        'client_info': {
                            'client_name': None,
                            'avatar': False,
                            'username_link': None,
                            'username_info': None,
                            'fl_created_acc': fl_created_acc.text.replace('\n', '').strip() if fl_created_acc else ' Нет информации',
                            'verification': None,
                            'orders': None,
                            'feedback': positive_feedback - negative_feedback
                        }
                    }
            last_count_fl += 1
            if 'час' not in fl_price:
                ready_dict[last_count_fl] = ready_order

        last_count = list(ready_dict.keys())[-1]
        freelance_tasks = freelance_ru_parser_link(self.sleep_time)
        filter_page = BeautifulSoup(get_response('https://freelance.ru/project/search/pro?c=&c%5B%5D=4&c%5B%5D=696&c%5B%5D=116&c%5B%5D=40&q=&m=or&e=&a=0&a=1&v=0&v=1&f=1000&t=&o=0&o=1&b=').text, 'html.parser')
        freelance_ru_url = 'https://freelance.ru'
        default_avatar_freelance = 'https://cdn.freelance.ru/img/ava/male.png'
        for row in filter_page.find_all('div', class_='project'):
            url = freelance_ru_url + row.find('a', class_='description')['href']
            for freelance_task in freelance_tasks:
                if url == freelance_task:
                    freelance_title = ' '.join(row.find('h2', class_='title').text.split())
                    freelance_description = ' '.join(row.find('a', class_='description').text.split())
                    freelance_technologies = [' '.join(tech.text.split()) for tech in  row.find_all('div', class_='specs-list')]
                    freelance_cost = ' '.join(row.find('div', class_='cost').text.split()) if row.find('div', class_='cost') else '?'
                    freelance_term = ' '.join(row.find('div', class_='term').text.split()) if row.find('div', class_='term') else '?'
                    freelance_price = 'Бюджет: ' + freelance_cost + ' Срок: ' + freelance_term
                    freelance_term_publish_time = ' '.join(row.find('div', class_='publish-time').text.split()) if row.find('div', class_='publish-time') else 'Нет информации'
                    freelance_avatar = row.find('img', class_='avatar-xs')['data-src'] if row.find('img', class_='avatar-xs') else False
                    freelance_avatar_true = True if freelance_avatar != default_avatar_freelance or freelance_avatar == False else False
                    ready_order = {
                        'task_name': freelance_title,
                        'task_link': url,
                        'description': freelance_description,
                        'price': freelance_price.replace('Договорная', '?').replace('за', ''), #.replace('дня', '').replace('день', '').replace('дней', ''),
                        'fl_true': True,
                        'date_publised': freelance_term_publish_time,
                        'technologies': freelance_technologies,
                        'file_add': None,
                        'client_info': {
                            'client_name': None,
                            'avatar': freelance_avatar_true,
                            'username_link': None,
                            'username_info': None,
                            'fl_created_acc': None,
                            'verification': None,
                            'orders': None,
                            'feedback': 0
                        }
                    }
                    last_count += 1
                    ready_dict[last_count] = ready_order

        return ready_dict


    def start_parse(self) -> None:
        self._main()
