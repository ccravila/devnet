

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config
from nornir.plugins.tasks.networking import napalm_get, napalm_configure
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

print_result(nr.run(task=netmiko_send_config, config_commands =['ip scp server enable']))
print_result(nr.run(task=napalm_configure, filename='defaultconf.cfg'))

# OPEN CONFIG FILE
with open ('defaultconf.cfg','r') as file:
    commandlist = []
    for i in file.readlines():
        commandlist.append(i.strip('\n').strip())

# OPEN SEND CONFIGS
print_result(nr.run(task=netmiko_send_config, config_commands = commandlist))

# GETTERS NAPALM
print_result(nr.run(task=napalm_get, getters=["facts"]))

# Get Output commands
result = nr.run(task=netmiko_send_command, command_string="show interfaces")

#Making filters
r1 = nr.filter(F(hostname__contains='192.168.99.10'))


##########
HOST FILE
##########


---
192.168.99.10:
  hostname: 192.168.99.10
  groups:
    - routers
192.168.99.11:
  hostname: 192.168.99.11
  groups:
    - routers
192.168.99.12:
  hostname: 192.168.99.12
  groups:
    - routers
192.168.99.13:
  hostname: 192.168.99.13
  groups:
    - routers


#### GROUPS FILE ####


---
routers:
    username: cisco
    password: cisco
    nornir_ssh_port: 22
    nornir_nos: "ios"
    platform: "ios"


#### CONFIG FILE ####


---
core:
  num_workers: 100
inventory:
  plugin: nornir.plugins.inventory.simple.SimpleInventory
  options:
      host_file: "hosts.yaml"
      group_file: "groups.yaml"


Validating Results



result = nr.run(task=napalm_get, getters=["facts"])



In [87]: result['192.168.99.10'].result['facts']
Out[87]: {'uptime': 19080, 'vendor': 'Cisco', 'os_version': 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(2)T4, DEVELOPMENT TEST SOFTWARE', 'serial_number': '67121270', 'model': 'Unknown', 'hostname': 'R1', 'fqdn': 'R1.lab.com', 'interface_list': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3']}





In [89]: result['192.168.99.11'].result['facts']['hostname']
Out[89]: 'R2'

In [88]: result['192.168.99.10'].result['facts']['os_version']
Out[88]: 'Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.4(2)T4, DEVELOPMENT TEST SOFTWARE'