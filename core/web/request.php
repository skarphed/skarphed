<?php
  require '../lib/core.php';
  
  use scv;
  
  $request = new Request();
  
  class Request {
    
    private $json = null;
    private $core = null;
    private $db = null;
    
    public function __construct() {
      $this->json = json_decode($_POST['data']);
      $this->core = scv\Core::getInstance();
      $this->db = $this->core->getDB();
      switch($this->json->t) {
        case "i":
          $this->ajaxinit();
          break;
        case "a":
          $this->ajaxaction();
          break;
      }
    }
    
    /**
      * Ajax Initialisation
      *
      * Is called if the ajax framework sends an init command to the server.
      *
      */
    private function ajaxinit() {
      switch($this->json->part) {
        case "site":
          $response = array("t"=>"m","modules"=>array());
          $resultset = $this->db->query($this->core, "select wgt_id
                                                            ,wgt_space
                                                            ,mod_name
                                                      from widgets
                                                      join modules on wgt_mod_id = mod_id
                                                      where wgt_sit_id = ?
                                                        and wgt_space is not null;", array($this->json->id));
          $responses = array();
          $mm = $this->core->getModuleManager();
          while ($result = $this->db->fetchArray($resultset)) {
            $module = $mm->loadModule($result['MOD_NAME']);
            $space = "s".$result["WGT_SPACE"];
            $widget = "w".$result["WGT_ID"];
            $response['modules'][] = array('id'=>$result["WGT_ID"]
            ,'s'=>$result["WGT_SPACE"]
            ,'c'=>$module->renderHTML($result["WGT_ID"],"s".$result["WGT_SPACE"]."w".$result["WGT_ID"])
            ,'j'=>"var $space$widget = {\"root\":\"$space\",\"widget\":\"$widget\",\"session\":\"$space$widget\",".$module->renderJavascript()."};"
			);
          }
          echo json_encode($response);
          break;
        case "module":
          break;
      }
    }
    
    
    /**
      * Ajax Action Request
      *
      * Is called if the ajax framework sends an action command to the server.
      *
      */
    private function ajaxaction() {
      //TODO nur provisorisch implementiert
      $resultset = $this->db->query($this->core, "select act_space
                                                        ,wgt_id
                                                        ,mod_name
                                                  from actionlists
                                                  join actions on act_atl_id = atl_id
                                                  join widgets on wgt_id = act_wgt_id
                                                  join modules on mod_id = wgt_mod_id
                                                  where atl_id = ?;", array($this->json->id));
      $response = array("t"=>"m","modules"=>array());
      $responses = array();
      $mm = $this->core->getModuleManager();
      while ($result = $this->db->fetchArray($resultset)) {
        $module = $mm->loadModule($result['MOD_NAME']);
        $space = "s".$result["ACT_SPACE"];
        $widget = "w".$result["WGT_ID"];
        $response['modules'][] = array('id'=>$result["WGT_ID"]
        ,'s'=>$result["ACT_SPACE"]
        ,'c'=>$module->renderHTML($result["WGT_ID"],"s".$result["ACT_SPACE"]."w".$result["WGT_ID"])
        ,'j'=>"var $space$widget = {\"root\":\"$space\",\"widget\":\"$widget\",\"session\":\"$space$widget\",".$module->renderJavascript()."};"
        );
      }
      echo json_encode($response);
    }
  }
?>