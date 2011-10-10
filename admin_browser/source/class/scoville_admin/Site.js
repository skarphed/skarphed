qx.Class.define("scoville_admin.Site",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
	},
	
	members: {
		app:null
	}
	
});
