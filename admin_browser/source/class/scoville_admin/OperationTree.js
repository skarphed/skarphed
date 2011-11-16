qx.Class.define("scoville_admin.OperationTree",{
	extend: qx.ui.tree.Tree,
	
	construct : function(app, server, operationtypes){
		this.app = app;
		this.server = server;
		this.base(arguments);
		this.operationtypes = (operationtypes)?operationtypes:null;
		
		this.root = new scoville_admin.OperationTreeFolder(this.app,{'type':'OPERATIONS','invoked':'Invoked At','status':-1});
		this.setRoot(this.root);
		this.root.setOpen(true);
		this.setHideRoot(true);
		
		this.updateTree();
		
	},
	
	members:{
		app:null,
		operationtypes:null,
		server:null,
		
		getOperationById : function(id,treefolder){
			var children = treefolder.getChildren();
			for (var i = 0; i < children.length; i++){
				if (children[i].getData().id == id){
					return children[i];
				}
				
				var res = this.getOperationById(id, children[i]);
				if (res != null){
					return res;
				}
			}
			return null;
		},
		
		deleteOld:function(idlist, treefolder){
			var children = treefolder.getChildren();
			for (var i = 0; i < children.length; i++){
				if (children[i].hasChildren()){
					this.deleteOld(idlist,children[i]);
				}
				if (idlist.indexOf(qx.data.Conversion.toString(children[i].getData().id)) == -1){
					treefolder.remove(children[i]);
				}
			}
			
		},
		
		updateHandler : function(me){
			return function(result,exc){
				if (exc == null){
					var idlist = [];
					for (var element in result){
						var op = me.getOperationById(element,me.root);
						if (op != null){
							op.update(result[element]);
						}else{
							if (result[element].parent == null){
								me.root.add(new scoville_admin.OperationTreeFolder(me.app, result[element], me))
							}else{
							    var chOp = me.getOperationById(result[element].parent, me.root);
							    if (chOp != null){
							    	chOp.add(new scoville_admin.OperationTreeFolder(me.app, result[element], me));
							    }else{
							    	// LOL Beschissener fall!
							    }
							}
						}
						idlist.push(element);
					}
					me.deleteOld(idlist,me.root);
				}else{
					alert(exc);
				}
			}
		},
		
		updateTree: function(){
			this.app.createRPCObject(this.server.getIp()).callAsync(this.updateHandler(this),"getOperations",this.operationtypes);
		},
		
		getServer: function(){
			return this.server;
		}
	}
});