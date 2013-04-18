#!/bin/bash

deb_root="./deb/scoville-repo/"

function generate_deb {
	cp -r ../src/* ${deb_root}var/www/scvrepo/
	cp ../gen_keypair.py ../repo_database.sql ${deb_root}tmp/
	cp ../config.json ${deb_root}etc/scvrepo/
	cp ../scvrepo_apache2 ${deb_root}etc/apache2/sites-enabled/scvrepo
	cp -r ../static ${deb_root}usr/share/scvrepo/
	cp ../templates/template.html ${deb_root}usr/share/scvrepo/
	dpkg-deb -z6 -Zgzip --build ${deb_root}
	mv "./deb/scoville-repo.deb" .
}

function generate_all {
	generate_deb
}

generate_all
