qx.Class.define("scoville_admin.Module",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
	},
	
	members: {
		app:null
		
	}
	
});
