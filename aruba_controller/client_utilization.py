from netmiko import ConnectHandler
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily, Gauge
from prometheus_client import start_http_server
import json, os, time, sys, re
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source-file", dest="list_ap", required=True, help="List of Access Point Aruba")
    parser.add_argument("-o", "--output-client", dest="output_client", required=True, help="Output Client Usage each Access Point")
    parser.add_argument("-j", "--output-json", dest="output_client_json", required=True, help="Output Client Usage each AP with JSON Format" )
    parser.add_argument("-p", "--port", dest="port",required=True, help="listening port service" )
    parser.add_argument("-ip", "--ip", dest="ip", required=True, help="IP Address Controller" )

    return parser.parse_args()

def gather_clients():
    args = get_args()
    ssh_connection = ConnectHandler(device_type="aruba_os", ip=args.ip, username="controller_user", password="controller_pass", port=22)

    with open(args.list_ap) as f:
        devices_list = f.read().splitlines()

    for device in devices_list:
        AP = ssh_connection.send_command("show user-table ap-name " + device +  " | include Entries") 
        out_ap = re.findall(r'(\d+)/', AP)
        result = ''.join([str(out_ap)])
        rem_chars = ("[']")
        for i in rem_chars:
            result = result.replace (i,"")
        outfile = "ap_name:" + device + " | " + "value:" + result + "\n"
        print (outfile)
        result = open (args.output_client, "a")
        result.write(outfile)
        result.close()
    ssh_connection.disconnect()

def line_to_dict(split_Line):
    line_dict = {}
    for part in split_Line:
        key, value = part.split(":", maxsplit=1)
        line_dict[key] = value

    return line_dict

def convert_json():
    f = open(args.output_client, "r")
    content = f.read()
    splitcontent = content.splitlines()
    lines = [line.split(' | ') for line in splitcontent]
    lines = [line_to_dict(l) for l in lines]
    with open(args.output_client_json, 'w') as fout:
        json.dump(lines, fout, indent=4)

class CustomCollector(object):
    def __init__(self):
        pass#
    def collect(self):
        args = get_args()
        prome_json =  open(args.output_client_json)
        data = json.load(prome_json)

        for key in data:
            g = GaugeMetricFamily("clients_usage", "Help text", labels=['node_ap'])
            g.add_metric([str(key['ap_name'])], key["value"])
            yield g


if __name__ == "__main__":
    args = get_args()
    start_http_server(int(args.port))
    print ("The aruba json exporter running on port " + str(args.port) )
    #The first running to generate file
    gather_clients()
    convert_json()
    REGISTRY.register(CustomCollector())
    while True:
        #Continue to generate file each 120 seconds 
        gather_clients()
        convert_json()
        remove_temp = os.system("rm -rf " + args.output_client )
        time.sleep(120)
