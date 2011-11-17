<?php
include_once "repo_database.php";

	$con = new repo_database();
	$con->set_all("zigapeda","10.8.0.58","scvrepo.gdb","test");
	$con->connect();
	$json = json_decode($_REQUEST["j"]);
	if ($json==null){
		throw Exception("Invalid Json in parameter j");
	}
	$command = $json->c;
	$module = $json->m;
	 
	switch($command){
		case 1:
			$resultset = $con->query("select mod_displayname, mod_md5, mod_name, mod_versionmajor, mod_versionminor, mod_versionrev
				from modules join (select mod_name vername 
				,max(mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_versionrev) ver 
				from modules 
				group by mod_name) 
				on vername = mod_name 
				and ver = mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_versionrev");
			$i=0;
			$modules = array();
			while($result = $con->fetchArray($resultset)){
				$modules[$i] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_DISPLAYNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_VERSIONREV"],
									 'md5'=>$result["MOD_MD5"]);
				$i ++;			
			}
			echo json_encode(array("r"=>$modules));
			break;
		case 2:
			$resultset = $con->query("select mod_name, mod_displayname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules 
										where mod_name = ? ;",array($module->name));
			$modules = array();
			while($result = $con->fetchArray($resultset)){
				$modules[] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_DISPLAYNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_VERSIONREV"],
									 'md5'=>$result["MOD_MD5"]);			
			}
			echo json_encode(array("r"=>$modules));
			break;
		case 3:
			$resultset = $con->query("select mod_id from modules
										where mod_name = ? and mod_versionmajor = ? and mod_versionminor = ? and mod_versionrev = ? and mod_md5 = ? ;",
										array($module->name, $module->version_major,$module->version_minor,$module->revision,$module->md5));
			if($result = $con->fetchArray($resultset)) {
				$modid = $result['MOD_ID'];
				$resultset = $con->query("select distinct dep_mod_dependson from dependencies where dep_mod_id = ?", array($modid));
				$moduleids = $modid;
				while($result = $con->fetchArray($resultset)) {
					do {
						$moduleids = $moduleids.",".$result["DEP_MOD_DEPENDSON"];
					} while ($result = $con->fetchArray($resultset));
					$resultset = $con->query("select dep_mod_dependson from dependencies where dep_mod_id in (" . $moduleids . ") and dep_mod_dependson not in (" . $moduleids . ")");
				}
				$resultset = $con->query("select mod_name, mod_displayname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules where mod_id in (".$moduleids.") and mod_id != ".$modid);
				$modules = array();
				while($result = $con->fetchArray($resultset)){
					$modules[] = array('name'=>$result["MOD_NAME"],
										 'hrname'=>$result["MOD_DISPLAYNAME"],
										 'version_major'=>$result["MOD_VERSIONMAJOR"],
										 'version_minor'=>$result["MOD_VERSIONMINOR"],
										 'revision'=>$result["MOD_VERSIONREV"],
										 'md5'=>$result["MOD_MD5"]);	
				}
				echo json_encode(array("r"=>$modules));
			}
			break;
		case 4:
			$resultset = $con->query("select mod_id from modules
										where mod_name = ? and mod_versionmajor = ? and mod_versionminor = ? and mod_versionrev = ? and mod_md5 = ? ;",
										array($module->name, $module->version_major,$module->version_minor,$module->revision,$module->md5));
			if($result = $con->fetchArray($resultset)) {
				$modid = $result['MOD_ID'];
				$resultset = $con->query("select distinct dep_mod_id from dependencies where dep_mod_dependson = ?", array($modid));
				$moduleids = $modid;
				while($result = $con->fetchArray($resultset)) {
					do {
						$moduleids = $moduleids.",".$result["DEP_MOD_ID"];
					} while ($result = $con->fetchArray($resultset));
					$resultset = $con->query("select dep_mod_id from dependencies where dep_mod_dependson in (" . $moduleids . ") and dep_mod_id not in (" . $moduleids . ")");
				}
				$resultset = $con->query("select mod_name, mod_displayname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules where mod_id in (".$moduleids.") and mod_id != ".$modid);
				$modules = array();
				while($result = $con->fetchArray($resultset)){
					$modules[] = array('name'=>$result["MOD_NAME"],
										 'hrname'=>$result["MOD_DISPLAYNAME"],
										 'version_major'=>$result["MOD_VERSIONMAJOR"],
										 'version_minor'=>$result["MOD_VERSIONMINOR"],
										 'revision'=>$result["MOD_VERSIONREV"],
										 'md5'=>$result["MOD_MD5"]);	
				}
				echo json_encode(array("r"=>$modules));
			}
			break;
		case 5:
			$resultset = $con->query("select mod_name, mod_data, mod_displayname, mod_md5, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules 
									where mod_name = ? and mod_versionmajor = ? and mod_versionminor = ? and mod_versionrev = ? and mod_md5 = ? ;",
									array($module->name, $module->version_major,$module->version_minor,$module->revision,$module->md5));
			if($result = $con->fetchArray($resultset)) {
				$module = array('name'=>$result["MOD_NAME"],
							    'hrname'=>$result["MOD_DISPLAYNAME"],
						 	    'version_major'=>$result["MOD_VERSIONMAJOR"],
							    'version_minor'=>$result["MOD_VERSIONMINOR"],
							    'revision'=>$result["MOD_VERSIONREV"],
							    'md5'=>$result["MOD_MD5"]);
				echo json_encode(array("r"=>$module,"data"=>base64_encode($result["MOD_DATA"])));
			}
			break;
			
	}
?>