#!/bin/bash

echo "Gathering Information..."
instanceid=$1
source /etc/skarphed/skarphed.conf
echo "Starting to tear down instance with ID: $instanceid..."
echo "    Stopping operation_daemon"
python $SCV_WEBPATH$instanceid/operation_daemon.py stop
echo "    Removing document root $SCV_WEBPATH$instanceid"
rm -r $SCV_WEBPATH$instanceid
echo "    Removing instance-specific apacheconfig and logdata"
rm /etc/apache2/sites-enabled/www_scv_$instanceid 
rm /etc/apache2/sites-available/www_scv_$instanceid
rm -r /var/log/apache2/www_scv_$instanceid
echo "    Restarting Webserver Apache2"
/etc/init.d/apache2 restart
echo "Finished tearing down instance with ID: $instanceid..."