from fr_parser import Parser
import time, datetime


def main() -> None:
    p = Parser('https://freelance.habr.com/tasks', 'categories=development_all_inclusive,development_backend,development_frontend,development_prototyping,development_ios,development_android,development_desktop,development_bots,development_games,development_1c_dev,development_scripts,development_voice_interfaces,development_other,design_sites,design_landings,design_logos,design_illustrations,design_mobile,design_icons,design_polygraphy,design_banners,design_graphics,design_corporate_identity,design_presentations,design_modeling,design_animation,design_photo,design_other')
    p.start_parse()


if __name__ == '__main__':
    diaposon_second = 600 # Нужно чтобы корректно работал sleep 10 минут
    while True:
        main()
        print('sleep', datetime.datetime.now())
        time.sleep(diaposon_second)