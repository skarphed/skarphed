qx.Class.define("scoville_admin.SpaceWidgetWrap",{
	extend: qx.ui.tree.TreeFolder,
	
	construct : function(app, number, initialdata, tree, site){
		this.app = app;
		this.data = initialdata;
		this.tree = tree;
		this.site = site;
		this.number = number;
		this.base(arguments);
		

		this.addIcon();
		this.setIcon("scoville_admin/operation.png");
		this.spaceWidget =new scoville_admin.SpaceWidget(this.app, this.number, this.data, this.tree, this.site); 
		this.addWidget(this.spaceWidget);
		this.renderGui();
	},
	
	members:{
		app: false,
		operationview: null,
		
	    renderGui: function(){
	    	this.spaceWidget.renderGui();
	    },
		
		update : function(data){
			this.data = data;
			this.renderGui();
		},
		
		getData : function(){
			return this.data;
		}
		
	}
});