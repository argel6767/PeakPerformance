import os
import subprocess
from pathlib import Path
import platform
from build_image import determine_docker_path_test, determine_docker_path_run

'''
Shuts down server
'''

is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def shut_down_server_test():
    print('SHUTTING DOWN SERVER')
    docker_path = determine_docker_path_test()
    process = subprocess.run(['docker-compose', 'down'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def shut_down_server_run():
    print('SHUTTING DOWN SERVER')
    docker_path = determine_docker_path_run
    process = subprocess.run(['docker-compose', 'down'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def main():
    shut_down_server_run()

if __name__ == "__main__":
    main()