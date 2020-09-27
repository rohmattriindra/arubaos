from netmiko import ConnectHandler
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily, Gauge
from prometheus_client import start_http_server
import json, os, time

def gather_clients():

    ssh_connection = ConnectHandler(
        device_type="aruba_os",
        ip="192.168.1.10",
        username="admin",
        password="password",
        port=22
    )
    with open("list_ap") as f:
        devices_list = f.read().splitlines()

    for device in devices_list:
        AP = ssh_connection.send_command("show user-table ap-name " + device +  " | include Entries") 
        result = AP[15:17].replace('/','')
        outfile = "ap_name:" + device + " | " + "value:" + result + "\n"
        print (outfile)
        hasil = open ("list_clients_ap", "a")
        hasil.write(outfile)
        hasil.close()


def line_to_dict(split_Line):
    # Assumes that the first ':' in a line
    # is always the key:value separator

    line_dict = {}
    for part in split_Line:
        key, value = part.split(":", maxsplit=1)
        line_dict[key] = value

    return line_dict

def convert_json():
    f = open("list_clients_ap", "r")
    content = f.read()
    splitcontent = content.splitlines()

    # Split each line by pipe
    lines = [line.split(' | ') for line in splitcontent]

    # Convert each line to dict
    lines = [line_to_dict(l) for l in lines]

    # Convert to json file
    with open("clients.json", 'w') as fout:
        json.dump(lines, fout, indent=4)

class CustomCollector(object):
    def __init__(self):
        pass#
    def collect(self):
        prome_json =  open("clients.json",)
        data = json.load(prome_json)

        for key in data:
            g = GaugeMetricFamily("clients_usage", "Help text", labels=['node_ap'])
            g.add_metric([str(key['ap_name'])], key["value"])
            yield g


if __name__ == "__main__":
    print ("the apps is running on port 9001")
    start_http_server(9001)
    REGISTRY.register(CustomCollector())
    while True:        
        gather_clients()
        convert_json()
        remove_temp = os.system("rm -rf list_clients_ap")
        time.sleep(120)
