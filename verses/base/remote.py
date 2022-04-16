from pathlib import Path

from .process import exec_command


def find_ssh_keyfile(base_path, *name):
    if base_path.is_dir():
        for i in name:
            file = Path(base_path) / f"keys/{i}"
            if file.is_file():
                return file.absolute()


def ssh_keyfile(*name, secrets_dir=None):
    secrets_dir = secrets_dir or "~/.ssh"
    return find_ssh_keyfile(Path(secrets_dir).expanduser(), *name)


def exec_ssh(user, ipaddress, key, terminal=True):
    exec_command("ssh", "-i", key, f"{user}@{ipaddress}", terminal=terminal)


CONF_FILE = """
Host {server}
  HostName {address}
  User {user}
  Port 22
  IdentityFile {key}
"""


def update_ssh_conf(name, user, server, address, key, secrets_dir=None):
    secrets_dir = secrets_dir or "~/.ssh"
    path = Path(secrets_dir).expanduser() / f"ssh.{name}.conf"
    with open(path, "w") as out:
        out.write(CONF_FILE.format(user=user, server=server, address=address, key=key))
