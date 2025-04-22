import os
from pathlib import Path
import platform
import subprocess
import argparse

'''
Builds the docker image of the backend
'''

cd = Path.cwd()
is_os_windows = platform.system() == 'Windows' #windows needs shell otherwise permissions errors will not let script run processes

# determines what docker path to use when a script is ran via the --env flag
def determine_docker_path_run():
    parser = argparse.ArgumentParser(description='environment flag')
    parser.add_argument('--env', type=str, choices=['dev', 'ci'], default='dev', help='Specify the environment (dev or ci)')
    args = parser.parse_args()
    global docker_path
    if args.env == 'dev':
        path = cd/'docker'/'run'
        print(f"Docker path (dev): {path}")
        return path
    else:
        path = cd/'backend'/'docker'/'run'
        print(f"Docker path (ci): {path}")
        return path
    
    
def determine_docker_path_test():
    parser = argparse.ArgumentParser(description='environment flag')
    parser.add_argument('--env', type=str, choices=['dev', 'ci'], default='dev', help='Specify the environment (dev or ci)')
    args = parser.parse_args()
    global docker_path
    if args.env == 'dev':
        return cd/'docker'/'test'
    else:
        return cd/'backend'/'docker'/'test'

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
    

def build_image_run():
    docker_path = determine_docker_path_run()
    print('BUILDING IMAGE WITH NEW CHANGES')
    process = subprocess.run(['docker-compose', 'build'], cwd=docker_path, shell=is_os_windows)
    print(process)

def build_image_test():
    docker_path = determine_docker_path_test()
    print('BUILDING IMAGE WITH NEW CHANGES')
    process = subprocess.run(['docker-compose', 'build'], cwd=docker_path, shell=is_os_windows)
    print(process)