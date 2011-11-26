qx.Class.define("scoville_admin.SitePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, site){
		this.app=app;
		this.base(arguments);
		this.site = site;
		this.setLabel(this.site.data.name);
		this.setIcon('scoville_admin/site.png');
		this.tabs = app.tabview;
		
		this.buildGui();
		this.buildToolbar();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		module:null,
		toolbarExtension:[],
		
		buildGui : function(){
			this.setLayout(new qx.ui.layout.VBox());
		},
		
		buildToolbar : function () {
			
		},
		
		getToolbarExtension : function(){
			return this.toolbarExtension;
		}	
	}
});
