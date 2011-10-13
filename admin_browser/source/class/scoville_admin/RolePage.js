qx.Class.define("scoville_admin.RolePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app,role){
		this.app=app;
		this.base(arguments);
		this.setLabel("Role Details: ");
		this.setIcon('scoville_admin/role.png');
		
		this.tabs = app.tabview;
		this.role=role;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		this.finalUserName = "";
		
	},
	
	members : {
		
		getServer : function (){
			return this.role.getServer();
		},
		
		createOnClose : function(me){
			return function(){
				me.app.newRolePage = null;
			}
		},
		
		

		
		buildGui: function(){
			this.setLayout(new qx.ui.layout.VBox());
			//TODO: Eliminate risk of Codeinjection in next line (HTML is interpreted)!!! Search for this.user.name !
			
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Create new user:</span>",rich:true});
			this.add(this.heading);
			
			
			
			
			
			//Credentials
			this.credbox = new qx.ui.groupbox.GroupBox("Credentials", "scoville_admin/credential.png");
			this.credbox.setLayout(new qx.ui.layout.Basic());
			
			this.add(this.credbox);
			
	    },
		
		
		heading:null,
		app:null,
		tabs:null
		
	}
	
});