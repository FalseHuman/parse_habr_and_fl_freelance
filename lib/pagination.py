import asyncio

import requests
from bs4 import BeautifulSoup

from .mainloop import Mainloop
from .req import get_response


class Pagination(Mainloop):
    def __init__(self, url: str, filter_url: str = '', pagination: bool=False) -> None:
        self.url = url
        self.filter_url = filter_url
        self.pagination = pagination
        self.pagination_pages = []

        super().__init__()
        self.start_mainloop(self._get_pagination_pages(self._get_page_count(self.url) + 1))

    def _get_page_count(self, url: str) -> int:
        html_data = get_response(url, self.filter_url).text

        soup = BeautifulSoup(html_data, 'html.parser')
        pagination_div = soup.find_all('div', class_='pagination')

        if not pagination_div:
            html_data = get_response(f'{url}?page=1', self.filter_url).text
            soup = BeautifulSoup(html_data, 'html.parser')
            pagination_div = soup.find_all('ul', class_='content-list content-list_tasks')
            
            assert pagination_div, 'page is empty'
            return 1

        pagination_text = BeautifulSoup(pagination_div[0].text, 'html.parser')

        links = pagination_text.text.split(' ')

        for i in links:
            if i.isdigit():
                max_pag_number = int(i)
                
        if self.pagination:
            return max_pag_number
        else:
            return 1

    async def _get_list_futures(self, url: str, page_count: int) -> None:
        return [self.mainloop.run_in_executor(None, get_response, f'{url}?page={i}', self.filter_url) for i in range(1, page_count)]

    async def _get_pagination_pages(self, page_count: int) -> list:
        for page in await self._get_list_futures(self.url, page_count):
            asyncio.ensure_future(page)
            self.pagination_pages.append(await page)
        return self.pagination_pages
