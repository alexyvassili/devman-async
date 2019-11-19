import logging
import asyncio
from aiohttp import web
import aiofiles
import os
from log import set_logs


async def archivate(request):
    hash_ = request.match_info.get('archive_hash')
    folder = os.path.join('test_photos', hash_)
    if not os.path.exists(folder):
        return web.HTTPNotFound(body="<h1>404 Not Found</h1><p>Archive does not exist or was deleted.</p>",
                                content_type="text/html")
    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="photos_{hash_}.zip"'
    response.headers['Content-Type'] = 'application/zip'
    await response.prepare(request)
    proc = await asyncio.create_subprocess_shell(
        f'zip - {folder} -r -j',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    count = 0
    while True:
        data = await proc.stdout.read(1024)
        if not data:
            break
        logging.info(f"Sending archive chunk {len(data)} bytes...")
        await response.write(data)
        count += len(data)
    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    set_logs()
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archivate),
    ])
    web.run_app(app)
