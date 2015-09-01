#!/usr/bin/env python
"""Simple heartbeat monitor for checking TCP port banner response on open ports
   Checks SSH port on predefined list."""

import socket
import time
import os
import errno


# Define server list (ip or hostname)
SERVERS = {'host_one': 22,'host_two': 22,'webserver': 80, 'fail-test':22}


class colors:
    OK='\033[92m'
    FAIL='\033[91m'
    END='\033[0m'
    BLU='\033[94m'
    WARN='\033[93m'
    PURP='\033[95m'

ERROR = '[ '+colors.FAIL+'ERROR'+colors.END+' ] '
SUCCESS = '[ '+colors.OK+'OK'+colors.END+' ] '

def _ping_check(ping_target):
    ping_host = os.system('ping -c1 -t1 '+ping_target+' >> /dev/null 2>&1')
    if ping_host is not None:
        return True
    else:
        return False

def socket_check(host,port):
    # create tcp connection to specified host and port
    socket.setdefaulttimeout(2)
    s = socket.socket()
    try:
        s.connect((host,port))
        s.send('ping')
        banner = s.recv(1024)
        if banner is not None:
            print '  '+SUCCESS+str(banner.strip('\n'))
        s.close()
    except socket.error, v:
        s.close()
        errorcode = v[0]
        if errorcode == errno.ECONNREFUSED:
            print'  '+ERROR+str(v[1])+colors.WARN+'\n  Trying to ping target...'+colors.END
            try_ping = _ping_check(host)
            if try_ping is True:
                print '  '+SUCCESS+'{} -- Ping successful.'.format(target)
                SERVERS[target] = True
            else:
                print '  '+ERROR+'Ping failed on {}.'.format(target) 
                SERVERS[target] = False
        else:
            print '  '+ERROR+str(v[1])
            SERVERS[target] = False
    except socket.timeout, t:
        s.close()
        print '  '+ERROR+str(t[1])+colors.WARN+'\n  Trying to ping target...'+colors.END
        try_ping = _ping_check(host)
        if try_ping is True:
            print '  '+SUCCESS+'{} -- Ping successful.'.format(target)
            SERVERS[target] = True
        else:
            print '  '+ERROR+'Ping failed on {}.'.format(target)
            SERVERS[target] = False
    except Exception, e:
        s.close()
        print ERROR+colors.PURP+str(e)+colors.END


if __name__ == '__main__':        
    for target in sorted(SERVERS.keys()):
        print colors.PURP+'Connecting to {}:{}'.format(target,SERVERS[target])+colors.END
        socket_check(target,SERVERS[target])
    print colors.BLU+'\nHealth check results: '+colors.END
    count = 0
    for result in sorted(SERVERS.keys()):
        if SERVERS[result] is False:
            print '  '+colors.FAIL+result+colors.END
            count += 1
        else:
            print '  '+colors.OK+result+colors.END
    if count > 1:
        print '\n '+colors.FAIL+str(count)+colors.BLU+' hosts down\n'+colors.END
    elif count == 1:
        print '\n '+colors.FAIL+str(count)+colors.BLU+' host down\n'+colors.END
    else:
        print '\n '+colors.OK+str(count)+colors.BLU+' hosts down\n'+colors.END
