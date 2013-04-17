#!/usr/bin/env python

import os
import fdb
import json
import Crypto.PublicKey.RSA as RSA

if __name__ == '__main__':
    f = open('/etc/scvrepo/config.json')
    config = json.loads(f.read())
    f.close()

    key = RSA.generate(1024, os.urandom)
    pub = key.publickey().exportKey()
    priv = key.exportKey()

    try:
        connection = fdb.connect(
                host = config['db.ip'],
                database = '/var/lib/firebird/2.5/data/' + config['db.name'],
                user = config['db.user'],
                password = config['db.password'])
        cursor = connection.cursor()
        cursor.execute('INSERT INTO CONFIG (PARAM, VAL) VALUES (?,?);',
                ('publickey', pub))
        connection.commit()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO CONFIG (PARAM, VAL) VALUES (?,?);',
                ('privatekey', priv))
        connection.commit()
        connection.close()
    except fdb.fbcore.DatabaseError, e:
        print "Failed to access database"
