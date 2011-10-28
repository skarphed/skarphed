qx.Class.define("scoville_admin.Widget",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
	},
	
	members: {
		app:null
		
	}
	
});
