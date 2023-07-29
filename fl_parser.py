import feedparser
from datetime import datetime
from calculate_parser_time import caluculate_diapason
import pytz
from time import mktime
from filter_rss import filter_rss

def fl_parser_link(sleep_time):
    categories_parse = ['2', '3&subcategory=172&subcategory=300&&subcategory=283&subcategory=300&subcategory=239&&subcategory=35','5', '23']
    start_time, end_time = caluculate_diapason(sleep_time(pytz.utc), 10)
    links = []
    for category in categories_parse:
        d = feedparser.parse(f'https://www.fl.ru/rss/projects.xml?category={category}')
        links = filter_rss(links=links, rss=d, start_time=start_time, end_time=end_time)
    return links