qx.Class.define("scoville_admin.User",{
	extend: qx.ui.tree.TreeFolder,
	
	construct: function(app,data){
		this.app=app;
		this.base(arguments);
		this.name = data.name;
		this.setLabel(this.name);
		this.setIcon('scoville_admin/user.png');
		this.addListener('dblclick', this.createUserCallback(this));
	},
	
	members : {
		app  : null,
		name : null,
				
		createUserCallback: function (me){
			var f = function(e){
				new scoville_admin.UserPage(me.app, me);
			};
			return f;
		},
		
		getServer : function(){
			return this.getParent().getParent();
		},
		
		getName: function(){
			return this.name;
		}
		
	}
	
});
