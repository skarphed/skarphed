qx.Class.define("scoville_admin.NewUserPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app,users){
		this.app=app;
		this.base(arguments);
		this.setLabel("New User: ");
		this.setIcon('scoville_admin/user.png');
		
		this.tabs = app.tabview;
		this.users = users;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		this.finalUserName = "";
		
	},
	
	members : {
		
		getServer : function (){
			return this.users.getParent();
		},
		
		createOnClose : function(me){
			return function(){
				me.app.newUserPage = null;
			}
		},
		
		
		createFinishedCallback: function(me){
			return function(result, exc){
				if (exc == null){
					if (result == true){
						var user = new scoville_admin.User(me.app, {'name':me.finalUserName});
						me.users.add(user);
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
				me.savebutton.setLabel("Create User");
				me.finalUserName = me.nameentry.getValue();
				if (me.validator.getValid()){
			        me.app.createRPCObject(me.getServer().getIp()).callAsync(me.createFinishedCallback(me),"createUser",me.nameentry.getValue(),me.pw1entry.getValue());
				}
			}
		},
		
		buildGui: function(){
			this.setLayout(new qx.ui.layout.VBox());
			//TODO: Eliminate risk of Codeinjection in next line (HTML is interpreted)!!! Search for this.user.name !
			
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Create new user:</span>",rich:true});
			this.add(this.heading);
			
			this.validator = new qx.ui.form.validation.Manager();
			
			var validatePasswordLength = function(value,item){
				var valid = value != null && value.length > 7;
				if (!valid){
					item.setInvalidMessage("The password has to have at least 8 characters");
				}
				return valid
			}
			
			var validatePasswordEquality = function(me){
				return function(items){
					var valid = me.pw1entry.getValue() == me.pw2entry.getValue();
					if (!valid){
						me.pw1entry.setValid(false);
						me.pw2entry.setValid(false);
						me.pw1entry.setInvalidMessage("The passwords have to be equal");
						me.pw2entry.setInvalidMessage("The passwords have to be equal");
					}
					return valid;
				}
			}
			
			var validateUsername = function(me){
				return function(value,item){
					var userNameFree = me.users.getUserNames().indexOf(value) == -1;
					if (!userNameFree){
						item.setValid(false);
						item.setInvalidMessage("This username is already in use on this server!");
					}
					var validCharacters = true;
					if (!validCharacters){
						item.setValid(false);
						item.setInvalidMessage("Usernames may only consist of alphabetic letters");
					}
					return userNameFree && validCharacters;
				}
			}
			
			//Credentials
			this.credbox = new qx.ui.groupbox.GroupBox("Credentials", "scoville_admin/credential.png");
			this.credbox.setLayout(new qx.ui.layout.Basic());
			this.credlabel = new qx.ui.basic.Label("Plaese enter the credentials for the new user here:");
			this.nameentry = new qx.ui.form.TextField();
			this.namelabel = new qx.ui.basic.Label("username:");
			this.pw1entry = new qx.ui.form.PasswordField();
			this.pw1label = new qx.ui.basic.Label("password:");
			this.pw2entry = new qx.ui.form.PasswordField();
			this.pw2label = new qx.ui.basic.Label("repeat password:");
			
			this.nameentry.setRequired(true);
			this.pw1entry.setRequired(true);
			this.pw2entry.setRequired(true);
			this.nameentry.setPlaceholder("username");
			this.pw1entry.setPlaceholder("password");
			this.pw2entry.setPlaceholder("repeat password");
			
			this.validator.add(this.nameentry,validateUsername(this));
			this.validator.add(this.pw1entry,validatePasswordLength);
			this.validator.add(this.pw2entry,validatePasswordLength);
			this.validator.setValidator(validatePasswordEquality(this));
			
			this.credbox.add(this.namelabel,{left:10,top:10});
			this.credbox.add(this.nameentry,{left:100,top:10});
			this.credbox.add(this.pw1label,{left:10,top:32});
			this.credbox.add(this.pw1entry,{left:100,top:32});
			this.credbox.add(this.pw2label,{left:10,top:54});
			this.credbox.add(this.pw2entry,{left:100,top:54});
			
			this.add(this.credbox);
			
			this.savebutton = new qx.ui.form.Button("Create User","scoville_admin/add.png");
			this.savebutton.addListener("execute",this.createSaveCallback(this));
			this.validator.addListener("complete",this.createValidatedCallback(this));
			this.add(this.savebutton);
			
			
	    },
		
		
		heading:null,
		app:null,
		tabs:null
		
	}
	
});