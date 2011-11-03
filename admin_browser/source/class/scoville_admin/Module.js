qx.Class.define("scoville_admin.Module",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app,data){
		this.app=app;
		this.base(arguments);
		
		this.name=data.name;
		this.hrname=data.hrname;
		this.version_major=data.version_major;
		this.version_minor=data.version_minor;
		this.revision = data.revision;
		this.md5 = data.md5;
		if (typeof(data.toUpdate) != 'undefined'){
			this.updateable = data.toUpdate;
		}
		if (typeof(data.serverModuleId) != 'undefined'){
			this.serverModuleId = data.serverModuleId;
		}
		
		this.setLabel(this.hrname+" ["+this.version_major+"."+this.version_minor+"."+this.revision+"]");
		this.setIcon("scoville_admin/module.png");
		this.addListener('dblclick',this.createModuleCallback(this));
		
	},
	
	members: {
		app:null,
		name: null,
		hrname: null,
		version_major:null,
		version_minor : null,
		revision:null,
		updateable:false,
		md5:null,
		
		getName:function(){
			return this.name;
		},
		
		getServer:function(){
			return this.getParent().getParent();
		},
		
		createModuleCallback: function (me){
			var f = function(e){
				new scoville_admin.ModulePage(me.app, me);
			};
			return f;
		}
		
	}
	
});
