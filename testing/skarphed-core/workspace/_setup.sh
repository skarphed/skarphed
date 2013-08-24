#!/bin/bash

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

echo -e "Loading latest version from git ..."

rm -r skarphed
git clone https://github.com/grindhold/skarphed
git submodule init
git submodule update

echo -e "[ done ]\n"
echo -e "Assembling together installation files ..."

installerpath=skarphed/admin/installer/debian6_apache2
libpath=skarphed/core/lib
webpath=skarphed/core/web
compath=skarphed/common

mkdir install
cp $installerpath/install.sh ./install/
cp $installerpath/teardown.sh ./install/
cp $installerpath/apache2.conf ./install/
cp $installerpath/skarphed.conf ./install/
cp -r ./$libpath ./install/
cp -r ./$webpath ./install/
rm ./install/lib/common
cp -r ./$compath ./install/lib/

sed s#%\(ip\)s#127.0.0.1# install/apache2.conf > install/apache2.conf
sed s#%\(port\)s#80# install/apache2.conf > install/apache2.conf
sed s#%\(domain\)s## install/apache2.conf > install/apache2.conf
sed s#%\(subdomain\)s## install/apache2.conf > install/apache2.conf

cat <<EOF > install/config.json
{"db.password": "gYzCxYC5", "db.name": "debconf.fdb", "core.name": "debconf", "db.user": "Idw8AZKU", "core.debug": true, "db.ip": "10.40.0.10", "core.session_duration": 2, "core.session_extend": 1, "core.cookielaw": 1}
EOF

echo -e "[ done ]\n"
echo -e "Setting up a Database ..."

dbauser="SYSDBA"
dbapass="test"
dbuser="test"
dbpass="test"
schemaroot_pw="ebc7252f1fbd51e427c76c8b8e6364033b6b42e22d022ab177b3d7c7f363193469919024f72c44bcfb976a6a023ece765fc6b7cf45e4fd4b478190ed0818320f"
schemaroot_salt="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
name="testcore"
repo="repo.skarphed.org"

cp skarphed/admin/installer/_database/scvdb.sql ./
sed s#%\(USER\)s#$dbuser#g scvdb.sql > scvdb.sql
sed s#%\(PASSWORD\)s#$schemaroot_pw#g scvdb.sql > scvdb.sql
sed s#%\(SALT\)s#$schemaroot_salt#g scvdb.sql > scvdb.sql
sed s#%\(NAME\)s#/var/lib/firebird/2.5/data/$name#g scvdb.sql > scvdb.sql
sed s#%\(REPO\)s#$repo#g scvdb.sql > scvdb.sql
#sudo mv scvdb.sql /var/lib/firebird/2.5/data/

echo "add $dbuser -pw $dbpass" | gsec -user $dbauser -pass $dbapass
cat scvdb.sql | isql-fb -user $dbuser -password $dbpass
rm scvdb.sql

echo -e "[ done ]\n"
echo -e "Installing prerequisite Files ..."

sudo mkdir /etc/skarphed
sudo cp $installerpath/skarphed.conf /etc/skarphed/

echo -e "[ done ]\n"
echo -e "Executing installer ..."

cd install
sudo bash install.sh
cd ..

echo -e "[ done ]\n"
echo -e "Moving latest tests to test directory ..."

rm -r tests
cp -r skarphed/testing/skarphed-core/workspace/tests ./

echo -e "[ done ]\n"
