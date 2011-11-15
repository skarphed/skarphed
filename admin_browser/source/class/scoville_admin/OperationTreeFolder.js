qx.Class.define("scoville_admin.OperationTreeFolder",{
	extend: qx.ui.tree.TreeFolder,
	
	construct : function(app, initialdata){
		this.app = app;
		this.data = initialdata;
		this.base(arguments);
		
		switch(this.data.status){
			case 1:
				this.addWidget(new qx.ui.basic.Image("scoville_admin/loading.gif"));
			    break;
			case 2:
				this.addWidget(new qx.ui.basic.Image("scoville_admin/error.png"));
				break;
			default:
				this.addWidget(new qx.ui.core.Spacer(16,16));
		}
		
		this.addSpacer();
		
		this.setOpenSymbolMode("auto");
		
		this.addOpenButton();
		
		
		this.addIcon();
		this.setIcon("scoville_admin/operation.png");
		this.addLabel(this.data.type);
		
		this.addWidget(new qx.ui.core.Spacer(), {flex:1});
		
		this.invokedLabel = new qx.ui.basic.Label(this.data.invoked);
		this.invokedLabel.setWidth(250);
		this.addWidget(this.invokedLabel);
		
		this.cancelbutton = new qx.ui.form.Button("Cancel", "scoville_admin/error.png");
		this.cancelbutton.setWidth(100);
		this.cancelbutton.setHeight(16);
		
		this.retrybutton = new qx.ui.form.Button("Retry", "scoville_admin/retry.png");
		this.retrybutton.setWidth(100);
		this.retrybutton.setHeight(16);
		
		this.dropbutton = new qx.ui.form.Button("Drop", "scoville_admin/error.png");
		this.dropbutton.setWidth(100);
		this.dropbutton.setHeight(16);
		
		switch(this.data.status){
			case 1:
				this.addWidget(new qx.ui.core.Spacer(200,16));
				break;
			case 2:
				this.addWidget(this.retrybutton);
				this.addWidget(this.dropbutton);
				break;
			default:
				this.addWidget(new qx.ui.core.Spacer(100,16));
				this.addWidget(this.cancelbutton);
		}
		
		
		
	},
	
	members:{
		app: false,
		update : function(data){
			
		}
		
	}
});