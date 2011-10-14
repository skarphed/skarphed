qx.Class.define("scoville_admin.Role",{
	extend: qx.ui.tree.TreeFolder,
	
	construct: function(app,data){
		this.app=app;
		this.base(arguments);
		this.name = data.name;
		this.id = data.id;  
		this.setLabel(this.name);
		this.setIcon('scoville_admin/role.png');
		this.addListener('dblclick', this.createUserCallback(this));
	},
	
	members : {
		app  : null,
		name : null,
				
		createUserCallback: function (me){
			var f = function(e){
				new scoville_admin.RolePage(me.app, me);
			};
			return f;
		},
		
		getServer : function(){
			return this.getParent().getParent();
		},
		
		getName: function(){
			return this.name;
		},
		
		getId:function(){
			return this.id;
		}
		
	}
	
});
