qx.Class.define("scoville_admin.RolePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app,role){
		this.app=app;
		this.base(arguments);
		this.setLabel("Role Details: ");
		this.setIcon('scoville_admin/role.png');
		
		this.tabs = app.tabview;
		this.role=role;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		this.finalUserName = "";
		
	},
	
	members : {
		
		getServer : function (){
			return this.role.getServer();
		},
		
		createOnClose : function(me){
			return function(){
				me.app.newRolePage = null;
			}
		},
		
		changedPermission : function(me){
			return function(result,exc){
				if (exc == null){
					me.permissionboxTable.setEnabled(true);
				}else{
					alert(exc);
				}
			}
		},
		
		changedData : function(me){ 
	        return function(event){
		    	if(!(event instanceof qx.event.type.Data)){
		    		return;
		    	}
		    	var changedData = event.getData();
		    	var model = me.permissionboxTableModel;
		    	var value = model.getValue(changedData.firstColumn, changedData.firstRow);
		    	var right = model.getValue(1, changedData.firstRow);
                if (value){
                	me.app.createRPCObject(me.role.getServer().getIp()).callAsync(me.changedPermission(me),"grantRightToRole",me.role.getId(),right);
                }else{
                	me.app.createRPCObject(me.role.getServer().getIp()).callAsync(me.changedPermission(me),"revokeRightFromRole",me.role.getId(),right);
                }
                me.permissionboxTable.setEnabled(false);
		    }
		},
		
		updatePermissionList : function(me){
			return function(result,exc){
				if (exc == null){
					var dataset = []
					var jsonResult = qx.lang.Json.parse(result);
					for (var i = 0; i<jsonResult.length; i++){
						var currentset = [jsonResult[i].granted, jsonResult[i].right, ""];
						dataset.push(currentset); 
					}
					me.permissionboxTableModel.setData(dataset);
					if (!me.permissionTableInitialized){
						me.permissionboxTableModel.addListener("dataChanged",me.changedData(me));
						me.permissionTableInitialized=true;
					}
				}else{
					alert(exc);
				}
				
			}
		},

		
		buildGui: function(){
			this.setLayout(new qx.ui.layout.VBox());
			//TODO: Eliminate risk of Codeinjection in next line (HTML is interpreted)!!! Search for this.user.name !
			
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Edit Role: </span>",rich:true});
			this.add(this.heading);
			
			this.infobox = new qx.ui.groupbox.GroupBox("Roleinfo", "scoville_admin/role.png");
			this.infobox.setLayout(new qx.ui.layout.Basic());
			this.infoboxName = new qx.ui.basic.Label(this.role.getName());
			this.infoboxNameLabel = new qx.ui.basic.Label("Name:");
			this.infoboxLabel = new qx.ui.basic.Label("Please enter information for the new Role");
			this.infobox.add(this.infoboxLabel,{left:10,top:10});
			this.infobox.add(this.infoboxNameLabel,{left:10,top:32});
			this.infobox.add(this.infoboxName,{left:100,top:32});
			
			this.add(this.infobox);
			
			
			
			//Permissions
			this.permissionbox = new qx.ui.groupbox.GroupBox("Permissions", "scoville_admin/permission.png");
			this.permissionbox.setLayout(new qx.ui.layout.VBox());

			var propertyCellEditorFactoryFunc = function (cellInfo)
		    {
		      if (cellInfo.col == 0){
		      	return new qx.ui.table.celleditor.CheckBox();
		      }else{
		      	//return new qx.ui.table.celleditor.TextField();
		      }
		    }
		    
		    
		    
		    var propertyCellEditorFactory = new qx.ui.table.celleditor.Dynamic(propertyCellEditorFactoryFunc);
			
			this.permissionboxTableModel = new qx.ui.table.model.Simple();
			this.permissionboxTableModel.setColumns(["Active","Permission Identifier","Permission Name"]);
			
            this.app.createRPCObject(this.role.getServer().getIp()).callAsync(this.updatePermissionList(this),"getRightsForRolePage",this.role.getId());
            
			this.permissionboxTable = new qx.ui.table.Table(this.permissionboxTableModel, {tableColumnModel : 
				                                                        function(obj){return (new qx.ui.table.columnmodel.Resize(obj));}});
			this.permissionboxTable.setColumnWidth(0,20);
            this.permissionboxTable.setColumnWidth(1,60);
            this.permissionboxTable.setColumnWidth(2,300);
            
            var permissionTCM = this.permissionboxTable.getTableColumnModel();
			permissionTCM.setDataCellRenderer(0, new qx.ui.table.cellrenderer.Boolean());
			permissionTCM.setCellEditorFactory(0, propertyCellEditorFactory);
			this.permissionboxTableModel.setColumnEditable(0,true);
            
			this.permissionboxLabel = new qx.ui.basic.Atom("Please choose the Permissions you want to assign to "+this.role.name+" here:", "scoville_admin/permission.png"); //TODO: Here be dragons: Injection of HTML via username
			this.permissionbox.add(this.permissionboxLabel);
			this.permissionbox.add(this.permissionboxTable);

			this.add(this.permissionbox);
			
	    },
		
		
		heading:null,
		app:null,
		tabs:null
		
	}
	
});