# -*- coding: utf-8 -*-
"""
File sorting service or a Directory Service which indexes file systems from all file servers.
"""
import os
import web ## to operate on web based API 
import shelve


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


_config = { 'dbfile' : 'names.db' }
## load initial config from each server about the PORT, IP

_dir = shelve.open(_config['dbfile'])