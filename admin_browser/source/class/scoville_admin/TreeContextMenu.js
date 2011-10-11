qx.Class.define("scoville_admin.TreeContextMenu",{
	extend: qx.ui.menu.Menu,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
		this.addListener("appear",this.createAppearListener(this));
	},
	
	members: {
		app:null,
		/*menustructure : {
			'scoville_admin.Server':{
				[new qx.ui.menu.Button('Close')]
			},
			'scoville_admin.User':{
				
			}
		}*/
		
		serverRemove : function(server){
			return function(){
				server.getParent().remove(server);
				server.app.storeServerlistCookie();
			}
		},
		
		userRemove : function(user){
			return function(){
				//TODO: Implement
				//server.getParent().remove(server);
			}
		},
		
		userAdd : function(users){
			return function(){
				users.app.addUser(users);
			}
		},
		
		createAppearListener: function(me){
			return function(){
				var treeobject = me.getOpener().getSelection()[0];
				var classname  = treeobject.classname;
				
				var button = null;
				this.removeAll();
				switch(classname){
					case "scoville_admin.Server":
					    button = new qx.ui.menu.Button('Remove Server',"scoville_admin/delete.png");
					    button.addListener('execute',this.serverRemove(treeobject));
						this.add(button);
						break;
						
				    case "scoville_admin.User":
				    	button = new qx.ui.menu.Button('Remove User',"scoville_admin/delete.png");
				    	button.addListener('execute',this.userRemove(treeobject));
						this.add(button);
				    	break;
				    	
				    case "scoville_admin.Users":
				        if (treeobject.getServer().rightsForSession.indexOf('scoville.users.create') != -1){
					    	button = new qx.ui.menu.Button('Add User',"scoville_admin/add.png");
					    	button.addListener('execute',this.userAdd(treeobject));
							this.add(button);
						}
				    	break;
					default:
						break;
				}
			}
		}
	}
	
});
