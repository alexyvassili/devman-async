# We need patch aiohttp stream writer
# before import web
# because we get unhandled ConnectionResetError('Cannot write to closing transport')
# while client broke the connection
# See aiohttp issue: https://github.com/aio-libs/aiohttp/issues/3648
from aiohttp import http_writer
from service.http_writer_patch import patch_streamwriter
patch_streamwriter(http_writer)

from aiohttp import web
from service.log import set_logs
from service.app import create_app


if __name__ == '__main__':
    set_logs()
    app = create_app()
    web.run_app(app)
