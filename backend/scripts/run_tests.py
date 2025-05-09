import subprocess
from pathlib import Path
import platform
from sys import exit
from build_image import load_env_files, delete_old_image_and_container, build_image_test, determine_docker_path_test
from end_server import shut_down_server_test
from sys import exit, argv


'''
Loads env variables into terminal before building image, then running tests inside using docker-compose
'''
cd = Path.cwd()
docker_path = determine_docker_path_test()  # checking if this is a pipeline being ran, or just dev
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def run_test_suite():
    print("RUNNING TESTS")
    process = subprocess.run(['docker-compose', 'run', '--rm', 'test'], cwd=docker_path, shell=is_os_windows)
    print(process)
    return process.returncode

def main():
    if (len(argv) == 1 or argv[2] == 'dev'):
        load_env_files()
    delete_old_image_and_container()
    build_image_test()
    exit_code = run_test_suite()
    shut_down_server_test()
    if (exit_code == 0):
        print('TEST PASSED')
    else:
        print('TESTS FAILED')
    exit(exit_code)

if __name__ == '__main__':
    main()