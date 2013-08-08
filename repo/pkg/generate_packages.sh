#!/bin/bash

deb_web_root="./deb/skdrepo-web/"

function generate_deb_web {
	# generate folder structure
	mkdir -p ${deb_web_root}var/www/skdrepo
	mkdir -p ${deb_web_root}tmp/
	mkdir -p ${deb_web_root}etc/skdrepo
	mkdir -p ${deb_web_root}etc/apache2/sites-enabled/skdrepo
	mkdir -p ${deb_web_root}usr/share/skdrepo

	# copy your files, hack your symlinks :)
	rm -rf ${deb_web_root}var/www/skdrepo/common
	cp -r ../src/* ${deb_web_root}var/www/skdrepo/
	rm  ${deb_web_root}var/www/skdrepo/common
	mkdir -p ${deb_web_root}var/www/skdrepo/common
	cp -r ../src/common/* ${deb_web_root}var/www/skdrepo/common/
	cp ../gen_keypair.py ../repo_database.sql ${deb_web_root}tmp
	cp ../config.json ${deb_web_root}etc/skdrepo/
	cp ../skdrepo_apache2 ${deb_web_root}etc/apache2/sites-enabled/skdrepo
	cp -r ../static ${deb_web_root}usr/share/skdrepo/
	cp ../templates/template.html ${deb_web_root}usr/share/skdrepo/


	SIZE=`du -c -s ${deb_web_root}etc ${deb_web_root}tmp ${deb_web_root}usr ${deb_web_root}var | tail -n1 |  cut -f1`
	cat << EOF > ${deb_web_root}DEBIAN/control
Package: skdrepo-web
Priority: optional
Section: web
Installed-Size: $SIZE
Maintainer: Andre Kupka <freakout@skarphed.org>
Architecture: all
Version: 0.1
Depends: firebird2.5-super (>= 2.5), apache2 (>= 2.2), libapache2-mod-wsgi (>= 3.3), python (>= 2.6), python-pip (>= 0.7), python-dev (>= 2.6)
Description: A Skarphed Repository
EOF

	fakeroot dpkg-deb -z6 -Zgzip --build ${deb_web_root}
	mv "./deb/skdrepo-web.deb" .
}

deb_root="./deb/skdrepo/"

function generate_deb {
	mkdir -p ${deb_root}tmp/
	mkdir -p ${deb_root}etc/skdrepo
	mkdir -p ${deb_root}usr/share/skdrepo/
	mkdir -p ${deb_root}usr/bin
	mkdir -p ${deb_root}etc/init.d/

	rm -rf ${deb_root}usr/share/skdrepo/common
	cp -r ../src/* ${deb_root}usr/share/skdrepo/
	rm ${deb_root}usr/share/skdrepo/skdrepo.py
	cp ../src/skdrepo.py ${deb_root}usr/bin/skdrepo
	rm  ${deb_root}usr/share/skdrepo/common
	mkdir -p ${deb_root}usr/share/skdrepo/common
	cp -r ../skdrepo ${deb_root}etc/init.d/
	cp -r ../src/common/* ${deb_root}usr/share/skdrepo/common/
	cp ../gen_keypair.py ../repo_database.sql ${deb_root}tmp
	cp ../config.json ${deb_root}etc/skdrepo/
	cp -r ../static ${deb_root}usr/share/skdrepo/
	cp ../templates/template.html ${deb_root}usr/share/skdrepo/

	SIZE=`du -c -s ${deb_root}etc ${deb_root}tmp ${deb_root}usr | tail -n1 |  cut -f1`
	cat << EOF > ${deb_root}DEBIAN/control
Package: skdrepo
Priority: optional
Section: web
Installed-Size: $SIZE
Maintainer: Andre Kupka <freakout@skarphed.org>
Architecture: all
Version: 0.1
Depends: firebird2.5-super (>= 2.5), python (>= 2.6), python-pip (>= 0.7), python-dev (>= 2.6)
Description: A Skarphed Repository
EOF

	fakeroot dpkg-deb -z6 -Zgzip --build ${deb_root}
	mv "./deb/skdrepo.deb" .
}

function generate_all {
	generate_deb
	generate_deb_web
}

generate_all
