#!/bin/bash

deb_root="./deb/skarphed-admin/"

function generate_deb {
	# clear package build
	rm -rf ${deb_root}var
	rm -rf ${deb_root}usr
	rm -rf ${deb_root}DEBIAN

	# generate folder structure
	mkdir -p ${deb_root}DEBIAN
	mkdir -p ${deb_root}usr/bin
	mkdir -p ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin
	mkdir -p ${deb_root}usr/share/applications
	mkdir -p ${deb_root}usr/share/skarphed
	mkdir -p ${deb_root}usr/share/skarphed/corefiles
	mkdir -p ${deb_root}usr/share/locale
	mkdir -p ${deb_root}usr/share/man/man1
	mkdir -p ${deb_root}usr/share/doc/skarphed-admin
	mkdir -p ${deb_root}usr/share/icons/hicolor/16x16/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/22x22/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/24x24/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/32x32/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/36x36/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/48x48/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/64x64/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/72x72/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/96x96/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/128x128/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/192x192/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/256x256/apps
	mkdir -p ${deb_root}usr/share/icons/hicolor/scalable/apps
	mkdir -p ${deb_root}var/lib/skarphed

	# copy your files, hack your symlinks :)

	cp -r ../src/* ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/
	cp ../skarphedadmin-0.1.0.egg-info ${deb_root}usr/lib/python2.7/dist-packages/
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/skarphed.ico
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/skarphed.iss
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/setup.py
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/DEVMODE
	rm ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/common
	cp -r ../../common ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/
	touch ${deb_root}usr/lib/python2.7/dist-packages/skarphedadmin/__init__.py

	cp -r ../data/* ${deb_root}usr/share/skarphed/
	cp -r ../../core/lib ${deb_root}usr/share/skarphed/corefiles/
	rm ${deb_root}usr/share/skarphed/corefiles/lib/common
	cp -r ../../common ${deb_root}usr/share/skarphed/corefiles/lib/
	cp -r ../../core/web ${deb_root}usr/share/skarphed/corefiles/

	cp -r ../installer ${deb_root}var/lib/skarphed/

	cp -r ../locale/* ${deb_root}usr/share/locale/
	rm ${deb_root}usr/share/locale/generate_pot.sh
	
	cp -r ../bin/* ${deb_root}usr/bin/
	chmod -R 755 ${deb_root}usr/bin/

	# ICONS AND DESKTOPFILE 

	cp desktop_icons/16x16.png ${deb_root}usr/share/icons/hicolor/16x16/apps/skarphed.png
	cp desktop_icons/22x22.png ${deb_root}usr/share/icons/hicolor/22x22/apps/skarphed.png
	cp desktop_icons/24x24.png ${deb_root}usr/share/icons/hicolor/24x24/apps/skarphed.png
	cp desktop_icons/32x32.png ${deb_root}usr/share/icons/hicolor/32x32/apps/skarphed.png
	cp desktop_icons/36x36.png ${deb_root}usr/share/icons/hicolor/36x36/apps/skarphed.png
	cp desktop_icons/48x48.png ${deb_root}usr/share/icons/hicolor/48x48/apps/skarphed.png
	cp desktop_icons/64x64.png ${deb_root}usr/share/icons/hicolor/64x64/apps/skarphed.png
	cp desktop_icons/72x72.png ${deb_root}usr/share/icons/hicolor/72x72/apps/skarphed.png
	cp desktop_icons/96x96.png ${deb_root}usr/share/icons/hicolor/96x96/apps/skarphed.png
	cp desktop_icons/128x128.png ${deb_root}usr/share/icons/hicolor/128x128/apps/skarphed.png
	cp desktop_icons/192x192.png ${deb_root}usr/share/icons/hicolor/192x192/apps/skarphed.png
	cp desktop_icons/256x256.png ${deb_root}usr/share/icons/hicolor/256x256/apps/skarphed.png
	cp desktop_icons/scalable.svg ${deb_root}usr/share/icons/hicolor/scalable/apps/skarphed.svg
	cp ../skarphed-admin.desktop ${deb_root}usr/share/applications/

	# HOOKSCRIPTS

	cp deb/resources/postinst ${deb_root}DEBIAN/
	cp deb/resources/prerm ${deb_root}DEBIAN/
	sudo chown root:root ${deb_root}DEBIAN/postinst ${deb_root}DEBIAN/prerm

	# COPYRIGHTFILE

	cp deb/resources/copyright ${deb_root}usr/share/doc/skarphed-admin/copyright
	cp deb/resources/changelog ${deb_root}usr/share/doc/skarphed-admin/changelog
	gzip -9 ${deb_root}usr/share/doc/skarphed-admin/changelog

	# MANPAGE

	cp deb/resources/skarphed.1 ${deb_root}usr/share/man/man1/skarphed.1
	gzip -9 ${deb_root}usr/share/man/man1/skarphed.1

	find ${deb_root}usr -name "*.pyc" -exec rm -rf {} \;
	find ${deb_root}var -name "*.pyc" -exec rm -rf {} \;
	sudo chown -R root:root ${deb_root}usr
	sudo chown -R nobody:nogroup ${deb_root}var

	# determine size of package

	SIZE=`du -c -s ${deb_root}usr ${deb_root}var | tail -n1 |  cut -f1`

	# CONTROLFILE

	sed s/\$SIZE/$SIZE/g deb/resources/control > ${deb_root}DEBIAN/control

	#BUILDING

	dpkg-deb -z6 -Zgzip --build ${deb_root}
	sudo chown -R $USER:$USER ${deb_root}usr
	sudo chown -R $USER:$USER ${deb_root}var
	mv "./deb/skarphed-admin.deb" .
}

function generate_all {
	generate_deb
}

generate_all
