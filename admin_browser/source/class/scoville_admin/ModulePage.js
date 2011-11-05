qx.Class.define("scoville_admin.ModulePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, module){
		this.app=app;
		this.base(arguments);
		this.module = module;
		this.setLabel(module.name);
		this.setIcon('scoville_admin/module.png');
		this.tabs = app.tabview;
		
		this.buildGui();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		module:null,
		
		buildGui : function(){
			this.setLayout(new qx.ui.layout.VBox());
			if (this.module.getServer().rightsForSession.indexOf('scoville.css.edit')!=-1){
				this.cssButton = new qx.ui.form.Button("Edit this module's CSS");
				this.add(this.cssButton);
				this.cssButton.addListener("execute", this.editCSSCallback(this));
			}
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
