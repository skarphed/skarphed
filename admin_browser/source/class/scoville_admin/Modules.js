qx.Class.define("scoville_admin.Modules",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
		this.setIcon("scoville_admin/module.png");
		this.setLabel("Modules");
	},
	
	members: {
		app:null,
		
		getServer : function(){
			return this.getParent();
		},
		
		getModuleNames : function(){
			var modules = this.getChildren();
			var ret = [];
			for (var i = 0; i < modules.length; i++){
				ret.push(modules[i].getName());
			}	
			return ret;
		}
		
	}
	
});