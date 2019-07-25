#!/usr/bin/env python
from netmiko import ConnectHandler
from datetime import time
import json

controller = {
     'device_type': 'aruba_os',
     'ip':   '10.1.2.3',
     'username': 'fakeuser',
     'password': 'fakepass',
     'port': 22,
     'verbose': False,
 }

print "Collecting data............"
net_connect = ConnectHandler(**controller)
AP1 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-01 | include Entries")
R1 = AP1[15:17].replace('/','')
AP2 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-02 | include Entries")
R2 = AP2[15:17].replace('/','')
AP3 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-03 | include Entries")
R3 = AP3[15:17].replace('/','')
AP4 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-04 | include Entries")
R4 = AP4[15:17].replace('/','')
AP5 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-05 | include Entries")
R5 = AP5[15:17].replace('/','')
AP6 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP335-06 | include Entries")
R6 = AP6[15:17].replace('/','')
AP7 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-07 | include Entries")
R7 = AP7[15:17].replace('/','')
AP8 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-08 | include Entries")
R8 = AP8[15:17].replace('/','')
AP9 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP325-09 | include Entries")
R9 = AP9[15:17].replace('/','')
AP10 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP335-10 | include Entries")
R10 = AP10[15:17].replace('/','')
AP11 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP335-11 | include Entries")
R11 = AP11[15:17].replace('/','')
AP12 = net_connect.send_command("show user-table ap-name OFFICE-01-CAP335-12 | include Entries")
R12 = AP12[15:17].replace('/','')
AP21 = net_connect.send_command("show user-table ap-name OFFICE-02-CAP325-01 | include Entries")
R21 = AP21[15:17].replace('/','')
AP22 = net_connect.send_command("show user-table ap-name OFFICE-02-CAP335-02 | include Entries")
R22 = AP22[15:17].replace('/','')
OUTPUT = "OFFICE_01_CAP325_01 {}\nOFFICE_01_CAP325_02 {}\nOFFICE_01-CAP325-03 {}\nOFFICE-01-CAP325-04 {}\nOFFICE-01-CAP325-05 {}\nOFFICE-01-CAP335-06 {}\nOFFICE-01-CAP325-07 {}\nOFFICE-01-CAP325-08 {}\nOFFICE-01-CAP325-09 {}\nOFFICE-01-CAP335-10 {}\nOFFICE-01-CAP335-11 {}\nOFFICE-01-CAP335-12 {}\nOFFICE-02-CAP325-01 {}\nOFFICE-02-CAP335-02 {}\n".format(R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R21,R22)
file = open("OUTPUT_TEXT","w")
file.write(OUTPUT)
file.close()
commands = {}
with open("OUTPUT_TEXT") as fh:
    for line in fh:
        command, description = line.strip().split(' ', 1)
        commands[command] = description.strip()
print(json.dumps(commands, indent=2, sort_keys=True))

with open('aruba_os.json', 'w') as json_file:
    json.dump(commands, json_file)