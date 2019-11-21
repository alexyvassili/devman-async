# We need patch aiohttp stream writer
# before import web
# because we get unhandled ConnectionResetError('Cannot write to closing transport')
# while client broke the connection
# See aiohttp issue: https://github.com/aio-libs/aiohttp/issues/3648
from aiohttp import http_writer
from service.http_writer_patch import patch_streamwriter
patch_streamwriter(http_writer)

import argparse
from aiohttp import web
from service.log import set_logs
from service.app import create_app
from settings import config


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logging', action='store_true', help='Enable access log')
    parser.add_argument('-d', '--enable-delay', action='store_true', help='Enable server response delay')
    parser.add_argument('-f', '--photo-folder', default=config.PHOTO_FOLDER, action='store', help='Photo folder name')
    return parser


def update_config_from_args():
    parser = create_parser()
    namespace = parser.parse_args()
    config.LOGGING = namespace.logging
    config.ENABLE_DELAY = namespace.enable_delay
    config.PHOTO_FOLDER = namespace.photo_folder


if __name__ == '__main__':
    update_config_from_args()
    set_logs()
    app = create_app()
    web.run_app(app)
