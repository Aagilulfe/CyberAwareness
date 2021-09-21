import subprocess

pwd='azerazet'
cmd='sudo grep psk= /etc/NetworkManager/system-connections/*'


subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)