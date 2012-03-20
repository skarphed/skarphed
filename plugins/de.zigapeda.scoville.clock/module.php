<?
class de_zigapeda_scoville_clock {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
	}
	
	public function getName(){
		return "de.zigapeda.scoville.clock";
	}
	
	public function renderHTML($moduleId, $moduleInstanceId){
		return "<div id='$moduleInstanceId' class='de_zigapeda_scoville_clock w$moduleId'></div>";
	}
	
	public function setWidgetId($widgetId){
		return 0;
	}
	
	public function renderJavascript(){
		return "\"interval\":null,
				\"timer\":function() {
					var date = new Date();
					var hours = date.getHours();
					var mins = date.getMinutes();
					var secs = date.getSeconds();
					time = hours;
					time += ((mins < 10) ? ':0' : ':') + mins;
					time += ((secs < 10) ? ':0' : ':') + secs;
					document.getElementById(this.root).innerHTML = time;
				},
				\"init\":function() { 
					this.timer();
					this.interval = window.setInterval(this.session+'.timer()',500);
				},
				\"destroy\":function() {
				  window.clearInterval(this.interval);
				}";
	}
	
}
?>