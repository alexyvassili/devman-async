import asyncio
import argparse
from datetime import datetime
from aiofile import AIOFile
from asyncio import Queue
from config import config


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--host', default=config.HOST, action='store', help='Chat server host')
    parser.add_argument('-p', '--port', default=config.PORT, action='store', help='Chat server port')
    parser.add_argument('-i', '--history', default=config.HISTORY, action='store', help='History filename')
    return parser


def update_config_from_args():
    parser = create_parser()
    namespace = parser.parse_args()
    config.HOST = namespace.host
    config.PORT = namespace.port
    config.HISTORY = namespace.history


def add_timestamp(log_line):
    timestamp = datetime.strftime(datetime.now(), "[%d.%m.%y %H:%M:%S]")
    return f"{timestamp} {log_line}"


async def chat_logging(chat_queue: Queue):
    async with AIOFile(config.HISTORY, 'a') as afp:
        offset = 0
        while True:
            log_line = await chat_queue.get()
            if log_line is None:
                break
            log_line_to_write = add_timestamp(log_line)
            print(log_line_to_write)
            await afp.write(log_line_to_write, offset=offset)
            await afp.fsync()


async def tcp_echo_client(chat_queue):
    reader, writer = await asyncio.open_connection(config.HOST, config.PORT)
    retry_timeout = 0

    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=3.0)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError, asyncio.TimeoutError) as e:
            if retry_timeout:
                await chat_queue.put("Нет соединения. Повторная попытка через 3 сек.\n")
            else:
                await chat_queue.put("Нет соединения. Повторная попытка.\n")
            await asyncio.sleep(retry_timeout)
            retry_timeout = 3
            continue
        else:
            if retry_timeout:
                await chat_queue.put("Установлено соединение.\n")
                retry_timeout = 0

        if not data:
            await chat_queue.put(None)
            break
        await chat_queue.put(data.decode())

    await chat_queue.put('Закрытие соединения.\n')
    writer.close()


async def main():
    chat_queue = Queue()
    await asyncio.gather(tcp_echo_client(chat_queue), chat_logging(chat_queue))


if __name__ == "__main__":
    update_config_from_args()
    asyncio.run(main())
