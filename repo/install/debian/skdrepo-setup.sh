#!/bin/bash

DATABASE_PATH="/var/lib/firebird/2.5/data/"

yes_no_prompt() {
	while true; do
		read -p "$1" yn
		case $yn in
			[Yy]* ) return 0 ;;
			[Nn]* ) return 1 ;;
		esac
	done
}

echo "Setting firebird database ..."

yes_no_prompt "Do you want to configure the firebird SYSDBA user? [YyNn]"
if [ $? = 0 ]; then
	dpkg-reconfigure firebird2.5-super
fi

echo ""
read -s -p "Please enter you SYSDBA password: " password

echo "add SKDREPO -pw $password" | gsec -user SYSDBA -pass $password 2> /dev/null
cd $DATABASE_PATH
cat "/usr/share/skdrepo/repo_database.sql" | isql-fb -user SYSDBA -pass $password 2> /dev/null

echo "Configure Skarphed Repository ..."

repoconf="/etc/skdrepo/config.json"
mkdir -p /etc/skdrepo

conf=$(sed "s/placeholder/${password}/" $repoconf)
echo $conf > $repoconf

echo "Generating key pair ..."
keygen="/usr/share/skdrepo/gen_keypair.py"
python $keygen

echo "Don't forget to change the repositories default password via the skarphed admin interface!"
