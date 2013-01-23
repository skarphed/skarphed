<?php
/*
 * qooxdoo - the new era of web development
 *
 * http://qooxdoo.org
 *
 * Copyright:
 *   2006-2009 Derrell Lipman, Christian Boulanger
 *
 * License:
 *   LGPL: http://www.gnu.org/licenses/lgpl.html
 *   EPL: http://www.eclipse.org/org/documents/epl-v10.php
 *   See the LICENSE file in the project's top-level directory for details.
 *
 * Authors:
 *  * Derrell Lipman (derrell)
 *  * Christian Boulanger (cboulanger) Error-Handling and OO-style rewrite
 */

//
// This is the entry script for rpc requests
//

/*
 * set error level
 */
error_reporting( E_ALL ^ E_NOTICE );


/*
 * start jsonrpc server
 */
require_once dirname(__FILE__) . "/server/JsonRpcServer.php";

/*
 * load Scovilleconfig
 */

$SCV_GLOBALCFG = array();
$configfile = file_get_contents("/etc/scoville/scoville.conf");
$configfile = preg_split("/\n/",$configfile);
foreach($configfile as $configline){
	if (preg_match("/^#/",$configline)){
		continue;
	}
	$linesplit = preg_split("/=/",$configline);
	$SCV_GLOBALCFG[$linesplit[0]] = $linesplit[1];
}

require_once 'instance.conf.php';

JsonRpcServer::run();
?>