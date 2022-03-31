from pathlib import Path
import subprocess
import platform


def terminal_command(*args, terminal=False):
    command_line = " ".join(args)
    if not terminal:
        return command_line

    if platform.system() == "Darwin":
        script = f"cd {Path.cwd()};{command_line}"
        return f'osascript -e \'tell application "Terminal" to do script "{script}"\''

    return command_line


def exec_command(*args, terminal=False):
    command_line = terminal_command(*args, terminal=terminal)
    subprocess.Popen(command_line, shell=True)
