#!/bin/sh

echo "Setting firebird SYSDBA user ..."

dpkg-reconfigure firebird2.5-super

echo "Setting up firebird database ..."
echo "Please enter your SYSDBA password:"

read password
echo "add SKDREPO -pw $password" | gsec -user SYSDBA -pass $password 2> /dev/null
cd "/var/lib/firebird/2.5/data/"
cat "/usr/share/skdrepo/repo_database.sql" | isql-fb -user SYSDBA -pass $password 2> /dev/null
rm "/usr/share/skdrepo/repo_database.sql"

echo "Configure Skarphed Repository ..."

repoconf="/etc/skdrepo/config.json"
mkdir -p /etc/skdrepo

conf=$(sed "s/placeholder/${password}/" $repoconf)
echo $conf > $repoconf

echo "Generating key pair ..."
keygen="/usr/share/skdrepo/gen_keypair.py"
python $keygen
