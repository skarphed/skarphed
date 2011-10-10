<?
class de_zigapeda_scoville_flatmenu {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
	}
	
	public function getName(){
		return "de.zigapeda.scoville.flatmenu";
	}
	
	public function renderHTML($moduleInstanceId){
	  $db = $this->core->getDB();
	  $resultset = $db->query($this,"select mnu_name, mni_name, mni_atl_id from widgets join sites on sit_id = wgt_sit_id join menus on mnu_id = sit_mnu_id join menuitems on mni_mnu_id = mnu_id where wgt_id = 1");
	  $text = "<div id='$moduleInstanceId'>";
	  while($result = $db->fetchArray($resultset)) {
	    $text .= "<a href='javascript:action(${result["MNI_ATL_ID"]}); void 0'>${result["MNI_NAME"]}</a>";
	  }
		return $text . "</div>";
	}
	
	public function renderJavascript($moduleInstanceId){
		return "function ${moduleInstanceId}init() {
	  }";
	}
	
}
?>