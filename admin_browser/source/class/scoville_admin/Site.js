qx.Class.define("scoville_admin.Site",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app,site){
		this.app=app;
		this.base(arguments);
				
		this.data = site;
		this.setIcon("scoville_admin/site.png");
		this.setLabel(this.data.name);
		this.addListener('dblclick',this.openSitePage(this))
	},
	
	members: {
		app:null,
		
		
		openSitePage: function (me){
			return function(e){
				new scoville_admin.SitePage(me.app, me);
			};
		}
	}
	
});
