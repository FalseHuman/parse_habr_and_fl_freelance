import feedparser
from datetime import datetime
from calculate_parser_time import caluculate_diapason
import pytz
from time import mktime

def fl_parser_link():
    categories_parse = ['2', '3', '5', '23']
    start_time, end_time = caluculate_diapason(datetime.now(pytz.utc), 10)
    links = []
    for category in categories_parse:
        d = feedparser.parse(f'https://www.fl.ru/rss/projects.xml?category={category}')
        for d in d['entries']:
            dt_rss = datetime.fromtimestamp(mktime(d['published_parsed'])) 
            if start_time.month == dt_rss.month and start_time.day == dt_rss.day and dt_rss.hour == start_time.hour:
                if  start_time.minute <= dt_rss.minute <= end_time.minute:
                    links.append(d['link'])
                elif dt_rss.minute > 50 and start_time.minute >= 50:
                    links.append(d['link'])
    return links