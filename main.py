from fr_parser import Parser
import time, datetime, logging

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',
                    level=logging.INFO, filename='main.log')


def main(sleep_time) -> None:
    p = Parser(
        url='https://freelance.habr.com/tasks',
        filter_url='categories=development_all_inclusive,development_backend,development_frontend,development_prototyping,development_ios,development_android,development_desktop,development_bots,development_games,development_1c_dev,development_scripts,development_voice_interfaces,development_other',
        diapason=10,
        sleep_time=sleep_time
        )
    p.start_parse()


if __name__ == '__main__':
    diaposon_second = 600 # Нужно чтобы корректно работал sleep 10 минут
    while True:
        sleep_time = datetime.datetime.now
        start_date = sleep_time()
        print('start', start_date)
        logging.info(f'start {str(start_date)}')
        try:
            main(sleep_time)
        except Exception as e:
            print(e)
            logging.error(e)
        end_date = sleep_time()
        print('sleep', end_date)
        logging.info(f'sleep {str(end_date)}')
        difference = end_date - start_date
        if difference.total_seconds() > 600:
            diaposon_second = diaposon_second - (difference - diaposon_second)
        time.sleep(diaposon_second)