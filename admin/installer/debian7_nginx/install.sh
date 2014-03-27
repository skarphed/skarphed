#!/bin/bash



if [[ -r /etc/skarphed/INSTALLED ]]
then
	echo Found Skarphed-Installation. Processing with Instance...
	source /etc/skarphed/skarphed.conf
else
	echo No Skarphed-Installation found. Installing components...
	
	#external component installation
	apt-get update
	apt-get install -y nginx uwsgi uwsgi-plugin-python python-pip libfbclient2 python-dev python-cssutils python-crypto sudo

	pip install fdb

	mkdir /etc/skarphed
	cp ./skarphed.conf /etc/skarphed/
	source /etc/skarphed/skarphed.conf

	
	mkdir -p $SCV_LIBPATH
	cp -r ./lib/* $SCV_LIBPATH/
    cp ./skarphedcore-0.1.egg-info $SCV_LIBPATH/..
	chmod -R 755 $SCV_LIBPATH

    mkdir -p $SCV_MODPATH
    chown -R www-data:www-data $SCV_MODPATH
    touch $SCV_MODPATH/__init__.py
    ln -s $SCV_MODPATH $SCV_LIBPATH/modules

	mkdir -p $SCV_BINARY_CACHEPATH
	chown -R www-data:www-data $SCV_BINARY_CACHEPATH

	touch /etc/skarphed/GEN_INSTANCE
	echo -1 > /etc/skarphed/GEN_INSTANCE

	rm /etc/nginx/sites-enabled/default

	touch /etc/skarphed/INSTALLED

fi

echo "Creating instanceID..."

instanceid=`cat /etc/skarphed/GEN_INSTANCE`
instanceid=`expr $instanceid + 1`
port=`expr $instanceid + 9000`

echo "Creating cache..."
mkdir -p $SCV_BINARY_CACHEPATH/$instanceid
chown -R www-data:www-data $SCV_BINARY_CACHEPATH/$instanceid

echo "Creating web..."
mkdir $SCV_WEBPATH$instanceid
cp -r ./web/* $SCV_WEBPATH$instanceid/
echo "SCV_INSTANCE_SCOPE_ID = \"$instanceid\"" > $SCV_WEBPATH$instanceid/instanceconf.py

cp ./config.json $SCV_WEBPATH$instanceid/

echo "Writing instanceconfig..."
mkdir /tmp/scv_$instanceid
sed s#//SCVWEBROOT//#$SCV_WEBPATH$instanceid#g ./uwsgi.conf > /tmp/scv_$instanceid/replace
sed s#//PORT//#$port#g /tmp/scv_$instanceid/replace > $SCV_WEBPATH$instanceid/uwsgi.conf

ln -s $SCV_WEBPATH$instanceid/uwsgi.conf /etc/uwsgi/apps-enabled/www_scv_$instanceid.ini

sed s#//PORT//#$port#g ./nginx.conf > /etc/nginx/sites-available/www_scv_$instanceid

rm /etc/nginx/sites-enabled/www_scv_$instanceid
ln -s /etc/nginx/sites-available/www_scv_$instanceid /etc/nginx/sites-enabled/www_scv_$instanceid
rm -r /tmp/scv_$instanceid

echo "Transferring privileges to nginx..."
chown -R www-data:www-data $SCV_WEBPATH$instanceid

#TODO : see if logs for each instance are possible in nginx

echo "Writing back current instance_id..."
echo $instanceid > /etc/skarphed/GEN_INSTANCE

echo "Restarting uwsgi..."
/etc/init.d/uwsgi restart
echo "Restarting nginx..."
/etc/init.d/nginx restart
echo "Starting operation daemon..."
sudo -u www-data python $SCV_WEBPATH$instanceid/operation_daemon.py start $instanceid

echo Installation Finished successfully.
