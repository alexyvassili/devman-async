import anyio
import asyncio
from datetime import datetime
from aiofile import AIOFile
from asyncio import Queue
from config import get_config


def add_timestamp(log_line):
    timestamp = datetime.strftime(datetime.now(), "[%d.%m.%y %H:%M:%S]")
    return f"{timestamp} {log_line}"


async def chat_logging(chat_queue: Queue, chat_logfile: str):
    async with AIOFile(chat_logfile, 'a') as afp:
        offset = 0
        while True:
            log_line = await chat_queue.get()
            if log_line is None:
                break
            log_line_to_write = add_timestamp(log_line)
            print(log_line_to_write)
            await afp.write(log_line_to_write, offset=offset)
            await afp.fsync()


async def read_chat(chat_queue, reader):
    retry_timeout = 0

    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=3.0)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError, asyncio.TimeoutError):
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


async def main(args):
    chat_queue = Queue()
    reader, writer = await asyncio.open_connection(args.server, args.read_port)
    try:
        async with anyio.create_task_group() as tg:
            tg.start_soon(read_chat, chat_queue, reader)
            tg.start_soon(chat_logging, chat_queue, args.chatlog)
    finally:
        writer.close()


if __name__ == "__main__":
    args = get_config()
    asyncio.run(main(args))
