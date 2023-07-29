import feedparser
from datetime import datetime
from calculate_parser_time import caluculate_diapason
import pytz
from time import mktime
from filter_rss import filter_rss

def freelance_ru_parser_link(sleep_time):
    start_time, end_time = caluculate_diapason(sleep_time(pytz.utc), 10)
    d = feedparser.parse('https://freelance.ru/rss/feed/list/s.696.116.40.4')
    links = filter_rss(links=[], rss=d, start_time=start_time, end_time=end_time)
    return links
