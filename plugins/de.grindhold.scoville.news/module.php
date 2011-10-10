<?
class de_grindhold_scoville_news {
	private $core = null;
	
	public function __construct($core){
		$this->core = $core;
	}
	
	public function getName(){
		return "de.grindhold.scoville.news";
	}
	
	public function renderHTML($moduleInstanceId){
		return "<p> NEWS! </p>";
	}
	
	public function renderJavascript($moduleInstanceId){
		return "<script type='text/javascript'>alter('TEST');</script></p>";
	}
	
}
?>