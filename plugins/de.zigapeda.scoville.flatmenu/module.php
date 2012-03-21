<?
class de_zigapeda_scoville_flatmenu {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
		$this->widgetId = null;
	}
	
	public function getName(){
		return "de.zigapeda.scoville.flatmenu";
	}
	
	/**
	 * Set the widgetId
	 * 
	 * Set the id of the widget the module has to operate on
	 */
	public function setWidgetId($widgetId){
		$this->widgetId = $widgetId;	
	}
	
	public function renderHTML($moduleId, $moduleInstanceId){
	  if (!isset($this->widgetId)){
	  	return("<p>this needs to be rendered with widgetId set!</p>");
	  }
	  $db = $this->core->getDB();//HERE BE DRAGONS ↓
	  $resultset = $db->query($this,"select mnu_name
	                                       ,mni_name
	                                       ,mni_atl_id
	                                 from widgets
	                                 join sites on sit_id = wgt_sit_id
	                                 join menus on mnu_id = sit_mnu_id
	                                 join menuitems on mni_mnu_id = mnu_id
	                                 where wgt_id = $this->widgetId 
	                                 order by mni_order");
	  $text = "<div id='$moduleInstanceId' class='de_zigapeda_scoville_flatmenu w$moduleId'>";
	  while($result = $db->fetchArray($resultset)) {
	    $text .= "<a href='javascript:action(${result["MNI_ATL_ID"]}); void 0'>${result["MNI_NAME"]}</a>";
	  }
		return $text . "</div>";
	}
	
	public function renderJavascript(){
		return "\"init\":function() { 
				},
				\"destroy\":function() {
				}";
	}
	
}
?>