#!/bin/bash



if [[ -r /etc/skarphed/INSTALLED ]]
then
	echo Found Skarphed-Installation. Processing with Instance...
	source /etc/skarphed/skarphed.conf
else
	echo No Skarphed-Installation found. Installing components...
	
	#external component installation

	apt-get install -y apache2 libapache2-mod-wsgi python-pip libfbclient2 python-dev sudo

	pip install fdb pycrypto tinycss

	mkdir /etc/skarphed
	cp ./skarphed.conf /etc/skarphed/
	source /etc/skarphed/skarphed.conf

	
	mkdir $SCV_LIBPATH
	cp -r ./lib/* $SCV_LIBPATH/
	chown -R www-data:www-data $SCV_LIBPATH

	mkdir -p $SCV_BINARY_CACHEPATH
	chown -R www-data:www-data $SCV_BINARY_CACHEPATH

	touch /etc/skarphed/GEN_INSTANCE
	echo -1 > /etc/skarphed/GEN_INSTANCE

	rm -r /var/www
	rm /etc/apache2/sites-enabled/000-default

	touch /etc/skarphed/INSTALLED

fi

instanceid=`cat /etc/skarphed/GEN_INSTANCE`
instanceid=`expr $instanceid + 1`

mkdir $SCV_WEBPATH$instanceid
cp -r ./web/* $SCV_WEBPATH$instanceid/
echo "SCV_INSTANCE_SCOPE_ID = \"$instanceid\"" > $SCV_WEBPATH$instanceid/instanceconf.py

cp ./config.json $SCV_WEBPATH$instanceid/

mkdir /tmp/scv_$instanceid
sed s#//SCVWEBROOT//#$SCV_WEBPATH$instanceid#g ./apache2.conf > /tmp/scv_$instanceid/replace
sed s#//SCVINSTANCEID//#$instanceid#g  /tmp/scv_$instanceid/replace > /etc/apache2/sites-available/www_scv_$instanceid
rm /etc/apache2/sites-enabled/www_scv_$instanceid
ln -s /etc/apache2/sites-available/www_scv_$instanceid /etc/apache2/sites-enabled/www_scv_$instanceid
rm -r /tmp/scv_$instanceid

chown -R www-data:www-data $SCV_WEBPATH$instanceid

mkdir /var/log/apache2/www_scv_$instanceid
touch /var/log/apache2/www_scv_$instanceid/error.log
touch /var/log/apache2/www_scv_$instanceid/access.log

echo $instanceid > /etc/skarphed/GEN_INSTANCE

/etc/init.d/apache2 restart
sudo -u www-data python $SCV_WEBPATH$instanceid/operation_daemon.py start $instanceid

echo Installation Finished successfully.
