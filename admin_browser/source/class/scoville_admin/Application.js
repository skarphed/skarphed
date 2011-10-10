/* ************************************************************************

   Copyright:

   License:

   Authors:

************************************************************************ */

/* ************************************************************************

#asset(scoville_admin/*)

************************************************************************ */

/**
 * This is the main application class of your custom application "scoville_admin"
 */
qx.Class.define("scoville_admin.Application",
{
  extend : qx.application.Standalone,



  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */

  members :
  {
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    
    addUser : function(users){
    	if (this.newUserPage == null){
    		this.newUserPage = new scoville_admin.NewUserPage(this,users);
    		this.tabview.setSelection([this.newUserPage]);
    	}else{
    	    this.tabview.setSelection([this.newUserPage]);
    	}
    },
    
    loadServer : function(ip,me,username,password){
    	//TODO: code Fuer Ajax-Request
    	var servers = this.tree.getRoot().getChildren();
    	for (var i = 0; i < servers.length; i++){
    		if (ip == servers[i].ip){
    			return 0;
    		}
    	}
    	try {
    		var servernode = new scoville_admin.Server(this,ip,username,password);
    		this.tree.getRoot().add(servernode);
    	}
    	catch(e){}
    	return 1;
    },
    
    main : function()
    {
      // Call super class
      this.base(arguments);

      // Enable logging in debug variant
      if (qx.core.Environment.get("qx.debug"))
      {
        // support native logging capabilities, e.g. Firebug for Firefox
        qx.log.appender.Native;
        // support additional cross-browser console. Press F7 to toggle visibility
        qx.log.appender.Console;
      }

      /*
      -------------------------------------------------------------------------
        Below is your actual application code...
      -------------------------------------------------------------------------
      */

      // Create a button
      this.mainpane = new qx.ui.splitpane.Pane();
      this.vbox = new qx.ui.layout.VBox();
      this.vcontainer = new qx.ui.container.Composite(this.vbox);
      this.tabview = new qx.ui.tabview.TabView();
      this.menu = new qx.ui.menubar.MenuBar();      
      this.button1 = new qx.ui.form.Button("First Button", "scoville_admin/test.png");
      this.button2 = new qx.ui.form.Button("LOL BUTTON" );
      this.testimg = new qx.ui.basic.Image("scoville_admin/config_header.png");
      
      this.tree = new qx.ui.tree.Tree();
      
      
      
      // Document is the application root
      var doc = this.getRoot();
      
      //var testseite1 = new qx.ui.tabview.Page('aha.llllo','');
      //var testseite2 = new qx.ui.tabview.Page('gnihihihilllo','');
      
      var treeroot = new qx.ui.tree.TreeFolder('Scoville Infrastructure');
      treeroot.setIcon('scoville_admin/scoville.png');
      
      
      this.treecontextmenu = new scoville_admin.TreeContextMenu(this);
      this.tree.setContextMenu(this.treecontextmenu);
      this.tree.setRoot(treeroot);
      //this.tree.hideRoot=true;
      
      //Menu
      this.men_server = new qx.ui.menu.Menu();
      this.but_server = new qx.ui.menubar.Button('Server',null,this.men_server);
      this.but_server_register_new = new qx.ui.menu.Button('Server Eintragen');
      
      this.men_server.add(this.but_server_register_new);
      this.menu.add(this.but_server);
      
      this.but_server_register_new.addListener("execute", this.createNewServerCallback(this));
      
      

      // Add button to document at fixed coordinates
      
      
      
      //this.tabview.add(testseite1);
      //this.tabview.add(testseite2);
      
      this.mainpane.add(this.tree, 1);
      this.mainpane.add(this.tabview, 4);
      this.vcontainer.add(this.testimg);
      this.vcontainer.add(this.menu);
      this.vcontainer.add(this.mainpane,{flex:1});
      doc.add(this.vcontainer, {width:'100%',height:'100%'});
      

      this.button1.addListener("execute", function(e) {
        alert("Hello World!");
      });
      
      this.loadServer('192.168.0.106','','');
      this.loadServer('192.168.0.13');
      this.loadServer('84.201.4.47');
      
    },

    createNewServerCallback: function (app){
		var f = function(e){
			new scoville_admin.NewServerPage(app);
		};
		return f;
	}
  }
});
