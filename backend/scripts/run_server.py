import os
import subprocess
from pathlib import Path
import platform

'''
Loads env variables into terminal before building then running the backend & database servers
'''

docker_path = Path.cwd()/'docker'
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def load_env_files():
    print('LOADING ENVIRONMENT VARIABLES')
    file_path = Path.cwd()/'.env'
    with open(file_path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, _, value = line.strip().partition("=")
            os.environ[key] = value
            print(f"Set environment variable: {key}={value}")
            
def delete_old_image_and_container():
    print('DELETING OLD IMAGE AND CONTAINER')
    process = subprocess.run(['docker', 'rmi', 'docker-web', '--force'], cwd=Path.cwd(), shell=is_os_windows)
    print(process)

def build_image():
    print('BUILDING IMAGE WITH NEW CHANGES')
    process = subprocess.run(['docker-compose', 'build'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def run_server_and_db():
    print('RUNNING BACKEND SERVER AND DATABASE')
    process = subprocess.run(['docker-compose', 'up'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def main():
    load_env_files()
    delete_old_image_and_container()
    build_image()
    run_server_and_db()
    
if __name__ == '__main__':
    main()