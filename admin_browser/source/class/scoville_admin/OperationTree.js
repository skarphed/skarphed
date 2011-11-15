qx.Class.define("scoville_admin.OperationTree",{
	extend: qx.ui.tree.Tree,
	
	construct : function(app, moduletypes){
		this.app = app;
		this.base(arguments);
		
		this.root = new scoville_admin.OperationTreeFolder(this.app,{'type':'OPERATIONS','invoked':'','status':1});
		this.setRoot(this.root);
		this.root.setOpen(true);
		this.setHideRoot(true);
		
		var treeItem1__ = new scoville_admin.OperationTreeFolder(this.app,{'type':'ModuleInstallOperation','invoked':'2011-11-15 10:02:15','status':2});
		var treeItem1_1 = new scoville_admin.OperationTreeFolder(this.app,{'type':'ModuleInstallOperation','invoked':'2011-11-15 10:02:13','status':2});
		
		treeItem1__.add(treeItem1_1);
		this.root.add(treeItem1__);
		
		var treeItem2__ = new scoville_admin.OperationTreeFolder(this.app,{'type':'ModuleInstallOperation','invoked':'2011-11-15 10:12:15','status':1});
		
		this.root.add(treeItem2__);
		
		var treeItem3__ = new scoville_admin.OperationTreeFolder(this.app,{'type':'ModuleUninstallOperation','invoked':'2011-11-15 10:13:18','status':0});
		
		this.root.add(treeItem3__);
		
	},
	
	members:{
		app:null
	}
});