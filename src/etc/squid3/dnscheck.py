#!/usr/bin/env python2.7

import socket
import sys
from os import path, remove, close, chmod, rename
import subprocess
import re
import stat
from tempfile import mkstemp
from shutil import move
import iptables_config

class Host:
    def __init__(self, name, url):
        self.name = name
        self.url = url

hosts = [Host("apple", "apple.com"),
         Host("apple2", "captive.apple.com"),
         Host("apple3", "www.ibook.info"),
         Host("apple4", "www.itools.info"),
         Host("apple5", "www.airport.us"),
         Host("apple6", "www.thinkdifferent.us"),
         Host("apple7", "www.appleiphonecell.com"),
         Host("google", "clients3.google.com")]

if len(sys.argv) > 1:
    if(sys.argv[1] == '-f'):
        FORCE = True


# From http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
# and modified to replace whole line
def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    for line in old_file:
        if re.search(pattern, line):
            new_file.write(subst + '\n')
        else:
            new_file.write(line)
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def main():
    for host in hosts:
        host.ip = socket.gethostbyname(host.url)

    ip_list = [line.strip() for line in open('/etc/squid3/hosts')]

    needs_updating = False
    for host in hosts:
        if not host.ip in ip_list:
            needs_updating = True

    if needs_updating or FORCE:
        rename('/etc/squid3/hosts', '/etc/squid3/hosts.old')
        f = open('/etc/squid3/hosts', 'w')
        for host in hosts:
            f.write(host.ip + '\n')
            dns_string = 'address=/' + host.url + '/' + host.ip
            replace('/etc/dnsmasq.conf', 'address=/' + host.url, dns_string) 
        f.close()
        chmod('/etc/dnsmasq.conf', 0644)
        iptables_config.add_rules()
        subprocess.call(['/etc/init.d/dnsmasq', 'restart'])



if __name__ == "__main__":
    main()
