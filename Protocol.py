# -*- coding: utf-8 -*-

# Protocols for parsing the files and tasks carried out for every interaction between the servers

import json
import os.path

from contextlib import closing
from http.client import HTTPConnection

def load_config(config,file_path):
	## parse data from config files
    if not os.path.exists(file_path):
        return
        with open(file_path) as f:
            c = json.loads(f.read())
            config.update(c)

def get_host(s):
    host, port = s.split(':')
    return host, int(port)


def Locked(file_path, host, port,Lockid):
    with closing(HTTPConnection(host, port)) as con:
        if Lockid is not None:
            file_path += '?lock_id=%s' % Lockid
            
            con.request('GET', file_path)
            
            r = con.getresponse()
    
    return r.status != 200