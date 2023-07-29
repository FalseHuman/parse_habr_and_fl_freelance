from datetime import datetime
from time import mktime

def filter_rss(rss,links, start_time, end_time) -> None:
    for d in rss['entries']:
        dt_rss = datetime.fromtimestamp(mktime(d['published_parsed'])) 
        if start_time.month == dt_rss.month and start_time.day == dt_rss.day and start_time.hour == dt_rss.hour:
            if  start_time.minute <= dt_rss.minute <= end_time.minute:
                links.append(d['link'])
            elif dt_rss.minute > 50 and start_time.minute >= 50:
                links.append(d['link'])
    return links