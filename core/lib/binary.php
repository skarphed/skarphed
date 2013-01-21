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
namespace scv;

require_once "core.php";

class BinaryException extends \Exception {}

class BinaryManager extends Singleton {
	private static $instance = null;
	
	public static function getInstance(){
		if (BinaryManager::$instance==null){
			BinaryManager::$instance = new BinaryManager();
			BinaryManager::$instance->init();
		}
		return BinaryManager::$instance;
	}
	
	protected function init(){}
	
	public function create($mime, $data, $right) {
		return new Binary(null, $mime, $data, $right);
	}
	
	public function load($id) {
		$core =  Core::getInstance();
		$con = $core->getDB();
		$resultset = $con->query($core, "select bin_mime, bin_rig_id, bin_data from binarys where bin_id = ?", array($id));
		if($result = $con->fetchArray($resultset)) {
			return new Binary($id, $result['BIN_MIME'], $result['BIN_DATA'], $result['BIN_RIG_ID']);
		} else {
			throw new BinaryException("Data ID not found!");
		}
	}
		
	public function loadmd5($md5) {
		$core =  Core::getInstance();
		$con = $core->getDB();
		$resultset = $con->query($core, "select bin_id, bin_mime, bin_data from binarys where bin_md5 = ?", array($md5));
		if($result = $con->fetchArray($resultset)) {
			return new Binary($result['BIN_ID'], $result['BIN_MIME'], $result['BIN_DATA']);
		} else {
				throw new BinaryException("Data ID not found!");
		}
	}
}

class Binary {
	private $id = null;
	private $mime = null;
	private $data = null;
	private $right = null;
	
	public function __construct($id, $mime, $data, $right = null) {
		$this->id = $id;
		$this->mime = $mime;
		$this->data = $data;
		$this->right = $right;
	}
	
	public function getId() {
		return $this->id;
	}
	
	public function getMime() {
		return $this->mime;
	}
	
	public function setMime($mime) {
		$this->mime = $mime;
	}
	
	public function getData() {
		return $this->data;
	}
	
	public function setData($data) {
		$this->data = $data;
	}
	
	public function getRight() {
		return $this->right;
	}
	
	public function setRight($right) {
		$this->right = $right;
	}
	
	public function getSize() {
		return strlen($this->data);
	}
	
	public function store() {
		$core =  Core::getInstance();
		$con = $core->getDB();
		if($this->id == null) {
			$this->id = $con->getSeqNext('BIN_GEN');
			$userid = $core->getUserManager()->getSessionUserId();
			$md5 = md5($this->data);
			$dataid = $con->createBlob($this->data);
			$con->query($core, "insert into binarys (bin_id, bin_mime, bin_usr_id_owner, bin_usr_id_lastchange, bin_date_lastchange, bin_rig_id, bin_md5, bin_data)
											values (?, ?, ?, ?, current_timestamp, ?, ?, ?);", array($this->id, $this->mime, $userid, $userid, $this->right, $md5, $dataid));
		} else {
			$md5 = md5($this->data);
			if($this->right == null) {
				$resultset = $con->query($core, "select 1 from binarys where bin_md5 = ? and bin_mime = ? and bin_rig_id is null", array($md5, $this->mime));
			} else {
				$resultset = $con->query($core, "select 1 from binarys where bin_md5 = ? and bin_mime = ? and bin_rig_id = ?", array($md5, $this->mime, $this->right));
			}
			if(!$con->fetchArray($resultset)) {
				$dataid = $con->createBlob($this->data);
				$con->query($core, "update binarys set bin_md5 = ?, bin_mime = ?, bin_rig_id = ?, bin_data = ? where bin_id = ?", array($md5, $this->mime, $this->right, $dataid, $this->id));
			}
		}
	}
}
	
class Image extends Binary {
	
		public function resize($w, $h) {
	
		}
	
		public function getImageSize() {
	
		}
	
		public function generateThumbnail() {
	
		}
}

// $binaryobject = BinaryManager::loadmd5($_GET['hs']);
// header("Content-type: $binaryobject->getMime()");
// echo $binaryobject->getData();
?>