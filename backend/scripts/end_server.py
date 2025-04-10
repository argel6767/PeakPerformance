import os
import subprocess
from pathlib import Path
import platform


'''
Shuts down server
'''

docker_path = Path.cwd()/'docker'
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def shut_down_server():
    process = subprocess.run(['docker-compose', 'down'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def main():
    shut_down_server()

if __name__ == "__main__":
    main()