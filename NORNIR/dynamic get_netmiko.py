
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

commands = input('Enter the commands: ')
cmds = commands.split(',')

for cmd in cmds:
    nr = InitNornir(config_file='config.yaml')

    result = nr.run(
        task=netmiko_send_command,
        command_string=cmd,
    )

    print_result(result)