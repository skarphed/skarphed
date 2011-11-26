qx.Class.define("scoville_admin.Widget",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app, widget){
		this.app=app;
		this.base(arguments);
		this.data = widget;
		
		this.setLabel(this.data.name);
		this.setIcon("scoville_admin/widget.png");
		
		
	},
	
	members: {
		app:null,
		
		getServer : function(){
			return this.getParent().getParent().getParent();
		},
		
		delHandler : function(me){
			return function(result,exc){
				if (exc==null){
					me.getParent().loadWidgets();
				}else{
					alert(exc);
				}
			}
		},
		
		del: function() {
			this.app.createRPCObject(this.getServer().getIp()).callAsync(this.delHandler(this),"deleteWidget",this.data.id);
		}
		
	}
	
});
