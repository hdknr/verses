import os
from pathlib import Path
import subprocess


def find_ssh_conf(root=None, name="ssh.conf"):
    root = root or os.getcwd()
    for _d, _subd, f in os.walk(root):
        if name in f:
            return Path(_d) / name


def ssh_command(params, root=None, conf="ssh.conf", command="ssh"):
    conf = find_ssh_conf(root=root)
    if not conf:
        print("no ssh.conf was found.")
    args = " ".join(params) if params else ""
    return f"{command} -F {conf} {args}"


def ssh(ctx, params, terminal):
    """ ssh """
    root = os.getcwd()
    command = ssh_command(params, root=root)

    if terminal:
        script = f"pushd .;cd {root};{command}; popd"
        # macos
        command = (
            f'osascript -e \'tell application "Terminal" to do script "{script}"\''
        )

    subprocess.Popen(command, shell=True)


def scp(ctx, params):
    """ scp """
    root = os.getcwd()
    command = ssh_command(params, root=root, command="scp")
    subprocess.Popen(command, shell=True)


def rsync(ctx, params):
    """ rysnc """
    root = os.getcwd()
    ssh = ssh_command([], root=root)
    args = " ".join(params)
    command = f"rsync -e '{ssh}' {args}"
    subprocess.Popen(command, shell=True)


def download(ctx, remote_dir, local_dir):
    """ download: ssh tar"""
    root = os.getcwd()
    ssh = ssh_command([], root=root)
    command = f"{ssh} sudo tar cvfz - {remote_dir} | tar xvfz - -C {local_dir}"
    subprocess.Popen(command, shell=True)
