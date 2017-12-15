# -*- coding: utf-8 -*-
### Service for locking file access so that two clients cannot access a file together

import atexit ## to implement lock closing
import shelve

class LockServer():
	## Locks file access as per requirements
    def GET():
        pass
    def POST():
        pass
    def DELETE():
        pass

_config = { 'dbfile' : 'locks.db',
	    'lock_lifetime' : 30
	  }

## loading config data

locks = shelve.open(_config['dbfile'])

atexit.register(lambda: locks.close())

