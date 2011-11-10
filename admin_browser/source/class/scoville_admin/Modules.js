qx.Class.define("scoville_admin.Modules",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app){
		this.app=app;
		this.base(arguments);
		
		this.setIcon("scoville_admin/module.png");
		this.setLabel("Modules");
	},
	
	members: {
		app:null,
		
		getServer : function(){
			return this.getParent();
		},
		
		getModuleNames : function(){
			var modules = this.getChildren();
			var ret = [];
			for (var i = 0; i < modules.length; i++){
				ret.push(modules[i].getName());
			}	
			return ret;
		},
		
		updateHandler : function(me){
			return function(result,exc){
				if (exc == null){
					if (result===false){
						return;
					}
					var resultJson = qx.lang.Json.parse(result);
					me.removeAll();
					for (var i = 0; i < resultJson.length; i++){
						var module = new scoville_admin.Module(me.app, resultJson[i]);
						me.add(module);
					}
				}else{
					alert(exc);
				}
			}
		},
		
		update: function(){
			this.app.createRPCObject(this.getServer().getIp()).callAsync(this.updateHandler(this),"getModules",true);
		}
		
	}
	
});