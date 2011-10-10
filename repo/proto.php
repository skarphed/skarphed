<?php
echo "<html>\n<body>";
include_once "repo_database.php";

	$con = new repo_database();
	$con->set_all("zigapeda","192.168.0.111","scvrepo.gdb","test");
	$con->connect();
	
	

	
	
//	$getin(json_decode($_REQUEST));
	$getin = $_GET;
	switch((int)$getin['a']){
		case 1:
			$resultset = $con->query("select mod_id, mod_name, mod_versionmajor, mod_versionminor, mod_revision 
				from module join (select mod_name vername 
				,max(mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_revision) ver 
				from module 
				group by mod_name) 
				on vername = mod_name 
				and ver = mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_revision");
			while($result = $con->fetchArray($resultset)){
			echo "${result["MOD_NAME"]} ${result["MOD_VERSIONMAJOR"]}.${result["MOD_VERSIONMINOR"]}.${result["MOD_REVISION"]}";
			echo "<br>";
			}
	//		return 1 + $getin['b'];	
			break;
		case 2:
			return 2;
			break;
		case 3:
			return 3;
			break;
		case 4:
			return 4;
			break;
		case 5:
			return 5;
			break;
			
	}
	



echo "</body>\n</html>";
?>