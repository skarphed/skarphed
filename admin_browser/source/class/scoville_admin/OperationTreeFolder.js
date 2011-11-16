qx.Class.define("scoville_admin.OperationTreeFolder",{
	extend: qx.ui.tree.TreeFolder,
	
	construct : function(app, initialdata, operationview){
		this.app = app;
		this.data = initialdata;
		this.operationview = operationview;
		this.base(arguments);
		
		this.tooltip = new qx.ui.tooltip.ToolTip();
		
		this.tooltip.setRich(true);
		this.tooltip.setShowTimeout(0);
		this.setToolTip(this.tooltip);
		
		this.loadImage = new qx.ui.basic.Image("scoville_admin/loading.gif");
		this.errorImage = new qx.ui.basic.Image("scoville_admin/error.png");
		this.iconSpacer = new qx.ui.core.Spacer(16,16);
		
		this.addWidget(this.loadImage);
		this.addWidget(this.errorImage);
		this.addWidget(this.iconSpacer);
		
		this.addSpacer();
		
		this.setOpenSymbolMode("auto");
		
		this.addOpenButton();

		this.addIcon();
		this.setIcon("scoville_admin/operation.png");
		this.addLabel(this.data.type);

		this.invokedLabel = new qx.ui.basic.Label();
		this.invokedLabel.setWidth(250);
		this.addWidget(this.invokedLabel);
		
		this.addWidget(new qx.ui.core.Spacer(), {flex:1});
		
		this.cancelbutton = new qx.ui.form.Button("Cancel", "scoville_admin/error.png");
		this.cancelbutton.addListener("execute",this.cancelCallback(this));
		this.cancelbutton.setWidth(100);
		this.cancelbutton.setHeight(16);
		
		this.retrybutton = new qx.ui.form.Button("Retry", "scoville_admin/retry.png");
		this.retrybutton.addListener("execute",this.retryCallback(this));
		this.retrybutton.setWidth(100);
		this.retrybutton.setHeight(16);
		
		this.dropbutton = new qx.ui.form.Button("Drop", "scoville_admin/error.png");
		this.dropbutton.addListener("execute",this.dropCallback(this));
		this.dropbutton.setWidth(100);
		this.dropbutton.setHeight(16);
		
		this.addWidget(this.retrybutton);
		this.addWidget(this.dropbutton);
		this.addWidget(this.cancelbutton);
		
		this.renderGui();
	},
	
	members:{
		app: false,
		operationview: null,
		
		operationCommandDone : function(me){
			return function(result,exc){
				if (exc == null){
					me.operationview.updateTree();
				}else{
					alert(exc);
				}
			}
		},
		
		cancelCallback : function(me){
			return function(e){
				me.app.createRPCObject(me.operationview.getServer().getIp()).callAsync(me.operationCommandDone(me), "cancelOperation", me.data.id);
			}
		},
		
		dropCallback : function(me){
			return function(e){
				me.app.createRPCObject(me.operationview.getServer().getIp()).callAsync(me.operationCommandDone(me), "dropOperation", me.data.id);
			}
		},
		
		retryCallback : function(me){
			return function(e){
				me.app.createRPCObject(me.operationview.getServer().getIp()).callAsync(me.operationCommandDone(me), "retryOperation", me.data.id);
			}
		},
		
		renderGui : function(){
			var tooltiptext = "<table>";
			for (var element in this.data.data){
	        	tooltiptext = tooltiptext+ "<tr><td><b>"+element+"</b></td><td>"+this.data.data[element]+"</td></tr>";
			}
			tooltiptext =tooltiptext+ "</table>";
			this.tooltip.setLabel(tooltiptext);
			switch(this.data.status){
				case 1:
					this.loadImage.setVisibility("visible"); 
					this.errorImage.setVisibility("excluded");
					
				    break;
				case 2:
					this.loadImage.setVisibility("excluded"); 
					this.errorImage.setVisibility("visible");
					
					break;
				case 0:
					this.loadImage.setVisibility("hidden"); 
					this.errorImage.setVisibility("excluded");
					
					break;
				default:
					this.loadImage.setVisibility("hidden"); 
					this.errorImage.setVisibility("excluded");
					
			}
			
			this.invokedLabel.setValue(this.data.invoked);
			
			switch(this.data.status){
				case 1:
					this.dropbutton.setVisibility("excluded");
					this.cancelbutton.setVisibility("excluded");
					this.retrybutton.setVisibility("excluded");
					break;
				case 2:
					this.dropbutton.setVisibility("visible");
					this.cancelbutton.setVisibility("excluded");
					this.retrybutton.setVisibility("visible");
					break;
				case 0:
					this.dropbutton.setVisibility("excluded");
					this.cancelbutton.setVisibility("visible");
					this.retrybutton.setVisibility("excluded");
					break;
				default:
					this.dropbutton.setVisibility("excluded");
					this.cancelbutton.setVisibility("excluded");
					this.retrybutton.setVisibility("excluded");
			}
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