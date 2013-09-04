#!/usr/bin/env python

import fdb
import getopt
import getpass
import json
import os
import re
import sys
import Crypto.PublicKey.RSA as RSA


# global configuration dictionary
config = {}

def main():
    """
    Processes the single setup steps.
    """
    print('The following steps will setup the skarphed repository and the corresponding firebird database.')
    print('')
    setup_database()
    print('')
    setup_config()
    print('')
    generate_keypair()
    print('')
    print('Do not forget to change the repositories default password via admin interface!')


def exit_status(ret):
    """
    Converts to the return value of a os.system call to the corresponding unix
    exit code.
    """
    return ret >> 8


DEFAULT_DB_USER = 'skdrepo'
DEFAULT_DB_PATH = '/var/lib/firebird/2.5/data/skdrepo.fdb'

SETUP_SQL_PATH = '/usr/share/skdrepo/repository.sql'

def setup_database():
    """
    Sets up the firebird database.
    """
    print('In order to setup the firebird database a new firebird user must be created.')

    # query database configuration until it is valid and accepted by the user 
    while True:
        # query database username
        db_user = raw_input('\nEnter a name for the database user (default: %s): ' % DEFAULT_DB_USER) 
        if db_user == '':
            db_user = DEFAULT_DB_USER

        # query database new users password
        while True:
            db_password = ''
            while db_password == '':
                db_password = getpass.getpass('Enter a password for %s: ' % db_user)
            db_password2 = getpass.getpass('Enter the password again: ')
            if db_password != db_password2:
                print('Passwords do not match!')
            else:
                break

        # query database path
        while True:
            db_path = raw_input('Enter the path of the database file to create (default: %s): ' % DEFAULT_DB_PATH)
            if db_path == '':
                db_path = DEFAULT_DB_PATH
            if os.path.isfile(db_path):
                # prompt whether an existing database file should be overwritten
                res = yes_no_prompt('%s already exists! Do you want to overwrite it?' % db_path, default=False)
                if res:
                    os.remove(db_path)
                    break
            else:
                break

        print('\nA firebird database with the following settings will be created:')
        print('\tuser: %s' % db_user)
        print('\tpath: %s' % db_path)
        
        # query whether to accept the database configuration
        res = yes_no_prompt('\nDo you want to use these settings?')
        if res:
            break 
    
    # set database keys in the global configuration
    config['db.ip'] = '127.0.0.1'
    config['db.user'] = db_user
    config['db.password'] = db_password
    config['db.path'] = db_path

    # try to read the generic database scheme
    try:
        setup_sql_file = open(SETUP_SQL_PATH, 'r')
        setup_sql = setup_sql_file.read()
        setup_sql_file.close()
    except IOError, e:
        print('Failed to read sql file!')
        sys.exit(1)

    # insert the database name and user into the generic sql scheme
    setup_sql = setup_sql.replace('DBNAME', os.path.basename(config['db.path']))
    setup_sql = setup_sql.replace('DBUSER', config['db.user'])

    print('Setting up database %s' % db_path)

    # set up the database via gsec and isql-fb
    while True:
        # query database SYSDBA password
        sysdba_password = getpass.getpass('Enter the SYSDBA password: ')

        # change to the current working directory to the database path
        cwd = os.getcwd()
        os.chdir(os.path.dirname(db_path))
        # delete the database user if it already exists
        ret = os.system('echo "de %s" | gsec -user SYSDBA -pass %s 2> /dev/null' % (db_user, sysdba_password))

        # invalid SYSDBA password, gsec returns exit code 15
        if exit_status(ret) == 15:
            print('Invalid SYSDBA password, try again')
            continue

        # add the new database user with password
        ret = os.system('echo "add %s -pw %s" | gsec -user SYSDBA -pass %s 2> /dev/null' % (db_user, db_password, sysdba_password))
        if ret != 0:
            print('Failed to initialize database user, gsec returned %d!' % exit_status(ret))
            sys.exit(1)
        # initialize the database itself with the previously loaded database scheme
        ret = os.system('echo "%s" | isql-fb -user SYSDBA -pass %s 2> /dev/null' % (setup_sql, sysdba_password))
        if ret != 0:
            print('Failed to initialize database, isql-fb returned %d!' % exit_status(ret))
            sys.exit(1)

        # reset current working directory
        os.chdir(cwd)
        break


DEFAULT_SERVER_IP = '0.0.0.0'
DEFAULT_SERVER_PORT = 80

# regular expression to match an ip address
RE_IP = re.compile(r'(((\d{1,2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(2[0-4]\d)|(25[0-5]))')


def setup_config():
    """
    Setup the general skarphed repository configuration.
    """
    print('Configuring skarphed repository...\n')

    # query general configuration until it is valid and accepted by the user 
    while True:
        # query listening ip
        while True:
            server_ip = raw_input('Enter a listening ip for the skarphed repository (default: %s): ' % DEFAULT_SERVER_IP)
            if server_ip == '':
                server_ip = DEFAULT_SERVER_IP
                break
            else:
                if RE_IP.match(server_ip):
                    break
                else:
                    print('%s is not a valid ip address!' % server_ip)

        # query listening port
        while True:
            server_port = raw_input('Enter a listening port for the skarphed repository (default: %d): ' % DEFAULT_SERVER_PORT)
            if server_port == '':
                server_port = DEFAULT_SERVER_PORT 
                break
            else:
                try:
                    server_port = int(server_port)
                    if server_port >= 1 and server_port <= 65535:
                        break
                    print('Port must be in range [1,65535]!')
                except ValueError, e:
                    print('%s is not a valid port!' % server_port)

        print('\nCurrent configuration:\n')
        print('\tlistening_ip:   %s' % server_ip)
        print('\tlistening_port: %d' % server_port)

        # query whether to accept the configuration
        res = yes_no_prompt('\nDo you want to use this configuration?')
        if res:
            break

    # set general keys in the global configuration
    config['server.ip'] = server_ip
    config['server.port'] = server_port
    config['session.expires'] = 7200

    # query the path where to store the configuration
    while True:
        config_path = raw_input('Enter a path where to save the configuration (default: /etc/skdrepo/config.json): ')
        if config_path == '':
            config_path = '/etc/skdrepo/config.json'

        if os.path.isfile(config_path):
            # prompt whether an existing configuration file should be overwritten
            res = yes_no_prompt('%s already exists. Do you want to overwrite it?' % config_path, default=False)
            if res:
                break
        else:
            break

    # try to write the configuration
    try:
        config_file = open(config_path, 'w')
        config_file.write(json.dumps(config))
        config_file.close()
    except IOError, e:
        print('Error writing configuration to %s:' % config_path)
        print(str(e))
        sys.exit(1)


def generate_keypair():
    """
    Generates the repositories public/private keypair and stores it in the
    database.
    """
    print('Generating keypair...')

    # generate keypair
    key = RSA.generate(1024, os.urandom)
    pub = key.publickey().exportKey()
    priv = key.exportKey()

    try:
        # establish database connection
        connection = fdb.connect(
                host = config['db.ip'],
                database = config['db.path'],
                user = config['db.user'],
                password = config['db.password'])
        # save public key
        cursor = connection.cursor()
        cursor.execute('INSERT INTO CONFIG (PARAM, VAL) VALUES (?,?);',
                ('publickey', pub))
        connection.commit()
        # save private key
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
    """
    Prompts the user to answer a yes/no question. If nothing is entered the
    default value will be taken.
    """
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
