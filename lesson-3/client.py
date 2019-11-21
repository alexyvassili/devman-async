import asyncio
from aiohttp import ClientSession, TCPConnector


async def get_from_server():
    chunks = []
    count = 0
    async with ClientSession(connector=TCPConnector(verify_ssl=False,
                                                    limit=1, )) as session:
        async with session.get("http://127.0.0.1:8080/archive/rur2/") as response:
            while True:
                chunk = await response.content.read(1048576)
                if not chunk:
                    break
                chunks.append(chunk)
                count += len(chunk)
                print("Get", len(chunk))
    print('Chunks', len(chunks))
    print('Getted', count)


asyncio.run(get_from_server())
