#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


import getopt
import sys
sys.path.append('/usr/share/skdrepo/')

from wsgiref.simple_server import make_server

from config import Config
from logger import logger
import wsgi





def main():
    """
    Executes a skdrepo as standalone application. 
    """

    # set default values
    config_path = '/etc/skdrepo/config.json'

    # parse commandline arguments
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'hvc:',
                ['help', 'version', 'config='])
    except getopt.GetoptError, e:
        print(str(e))
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
            sys.exit()
        if o in ['-v', '--version']:
            version()
            sys.exit()
        elif o in ['-c', '--config']:
            config_path = a
        else:
            assert False, 'Unhandled option!'

    # initialize global configuration
    config = Config()
    try:
        config.load_from_file(config_path)
    except IOError, e:
        logger.error('Failed to open configuration file: %s' % config_path)
        sys.exit(1)

    # start skdrepo wsgi server
    listen_ip = config['server.ip']
    listen_port = config['server.port']

    logger.info('Skarphed repository listening on %s:%d' % (listen_ip, listen_port))
    httpd = make_server(listen_ip, listen_port, wsgi.application)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt, e:
        pass


def usage():
    """
    Prints the usage description.
    """
    print('Usage: skdrepo [options]')
    print('')
    print('Options:')
    print('  -h|--help                     print help information')
    print('  -v|--version                  print version')
    print('  -c|--config <path>            specify a configuration file')


def version():
    """
    Prints version information.
    """
    print('skdrepo 0.1')
    print('')
    print('Written by Andre Kupka (freakout@skarphed.org)')


if __name__ == '__main__':
    main()
