<?
class de_zigapeda_scoville_date {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
	}
	
	public function getName(){
		return "de.zigapeda.scoville.date";
	}
	
	public function renderHTML($moduleInstanceId){
		return "<div id='$moduleInstanceId'></div>";
	}
	
	public function renderJavascript($moduleInstanceId){
		return "function " . $moduleInstanceId . "timer() {
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
		  window.setInterval('" . $moduleInstanceId . "timer()',1000);
	  }";
	}
	
}
?>