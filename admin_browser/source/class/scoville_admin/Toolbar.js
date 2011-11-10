qx.Class.define("scoville_admin.Toolbar",{
	extend: qx.ui.toolbar.ToolBar,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
		
		var logout = new qx.ui.toolbar.Button("Logout","scoville_admin/server.png");
		logout.addListener("execute",function(){alert("TEST");});
		this.regularButtons.push(logout);
		
		for (var i = 0; i < this.regularButtons.length; i++){
			this.add(this.regularButtons[i]);
		}
		
		this.add(new qx.ui.toolbar.Separator());
		
	},
	
	members: {
		app:null,
		additionalButtons : [],
		regularButtons : [],
		
		updateForPage : function(page){
			this.removeAdditional();
			if (typeof(page) != 'undefined'){
				if (typeof(page.getToolbarExtension) == 'function'){
					var buttons = page.getToolbarExtension();		
					for (var i = 0; i < buttons.length; i++){
						this.add(buttons[i]);
						this.additionalButtons.push(buttons[i]);
					}
				}
			}
		},
		
		removeAdditional: function(page){
			for (var i = 0; i < this.additionalButtons.length;  i++){
				this.remove(this.additionalButtons[i]);
			}
			this.additionalButtons = [];
		}
		
	}
	
});