#!/usr/bin/env python
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
import json,time,os

with open('/aruba_os/office1/devices_iap') as f:
    devices_list = f.read().splitlines()

for a_device in devices_list:
    hostname = a_device
    aos_device = {
        'device_type': 'aruba_os',
        'ip': hostname,
        'username': 'your_username',
        'password': 'your_password'
    }
    # if one of devices down, the script will running next job
    try:
        net_connect= ConnectHandler(**aos_device)
    except (AuthenticationException):
        print 'auth failure ' + hostname
        continue
    except (NetMikoTimeoutException):
        print 'IP Timeout ' + hostname
        continue
    except (EOFError):
        print 'End of file while attempting device ' + hostname
        continue
    except (SSHException):
        print 'SSH not enble ' + hostname
        continue
    except Exception as unknown_error:
        print 'unknown error ' + str(unknown_error)
        continue
    net_connect = ConnectHandler(**aos_device)
    excecute_command = net_connect.send_command("show ap association | in Num")
    parse_command = excecute_command[12:16]
    result = "{} ".format(aos_device['ip']) +  parse_command + "\n"
    print result
    output_file = open("output_client.txt", "a")
    output_file.write(result)
    output_file.close()
print "print format json"
commands = {}
with open("output_client.txt") as fh:
    for line in fh:
        command, description = line.strip().split(' ', 1)
        commands[command] = description.strip()
print(json.dumps(commands, indent=2, sort_keys=True))

with open('/var/www/html/aruba_iap.json', 'w') as json_file:
    json.dump(commands, json_file)
print "Waiting 60s for delete file & prometheus still collect data......"
time.sleep(10)
remove_file = os.system("rm -rf output_client.txt")
print "Done"
