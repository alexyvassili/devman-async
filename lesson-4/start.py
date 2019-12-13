import asyncio
from datetime import datetime
from aiofile import AIOFile, Writer
from asyncio import Queue


def add_timestamp(log_line):
    timestamp = datetime.strftime(datetime.now(), "[%d.%m.%y %H:%M:%S]")
    return f"{timestamp} {log_line}"


async def chat_logging(chat_queue: Queue):
    async with AIOFile("chatlog.txt", 'a') as afp:
        offset = 0
        while True:
            log_line = await chat_queue.get()
            print(add_timestamp(log_line))
            if log_line is None:
                break
            log_line_to_write = add_timestamp(log_line)
            await afp.write(log_line_to_write, offset=offset)
            await afp.fsync()


async def tcp_echo_client(chat_queue):
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5000)
    retry_timeout = 0

    while True:
        try:
            data = await reader.readline()
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError) as e:
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

asyncio.run(main())
