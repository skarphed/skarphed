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

	session_start();
	
	if (isset($_REQUEST['j'])){
		require_once('protocolhandler.php');
		try{
			$protocolHandler = new ProtocolHandler($_REQUEST['j']);
			$protocolHandler->execute();
			echo $protocolHandler->getResult();
		} catch (Exception $e) {
			echo '{"error": "'.$e->getMessage().'"}';
		}
	}else{
		require_once('repository.php');
		$repository = Repository::getInstance();
?>
<!DOCTYPE HTML>
<html>
	<head>
		<title>Scoville Repository</title>
		<meta name="description" content="Scoville Repository">
		<meta name="author" content="Scoville">
		<style type="text/css">
			body {
			  padding: 0px;
			  margin: 0px;
			  background-color: #e1e1e1;
				font-family:Arial,Helvetica,Verdana;
				color: #555;
				font-size:12px;
			}
			
			a {
				color:#666;
			}
			
			a:hover{
				color:#777;
			}
			
			div#head {
			  height: 100px;
			  background:-moz-linear-gradient(top, #b7b7b7, #e1e1e1);
			  background:-webkit-gradient(linear, left top, left bottom, from(#b7b7b7), to(#e1e1e1)); 
			}
			
			div#left {
			  position: absolute;
			  top: 100px;
			  left: 0px;
			  width: 160px;
			  bottom: 0px;
				margin-left:3px;
			}
			
			div#content {
			  position: absolute;
			  width: 600px;
			  top: 100px;
			  left: 162px;
			  right: 0px;
			  bottom: 0px;
			  border-left: 1px solid silver;
				padding-left:20px;
			}
			
			div#login {
			  width: 250px;
			  margin-top: 100px;
			  margin-left: 100px;
			  text-align: right;
			}
			
			div#login input[type=submit] {
			  margin-right: 50px;
			}
			
			div.info{
				border: 1px dashed silver;
				text-align:left;
			}
			
			p.info{
				 text-align:left;
				 line-height: 200%;
			 }
			
			p{
				 text-align:justify;
				 line-height: 200%;
			}
		</style>
	</head>
	<body>
		<div id="head">
	    	<a id="begin"><img src="repo.png"></a>
	    </div>
	    <div id="left">
		    <p>Scoville Repository<br></p>		
	    </div>
	    <div id="content">
	    	<p>
	    		This is a Scoville repository. It supplies Modules and Templates for Scoville Instances.
	    	</p>
	    	<p>
		    	The data provided is signed via RSA to ensure that there is no manipulated data coming onto
		    	your server.
	    	</p>
	    	
	    	<div class="info" style="font-family: Monospace;">
	    		<h5>This repository's RSA public key is:</h5>
	    		<p><?php echo $repository->getPublicKeyForPage(); ?></p>
	    	</div>
	    	<p>
	    		Register this Repository with your Scoville Admintool if you trust the maintainer.
	    	</p>
	    </div>
	</body>
	
</html>		
<?php
	}
?>