# -*- coding: utf-8 -*-
"""
File sorting service or a Directory Service which indexes file systems from all file servers.
"""
import os
import web ## to operate on web based API 
import shelve
import logging

import Protocol

class DirServer:
    def GET(self, file_path):
        """DirServer is responsible of the mapping between directory names
        and file servers.
        """

        web.header('Content-Type', 'text/plain; charset=UTF-8')
        file_path = str(file_path)
        if file_path == '/':
            return '/n'.join('%s=%s' % (directory, _dir[directory])
                    for directory in sorted(_dir))

        directory = str(os.file_path.dirname(file_path))

        if directory in _dir:
            return _dir[directory]

def UPDATE(directory, add=True):
    """Add pair of directory/server to the name server."""
    web.header('Content-Type', 'text/plain; charset=UTF-8')
    i = web.input()
    srv = i['srv']
        
    if directory == '/':
        if 'dirs' not in i:
            raise web.badrequest()
        
        for directory in i['dirs'].split('\n'):
            if not directory:
                UPDATE_PATH(directory, srv, add)
    else:
        UPDATE_PATH(directory, srv, add)
    return 'ok'
                
def UPDATE_PATH(directory, srv, add=True):
     """Just update the name dictionnary and the database"""
     if directory[-1] == '/':
         directory = os.path.dirname(directory)
     if add:
         logging.info('Update directory %s on %s.', directory, srv)
         _dir[directory] = srv
     elif directory in _dir:
         logging.info('Remove directory %s on %s.', directory, srv)
         del _dir[directory]
     else:
         raise ValueError('%s wasn\'t not deleted!!' %directory)
        
        
_config = { 'dbfile' : 'names.db' }
logging.info('Loading config file DirServer.dfs.json.')
Protocol.load_config(_config, 'DirServer.dfs.json')
## load initial config from each server about the PORT, IP
_dir = shelve.open(_config['dbfile'])
