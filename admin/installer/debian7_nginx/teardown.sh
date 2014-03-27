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
rm /etc/nginx/sites-enabled/www_scv_$instanceid 
rm /etc/nginx/sites-available/www_scv_$instanceid
rm /etc/uwsgi/apps-enabled/www_scv_$instanceid.ini

echo "    Restarting Webserver nginx"
/etc/init.d/uwsgi restart
echo "    Restarting uwsgi"
/etc/init.d/nginx restart
echo "Finished tearing down instance with ID: $instanceid..."
