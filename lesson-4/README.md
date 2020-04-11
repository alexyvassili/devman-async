# Клиент для майнкрафт-чата

Позволяет читать и писать сообщения. Сообщения чата отображаются на экране, а также сохраняются в файл.  

## Как установить

Для работы микросервиса нужен Python версии не ниже 3.7
Параметры скрипта устанавливаются через аргументы командной строки, 
файлы `/etc/minechat.conf` и `~/.minechat.conf`, а также переменные окружения 

```bash
pip install -r requirements.txt
```

## Чтение чата

```bash
startchat.py [-h] [-s SERVER] [-p READ_PORT] [-c CHATLOG]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Minechat server [env var: APP_SERVER] (default: minechat.dvmn.org)
  -p READ_PORT, --read-port READ_PORT
                        Read port [env var: APP_READ_PORT] (default: 5000)
  -c CHATLOG, --chatlog CHATLOG
                        Chat log file [env var: APP_CHATLOG] (default: chatlog.txt)
```

По умолчанию имя файла с историей чата - `chatlog.txt`  


## Отправка сообщений в чат  
```bash
sendmessage.py [-h] [-s SERVER] [-w WRITE_PORT] [-u USER] [-t TOKEN] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Minechat server [env var: APP_SERVER] (default: minechat.dvmn.org)
  -w WRITE_PORT, --write-port WRITE_PORT
                        Write port [env var: APP_WRITE_PORT] (default: 5050)
  -u USER, --user USER  Send message: User name [env var: APP_USER] (default: None)
  -t TOKEN, --token TOKEN
                        Send message: User token [env var: APP_TOKEN] (default: None)
  -m MESSAGE, --message MESSAGE
                        Send message and exit [env var: APP_MESSAGE] (default: None)
```

С параметром `-m` вы можете отправить единичное сообщение и выйти,
без него вы можете отправлять множество сообщений из консоли.  
Указание имени пользователя будет работать только если такой пользователь сохранен в словаре `user`.  
Если указан токен, имя пользователя будет проигнорировано.  


# Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).