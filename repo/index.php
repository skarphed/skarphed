<?php 
	include_once "repo_database.php";
	
	function rrmdir($dir) {
		if (is_dir($dir)) {
			$objects = scandir($dir);
			foreach ($objects as $object) {
				if ($object != "." && $object != "..") {
					if (filetype($dir."/".$object) == "dir") rrmdir($dir."/".$object); else unlink($dir."/".$object);
				}
			}
			reset($objects);
			rmdir($dir);
		}
	}
	
	echo "<!DOCTYPE html>";
	echo "<html>";
	echo "  <head>";
	echo "    <title>Module Uploader</title>";
	echo "  </head>";
	echo "  <body>";
	if($_REQUEST['upload'] != null) {
		$uploaddir = './uploads';
		if(!is_dir($uploaddir)) {
			mkdir($uploaddir);
		}
		$uploadfile = $uploaddir . "/" . $_FILES['data']['name'];
		if (move_uploaded_file($_FILES['data']['tmp_name'], $uploadfile)) {
			echo "    <h2>Uploaded:</h2>";
			$extractdir = substr($uploadfile,0,-7);
			system('mkdir '.$extractdir." > /dev/null");
			system('tar xfz '.$uploadfile.' -C '.$extractdir.'/ > /dev/null');
			$manifestRaw = file_get_contents($extractdir.'/manifest.json');
			if ($manifestRaw == false){
				echo "    <p>error while reading manifest</p>";
			} else {
				$manifest = json_decode($manifestRaw);
				if ($manifest == null){
					echo "    <p>error while parsing manifest</p>";
				} else {
					echo "    <p>Name: ".$manifest->name."</p>";
					echo "    <p>HR Name: ".$manifest->hrname."</p>";
					echo "    <p>Version: ".$manifest->version_major.".".$manifest->version_minor.".".$manifest->revision."</p>";
					$con = new repo_database();
					$con->set_all("zigapeda","10.8.0.58","scvrepo.gdb","test");
					$con->connect();
					$mod_id = $con->getSeqNext("MOD_GEN");
					$md5 = md5_file($uploadfile);
					$file = fopen($uploadfile, 'r');
					$data = fread($file, filesize($uploadfile));
					$blobid = $con->createBlob($data);
					$con->query("insert into modules (mod_id, mod_name, mod_displayname, mod_versionmajor, mod_versionminor, mod_versionrev, mod_md5, mod_data) 
					                          values (?, ?, ?, ?, ?, ?, ?, ?)",
					                          array($mod_id, $manifest->name, $manifest->hrname, $manifest->version_major, $manifest->version_minor, $manifest->revision, $md5, $blobid));
					echo "    <p>MD%: ".$md5."</p>";
				}
			}
			echo "    <a href='index.php'>Zurueck zum Uploaddialog</a>";
			rrmdir($extractdir);
			unlink($uploadfile);
		}
	} else {
		echo "    <form enctype='multipart/form-data' method='POST' action='index.php'>";
		echo "      <h2>Modul waehlen:</h2>";
		echo "      <input type='file' name='data'><br>";
		echo "      <input type='submit' name='upload' value='Hochladen'>";
		echo "    </form>";
	}
	echo "  </body>";
	echo "</html>";
?>