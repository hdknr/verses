from pathlib import Path

import environ

from .process import exec_command

env = environ.Env()


def secret_path(name=""):
    base = Path(env.str("SECRETS", default=".secrets"))
    return name and (base / name) or base


def ssh_keyfile(*name):
    base = secret_path()
    for i in name:
        file = Path(base) / f"keys/{i}"
        print(file)
        if file.is_file():
            return file


def exec_ssh(user, ipaddress, key, terminal=True):
    exec_command("ssh", "-i", key, f"{user}@{ipaddress}", terminal=terminal)


CONF_FILE = """
Host {server}
  HostName {address}
  User {user}
  Port 22
  IdentityFile {key}
"""


def update_ssh_conf(name, user, server, address, key):
    path = secret_path(f"ssh.{name}.conf")
    with open(path, "w") as out:
        out.write(CONF_FILE.format(user=user, server=server, address=address, key=key))
