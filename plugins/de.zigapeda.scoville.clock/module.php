<?
class de_zigapeda_scoville_clock {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
	}
	
	public function getName(){
		return "de.zigapeda.scoville.clock";
	}
	
	public function renderHTML($moduleInstanceId){
		return "<div id='$moduleInstanceId'></div>";
	}
	
	public function renderJavascript($moduleInstanceId){
		return "var ${moduleInstanceId}interval;
		function " . $moduleInstanceId . "timer() {
	    var date = new Date();
	    var hours = date.getHours();
      var mins = date.getMinutes();
      var secs = date.getSeconds();
      time = hours;
      time += ((mins < 10) ? ':0' : ':') + mins;
      time += ((secs < 10) ? ':0' : ':') + secs;
	    document.getElementById('" . $moduleInstanceId . "').innerHTML = time;
	  }
	  
	  function " . $moduleInstanceId . "init() { 
		  " . $moduleInstanceId . "timer();
		  ${moduleInstanceId}interval = window.setInterval('" . $moduleInstanceId . "timer()',500);
	  }
	  
	  function ${moduleInstanceId}destroy() {
	    window.clearInterval(${moduleInstanceId}interval);
	  }";
	}
	
}
?>