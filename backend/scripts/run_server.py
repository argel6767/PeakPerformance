import os
import subprocess
from pathlib import Path
import platform
from build_image import load_env_files, delete_old_image_and_container, build_image, determine_environment

'''
Loads env variables into terminal before building then running the backend & database servers
'''

docker_path = None
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def run_server_and_db():
    print('RUNNING BACKEND SERVER AND DATABASE')
    process = subprocess.run(['docker-compose', 'up'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def main():
    determine_environment()
    load_env_files()
    delete_old_image_and_container()
    build_image()
    run_server_and_db()
    
if __name__ == '__main__':
    main()