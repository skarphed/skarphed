<?php
###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

  global $SCV_GLOBALCFG;
  $SCV_GLOBALCFG = array();
  $configfile = file_get_contents("/etc/scoville/scoville.conf");
  $configfile = preg_split("/\n/",$configfile);
  foreach($configfile as $configline){
    if (preg_match("/^#/",$configline)){
      continue;
    }
    $linesplit = preg_split("/=/",$configline);
    $SCV_GLOBALCFG[$linesplit[0]] = $linesplit[1];
  }

  require_once 'instance.conf.php';

  require_once $SCV_GLOBALCFG['SCV_LIBPATH'].'/core.php';
  
  $request = new Request();
  
  class Request {
    
    private $json = null;
    private $core = null;
    private $db = null;
    
    public function __construct() {
      $this->json = json_decode($_POST['data']);
      $this->core = Core::getInstance();
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
			$module->setWidgetId($result['WGT_ID']);
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
		$module->setWidgetId($result['WGT_ID']);
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