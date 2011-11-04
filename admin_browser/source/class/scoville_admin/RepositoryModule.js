qx.Class.define("scoville_admin.RepositoryModule",{
	extend: qx.ui.form.ListItem,
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
		}else{
			this.updateable = false;
		}
		if (typeof(data.serverModuleId) != 'undefined'){
			this.serverModuleId = data.serverModuleId;
		}else{
			this.serverModuleId = null;
		}
		if (typeof(data.installed) != 'undefined'){
			this.installed = data.installed;
		}else{
			this.installed = false;
		}
		
		this.setLabel(this.hrname+" ["+this.version_major+"."+this.version_minor+"."+this.revision+"]");
		if(this.updateable){
			this.setIcon("scoville_admin/module_updateable.png");
		}else{
			this.setIcon("scoville_admin/module.png");
		}
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
		installed:null,
		
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
