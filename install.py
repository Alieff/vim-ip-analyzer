import os
import subprocess
import glob

def run_cmd(cmd):
    """
    cmd: is an array of command, ex: ['pipenv', '--venv']
    """
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

print('> Finding python location in pipenv virtual environment...')
env_root = run_cmd(['pipenv', '--venv'])
print(f'.. found: {env_root}')

print('> Infering OS')
operating_system = 'linux'
for file in glob.glob(f'{env_root}{os.sep}*'):
    if 'script' in file.replace(env_root,'').lower():
        operating_system = 'windows'
if operating_system == 'windows':
    result = f'{env_root}{os.sep}Scripts{os.sep}python.exe'
    print(f'.. found: {result}')
else:
    result = f'{env_root}{os.sep}bin{os.sep}python'
    print(f'.. found: {result}')

print('> Generating VIM config, containing obtained python path')
with open("virtual_environment_info.vim","w") as f :
    f.write(f"let g:ip_analyzer_virtual_python_path = '{result}'")
f.closed
