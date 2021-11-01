# ciscoSwitchSaveRunningConfig.py
# Saves running configurations of Cisco Catalyst switches from a list of IP addresses

#Import Python Libraries
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
import argparse
import getpass


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

def WriteMemory(givenUsername, givenPassword):
    #Open ciscoiplist file
    ciscoiplist = open("ciscoiplist.txt", "r")
    
    for host in ciscoiplist:
        #Device configuration
        device = {
            'device_type': 'cisco_ios',
            'ip': host,
            'username': username,
            'password': password,
            'secret': secret,
            'use_keys': True
        }

        #Connect to host
        try:
            print("\n> Connecting to host " + host)
            net_connect = ConnectHandler(**device)

            print("\n> Writing configuration to memory")
            #Enable executive priviledge mode
            net_connect.enable()
            #Send command 'write-host'
            net_connect.send_command_timing("write memory", strip_command=False, strip_prompt=False)

        except (NetMikoTimeoutException):
            print("\n> Timeout while connecting to device" + host)
            continue
    
    #Done with file, close it
    ciscoiplist.close()

#Run 'WriteMemory' function to open the ciscoiplist.txt file and connect to each device
WriteMemory(username, password)