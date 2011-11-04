qx.Class.define("scoville_admin.RepositoryPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, repo){
		this.app=app;
		this.base(arguments);
		this.repo = repo;
		this.setLabel(repo.name);
		this.setIcon('scoville_admin/repo.png');
		this.tabs = app.tabview;
		
		this.buildGui();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		module:null,
		
		createGetModulesHandler:function(me){
			return function(result,exc){
				if (exc == null){
					var resultJson = qx.lang.Json.parse(result);
					for (var element in resultJson){
						if (resultJson[element].installed){
							me.modboxIList.add(new scoville_admin.RepositoryModule(me.app,resultJson[element]));
						}else{
							me.modboxAList.add(new scoville_admin.RepositoryModule(me.app,resultJson[element]));
						}
					}
				}else{
					alert(exc);
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
			
			this.app.createRPCObject(this.repo.getServer().ip).callAsync(this.createGetModulesHandler(this),"getModules",false);
			
		},
		
		createOpenCSSHandler: function (me){
			return function (result,exc){
				if (exc == null){
					new scoville_admin.CssEditorPage(me.app, me.module.getServer(),result);
				}else{
					alert(exc);
				}
			}
		},
		
		editCSSCallback : function(me){
			return function(){
				me.app.createRPCObject(me.module.getServer().ip).callAsync(me.createOpenCSSHandler(me),"getCssPropertySet",me.module.serverModuleId,null,null);
			}
		}	
	}
});
