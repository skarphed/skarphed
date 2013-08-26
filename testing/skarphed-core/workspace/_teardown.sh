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

echo -e "Tearing down instance ..."

cd install
sudo bash teardown.sh 0
cd ..

echo -e "[ done ]\n"
echo -e "Tearing down database ..."

dbauser="SYSDBA"
dbapass="test"
dbuser="test"
sudo rm /var/lib/firebird/2.5/data/testcore.fdb
echo "delete $dbuser" | gsec -user $dbauser -pass $dbapass

echo -e "[ done ]\n"
echo -e "Tearing down files ..."
rm -rf skarphed
rm -rf install
sudo rm -rf /etc/skarphed
sudo rm -rf /usr/lib/skarphed
