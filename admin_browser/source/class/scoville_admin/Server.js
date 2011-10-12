var _serverTestDataset = {
    	"name":"TestServer1",
    	"users":[
    	  {"name":"grindhold"},
    	  {"name":"zigapeda"},
    	  {"name":"kochchef"}
    	],
    	"projects":[
    	  {"name":"testseite1",
    	   "modules":[],
    	   "sites":[]
    	  },
    	  {"name":"testseite",
    	   "modules":[],
    	   "sites":[]
    	  }
    	],
    	"permissions":[]
        }

qx.Class.define("scoville_admin.Server",
{
	extend : qx.ui.tree.TreeFolder,
	
	construct : function(app,ip,username,password){
	    
		this.app = app;
		this.base(arguments);
		this.ip = ip;
		
		this.username = username;
		this.password = password;
		
		this.setLabel( "-> loading <- ["+this.ip+"]");
	    this.setIcon('scoville_admin/loading.gif');
	    
	    this.rightsForSession = [];
	    
		var rpc = new qx.io.remote.Rpc("http://"+ip+"/rpc/","scoville_admin.scvRpc");
        rpc.setCrossDomain(true);
        rpc.callAsync(this.createGetServerInfoHandler(this),"getServerInfo","");

	},
	members:{
		
		getIp: function(){
			return this.ip;
		},
		
		createGetUsersHandler : function(me){
			var f = function(result,exc){
				if (exc == null){
					if (result === false){
						return;
					}
					me.users = new scoville_admin.Users(me.app);
					me.users.setIcon('scoville_admin/user.png');
					me.add(me.users);
					for (var i = 0; i < result.length; i++ ){
						var user = new scoville_admin.User(me.app, result[i])
						me.users.add(user);
					}
						
				}else{
					
				}
			}
			return f;
		},
		
		createAuthenticationHandler : function(me){
			var f = function(result,exc){
				if (exc == null){
					if (me.newtablistener != null){
						me.removeListenerById(me.newtablistener);
					}
					if (result != false){
						me.loggedin = true;
												
						me.rightsForSession = result;
						
						me.setIcon('scoville_admin/server.png');
						
						me.sites = new qx.ui.tree.TreeFolder('Sites');
						me.modules = new qx.ui.tree.TreeFolder('Modules');
						me.roles = new qx.ui.tree.TreeFolder('Userroles');
						
						
						me.sites.setIcon('scoville_admin/site.png');
						me.modules.setIcon('scoville_admin/module.png');
						me.roles.setIcon('scoville_admin/role.png');
						
						
						me.add(me.sites);
						me.add(me.modules);
						me.add(me.roles);
						
						if (me.rightsForSession.indexOf('scoville.users.view')!=-1){
							var rpc = new qx.io.remote.Rpc("http://"+me.ip+"/rpc/","scoville_admin.scvRpc");
					        rpc.setCrossDomain(true);
					        rpc.callAsync(me.createGetUsersHandler(me),"getUsers");
					    }
						
					}else{
						me.password = '';
						me.loggedin = false;
						me.setIcon('scoville_admin/server_locked.png');
					}
					me.newtablistener = me.addListener('dblclick', me.openServerCallback(me));
					
					
					
				}else{
					me.setLabel("Auth Error ["+me.ip+"]");
					me.setIcon('scoville_admin/server_invalid.png');
				}
			}
			return f;
		},
		
		openServerCallback: function (me){
			var f = function(e){
				new scoville_admin.ServerPage(me.app, me);
			};
			return f;
		},
		
		createGetServerInfoHandler : function(me){
			var f = function(result,exc){
				if (exc == null){
			        me.id = this.loadedServers++;
					//TODO: Ajax-Request for Dataset;
					var data = _serverTestDataset;
					
					me.name = result;
					
					me.setLabel(me.name+" ["+me.ip+"]");
					me.setIcon('scoville_admin/server.png');
					me.invalid = false;
					
					var rpc = new qx.io.remote.Rpc("http://"+me.ip+"/rpc/","scoville_admin.scvRpc");
			        rpc.setCrossDomain(true);
			        rpc.callAsync(me.createAuthenticationHandler(me),"authenticateUser",me.username,me.password);
					
				}else{
					me.setLabel("Invalid Server ["+me.ip+"]");
					me.setIcon('scoville_admin/server_invalid.png');
				}
			}
			return f;
		},
		
		app: null,
		ip: null,
		name: null,
		id: null,
		invalid : true,
		loggedin : false,
		newtablistener : null
	},
	statics:{
		loadedServers: 0
	}
});
