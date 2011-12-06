qx.Class.define("scoville_admin.Sites",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
		this.setIcon("scoville_admin/site.png");
		this.setLabel("Sites");
	},
	
	members: {
		app:null,
		
		getServer : function(){
			return this.getParent();
		}
		
	}
	
});