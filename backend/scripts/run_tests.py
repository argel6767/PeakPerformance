import subprocess
from pathlib import Path
import platform
from sys import exit
from build_image import load_env_files, delete_old_image_and_container, build_image

'''
Loads env variables into terminal before building image, then running tests inside using docker-compose
'''
cd = Path.cwd()
docker_path = cd/'docker' if platform.system() != 'Linux' else cd/'backend'/'docker' # checking if this is a pipeline being ran, since its a linux machine
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def run_test_suite():
    print("RUNNING TESTS")
    process = subprocess.run(['docker-compose', 'run', '--rm', 'test'], cwd=docker_path, shell=is_os_windows)
    print(process)
    return process.returncode

def main():
    load_env_files()
    delete_old_image_and_container()
    build_image()
    exit_code = run_test_suite()
    if (exit_code == 0):
        print('TEST PASSED')
    else:
        print('TESTS FAILED')
    exit(exit_code)

if __name__ == '__main__':
    main()