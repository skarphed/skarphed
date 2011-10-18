qx.Class.define("scoville_admin.NewRolePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app,roles){
		this.app=app;
		this.base(arguments);
		this.setLabel("New Role");
		this.setIcon('scoville_admin/role.png');
		
		this.tabs = app.tabview;
		this.roles = roles;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		this.finalUserName = "";
		
	},
	
	members : {
		
		getServer : function (){
			return this.roles.getParent();
		},
		
		createOnClose : function(me){
			return function(){
				me.app.newRolePage = null;
			}
		},
		
		
		createFinishedCallback: function(me){
			return function(result, exc){
				if (exc == null){
					if (typeof(result) == "number"){
						var role = new scoville_admin.Role(me.app, {'name':me.finalRoleName,'id':result});
						me.roles.add(role);
						me.app.newUserPage=null;
						me.app.tabview.remove(me);
					}else{
						alert("FFFUUUUU");
					}
				}else{
					alert (exc);
				}
			}
		},
		
		createSaveCallback: function(me){
			return function(){
				me.savebutton.setEnabled(false);
				me.savebutton.setLabel("Checking...");
				me.validator.validate();
			}
		},
		
		createValidatedCallback: function(me){
			return function(){
				me.savebutton.setEnabled(true);
				me.savebutton.setLabel("Create Role");
				me.finalRoleName = me.infoboxNameEntry.getValue();
				if (me.validator.getValid()){
			        me.app.createRPCObject(me.getServer().getIp()).callAsync(me.createFinishedCallback(me),"createRole",{'name':me.infoboxNameEntry.getValue()});
				}
			}
		},
		
	
		buildGui: function(){
			this.setLayout(new qx.ui.layout.VBox());
			//TODO: Eliminate risk of Codeinjection in next line (HTML is interpreted)!!! Search for this.user.name !
			
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Create new Role:</span>",rich:true});
			this.add(this.heading);
			
			this.validator = new qx.ui.form.validation.Manager();
			
			var validateRole = function(me){
				return function(value,item){
					var roleNameFree = me.roles.getRoleNames().indexOf(value) == -1;
					if (!roleNameFree){
						item.setValid(false);
						item.setInvalidMessage("This rolename is already in use on this server!");
					}
					var validCharacters = true;
					if (!validCharacters){
						item.setValid(false);
						item.setInvalidMessage("Usernames may only consist of alphabetic letters");
					}
					return roleNameFree && validCharacters;
				}
			}
			
			//Info
			this.infobox = new qx.ui.groupbox.GroupBox("Roleinfo", "scoville_admin/role.png");
			this.infobox.setLayout(new qx.ui.layout.Basic());
			this.infoboxNameEntry = new qx.ui.form.TextField();
			this.infoboxNameLabel = new qx.ui.basic.Label("Name:");
			this.infoboxLabel = new qx.ui.basic.Label("Please enter information for the new Role");
			this.infobox.add(this.infoboxLabel,{left:10,top:10});
			this.infobox.add(this.infoboxNameLabel,{left:10,top:32});
			this.infobox.add(this.infoboxNameEntry,{left:100,top:32});
			
			this.validator.add(this.infoboxNameEntry,validateRole(this));
			
			this.add(this.infobox);
			
			this.savebutton = new qx.ui.form.Button("Create Role","scoville_admin/add.png");
			this.savebutton.addListener("execute",this.createSaveCallback(this));
			this.validator.addListener("complete",this.createValidatedCallback(this));
			this.add(this.savebutton);
			
			
			
			
	    },
		
		
		heading:null,
		app:null,
		tabs:null
		
	}
	
});