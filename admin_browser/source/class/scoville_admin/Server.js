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
	    
        this.app.createRPCObject(this.ip).callAsync(this.createGetServerInfoHandler(this),"getServerInfo","");

	},
	members:{
		
		getIp: function(){
			return this.ip;
		},
		
		createGetModulesHandler : function (me){
			return function(result,exc){
				if (exc == null){
					if (result===false){
						return;
					}
					var resultJson = qx.lang.Json.parse(result);
					me.modules = new scoville_admin.Modules(me.app);
					me.add(me.modules);
					for (var i = 0; i < resultJson.length; i++){
						var module = new scoville_admin.Module(me.app, resultJson[i]);
						me.modules.add(module);
					}
				}else{
					alert(exc);
				}
			}
		},
		
		createGetUsersHandler : function(me){
			var f = function(result,exc){
				if (exc == null){
					if (result === false){
						return;
					}
					me.users = new scoville_admin.Users(me.app);
					me.add(me.users);
					for (var i = 0; i < result.length; i++ ){
						var user = new scoville_admin.User(me.app, result[i]);
						me.users.add(user);
					}
						
				}else{
					
				}
			}
			return f;
		},
		
		createGetRolesHandler : function(me){
			return function(result,exc){
				if (exc == null){
					if (result === false){
						return;
					}
					var resultJson = qx.lang.Json.parse(result);
					me.roles = new scoville_admin.Roles(me.app);
					me.add(me.roles);
					for (var i = 0; i < resultJson.length; i++ ){
						var role = new scoville_admin.Role(me.app, resultJson[i])
						me.roles.add(role);
					}
				}else{
					alert(exc);
				}
			}
		},
		
		createGetRepositoryHandler: function(me){
			return function(result,exc){
				if (exc == null){
					if (result == null){
						return;
					}
					var resultJson = qx.lang.Json.parse(result);
					me.add(new scoville_admin.Repository(me.app,resultJson));
				}else{
					alert(exc);
				}
			}
		},
		
		createGetSitesHandler: function(me){
			return function(result,exc){
				if (exc == null){
					if (result === false){
						return;
					}
					me.sites = new scoville_admin.Sites(me.app);
					me.add(me.sites);
					for (var i = 0; i < result.length; i++ ){
						var site = new scoville_admin.Site(me.app, result[i])
						me.sites.add(site);
					}
				}else{
					alert(exc);
				}
			}
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
						
						
						
						if (me.rightsForSession.indexOf('scoville.users.view')!=-1){
					        me.app.createRPCObject(me.ip).callAsync(me.createGetUsersHandler(me),"getUsers");
					    }
					    
						if (me.rightsForSession.indexOf('scoville.roles.view')!=-1){
					        me.app.createRPCObject(me.ip).callAsync(me.createGetRolesHandler(me),"getRoles");
					    }
					    
					    if (true){
					    	me.app.createRPCObject(me.ip).callAsync(me.createGetModulesHandler(me),"getModules",true);
					    }
					    
					    if (me.rightsForSession.indexOf('scoville.modules.install')!=-1
					    ||me.rightsForSession.indexOf('scoville.modules.uninstall')!=-1){
							me.app.createRPCObject(me.ip).callAsync(me.createGetRepositoryHandler(me),"getRepository");
						}
						
						if (true){
							me.templates = new scoville_admin.Template(me.app);
							me.add(me.templates);
						}
						
						if (true){
							me.app.createRPCObject(me.ip).callAsync(me.createGetSitesHandler(me),"getSites");
						}
					    
						
					}else{
						me.password = '';
						me.loggedin = false;
						me.setIcon('scoville_admin/server_locked.png');
					}
					me.newtablistener = me.addListener('dblclick', me.openServerCallback(me));
				}else{
					alert(exc);
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
					
			        me.app.createRPCObject(me.ip).callAsync(me.createAuthenticationHandler(me),"authenticateUser",me.username,me.password);
					
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
