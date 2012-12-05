<?php
###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################
  
  $SCV_GLOBALCFG = array();
  $configfile = file_get_contents("/etc/scoville/scoville.conf");
  $configfile = preg_split("/\n/",$configfile);
  foreach($configfile as $configline){
  	if (preg_match("/^#/",$configline)){
  		continue;
  	}
  	$linesplit = preg_split("/=/",$configline);
  	echo $linesplit[0]."<>".$linesplit[1];
  	$SCV_GLOBALCFG[$linesplit[0]] = $linesplit[1];
  }

  require 'instance.conf.php';

  require $SCV_GLOBALCFG['SCV_LIBPATH'].'/core.php';
  
  use scv;
  
  $core = scv\Core::getInstance();
  $db = $core->getDB();
  
  $moduleM = $core->getModuleManager();
  
  $cm = $core->getCompositeManager();
  $site = $cm->getFirstSite();
  echo $site->getHTML();
//   $parser = $core->getHtmlParser();
//   $parser->parseHtml();

?>