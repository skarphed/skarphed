#!/bin/bash

deb_root="./deb/skarphed-admin/"

function generate_deb {
	# clear package build
	rm -rf ${deb_root}usr
	rm -rf ${deb_root}DEBIAN

	# generate folder structure
	mkdir -p ${deb_root}DEBIAN
	mkdir -p ${deb_root}usr/bin
	mkdir -p ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin
	mkdir -p ${deb_root}usr/share/skarphed
	mkdir -p ${deb_root}usr/share/locale
	
	# copy your files, hack your symlinks :)

	cp -r ../src/* ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/
	cp ../skarphedadmin-0.1.0.egg-info ${deb_root}usr/lib/python2.7/dist-packages/
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/skarphed.ico
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/skarphed.iss
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/setup.py
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/DEVMODE
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/common
	cp -r ../../common ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/

	cp -r ../data/* ${deb_root}usr/share/skarphed/

	cp -r ../installer ${deb_root}usr/share/skarphed/

	cp -r ../locale/* ${deb_root}usr/share/locale/
	rm ${deb_root}usr/share/locale/generate_pot.sh
	
	cp -r ../bin/* ${deb_root}usr/bin/

	# determine size of package

	SIZE=`du -c -s ${deb_root}usr | tail -n1 |  cut -f1`
	cat << EOF > ${deb_root}DEBIAN/control
Package: skarphed-admin
Priority: optional
Section: web
Installed-Size: $SIZE
Maintainer: Daniel Brendle <grindhold@gmx.net>
Architecture: all
Version: 0.1
Depends: python (>= 2.6), python-paramiko (>= 1.7), python-crypto (>= 2.1)
Description: A webmanagement system.
EOF

	dpkg-deb -z6 -Zgzip --build ${deb_root}
	mv "./deb/skarphed-admin.deb" .
}

function generate_all {
	generate_deb
}

generate_all
