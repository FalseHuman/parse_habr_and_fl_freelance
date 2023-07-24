from fr_parser import Parser
import time, datetime


def main(sleep_time) -> None:
    p = Parser(
        url='https://freelance.habr.com/tasks',
        filter_url='categories=development_all_inclusive,development_backend,development_frontend,development_prototyping,development_ios,development_android,development_desktop,development_bots,development_games,development_1c_dev,development_scripts,development_voice_interfaces,development_other,design_sites,design_landings,design_logos,design_illustrations,design_mobile,design_icons,design_polygraphy,design_banners,design_graphics,design_corporate_identity,design_presentations,design_modeling,design_animation,design_photo,design_other',
        diapason=10,
        sleep_time=sleep_time
        )
    p.start_parse()


if __name__ == '__main__':
    diaposon_second = 600 # Нужно чтобы корректно работал sleep 10 минут
    while True:
        sleep_time = datetime.datetime.now
        print('start', sleep_time())
        main(sleep_time)
        print('sleep', sleep_time())
        time.sleep(diaposon_second - sleep_time().second)