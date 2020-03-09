import asyncio
from config import config

TOKEN = "405b8f4e-2bd8-11ea-b989-0242ac110002"


async def read_response(reader):
    retry_timeout = 0
    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=3.0)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionError, asyncio.TimeoutError) as e:
            if retry_timeout:
                print("Нет соединения. Повторная попытка через 3 сек.\n")
            else:
                print("Нет соединения. Повторная попытка.\n")
            await asyncio.sleep(retry_timeout)
            retry_timeout = 3
            continue
        else:
            if retry_timeout:
                print("Установлено соединение.\n")
                retry_timeout = 0

        return data


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(config.HOST, config.WRITE_PORT)
    data = await read_response(reader)
    print('Get', data.decode())
    print("Logging in with token")
    writer.write(f"{TOKEN}\n".encode())

    data = await read_response(reader)
    print(f'Received: {data.decode()!r}')
    data = await read_response(reader)
    print(f'Received: {data.decode()!r}')
    print('Sending message')
    writer.write(f"{message}\n\n".encode())
    data = await read_response(reader)
    print(data.decode())
    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!'))
