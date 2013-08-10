#!/bin/bash

deb_root="./deb/skdrepo/"

function generate_deb {
	rm -rf ${deb_root}usr
	rm -rf ${deb_root}etc

	mkdir -p ${deb_root}etc/init.d
	mkdir -p ${deb_root}etc/skdrepo
	mkdir -p ${deb_root}usr/share/skdrepo
	mkdir -p ${deb_root}usr/bin

	# code
	cp -r ../src/*.py ${deb_root}usr/share/skdrepo/
	rm ${deb_root}usr/share/skdrepo/skdrepo.py
	cp ../src/skdrepo.py ${deb_root}usr/bin/skdrepo
	mkdir -p ${deb_root}usr/share/skdrepo/common
	cp -r ../src/common/*.py ${deb_root}usr/share/skdrepo/common/

	# database
	cp ../repo_database.sql ${deb_root}usr/share/skdrepo/

	# setup
	cp ../install/debian/skdrepo-setup.py ${deb_root}usr/bin/skdrepo-setup

	# static
	cp ../templates/template.html ${deb_root}usr/share/skdrepo/
	cp -r ../static ${deb_root}usr/share/skdrepo/

	# config
	cp ../config.json ${deb_root}etc/skdrepo/

	# init script
	cp ../skdrepo.init ${deb_root}etc/init.d/skdrepo

	SIZE=`du -c -s ${deb_root}etc ${deb_root}usr | tail -n1 |  cut -f1`
	cat << EOF > ${deb_root}DEBIAN/control
Package: skdrepo
Priority: optional
Section: web
Installed-Size: $SIZE
Maintainer: Andre Kupka <freakout@skarphed.org>
Architecture: all
Version: 0.1
Depends: firebird2.5-super (>= 2.5), python (>= 2.6), python-pip (>= 0.7), python-dev (>= 2.6)
Description: A skarphed repository
 A repository that manages skarphed modules and templates.
EOF

	fakeroot dpkg-deb -z6 -Zgzip --build ${deb_root}
	mv "./deb/skdrepo.deb" .
}

generate_deb
