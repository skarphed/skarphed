#!/bin/bash

deb_root="./deb/skarphed-common/"

function generate_deb {
	# clear package build
	rm -rf ${deb_root}usr
	rm -rf ${deb_root}DEBIAN

	# generate folder structure
	mkdir -p ${deb_root}DEBIAN
	mkdir -p ${deb_root}usr/lib/python2.7/dist-packages/skarphedcommon
	mkdir -p ${deb_root}usr/share/doc/skarphed-common

	# copy your files, hack your symlinks :)

	cp -r ../skarphedcommon/* ${deb_root}usr/lib/python2.7/dist-packages/skarphedcommon/
	cp ../skarphedcommon-0.1.0.egg-info ${deb_root}usr/lib/python2.7/dist-packages/
	touch ${deb_root}usr/lib/python2.7/dist-packages/skarphedcommon/__init__.py

	# COPYRIGHTFILE

	cp deb/resources/copyright ${deb_root}usr/share/doc/skarphed-common/copyright
	cp deb/resources/changelog ${deb_root}usr/share/doc/skarphed-common/changelog
	gzip -9 ${deb_root}usr/share/doc/skarphed-common/changelog

	# MANPAGE

	find ${deb_root}usr -name "*.pyc" -exec rm -rf {} \;
	sudo chown -R root:root ${deb_root}usr

	# determine size of package

	SIZE=`du -c -s ${deb_root}usr | tail -n1 |  cut -f1`

	# CONTROLFILE

	sed s/\$SIZE/$SIZE/g deb/resources/control > ${deb_root}DEBIAN/control

	#BUILDING

	dpkg-deb -z6 -Zgzip --build ${deb_root}
	sudo chown -R $USER:$USER ${deb_root}usr
	mv "./deb/skarphed-common.deb" .
    rm -rf ${deb_root}
}

function generate_all {
	generate_deb
}

generate_all
