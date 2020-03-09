import os


class Config:
    HOST = os.environ.get('HOST', 'minechat.dvmn.org')
    PORT = os.environ.get('PORT', '5000')
    WRITE_PORT = 5050
    HISTORY = os.environ.get('HISTORY', 'chatlog.txt')


config = Config()
