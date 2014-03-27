#!/bin/bash



if [[ -r /etc/skarphed/INSTALLED ]]
then
	echo Found Skarphed-Installation. Processing with Instance...
	source /etc/skarphed/skarphed.conf
else
	echo No Skarphed-Installation found. Installing components...
	
	#external component installation
	apt-get update
	apt-get install -y apache2 libapache2-mod-wsgi python-pip libfbclient2 python-dev python-cssutils python-crypto sudo

	pip install fdb

	mkdir /etc/skarphed
	cp ./skarphed.conf /etc/skarphed/
	source /etc/skarphed/skarphed.conf

	
	mkdir -p $SCV_LIBPATH
	cp -r ./lib/* $SCV_LIBPATH/
    cp ./skarphedcore-0.1.egg-info $SCV_LIBPATH/..
	chmod -R 755 $SCV_LIBPATH

	mkdir -p $SCV_BINARY_CACHEPATH
	chown -R www-data:www-data $SCV_BINARY_CACHEPATH

	touch /etc/skarphed/GEN_INSTANCE
	echo -1 > /etc/skarphed/GEN_INSTANCE

	rm -r /var/www
	rm /etc/apache2/sites-enabled/000-default

	touch /etc/skarphed/INSTALLED

fi

echo "Creating instanceID..."

instanceid=`cat /etc/skarphed/GEN_INSTANCE`
instanceid=`expr $instanceid + 1`

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
sed s#//SCVWEBROOT//#$SCV_WEBPATH$instanceid#g ./apache2.conf > /tmp/scv_$instanceid/replace
sed s#//SCVINSTANCEID//#$instanceid#g  /tmp/scv_$instanceid/replace > /etc/apache2/sites-available/www_scv_$instanceid
rm /etc/apache2/sites-enabled/www_scv_$instanceid
ln -s /etc/apache2/sites-available/www_scv_$instanceid /etc/apache2/sites-enabled/www_scv_$instanceid
rm -r /tmp/scv_$instanceid

echo "Transferring privileges to apache2..."
chown -R www-data:www-data $SCV_WEBPATH$instanceid

echo "Creating apache2-logfiles"
mkdir /var/log/apache2/www_scv_$instanceid
touch /var/log/apache2/www_scv_$instanceid/error.log
touch /var/log/apache2/www_scv_$instanceid/access.log

echo "Writing back current instance_id..."
echo $instanceid > /etc/skarphed/GEN_INSTANCE

echo "Restarting apache2..."
/etc/init.d/apache2 restart
echo "Starting operation daemon..."
sudo -u www-data python $SCV_WEBPATH$instanceid/operation_daemon.py start $instanceid

echo Installation Finished successfully.
