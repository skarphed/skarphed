qx.Class.define("scoville_admin.NewServerPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app){
		this.app=app;
		this.base(arguments);
		this.setLabel("New Server");
		this.setIcon('scoville_admin/server.png');
		
		this.tabs = app.tabview;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		buttonEnter:null,
		buttonCancel:null,
		label:null,
		ipentry:null,
		infobox:null,
		infolabel:null,
		heading:null,
				
		buildGui : function (){
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Enter new server</span>",rich:true});
			
			this.infobox = new qx.ui.groupbox.GroupBox("Credentials", "scoville_admin/server.png");
			this.infobox.setLayout(new qx.ui.layout.Basic());
			this.setLayout(new qx.ui.layout.VBox());
			this.buttonEnter = new qx.ui.form.Button("Add Server");
			this.buttonCancel = new qx.ui.form.Button("Cancel");
			this.infolabel = new qx.ui.basic.Label("Please enter your credentials for a Scoville server here!");
			this.iplabel = new qx.ui.basic.Label("Server IP or Hostname:");
			this.ipentry = new qx.ui.form.TextField();
			this.userlabel = new qx.ui.basic.Label("Username:");
			this.userentry = new qx.ui.form.TextField();
			this.passwordlabel = new qx.ui.basic.Label("Password:");
			this.passwordentry = new qx.ui.form.PasswordField();
			
			this.buttonEnter.addListener("execute", this.enterNewServerCallback(this));
			this.buttonCancel.addListener("execute", this.cancelCallback(this));
			this.infobox.add(this.infolabel,{top:10,left:100});
			this.infobox.add(this.iplabel,{top:50,left:100});
			this.infobox.add(this.ipentry,{top:50,left:250});
			this.infobox.add(this.userlabel,{top:75,left:100});
			this.infobox.add(this.userentry,{top:75,left:250});
			this.infobox.add(this.passwordlabel,{top:100,left:100});
			this.infobox.add(this.passwordentry,{top:100,left:250});
			this.infobox.add(this.buttonCancel,{top:125,left:100});
			this.infobox.add(this.buttonEnter,{top:125, left:250});
			this.add(this.heading);
			this.add(this.infobox);
		},
		
		enterNewServer : function(){
			
		},
		
		cancelCallback: function(me){
			return function(){
				me.tabs.remove(me);
			}
		},
		
		enterNewServerCallback : function(me){
			var r = function(){
			  var raw_ip = me.ipentry.getValue();
			  var username = me.userentry.getValue();
			  var password = me.passwordentry.getValue();
			  me.app.loadServer(raw_ip,me,username,password);
			  me.app.storeServerlistCookie();
			  me.tabs.remove(me);
			};
			return r;
		}
		
		
	}
});
