# Устанока

`git clone https://github.com/Madara225/telegram-raid-botnet-pyrogram`

`cd telegram-raid-botnet-pyrogram`

`pip3 install -r requirements.txt`

`python3 main.py`

авторизуемся: https://my.telegram.org/

оттуда берем id и hash

# Добавление аккаунтов
`cd sessions`

`python3 add_acc.py`

Для начала запускаем первую функцию, вводим номер телефона аккаунта или токен бота.

После того как добавили все аккаунты, запускаем вторую функцию, она привяжет аккаунты к ботнету.

Третья функция проверяет аккаунты на валидность, в случае, если аккаунт не валидный, сессия переносится в папку sessions/dead, тем самым, больше не задействуется в ботнете, после этого нужно **обязательно** запустить ещё раз вторую функцию.
 

 
# Конфиг
`cd settings`

`nano config.py` (в конфиге прокомментированы все переменные)

# Запуск

`python3 main.py`
 
Видео-инструкция по запуску ботнета: [YouTube](https://www.youtube.com/watch?v=DKKpfHzMR78)

Если есть вопросы, Вы можете обратится в наш [чат](https://t.me/pepe_devs)

Идею и часть кода взял у [huis_bn](https://t.me/huis_bn)

Ботнет [huis_bn](https://t.me/huis_bn) > [json1c/telegram-raid-botnet](https://github.com/json1c/telegram-raid-botnet)
