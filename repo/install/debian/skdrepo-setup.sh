#!/bin/bash

DB_PATH="/var/lib/firebird/2.5/data/"
DB_FILE="${DB_PATH}skdrepo.fdb"

yes_no_prompt() {
	while true; do
		read -p "$1 [Y/n] " yn
		case $yn in
			[Yy]*|"" ) return 0 ;;
			[Nn]* ) return 1 ;;
		esac
	done
}

echo "Setting up firebird database ..."

yes_no_prompt "Do you want to configure the firebird SYSDBA user?"
if [ $? = 0 ]; then
	dpkg-reconfigure firebird2.5-super
fi

read -s -p "Please enter you SYSDBA password: " password
echo ""
read -s -p "Please enter a db password: " db_password

if [ -f $DB_FILE ]; then
	echo ""
	yes_no_prompt "$DB_FILE already exists. Do you want to overwrite it?"
	create_db=$?
else
	create_db=0
fi
echo $password
echo $db_password

if [ $create_db = 0 ]; then
	rm -f "$DB_FILE"
	echo "add SKDREPO -pw $db_password" | gsec -user SYSDBA -pass $password #2> /dev/null
	cd $DB_PATH
	cat "/usr/share/skdrepo/repo_database.sql" | isql-fb -user SYSDBA -pass $password #2> /dev/null
else
	echo "Without a database the skarphed repository will not work!" >&2
	exit 1
fi

echo "Configure skarphed repository ..."

repoconf="/etc/skdrepo/config.json"
conf=$(sed "s/admin/${db_password}/" $repoconf)
echo $conf > $repoconf

echo "Generating key pair ..."
keygen="/usr/share/skdrepo/gen_keypair.py"
python $keygen

echo "Don't forget to change the repositories default password via the skarphed admin interface!"
