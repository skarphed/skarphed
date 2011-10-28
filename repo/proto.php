<?php
include_once "repo_database.php";

	$con = new repo_database();
	$con->set_all("zigapeda","192.168.0.109","scvrepo.gdb","test");
	$con->connect();
	//	$getin(json_decode($_REQUEST));
	$json = json_decode($_REQUEST["j"]);
//	$json = json_decode('{"c":1}');
	$command = $json->c;
//	$json = json_decode('{"m":12}');
	$module = $json->m;
	 
	switch($command){
		case 1:
			$resultset = $con->query("select mod_id, mod_hrname, mod_md5, mod_name, mod_versionmajor, mod_versionminor, mod_revision 
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
			$i=0;
			$modules = array();
			while($result = $con->fetchArray($resultset)){
//			echo "${result["MOD_NAME"]} ${result["MOD_VERSIONMAJOR"]}.${result["MOD_VERSIONMINOR"]}.${result["MOD_REVISION"]}";
//			echo "<br>";

				$modules[$i] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_HRNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_REVISION"],
									 'md5'=>$result["MOD_MD5"]);
				$i ++;			
			}
			echo json_encode(array("r"=>$modules));
			
	//		return 1 + $getin['b'];	
			break;
		case 2:
			$resultset = $con->query("select mod_name, mod_hrname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_revision from module where mod_id = '".$module."'");
			$i=0;
			$modules = array();
			while($result = $con->fetchArray($resultset)){
//			echo "${result["MOD_NAME"]} ${result["MOD_VERSIONMAJOR"]}.${result["MOD_VERSIONMINOR"]}.${result["MOD_REVISION"]}";
//				echo "<br>";

				$modules[$i] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_HRNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_REVISION"],
									 'md5'=>$result["MOD_MD5"]);
				$i ++;			
			
			}
			echo json_encode(array("r"=>$modules));
			break;
		case 3:
			$resultset = $con->query("select distinct dep_mod_dependson from dependency where dep_mod_id = ?", array($module));
			$moduleids = $module;
			while($result = $con->fetchArray($resultset)) {
				do {
					$moduleids = $moduleids.",".$result["DEP_MOD_DEPENDSON"];
				} while ($result = $con->fetchArray($resultset));
				$resultset = $con->query("select dep_mod_dependson from dependency where dep_mod_id in (" . $moduleids . ") and dep_mod_dependson not in (" . $moduleids . ")");
			}
			$resultset = $con->query("select mod_name, mod_hrname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_revision from module where mod_id in (".$moduleids.") and mod_id != ".$module);
			$i=0;
			$modules = array();
			while($result = $con->fetchArray($resultset)){
				$modules[$i] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_HRNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_REVISION"],
									 'md5'=>$result["MOD_MD5"]);
				$i ++;			
			}
			echo json_encode(array("r"=>$modules));	
			break;
		case 4:
			return 4;
			break;
		case 5:
			$resultset = $con->query("select mod_name, mod_data, mod_hrname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_revision from module where mod_id = ?", array($module));
			if($result = $con->fetchArray($resultset)) {
				$module = array('name'=>$result["MOD_NAME"],
							    'hrname'=>$result["MOD_HRNAME"],
						 	    'version_major'=>$result["MOD_VERSIONMAJOR"],
							    'version_minor'=>$result["MOD_VERSIONMINOR"],
							    'revision'=>$result["MOD_REVISION"],
							    'md5'=>$result["MOD_MD5"]);
				echo json_encode(array("r"=>$module,"data"=>base64_encode($result["MOD_DATA"])));
			}
			break;
			
	}
?>