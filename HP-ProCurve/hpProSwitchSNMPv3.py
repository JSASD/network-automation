import string
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import argparse
import os
import logging 
import base64

#Set location of current directory for reliable file opening
__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(
            __file__
        )
    )
)
# Set variables using Base64
b64_username = "username"
b64_password = "super-secret-password"

# Decode variables just for use in script
#User
base64_bytes_username = b64_username.encode('ascii')
username_bytes = base64.b64decode(base64_bytes_username)
username = username_bytes.decode('ascii')
#Pass
base64_bytes_password = b64_password.encode('ascii')
password_bytes = base64.b64decode(base64_bytes_password)
password = password_bytes.decode('ascii')

#Open hpiplist file
hpiplist = open(os.path.join(__location__, "hpiplist.txt"), "r")


#def copyConfigs(givenUsername, givenPassword, passPromptSFTP, __location__):
def copyConfigs(usernameDecode, passwordDecode):

    """
    Parameters
    ----------
    usernameDecode: str
        Username to authenticate with
    passwordDecode: str
        Password to authenticate with
    """
    #Open hpiplist file
    hpiplist = open(os.path.join(__location__, "hpiplist.txt"), "r")
    iplist = [s.rstrip('\n') for s in hpiplist]

    for host in iplist:
        #Device configuration
        device = {
            'device_type': 'hp_procurve',
            'ip': host,
            'username': usernameDecode,
            'password': passwordDecode,
            'secret': str(passwordDecode),
            'port': "22"
            #'use_keys': True
        }
        #Connect to host
        try:
            print("\n> Connecting to host " + host)
            net_connect = ConnectHandler(**device)
            
            print("> Entering Config Mode")
            net_connect.send_command_timing("conf t", strip_command=False, strip_prompt=False)
            
            print("> Set SNMPv3 to enable")
            net_connect.send_command_timing("snmpv3 enable", strip_command=False, strip_prompt=False)        
            
            print("> Set to use SMPv3 only") 
            net_connect.send_command_timing("snmpv3 only", strip_command=False, strip_prompt=False)
                       
            print("> Setup User for Zabbix")              
            net_connect.send_command_timing("snmpv3 user zabbix auth md5 " + passwordDecode + " priv aes " + passwordDecode, strip_command=False, strip_prompt=False)

            print("> Add Zabbix user to management privledge group for SNMP")  
            net_connect.send_command_timing("snmpv3 group managerpriv user zabbix sec-model ver3", strip_command=False, strip_prompt=False)

            print("> Ensure it finished")
            net_connect.send_command_timing("")
            
            net_connect.disconnect()
        
        except(NetMikoTimeoutException):
            logging.warning("Timeout while connecting to device " + host + ". Is the device online?")
            continue
        except(NetMikoAuthenticationException):
            logging.warning("Error authenticating to switch/SFTP server on  " + host + ". Did you use the right password?")
        except:
            logging.warning('General error. Is the device working properly?')
    hpiplist.close()

copyConfigs(username, password)

