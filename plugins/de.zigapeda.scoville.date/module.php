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
	
	public function renderJavascript(){
		return "\"interval\":null,
				\"timer\":function() {
					var date = new Date();
					var day = date.getDate();
					var mon = date.getMonth() + 1;
					var year = date.getFullYear();
				    date = ((day < 10) ? '0' : '') + day;
				    date += ((mon < 10) ? '.0' : '.') + mon;
				    date += '.' + year;
					document.getElementById(this.root).innerHTML = date;
				},
				\"init\":function() { 
					this.timer();
					this.interval = window.setInterval(this.session+'.timer()',1000);
				},
				\"destroy\":function() {
				  window.clearInterval(this.interval);
				}";
	}
	
}
?>