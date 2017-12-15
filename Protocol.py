# -*- coding: utf-8 -*-

# Protocols for parsing the files and tasks carried out for every interaction between the servers

import json
import os.path

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
