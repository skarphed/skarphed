<?php
  require '../lib/core.php';
  
  use scv;
  
  $json = json_decode($_POST['data']);
  $core = scv\Core::getInstance();
  $db = $core->getDB();
  switch($json->t) {
    case "i":
      switch($json->part) {
        case "site":
          $response = array("t"=>"m","modules"=>array());
          $resultset = $db->query($core, "select wgt_id, wgt_space, mod_name from widgets join modules on wgt_mod_id = mod_id where wgt_sit_id = ? and wgt_init = 1;", array($json->id));
          $responses = array();
          $mm = $core->getModuleManager();
          while ($result = $db->fetchArray($resultset)) {
            $module = $mm->loadModule($result['MOD_NAME']);
            $response['modules'][] = array('id'=>$result["WGT_ID"]
                ,'s'=>$result["WGT_SPACE"]
            		,'c'=>$module->renderHTML("w".$result["WGT_ID"])
            		,'j'=>$module->renderJavascript("w".$result["WGT_ID"]));
          }
          echo json_encode($response);
          break;
        case "module":
          break;
      }
      break;
    case "a":
      $resultset = $db->query($core, "select wgt_space, wgt_id, mod_name from actionlists join actions on act_atl_id = atl_id join widgets on wgt_id = act_wgt_id join modules on mod_id = wgt_mod_id where atl_id = ?;", array($json->id));
      $response = array("t"=>"m","modules"=>array());
      $responses = array();
      $mm = $core->getModuleManager();
      while ($result = $db->fetchArray($resultset)) {
        $module = $mm->loadModule($result['MOD_NAME']);
        $response['modules'][] = array('id'=>$result["WGT_ID"]
            ,'s'=>$result["WGT_SPACE"]
        		,'c'=>$module->renderHTML("w".$result["WGT_ID"])
        		,'j'=>$module->renderJavascript("w".$result["WGT_ID"]));
      }
      echo json_encode($response);
      break;
  }
?>