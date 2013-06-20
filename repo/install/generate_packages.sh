#!/bin/bash

deb_root="./deb/skarphed-repo/"

function generate_deb {
	# generate folder structure
	mkdir -p ${deb_root}var/www/skdrepo
	mkdir -p ${deb_root}tmp/
	mkdir -p ${deb_root}etc/skdrepo
	mkdir -p ${deb_root}etc/apache2/sites-enabled/skdrepo
	mkdir -p ${deb_root}usr/share/skdrepo

	# copy your files, hack your symlinks :)
	rm -rf ${deb_root}var/www/skdrepo/common
	cp -r ../src/* ${deb_root}var/www/skdrepo/
	rm  ${deb_root}var/www/skdrepo/common
	mkdir -p ${deb_root}var/www/skdrepo/common
	cp -r ../src/common/* ${deb_root}var/www/skdrepo/common/
	cp ../gen_keypair.py ../repo_database.sql ${deb_root}tmp
	cp ../config.json ${deb_root}etc/skdrepo/
	cp ../skdrepo_apache2 ${deb_root}etc/apache2/sites-enabled/skdrepo
	cp -r ../static ${deb_root}usr/share/skdrepo/
	cp ../templates/template.html ${deb_root}usr/share/skdrepo/
	dpkg-deb -z6 -Zgzip --build ${deb_root}
	mv "./deb/skarphed-repo.deb" .
}

function generate_all {
	generate_deb
}

generate_all
