#!/bin/bash



if [[ -r /etc/scoville/INSTALLED ]]
then
	echo Found Scoville-Installation. Processing with Instance...
	source /etc/scoville/scoville.conf
else
	echo No Scoville-Installation found. Installing components...
	
	#external component installation

	apt-get install -y apache2 php5-interbase php-pear

	pear channel-discover phpseclib.sourceforge.net
	pear remote-list -c phpseclib
	pear install phpseclib/Crypt_RSA-0.3.1 #version unbedingt noetig?

	mkdir /etc/scoville
	cp ./scoville.conf /etc/scoville/
	source /etc/scoville/scoville.conf
	
	mkdir $SCV_LIBPATH
	cp -r ./lib/* $SCV_LIBPATH/

	touch /etc/scoville/GEN_INSTANCE
	echo -1 > /etc/scoville/GEN_INSTANCE

	rm -r /var/www
	rm -r /etc/apache/sites-enabled/000-default

	touch /etc/scoville/INSTALLED

fi

instanceid=`cat /etc/scoville/GEN_INSTANCE`
instanceid=`expr $instanceid + 1`

mkdir $SCV_WEBPATH$instanceid
cp -r ./web/ $SCV_WEBPATH$instanceid/
touch $SCV_WEBPATH$instanceid/web/instance.conf.php
sed s#//number//#$instanceid#g ./instance.conf.php $SCV_WEBPATH$instanceid/web/instance.conf.php > $SCV_WEBPATH$instanceid/web/instance.conf.php

cp ./index.php $SCV_WEBPATH$instanceid/

cp ./config.json $SCV_WEBPATH$instanceid/web/
cp -r ./rpc/ $SCV_WEBPATH$instanceid/
cp $SCV_WEBPATH$instanceid/web/instance.conf.php $SCV_WEBPATH$instanceid/rpc/instance.conf.php

mkdir /tmp/scv_$instanceid
sed s#//SCVWEBROOT//#$SCV_WEBPATH$instanceid#g ./apache2.conf > /tmp/scv_$instanceid/replace
sed s#//SCVINSTANCEID//#$instanceid#g  /tmp/scv_$instanceid/replace > /etc/apache2/sites-enabled/www_scv_$instanceid
rm -r /tmp/scv_$instanceid

mkdir /var/log/apache2/www_scv_$instanceid
touch /var/log/apache2/www_scv_$instanceid/error.log
touch /var/log/apache2/www_scv_$instanceid/access.log


/etc/init.d/apache2 restart

echo $instanceid > /etc/scoville/GEN_INSTANCE

echo Installation Finished successfully.





