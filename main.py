import asyncio
import subprocess
import os
import simplejson as json 

config = json.load(open("./config.json", "r", encoding="utf-8"))

def makemkv(cmd_string):
    command = cmd_string.split()
    command = ['makemkvcon', '-r'] + command
    output = subprocess.run(command, capture_output=True, encoding="utf-8", check=True)
    print(output.stdout)
    return output

# Locate available drives

drives = []

prgmout = makemkv("info disc:-1")
prgmout = prgmout.stdout
for line in prgmout.split("\n"):
    data = line.split(",")
    if data[0].startswith("DRV:") and data[6] != '""':
        drives.append(data[6].strip("\""))

print(f"Available Drives: {drives}")

async def rip(device):
    makemkv(f"mkv dev:{device} all {config['makemkv']['output_dir']}")

async def main():
    subprocess.run(['setcd', '-i'] + drives, check=True)
asyncio.run(main())