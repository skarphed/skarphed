qx.Class.define("scoville_admin.UserPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, user){
		this.app=app;
		this.base(arguments);
		this.setLabel(user.getParent().getParent().name+" → "+user.name);
		this.setIcon('scoville_admin/user.png');
		
		this.tabs = app.tabview;
		this.user = user;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members : {
		buildGui: function(){
			this.setLayout(new qx.ui.layout.VBox());
			//TODO: Eliminate risk of Codeinjection in next line (HTML is interpreted)!!! Search for this.user.name !
			
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Settings for User: "+this.user.name+"</span>",rich:true});
			this.add(this.heading);
			
			
			//UserInfo
			this.infobox = new qx.ui.groupbox.GroupBox("Info", "scoville_admin/user.png");
			this.infobox.setLayout(new qx.ui.layout.Basic());
			this.add(this.infobox);
			
			//Right management
			if (this.user.getServer().rightsForSession.indexOf('scoville.users.grant_revoke') != -1){
				this.permissionbox = new qx.ui.groupbox.GroupBox("Permissions/Roles", "scoville_admin/role.png");
				this.permissionbox.setLayout(new qx.ui.layout.HBox(5));
				
				this.permissionPermissionBox = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
				this.permissionRoleBox = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
				
				this.permissionbox.add(this.permissionPermissionBox,{flex:5});
				this.permissionbox.add(this.permissionRoleBox,{flex:5});
				
				this.permissionPermissionTableModel = new qx.ui.table.model.Simple();
				this.permissionPermissionTableModel.setColumns(["Active","Permission Identifier","Permission Name"]);
				this.permissionPermissionTableModel.setData([[false,"scoville.users.view","The user is allowed to view all Users!"],
															 [true ,"scoville.roles.assign","The user is allowed to assign Roles to Users"]]);
				this.permissionPermissionTable = new qx.ui.table.Table(this.permissionPermissionTableModel, {tableColumnModel : 
					                                                        function(obj){return (new qx.ui.table.columnmodel.Resize(obj));}});
				this.permissionPermissionTable.setColumnWidth(0,20);
                this.permissionPermissionTable.setColumnWidth(1,60);
                this.permissionPermissionTable.setColumnWidth(2,300);
				this.permissionPermissionLabel = new qx.ui.basic.Atom("Please choose the Permissions you want to assign to "+this.user.name+" here:", "scoville_admin/permission.png");
				this.permissionPermissionBox.add(this.permissionPermissionLabel);
				this.permissionPermissionBox.add(this.permissionPermissionTable);
				
				this.permissionRoleTableModel = new qx.ui.table.model.Simple();
				this.permissionRoleTableModel.setColumns(["Active","Role Identifier","Role Name"]);
				this.permissionRoleTableModel.setData([[false,"scoville.usermanager","The user can change every User attribute!"],
															 [true ,"scoville.rolemanager","The user can change any role"]]);
				this.permissionRoleTable = new qx.ui.table.Table(this.permissionRoleTableModel, {tableColumnModel : 
					                                                        function(obj){return (new qx.ui.table.columnmodel.Resize(obj));}});
                this.permissionRoleTable.setColumnWidth(0,20);
                this.permissionRoleTable.setColumnWidth(1,60);
                this.permissionRoleTable.setColumnWidth(2,300);
				this.permissionRoleLabel = new qx.ui.basic.Atom("Please choose the Roles you want to assign to "+this.user.name+" here:","scoville_admin/role.png");
				this.permissionRoleBox.add(this.permissionRoleLabel);
				this.permissionRoleBox.add(this.permissionRoleTable);
				
				this.add(this.permissionbox);
			}
			
			
			/*
			this.testbutton = new qx.ui.form.Button('test');
			
			this.testbutton.addListener("execute", function(e) {
		        var rpc = new qx.io.remote.Rpc("http://192.168.0.30/rpc/","scoville_admin.scvRpc");
		        rpc.setCrossDomain(true);
		        var handler= function(result,exc){
		        	if(exc == null){
		        		alert("Result of call"+result);
		        	}else{
		        		alert("Error: "+exc);
		        	}
		        };
		        rpc.callAsync(handler,"test","test");
		      });
			this.infobox.add(this.testbutton, {top:200, left:300});
			*/
			
			
	    },
		
		
		heading:null,
		app:null,
		tabs:null,
		user:null
	}
	
});
