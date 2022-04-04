##################################################
# --------- network-device-port-finder --------- #
#                                                #
# - Saves current running configs of HP ProCurve #
# ------- switches to a chosen directory ------- #
#                                                #
# ------------ JSASD Tech Department ----------- #
##################################################

#Import Python Libraries
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import argparse
import getpass
import os

#Set location of current directory for reliable file opening
__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(
            __file__)
        )
)

#Initialize parser
parser = argparse.ArgumentParser(description="Saves running configs of HP ProCurve switches from a given IP list to a given directory.")

#Help prompts:
userPrompt = "Set username to log in with"
passPrompt = "Set password to log in with"
directoryPrompt = "Set directory to output to. Ex. Z:\\Path\\To\\Folder"

#Add optional arguments
parser.add_argument("-u", "--Username", help = userPrompt)
parser.add_argument("-p", "--Password", help = passPrompt)
parser.add_argument("-d", "--Directory", help = directoryPrompt)

#Read arguments from command line
args = parser.parse_args()

#If read arguments contain information, use those
if bool(args.Username) and bool(args.Password):
    username = args.Username
    password = args.Password
    directory = args.Directory
#Otherwise, ask user for username/password for switches
else:
    username = input(userPrompt + "\n")
    password = getpass.getpass("\n" + passPrompt + "\n")
    directory = input("\n" + directoryPrompt + "\n")

def GetConfig(givenUsername, givenPassword, givenDirectory):
    #Open hpiplist file
    hpiplist = open(os.path.join(__location__, "hpiplist.txt"), "r")
    #Strip newlines from file for later use
    iplist = [s.rstrip('\n') for s in hpiplist]

    for host in iplist:
        #Device configuration
        device = {
            'device_type': 'hp_procurve',
            'ip': host,
            'username': givenUsername,
            'password': givenPassword,
            'use_keys': True
        }

        #Connect to host
        try:
            print("\n> Connecting to host " + host)
            net_connect = ConnectHandler(**device)

            print("\n> Getting configuration from memory")
            #Send command 'sh run'
            output = net_connect.send_command_timing("sh run", strip_command=False, strip_prompt=False)

            #Disconnect from host
            net_connect.disconnect()
            
        except(NetMikoTimeoutException):
            print("\n> Timeout while connecting to device " + host)
            output = "Timeout while connecting to device...\n     No configuration gathered."
        except(NetMikoAuthenticationException):
            print("\n> Error authenticating to switch " + host + ". Did you use the right password?")
        except:
            print("\n> General error. Is the device working properly?")

        #Open file to write running config to
        save_file = open(givenDirectory + "\\" + host + "Config.txt",'w')
        #Write to file
        save_file.write(output)
        #Close file
        save_file.close()

GetConfig(username, password, directory)