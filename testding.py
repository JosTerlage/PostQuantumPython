#import os


#os.system('curl http://stempoljos.westeurope.cloudapp.azure.com:8086/health')


import subprocess


command = "curl http://stempoljos.westeurope.cloudapp.azure.com:8086/health"
subprocess = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
response = subprocess.stdout.read()
print(response)