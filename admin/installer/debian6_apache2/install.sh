#!/bin/bash



if [[ -r /etc/scoville/INSTALLED ]]
then
	echo Found Scoville-Installation. Processing with Instance...
	source /etc/scoville/scoville.conf
else
	echo No Scoville-Installation found. Installing components...
	
	#external component installation

	apt-get install -y apache2 libapache2-mod-wsgi python-pip libfbclient2 python-dev

	pip install fdb pycrypto tinycss

	mkdir /etc/scoville
	cp ./scoville.conf /etc/scoville/
	source /etc/scoville/scoville.conf
	
	mkdir $SCV_LIBPATH
	cp -r ./lib/* $SCV_LIBPATH/
	chown -R www-data:www-data $SCV_LIBPATH

	touch /etc/scoville/GEN_INSTANCE
	echo -1 > /etc/scoville/GEN_INSTANCE

	rm -r /var/www
	rm /etc/apache2/sites-enabled/000-default

	touch /etc/scoville/INSTALLED

fi

instanceid=`cat /etc/scoville/GEN_INSTANCE`
instanceid=`expr $instanceid + 1`

mkdir $SCV_WEBPATH$instanceid
cp -r ./web/* $SCV_WEBPATH$instanceid/
touch $SCV_WEBPATH$instanceid/instanceconf.py
sed s#//number//#$instanceid#g ./instanceconf.py $SCV_WEBPATH$instanceid/instanceconf.py > $SCV_WEBPATH$instanceid/instanceconf.py

cp ./scoville.py $SCV_WEBPATH$instanceid/

cp ./config.json $SCV_WEBPATH$instanceid/

mkdir /tmp/scv_$instanceid
sed s#//SCVWEBROOT//#$SCV_WEBPATH$instanceid#g ./apache2.conf > /tmp/scv_$instanceid/replace
sed s#//SCVINSTANCEID//#$instanceid#g  /tmp/scv_$instanceid/replace > /etc/apache2/sites-enabled/www_scv_$instanceid
rm -r /tmp/scv_$instanceid

chown -R www-data:www-data $SCV_WEBPATH$instanceid

mkdir /var/log/apache2/www_scv_$instanceid
touch /var/log/apache2/www_scv_$instanceid/error.log
touch /var/log/apache2/www_scv_$instanceid/access.log

echo $instanceid > /etc/scoville/GEN_INSTANCE

/etc/init.d/apache2 restart

echo Installation Finished successfully.
