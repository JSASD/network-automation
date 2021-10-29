###################################
#                                 #
# PLEASE NOTE: THIS IS NOT TESTED #
#                                 #
###################################


# hpSwitchSaveRunningConfig.py
# Saves running configurations of HP ProCurve switches from a list of IP addresses

#Import Python Libraries
from  netmiko import ConnectHandler
import argparse
import getpass

#Open hpiplist file
hpiplist = open("hpiplist.txt", "r")

#Initialize parser
parser = argparse.ArgumentParser()

#Help prompts:
userPrompt = "Set username to log in with"
passPrompt = "Set password to log in with"

#Add optional arguments
parser.add_argument("-u", "--Username", help = "Set username to log in with")
parser.add_argument("-p", "--Password", help = "Set password to log in with")

#Read arguments from command line
args = parser.parse_args()

#If read arguments contain information, use those
if bool(args.Username) and bool(args.Password):
    username = args.Username
    password = args.Password
#Otherwise, ask user for username/password for switches
else:
    username = input(userPrompt + "\n")
    password = getpass.getpass("\n" + passPrompt + "\n")
#Print variables to terminal
print("\n")
print("Username: " + username)
print("Password: " + password)
print("\n")

def WriteMemory(givenUsername, givenPassword, givenHosts):
    for host in givenHosts:
        #Device configuration
        device = {
            'device_type': 'hp_procurve',
            'ip': host,
            'username': givenUsername,
            'password': givenPassword,
            'use_keys': True
        }

        print("\n--------> Connecting to host " + host + " <--------")
        #Connect to host
        net_connect = ConnectHandler(**device)

        print("\n--------> Writing configuration to memory <--------")
        #Send command 'write-host'
        net_connect.send_command_timing("write memory", strip_command=False, strip_prompt=False)

WriteMemory(username, password, hosts)

iplist.close()
