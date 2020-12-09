 ### Simple script for collect user capacity per Access Point and as Prometheus Exporter

#### Requirements

```bash
pip3 -r requirements.txt
```

#### Usage

```bash
python3 clients_utilization.py --source-file ~/arubaos/aruba_controller/list_ap \
--output-client ~/arubaos/aruba_controller/list_clients_access_point \
--output-json ~/arubaos/aruba_controller/list_clients_access_point.json \
--ip 192.168.100.101 --port 9001
```


Once the script is running properly, Ensure the prometheus exporter already run on URL http://192.168.100.101:9001

#### Prometheus Server COnfiguration

```bash
- job_name: aruba_controller
  scrape_interval: 2m
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  static_configs:
  - targets:
    - 192.168.100.101:9001
 ```
