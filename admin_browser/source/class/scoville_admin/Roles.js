qx.Class.define("scoville_admin.Roles",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
		this.setIcon("scoville_admin/role.png");
		this.setLabel("Roles");
	},
	
	members: {
		app:null,
		
		getServer : function(){
			return this.getParent();
		},
		
		getRoleNames : function(){
			var users = this.getChildren();
			var ret = [];
			for (var i = 0; i < users.length; i++){
				ret.push(users[i].getName());
			}	
			return ret;
		}
		
	}
	
});