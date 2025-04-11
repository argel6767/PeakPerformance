import os
import subprocess
from pathlib import Path
import platform
from run_server import load_env_files, delete_old_image_and_container, build_image

'''
Loads env variables into terminal before building image, then running tests inside using docker-compose
'''

docker_path = Path.cwd()/'docker'
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def run_test_suite():
    print("RUNNING TESTS")
    process = subprocess.run(['docker-compose', 'run', '--rm', 'test'], cwd=docker_path, shell=is_os_windows)
    print(process)

def main():
    load_env_files()
    delete_old_image_and_container()
    build_image()
    run_test_suite()

if __name__ == '__main__':
    main()