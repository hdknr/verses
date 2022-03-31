import environ
from pathlib import Path
from .process import exec_command


env = environ.Env()


def ssh_keyfile(*name):
    base = env.str("SECRETS", default=".secrets")
    for i in name:
        file = Path(base) / f"keys/{i}"
        print(file)
        if file.is_file():
            return file


def exec_ssh(user, ipaddress, key, terminal=True):
    exec_command("ssh", "-i", key, f"{user}@{ipaddress}", terminal=terminal)
