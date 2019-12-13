import os


class Config:
    HOST = os.environ.get('HOST', 'minechat.dvmn.org')
    PORT = os.environ.get('PORT', '5000')
    HISTORY = os.environ.get('HISTORY', 'chatlog.txt')


config = Config()
