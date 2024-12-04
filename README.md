# Парсер заказов с http://fl.ru http://freelance.ru и http://freelance.habr.com/ c 10 минутным интервалом

## Установка зависимостей и запуск
```bash
$ pip install virtualenv -> если запускаете не в docker
$ python3 -m venv env -> если запускаете не в docker
$ source env/bin/activate -> если запускаете не в docker
$ pip install -r ./requirements.txt -> если запускаете не в docker
$ mkdir orders -> если папка не создана
$ touch .env.prod -> создать файл конфига
$ vim .env.prod -> добавить токен бота token=токен
$ python bot.py -> docker-compose up --build
```
Зайти в бота нажать /start

Далее /restart_parser - перезапустить парсер


## Парсинг
freelance.habr.com:
 - наличие фото
 - тэги
 - описание
 - название заказа
 - цена 
 - срок
 - данные по заказчику (дата регистрации, отзывы исполнителей, ФИО)
 - наличие вложений

fl.ru:
 - тэги
 - описание
 - название заказа
 - цена 
 - срок
 - данные по заказчику (дата регистрации)
 - наличие вложений

fl.ru:
 - тэги
 - описание
 - название заказа
 - цена 
 - срок

 Связаться со мной в  [Telegram](https://t.me/FalseHuman)