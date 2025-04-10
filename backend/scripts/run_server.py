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
    file_path = Path.cwd()/'.env'
    
    with open(file_path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, _, value = line.strip().partition("=")
            os.environ[key] = value
            print(f"Set environment variable: {key}={value}")

def build_image():
    process = subprocess.run(['docker-compose', 'build'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def run_server():
    process = subprocess.run(['docker-compose', 'up'], cwd=docker_path, shell=is_os_windows)
    print(process)
    
def main():
    load_env_files()
    build_image()
    run_server()
    
if __name__ == '__main__':
    main()