import subprocess
import time

command = "curl http://stempoljos.westeurope.cloudapp.azure.com:8086/health"

amount = 1000
totaltimetakenall = 0

for x in range(amount):
    starttime = time.time_ns()
    subprocess2 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    response = str(subprocess2.stdout.read())
    timetaken = time.time_ns()-starttime
    totaltimetakenall += timetaken
    print(timetaken)

print("average time taken: ")
print(totaltimetakenall/amount)

