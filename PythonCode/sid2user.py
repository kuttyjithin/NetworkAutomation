import subprocess
import re
sSID = "S-1-5-21-798167801-2843571222-2892612796"
lSID = sSID.split("-")
nIndex=0
maxIndex=500
rIndex= str(nIndex)
subProccessOutput = subprocess.call(["C:\\Users\\jjose10\\OneDrive - NAIT\\BAITS\\SECR3000\\PythonCode\\sid\\sid2user.exe", lSID[0],lSID[1],lSID[2],lSID[3],lSID[4],lSID[5],rIndex])
lSubProces = subProccessOutput.split(" ")
print(str(subProccessOutput.split(" ")))
""" lSubProces = subProccessOutput.split(" ")
for fail in lSubProces:
    if not(fail== "failed"):
        print (subProccessOutput) """

