import os
from pathlib import Path
import platform
import subprocess
import argparse

cd = Path.cwd()
docker_path = None # checking if this is a pipeline being ran, since its a linux machine
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

def determine_environment():
    print('SETTING ENVIRONMENT SPECIFIC VALUES')
    parser = argparse.ArgumentParser(description='environment flag')
    parser.add_argument('--env', type=str, choices=['dev', 'ci'], default='dev', help='Specify the environment (dev or ci)')
    args = parser.parse_args()
    global docker_path
    if args == 'dev':
        docker_path = cd/'docker'
    else:
        docker_path = cd/'backend'/'docker'
    
    
def load_env_files():
    print('LOADING ENVIRONMENT VARIABLES')
    file_path = cd/'.env'
    if not file_path.exists(): #CI Pipeline being ran
        file_path = cd/'backend'/'.env.ci'
        
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