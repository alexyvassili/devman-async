import os
import configargparse
import argparse


def get_config():
    parser = configargparse.ArgumentParser(
        allow_abbrev=False,
        auto_env_var_prefix="APP_",
        description="Minechat app",
        default_config_files=[
            os.path.join(os.path.expanduser("~"), ".minechat.conf"),
            "/etc/minechat.conf",
        ],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        ignore_unknown_config_file_keys=True,
    )

    parser.add_argument("-s", "--server", type=str, default='minechat.dvmn.org', help="Minechat server")
    parser.add_argument("-p", "--read-port", type=int, default=5000, help="Read port")
    parser.add_argument("-w", "--write-port", type=int, default=5050, help="Write port")
    parser.add_argument("-c", "--chatlog", type=str, default="chatlog.txt", help="Chat log file")
    parser.add_argument("-u", "--user", type=str, help="User name")
    parser.add_argument("-t", "--token", type=str, help="User token")

    args = parser.parse_args()
    return args
