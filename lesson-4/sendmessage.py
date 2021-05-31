import asyncio
import logging
import os
import json
from config import get_config


ACCESS_LOG_FILE = 'sendmessage.log'
LOGGING_FORMAT = '[%(asctime)s] %(levelname).1s %(message)s'

log = logging.getLogger('send_message')


def get_token(user, token):
    users = {
        "test": "405b8f4e-2bd8-11ea-b989-0242ac110002"
    }
    if token:
        return token
    if user and user in users:
        return users[user]
    return None


async def sign_up(reader, writer):
    # Enter preferred nickname below
    data = await read_response(reader)
    log.debug(data.decode())
    nickname = input()
    log.debug("Nickname: %s", nickname)
    writer.write(f"{nickname}\n".encode())
    await writer.drain()
    # account data
    data = await read_response(reader)
    account = json.loads(data.decode())
    return account


async def login(reader, writer, user, token):
    token = get_token(user, token)
    data = await read_response(reader)
    # Enter your personal hash or leave it empty...
    log.debug(data.decode())
    if token:
        writer.write(f"{token}\n".encode())
        # Return nickname and hash
        data = await read_response(reader)
        account = json.loads(data.decode())
        # Token may be invalid and we have empty account
        # So we try create user
        if not account:
            log.debug("Your TOKEN is invalid! Let's try to create new user!")
            account = await sign_up(reader, writer)
    else:
        writer.write(b"\n")
        account = await sign_up(reader, writer)
    await writer.drain()
    log.debug("Logged in as: %s", account["nickname"])


async def read_response(reader):
    retry_timeout = 0
    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=3.0)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError, asyncio.TimeoutError) as e:
            if retry_timeout:
                log.debug("Нет соединения. Повторная попытка через %s сек.\n", retry_timeout)
            else:
                log.debug("Нет соединения. Повторная попытка.\n")
            await asyncio.sleep(retry_timeout)
            retry_timeout = 3
            continue
        else:
            if retry_timeout:
                log.debug("Установлено соединение.\n")
                retry_timeout = 0

        return data


async def send_message(reader, writer, message):
    log.debug("Sending message: %s", message)
    # NB:  мне не удалось сломать скрипт, передавая \n в середине сообщения или ника
    writer.write(f"{message}\n\n".encode())
    await writer.drain()
    data = await read_response(reader)
    log.debug(data.decode())


async def send_many_messages(reader, writer):
    while True:
        try:
            message = input()
        except KeyboardInterrupt:
            break
        await send_message(reader, writer, message)


async def write_to_chat(args):
    reader, writer = await asyncio.open_connection(args.server, args.write_port)
    try:
        await login(reader, writer, args.user, args.token)
        log.debug("Start send message. Press Ctrl-C to quit")
        data = await read_response(reader)
        log.debug(data.decode())

        if args.message:
            # Send message and exit
            await send_message(reader, writer, args.message)
        else:
            await send_many_messages(reader, writer)

    finally:
        log.debug('Close the connection')
        writer.close()


if __name__ == '__main__':
    if not os.path.exists(ACCESS_LOG_FILE):
        os.mknod(ACCESS_LOG_FILE)

    logFormatter = logging.Formatter(LOGGING_FORMAT)

    message_file_handler = logging.FileHandler(ACCESS_LOG_FILE)
    message_file_handler.setFormatter(logFormatter)
    log.addHandler(message_file_handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    log.addHandler(consoleHandler)

    log.setLevel(logging.DEBUG)
    args = get_config()
    asyncio.run(write_to_chat(args))
