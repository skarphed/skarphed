<?php
namespace scv;

include_once "core.php";

class BinaryException extends \Exception {}

class Binary {
	private $id = null;
	private $mime = null;
	private $data = null;
	private $right = null;
	
	public function __construct($id, $mime, $data) {
		$this->id = $id;
		$this->mime = $mime;
		$this->data = $data;
	}
	
	public function getId() {
		return $this->id;
	}
	
	public function setId($id) {
		$this->id = $id;
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
			$dataid = $con->createBlob($data);
			$con->query($core, "insert into binarys (bin_id, bin_mime, bin_usr_id_owner, bin_usr_id_lastchange, bin_date, bin_rig_id, bin_md5, bin_data)
											values (?, ?, ?, ?, current_timestamp, ?, ?, ?);", array($this->id, $this->mime, $userid, $userid, $this->right, $md5, $dataid));
		} else {
			$md5 = md5($this->data);
			if($this->right == null) {
				$resultset = $con->query($core, "select 1 from binarys where bin_md5 = ? and bin_mime = ? and bin_rig_id is null", array($md5, $this->mime));
			} else {
				$resultset = $con->query($core, "select 1 from binarys where bin_md5 = ? and bin_mime = ? and bin_rig_id = ?", array($md5, $this->mime, $this->right));
			}
			if(!$con->fetchArray($resultset)) {
				$con->query($core, "update binarys set bin_md5 = ?, bin_mime = ?, bin_rig_id = ? where bin_id = ?", array($md5, $this->mime, $this->right, $this->id));
			}
		}
	}
	
	public static function load($id) {
		$core =  Core::getInstance();
		$con = $core->getDB();
		$resultset = $con->query($core, "select bin_mime, bin_data from binarys where bin_id = ?", array($id));
		if($result = $con->fetchArray($resultset)) {
			return new Binary($id, $result['BIN_MIME'], $result['BIN_DATA']);
		} else {
			throw new BinaryException("Data ID not found!");
		}
	}
	
	public static function loadmd5($md5) {
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
	
class Image extends Binary {
	
		public function resize($w, $h) {
	
		}
	
		public function getImageSize() {
	
		}
	
		public function generateThumbnail() {
	
		}
}

// $binaryobject = Binary::loadmd5($_GET['hs']);
// header("Content-type: $binaryobject->getMime()");
// echo $binaryobject->getData();
Binary::test();
?>