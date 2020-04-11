import asyncio
import logging
import os
import json
from config import get_config


args = get_config()

ACCESS_LOG_FILE = 'sendmessage.log'
LOGGING_FORMAT = '[%(asctime)s] %(levelname).1s %(message)s'


def create_log_files_if_not_exist():
    if not os.path.exists(ACCESS_LOG_FILE):
        os.mknod(ACCESS_LOG_FILE)


def setup_loggers():
    logFormatter = logging.Formatter(LOGGING_FORMAT)
    rootLogger = logging.getLogger()

    message_file_handler = logging.FileHandler(ACCESS_LOG_FILE)
    message_file_handler.setFormatter(logFormatter)
    rootLogger.addHandler(message_file_handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.DEBUG)


create_log_files_if_not_exist()
setup_loggers()


def get_token():
    users = {
        "test": "405b8f4e-2bd8-11ea-b989-0242ac110002"
    }
    if args.token:
        return args.token
    if args.user and args.user in users:
        return users[args.user]
    return None


async def sign_up(reader, writer):
    # Enter preferred nickname below
    data = await read_response(reader)
    logging.debug(data.decode())
    nickname = input()
    logging.debug("Nickname: %s", nickname)
    writer.write(f"{nickname}\n".encode())
    # account data
    data = await read_response(reader)
    account = json.loads(data.decode())
    return account


async def login(reader, writer):
    token = get_token()
    data = await read_response(reader)
    # Enter your personal hash or leave it empty...
    logging.debug(data.decode())
    if token:
        writer.write(f"{token}\n".encode())
        # Return nickname and hash
        data = await read_response(reader)
        account = json.loads(data.decode())
        # Token may be invalid and we have empty account
        # So we try create user
        if not account:
            logging.debug("Your TOKEN is invalid! Let's try to create new user!")
            account = await sign_up(reader, writer)
    else:
        writer.write(b"\n")
        account = await sign_up(reader, writer)
    logging.debug("Logged in as: %s", account["nickname"])


async def read_response(reader):
    retry_timeout = 0
    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=3.0)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError, asyncio.TimeoutError) as e:
            if retry_timeout:
                logging.debug("Нет соединения. Повторная попытка через %s сек.\n", retry_timeout)
            else:
                logging.debug("Нет соединения. Повторная попытка.\n")
            await asyncio.sleep(retry_timeout)
            retry_timeout = 3
            continue
        else:
            if retry_timeout:
                logging.debug("Установлено соединение.\n")
                retry_timeout = 0

        return data


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(args.server, args.write_port)
    await login(reader, writer)
    logging.debug("Start send message. Press Ctrl-C to quit")
    data = await read_response(reader)
    logging.debug(data.decode())

    while True:
        try:
            message = input()
        except KeyboardInterrupt:
            break
        logging.debug("Sending message: %s", message)
        # NB:  мне не удалось сломать скрипт, передавая \n в середине сообщения или ника
        writer.write(f"{message}\n\n".encode())
        data = await read_response(reader)
        logging.debug(data.decode())
    logging.debug('Close the connection')
    writer.close()


asyncio.run(tcp_echo_client())
