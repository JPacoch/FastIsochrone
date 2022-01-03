"""
Runnable script that starts command line interface.

Script launches python environment defined by name in ENV_NAME variable.
If environment does not exist, will be created using file defined in ENV_FILE_NAME variable.
"""

import os
import sys
import subprocess

ENV_FILE_NAME = "requirements.yml"
ENV_NAME = "fastisochrone"


PATHS_PATTERNS = [
    f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Continuum\\anaconda3",
    "C:\\ProgramData\\Anaconda3",
    f"C:\\Users\\{os.getlogin()}\\.conda",
]


ENV_DIR = os.path.dirname(os.path.abspath(__file__))

PYTHON_PATHS = [os.path.join(p, f"envs\\{ENV_NAME}\\python.exe") for p in PATHS_PATTERNS]
CONDA_PATHS = [os.path.join(p, "Scripts\\activate.bat") for p in PATHS_PATTERNS]


def main():
    for python_path in PYTHON_PATHS:
        if os.path.exists(python_path):
            # run application of python within given conda environment
            subprocess.call([python_path, ".\\app.py"], shell=True)
            return True

    # if path does not exist
    go = True if input(f"[y/n] **{ENV_NAME}** needs to be installed. Continue?: ").upper() == "Y" else False

    if go:
        for conda_path in CONDA_PATHS:
            if os.path.exists(conda_path):
                p = subprocess.Popen("cmd.exe", stdin=subprocess.PIPE)
                for cmd in [conda_path, f'conda env create -f "{os.path.join(ENV_DIR, ENV_FILE_NAME)}"']:
                    p.stdin.write((cmd + "\n").encode())
                p.stdin.close()

    else:
        sys.exit()


if __name__ == '__main__':
    main()