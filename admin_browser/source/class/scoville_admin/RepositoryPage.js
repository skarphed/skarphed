qx.Class.define("scoville_admin.RepositoryPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, repo){
		this.app=app;
		this.base(arguments);
		this.repo = repo;
		this.setLabel(repo.name);
		this.setIcon('scoville_admin/repo.png');
		this.tabs = app.tabview;
		
		this.operationsActive = false;
		
		this.buildGui();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		module:null,
		
		operationsActive: false,
		
		refreshTimer: function(me){
			return function(evt){
				if (!me.operationsActive){
					return;
				}
				me.app.createRPCObject(me.repo.getServer().ip).callAsync(me.createGetModulesHandler(me),"getModules",false);
			}
		},
		
		createGetModulesHandler:function(me){
			return function(result,exc){
				if (exc == null){
					var resultJson = qx.lang.Json.parse(result);
					me.modboxIList.removeAll();
					me.modboxAList.removeAll();
					me.modboxCList.removeAll();
					var countProcessing = 0;
					for (var element in resultJson){
						if (typeof(resultJson[element].processing) != 'undefined'){
							var mod = new scoville_admin.RepositoryModule(me.app,resultJson[element]);
							mod.setLabel(mod.getLabel()+" [ "+resultJson[element].processing+"]");
							me.modboxCList.add(mod);
							countProcessing++;
						}else{
							if (resultJson[element].installed){
								me.modboxIList.add(new scoville_admin.RepositoryModule(me.app,resultJson[element]));
							}else{
								me.modboxAList.add(new scoville_admin.RepositoryModule(me.app,resultJson[element]));
							}
						}
					}
					me.operationsActive = countProcessing != 0;
				}else{
					alert(exc);
				}
			}
		},
		
		dragStartHandlerIList : function(me){
			return function (evt){
				evt.addType("modules_uninstall");
				
				evt.addAction("copy");
				evt.addAction("move");
				evt.addAction("alias");
			}
		},

		dragStartHandlerAList : function(me){
			return function (evt){
				evt.addType("modules_install");
				
				evt.addAction("copy");
				evt.addAction("move");
				evt.addAction("alias");
			}
		},
		
		dropRequestHandlerIList : function(me){
			return function (evt){
				if (evt.getCurrentType() == "modules_uninstall"){
					evt.addData("modules_uninstall",me.modboxIList.getSelection());
				}
				return null;
			}
		},
		
		dropRequestHandlerAList : function(me){
			return function (evt){
				if (evt.getCurrentType() == "modules_install"){
					evt.addData("modules_install",me.modboxAList.getSelection());
				}
				return null;
			}
		},
		
		dropHandlerIList:function(me){
			return function(evt){
				var modulesToInstall = evt.getData("modules_install");
				for (var i = 0; i < modulesToInstall.length; i++){
					var operationId = modulesToInstall[i].toHashCode();
					me.app.createRPCObject(me.repo.getServer().ip).callAsync(me.createInstallCallback(me,modulesToInstall[i]),
																			"installModule",
																			modulesToInstall[i].toTransferObject(),
																			operationId);
					me.modboxAList.remove(modulesToInstall[i]);	
				}
				
			}
		},
		
		dropHandlerAList:function(me){
			return function(evt){
				var modulesToUninstall = evt.getData("modules_uninstall");
				for (var i = 0; i < modulesToUninstall.length; i++){
					var operationId = modulesToUninstall[i].toHashCode();
					me.app.createRPCObject(me.repo.getServer().ip).callAsync(me.createUninstallCallback(me,modulesToUninstall[i]),
																			"uninstallModule",
																			modulesToUninstall[i].toTransferObject(),
																			operationId);
					me.modboxIList.remove(modulesToUninstall[i]);	
				}
				
			}
		},
		
		createInstallCallback : function(me,module){
			return function(result,exc){
				if (exc == null){
					module.setLabel(module.getLabel()+" [ Installing ]");
					me.modboxCList.add(module);
					me.operationsActive = true;
				}else{
					alert(exc);
				}
			}
		},
		
		createUninstallCallback : function(me,module){
			return function(result,exc){
				if (exc == null){
					module.setLabel(module.getLabel()+" [ Uninstalling ]");
					me.modboxCList.add(module);
					me.operationsActive = true;
				}else{
					alert(exc);
				}
			}
		},
		
		preventDropIList : function (me){
			return function(evt){
				if (!evt.supportsType("modules_install")){
					evt.preventDefault();
				}
			}
		},
		
		preventDropAList : function (me){
			return function(evt){
				if (!evt.supportsType("modules_uninstall")){
					evt.preventDefault();
				}
			}
		},
		
		buildGui : function(){
			
			this.setLayout(new qx.ui.layout.VBox());
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Install / Uninstall Modules</span>",rich:true});
			this.add(this.heading);
			
			this.infobox = new qx.ui.groupbox.GroupBox("Repository Information","scoville_admin/repo.png");
			this.infobox.setLayout(new qx.ui.layout.Basic());
			this.infobox.add(new qx.ui.basic.Label("Name:"),{top:10,left:10});
			this.infobox.add(new qx.ui.basic.Label(this.repo.name),{top:10,left:150});
			this.infobox.add(new qx.ui.basic.Label("Host:"),{top:25,left:10});
			this.infobox.add(new qx.ui.basic.Label(this.repo.host),{top:25,left:159});
			this.add(this.infobox);
			
			this.modbox = new qx.ui.groupbox.GroupBox("Available and Installed Modules", "scoville_admin/module.png");
			this.modboxInnerCont = new qx.ui.container.Composite(new qx.ui.layout.HBox(5));
			this.modbox.setLayout(new qx.ui.layout.VBox());
			this.modbox.add(new qx.ui.basic.Label("Please drag a module into the opposing list to install/uninstall it"));
			this.modboxContainer = new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
			this.modboxCL = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
			this.modboxCR = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
			this.modboxCL.add(new qx.ui.basic.Label("Installed Modules"));
			this.modboxCR.add(new qx.ui.basic.Label("Available Modules"));
			this.modboxInnerCont.add(this.modboxCL,{flex:5});
			this.modboxInnerCont.add(this.modboxCR,{flex:5});
			this.modboxContainer.add(this.modboxInnerCont);
			this.modboxCurrentLabel = new qx.ui.basic.Label("Currenty Processed Modules:");
			this.modboxContainer.add(this.modboxCurrentLabel);
			this.modbox.add(this.modboxContainer);
			
			this.modboxIList = new qx.ui.form.List();  // Installed modules
			this.modboxAList = new qx.ui.form.List();  // Available modules
			this.modboxCList = new qx.ui.form.List();  // Current processed
			this.modboxCL.add(this.modboxIList);
			this.modboxCR.add(this.modboxAList);
			this.modboxContainer.add(this.modboxCList);
			this.add(this.modbox);
			
			this.modboxIList.addListener("dragstart",this.dragStartHandlerIList(this));
			this.modboxAList.addListener("dragstart",this.dragStartHandlerAList(this));
			this.modboxIList.addListener("droprequest", this.dropRequestHandlerIList(this));
			this.modboxAList.addListener("droprequest", this.dropRequestHandlerAList(this));
			this.modboxIList.addListener("drop", this.dropHandlerIList(this));
			this.modboxAList.addListener("drop", this.dropHandlerAList(this));
			this.modboxIList.addListener("dragover", this.preventDropIList(this));
			this.modboxAList.addListener("dragover", this.preventDropAList(this));
			this.modboxIList.setDraggable(true);
			this.modboxAList.setDraggable(true);
			this.modboxIList.setDroppable(true);
			this.modboxAList.setDroppable(true);
			this.modboxIList.setSelectionMode("multi");
			this.modboxAList.setSelectionMode("multi");
			
			this.refreshtimer = new qx.event.Timer(500);
			this.refreshtimer.addListener("interval",this.refreshTimer(this));
			this.refreshtimer.setEnabled(true);
			
			this.app.createRPCObject(this.repo.getServer().ip).callAsync(this.createGetModulesHandler(this),"getModules",false);
			
		}
	}
});