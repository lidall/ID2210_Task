# -*- coding: utf-8 -*-
"""
 Author      : Lida Liu
 Version     : 1.0
 Copyright   : All rights reserved. Do not distribute. 
 You are welcomed to modify the code.
 But any commercial use you need to contact me
"""

import paramiko
import os

def main():
    host = raw_input('Host:')
    user = 'test1'
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekeyfile = os.path.expanduser('~/.ssh/my-ssh-key')         
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile,password='test1')
    s.connect(host,22,user,pkey=mykey,timeout=5)
    cmd = raw_input('cmd:')
    stdin,stdout,stderr = s.exec_command(cmd)
    cmd_result = stdout.read(),stderr.read()
    for line in cmd_result:
            print line,
    s.close()
    
    
    
if __name__ == "__main__": 
  main()