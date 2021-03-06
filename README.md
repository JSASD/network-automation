# Network Automation
Set of scripts used to automate our network.

<br>

## What is this?

A set of automation scripts! Mostly for the HP ProCurve series and Cisco Catalyst series network switches.

<br>

## Requirements

 - The Netmiko network automation library
    - `python3 pip install netmiko`

<br>

## General Usage

Almost all of these scripts can be run at a basic level, typically you can just run `pythonScript.py -h` or `pythonScript.py --help` to get command line options (This is good if this needs to be run on a schedule)

Each script uses `argparse` to accept command-line arguments.

<br>

Otherwise, you can just run the script, and it will prompt you for the required input

- This is typically a username, password

<br>

## IPList
Almost all scripts require a list of IP addresses to loop through.

<br>

 All you need to have is have a file named hpiplist(.txt) (for HP ProCurve scripts) OR ciscoiplist(.txt) (for Cisco Catalyst Scripts) with the list of IP addresses in plain text, line by line, in the same directory as the script.

Ex:

```
192.168.0.1
192.168.0.2
192.168.0.3
192.168.0.4
192.168.0.5
192.168.0.6
192.168.0.7
192.168.0.8
192.168.0.9
192.168.0.10
```