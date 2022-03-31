import environ
from pathlib import Path
from .process import exec_command


env = environ.Env()


def ssh_keyfile(name):
    base = env.str("SECRETS", default=".secrets")
    file = Path(base) / f"keys/{name}"
    return file.is_file() and file or None


def exec_ssh(user, ipaddress, key, terminal=True):
    exec_command("ssh", "-i", key, f"{user}@{ipaddress}", terminal=terminal)
