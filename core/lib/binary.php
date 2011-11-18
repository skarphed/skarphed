<?php
namespace scv;

include_once "core.php";

class Binary {
	private $id = null;
	private $data = null;
	
	public __construct($id, ) {
		
	}
	
	public getId() {
		return $this->id;
	}
	
	public setId($id) {
		$this->id = $id;
	}
	
	public getSize() {
		
	}
	
	public store() {
		
	}
	
	public getMimetype() {
		
	}
	
	public static load($id) {
		
	}
	
	public static getList() {
		
	}
}

class Image extends Binary {
	
	public resize($w, $h) {
		
	}
	
	public getImageSize() {
		
	}
	
	public generateThumbnail() {
		
	}
}
?>