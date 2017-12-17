# -*- coding: utf-8 -*-
### Service for locking file access so that two clients cannot access a file together

import atexit ## to implement lock closing
import collections
import shelve
import web
import logging
import random
import datetime
import Protocol

class LockServer():
	## Locks file access as per requirements
    def GET(self, file_path):
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        file_path = str(file_path)
        i = web.input()
        if file_path == '/':
            return '\n'.join('%s=(%s, %s)' % (file_path,str(locks[file_path].granted),
                   str(locks[file_path].last_used),)
                   for file_path in sorted(locks))
        elif file_path not in locks and 'lock_id' not in i:
            return 'OK'
        elif 'lock_id' in i:
            lock = locks.get(file_path, -1)
            if int(i['lock_id']) == lock.lock_id:
                Update_Lock(file_path)
                return 'OK'
        elif Lock_Expired(file_path):
            Revoke_Lock(file_path)
            return 'OK'
            
    def POST(self, file_path):
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        file_path = str(file_path)
        
        if file_path == '/':
            Locked = {}
            for file_path in web.data().split('\n'):
                if not file_path:
                    Locked[file_path] = New_Lock(file_path)
                    
                    for file_path in Locked:
                        Revoke_Lock(file_path)
                    
            return '\n'.join('%s=%d' % (file_path, lock_id,)\
                    for file_path, lock_id in Locked.items())        
            
        
    def DELETE():
        pass
                

def Lock_Expired(file_path):
    last_used = locks[file_path].last_used
    return (datetime.datetime.now() - last_used).seconds > _config['lock_lifetime']

def New_Lock(file_path):
    if file_path in locks:
        if not Lock_Expired(file_path):
            # can't revoke the lock, it's still active
            print('Unable to grant a new lock (%s).' % file_path)

        Revoke_Lock(file_path)

    else:
        lock_id = random.randrange(0, 32768)
        logging.info('Granting lock (%d) on %s.', lock_id, file_path)
        t = datetime.datetime.now()
        locks[file_path] = Lock(lock_id, t, t)
        
    return lock_id

def Update_Lock(file_path):
    t = datetime.datetime.now()
    logging.info('Update lock on %s from %s to %s.',file_path, locks[file_path].last_used, t)
    
    l =locks[file_path]
    l = Lock(l.lock_id, l.granted, t)
    locks[file_path] = l

Lock = collections.namedtuple('Lock', 'lock_id granted last_used')

def Revoke_Lock(file_path):
    if file_path in locks:
        logging.info('Revoking lock on %s.', file_path)
        del locks[file_path]
        
        

_config = { 'dbfile' : 'locks.db',
	    'lock_lifetime' : 30
	  }

## loading config data
logging.info('Loading config file lockserver.dfs.json.')

locks = shelve.open(_config['dbfile'])
Protocol.load_config(_config, 'lockserver.dfs.json')
atexit.register(lambda: locks.close())

