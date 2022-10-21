#!/usr/bin/env python3

#Script is used to track changes of hosts IPs
#It requires file with list of hosts to track to be created (hostfile.txt)

import socket
import os.path
import json
import yaml

hostlist={}
hostfile = 'hostlist.txt'
hostfile_json=hostfile.replace('txt','json')
hostfile_yaml=hostfile.replace('txt','yaml')
errcount = 0 #used to count DNS resolution errors
errlimit = 3 #after reaching this errors limit script is terminated
errmsg_done = False #used to track if error message was printed already

if not os.path.isfile(hostfile):
  print (f'Hostfile {hostfile} doesn\'t exist. Please create it and populate with hosts')
  print ('Each host must be on separate line')
  exit (1)

#Populating hosts dict from hostfile
with open(hostfile,'r') as f:
  for line in f:
    ls = line.split(' ')
    if len(ls) < 2:  #New host which IPs are not known yet
      hostlist[ls[0].rstrip('\n')] = ''
    else:
      hostlist[ls[0].rstrip('\n')] = ls[1].rstrip('\n')

for (host,ip) in hostlist.items():
  print (f'Checking {host}...')
  try:
    new_ip = socket.gethostbyname(host)
  except:
    new_ip = ip
    print (f'Unable to resolve {host} for some reason. There may be DNS or network issue or hostname is not correct')
    print ('Keeping old ip')
    errcount += 1 
  if errcount == errlimit:  #IF there were too many errors we just write all hosts back to file and exit
    print ('Too many DNS resolution errors. Flushing host list and quitting...')
    break
  hostlist[host] = new_ip
  print (host, new_ip)
  if new_ip != ip and ip !='':
    print (f'IP for host {host} changed from {ip} to {new_ip}!')

#Flushing updated dict to file
with open(hostfile,'w') as f:
    for host,ip in hostlist.items(): 
      f.write (host + ' ' + ip + '\n')

#Writing json
with open (hostfile_json,'w') as f:
    json.dump(hostlist,f)
    
#Writing yaml
with open (hostfile_yaml,'w') as f:
    yaml.dump(hostlist,f)

