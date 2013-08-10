#!/usr/bin/env python

import fdb
import getopt
import getpass
import json
import os
import sys
import Crypto.PublicKey.RSA as RSA


config = {}

def main():
    print('The following steps will setup the skarphed repository and the corresponding firebird database.')
    print('')
    setup_database()
    print('')
    setup_config()
    print('')
    generate_keypair()
    print('')
    print('Do not forget to change the repositories default password via admin interface!')


DEFAULT_DB_USER = 'skdrepo'
DEFAULT_DB_PATH = '/var/lib/firebird/2.5/data/skdrepo.fdb'

SETUP_SQL_PATH = '/usr/share/skdrepo/repository.sql'

def setup_database():
    print('In order to setup the firebird database a new firebird user must be created.')

    while True:
        db_user = raw_input('\nEnter a name for the database user (default: %s): ' % DEFAULT_DB_USER) 
        if db_user == '':
            db_user = DEFAULT_DB_USER

        while True:
            db_password = ''
            while db_password == '':
                db_password = getpass.getpass('Enter a password for %s: ' % db_user)
            db_password2 = getpass.getpass('Enter the password again: ')
            if db_password != db_password2:
                print('Passwords do not match!')
            else:
                break

        while True:
            db_path = raw_input('Enter the path of the database file to create (default: %s): ' % DEFAULT_DB_PATH)
            if db_path == '':
                db_path = DEFAULT_DB_PATH
            if os.path.isfile(db_path):
                res = yes_no_prompt('%s already exists! Do you want to overwrite it?' % db_path, default=False)
                if res:
                    os.remove(db_path)
                    break
            else:
                break

        print('\nA firebird database with the following settings will be created:')
        print('\tuser: %s' % db_user)
        print('\tpath: %s' % db_path)
        res = yes_no_prompt('\nDo you want to use these settings?')
        if res:
            break 
    
    config['db.ip'] = '127.0.0.1'
    config['db.user'] = db_user
    config['db.password'] = db_password
    config['db.path'] = db_path

    print('Setting up database %s' % db_path)
    sysdba_password = getpass.getpass('Enter the SYSDBA password: ')

    try:
        setup_sql_file = open(SETUP_SQL_PATH, 'r')
        setup_sql = setup_sql_file.read()
        setup_sql_file.close()
    except IOError, e:
        print('Failed to read sql file!')
        sys.exit(1)

    setup_sql = setup_sql.replace('DBNAME', os.path.basename(config['db.path']))
    setup_sql = setup_sql.replace('DBUSER', config['db.user'])

    cwd = os.getcwd()
    os.chdir(os.path.dirname(db_path))
    os.system('echo "de %s" | gsec -user SYSDBA -pass %s 2> /dev/null' % (db_user, sysdba_password))
    os.system('echo "add %s -pw %s" | gsec -user SYSDBA -pass %s 2> /dev/null' % (db_user, db_password, sysdba_password))
    os.system('echo "%s" | isql-fb -user SYSDBA -pass %s 2> /dev/null' % (setup_sql, sysdba_password))
    os.chdir(cwd)


DEFAULT_SERVER_IP = '0.0.0.0'
DEFAULT_SERVER_PORT = 80

def setup_config():
    print('Configuring skarphed repository...\n')

    while True:
        # TODO check for valid input
        server_ip = raw_input('Enter a listening ip for the skarphed repository (default: %s): ' % DEFAULT_SERVER_IP)
        if server_ip == '':
            server_ip = DEFAULT_SERVER_IP

        server_port = raw_input('Enter a listening port for the skarphed repository (default: %d): ' % DEFAULT_SERVER_PORT)
        if server_port == '':
            server_port = DEFAULT_SERVER_PORT 
        server_port = int(server_port)

        print('\nCurrent configuration:\n')
        print('\tlistening_ip:   %s' % server_ip)
        print('\tlistening_port: %d' % server_port)
        res = yes_no_prompt('\nDo you want to use this configuration?')
        if res:
            break

    config['server.ip'] = server_ip
    config['server.port'] = server_port
    config['session.expires'] = 7200

    config_path = raw_input('Enter a path where to save the configuration (default: /etc/skdrepo/config.json): ')
    if config_path == '':
        config_path = '/etc/skdrepo/config.json'

    if os.path.isfile(config_path):
        res = yes_no_prompt('%s already exists. Do you want to overwrite it?' % config_path, default=False)
        if not res:
            print('Setup aborted!')
            sys.exit(1)

    try:
        config_file = open(config_path, 'w')
        config_file.write(json.dumps(config))
        config_file.close()
    except IOError, e:
        print('Error writing configuration to %s:' % config_path)
        print(str(e))
        sys.exit(1)


def generate_keypair():
    print('Generating keypair...')

    key = RSA.generate(1024, os.urandom)
    pub = key.publickey().exportKey()
    priv = key.exportKey()
 
    try:
        connection = fdb.connect(
                host = config['db.ip'],
                database = config['db.path'],
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
        print 'Failed to access database!'
        sys.exit(1)


def usage():
    """
    Prints the usage description.
    """
    print('Usage: skdrepo-setup [options]')
    print('')
    print('Options:')
    print('  -h|--help                     print help information')
    print('  -v|--version                  print version')


def version():
    """
    Prints version information.
    """
    print('skdrepo-setup 0.1')
    print('')
    print('Written by Andre Kupka (freakout@skarphed.org)')


def yes_no_prompt(prompt, default=True):
    if default:
        prompt = prompt + ' [Y/n] '
    else:
        prompt = prompt + ' [y/N] '
    while True:
        s = raw_input(prompt)
        if s in ['Y', 'y']:
            return True
        elif s in ['N', 'n']:
            return False
        elif s == '':
            return default


if __name__ == '__main__':
    try:
        main()
    except EOFError, e:
        print('\nSetup aborted!')
    except KeyboardInterrupt, e:
        print('\nSetup aborted!')
