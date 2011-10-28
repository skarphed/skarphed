<?
class de_zigapeda_scoville_date {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
	}
	
	public function getName(){
		return "de.zigapeda.scoville.date";
	}
	
	public function renderHTML($moduleId, $moduleInstanceId){
		return "<div id='$moduleInstanceId' class='de_zigapeda_scoville_date w$moduleId'></div>";
	}
	
	public function renderJavascript($moduleId, $moduleInstanceId){
		return "var ${moduleInstanceId}interval;
		function " . $moduleInstanceId . "timer() {
	    var date = new Date();
	    var day = date.getDate();
      var mon = date.getMonth();
      var year = date.getFullYear();
      date = ((day < 10) ? '0' : '') + day;
      date += ((mon < 10) ? '.0' : '.') + mon;
      date += '.' + year;
	    document.getElementById('" . $moduleInstanceId . "').innerHTML = date;
	  }
	  
	  function " . $moduleInstanceId . "init() { 
		  " . $moduleInstanceId . "timer();
		  ${moduleInstanceId}interval = window.setInterval('" . $moduleInstanceId . "timer()',1000);
	  }
	  
	  function ${moduleInstanceId}destroy() {
	    window.clearInterval(${moduleInstanceId}interval);
	  }";
	}
	
}
?>