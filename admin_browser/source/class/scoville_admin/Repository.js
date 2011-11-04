qx.Class.define("scoville_admin.Repository",{
	extend: qx.ui.tree.TreeFolder,
	construct: function(app,data){
		this.app=app;
		this.base(arguments);
		
		this.name=data.name;
		this.ip=data.ip;
		this.port = data.port;
		this.id = data.ip;
		this.host = data.ip+":"+data.port;
		
		this.setLabel(this.name+" ["+this.host+"]");
		this.setIcon("scoville_admin/repo.png");
		this.addListener('dblclick',this.createRepositoryCallback(this));
		
	},
	
	members: {
		app:null,
		name: null,
		ip:null,
		id:null,
		port:null,
		host:null,
		
		getName:function(){
			return this.name;
		},
		
		getServer:function(){
			return this.getParent();
		},
		
		createRepositoryCallback: function (me){
			var f = function(e){
				new scoville_admin.RepositoryPage(me.app, me);
			};
			return f;
		}
		
	}
	
});