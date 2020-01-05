 Simple script for collect user capacity each Access Point

#### requirements

```bash
pip install netmiko
```

#### Usage

```bash
chmod +x arubaos_controller.py

./arubaos_controller.py

Collecting data............
{
  "OFFICE-01-CAP325-04": "10", 
  "OFFICE-01-CAP325-05": "13", 
  "OFFICE-01-CAP325-07": "7", 
  "OFFICE-01-CAP325-08": "16", 
  "OFFICE-01-CAP325-09": "31", 
  "OFFICE-01-CAP335-06": "17", 
  "OFFICE-01-CAP335-10": "8", 
  "OFFICE-01-CAP335-11": "26", 
  "OFFICE-01-CAP335-12": "12", 
  "OFFICE-02-CAP325-01": "7", 
  "OFFICE-02-CAP335-02": "26", 
  "OFFICE_01-CAP325-03": "30", 
  "OFFICE_01_CAP325_01": "21", 
  "OFFICE_01_CAP325_02": "2"
}


```
