# -*- coding: utf-8 -*-

#Stores the files for clients; assigned by the DirServer

import os.path
import time
import web
import logging
from contextlib import closing
from httplib import HTTPConnection
import Protocol

class FileServer():
	# Takes and stores the client files.
    def GET(self, file_path):
        """Return the requested file if it's not locked"""
        p = Local_path(file_path)
        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        with open(p) as f:
            return f.read()

    def POST(self,file_path):
        p = Local_path(file_path)
        with open(p, 'w') as f:
            f.write(web.data())

        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        return ''
        
    def DELETE(self, file_path):
        """Remove the filepath if it's unlocked"""
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        os.unlink(Local_path(file_path))
        return 'OK'
        
    def HEAD(self, file_path):
        """If the file exists/isn't locked, return the last-modified http
           header which corresponds to the last time was modified."""
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        p = Local_path(file_path)
        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        return ''
        
def Local_path(file_path):
    return os.path.join(os.getcwd(), _config['fsroot'], file_path[1:])

def init_File_server():
    host, port = Protocol.get_host(_config['nameserver'])
    with closing(HTTPConnection(host, port)) as conn:
        data = 'srv=%s&dirs=%s' % (_config['srv'],
                                '\n'.join(_config['directories']),)
        conn.request('POST', '/', data)


_config = { 'lockserver' : None,'nameserver' : None, 'directories' : [],'fsroot' : 'fs/','server' : None }

logging.info('Loading config file fileserver.dfs.json.')
Protocol.load_config(_config, 'fileserver.dfs.json')

init_File_server()



