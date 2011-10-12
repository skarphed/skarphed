qx.Class.define("scoville_admin.UserPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, user){
		this.app=app;
		this.base(arguments);
		this.setLabel(user.getParent().getParent().name+" → "+user.name);
		this.setIcon('scoville_admin/user.png');
		
		this.tabs = app.tabview;
		this.user = user;
		this.buildGui();
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members : {
		updatePermissionList : function(me){
			return function(result,exc){
				if (exc == null){
					var dataset = []
					var jsonResult = qx.lang.Json.parse(result);
					for (var i = 0; i<jsonResult.length; i++){
						var currentset = [jsonResult[i].granted, jsonResult[i].right, ""];
						dataset.push(currentset); 
					}
					me.permissionPermissionTableModel.setData(dataset);
					if (!me.permissionTableInitialized){
						me.permissionPermissionTableModel.addListener("dataChanged",me.changedData(me));
						me.permissionTableInitialized=true;
					}
				}else{
					alert(exc);
				}
				
			}
		},
		
		changedPermission : function(me){
			return function(result,exc){
				if (exc == null){
					me.permissionPermissionTable.setEnabled(true);
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
		    	var model = me.permissionPermissionTableModel;
		    	var value = model.getValue(changedData.firstColumn, changedData.firstRow);
		    	var right = model.getValue(1, changedData.firstRow);
		    	var rpc = new qx.io.remote.Rpc("http://"+me.user.getServer().getIp()+"/rpc/","scoville_admin.scvRpc");
                rpc.setCrossDomain(true);
                if (value){
                	rpc.callAsync(me.changedPermission(me),"grantRightToUser",me.user.getName(),right);
                }else{
                	rpc.callAsync(me.changedPermission(me),"revokeRightFromUser",me.user.getName(),right);
                }
                me.permissionPermissionTable.setEnabled(false);
		    }
		},
		
		
		buildGui: function(){
			this.setLayout(new qx.ui.layout.VBox());
			//TODO: Eliminate risk of Codeinjection in next line (HTML is interpreted)!!! Search for this.user.name !
			
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Settings for User: "+this.user.name+"</span>",rich:true});
			this.add(this.heading);
			
			
			//UserInfo
			this.infobox = new qx.ui.groupbox.GroupBox("Info", "scoville_admin/user.png");
			this.infobox.setLayout(new qx.ui.layout.Basic());
			this.add(this.infobox);
			
			//Right management
			if (this.user.getServer().rightsForSession.indexOf('scoville.users.grant_revoke') != -1){
				this.permissionbox = new qx.ui.groupbox.GroupBox("Permissions/Roles", "scoville_admin/role.png");
				this.permissionbox.setLayout(new qx.ui.layout.HBox(5));
				
				this.permissionPermissionBox = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
				this.permissionRoleBox = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
				
				this.permissionbox.add(this.permissionPermissionBox,{flex:5});
				this.permissionbox.add(this.permissionRoleBox,{flex:5});
				
				
				//Permission-Table
				
				var propertyCellEditorFactoryFunc = function (cellInfo)
			    {
			      if (cellInfo.col == 0){
			      	return new qx.ui.table.celleditor.CheckBox();
			      }else{
			      	//return new qx.ui.table.celleditor.TextField();
			      }
			    }
			    
			    
			    
			    var propertyCellEditorFactory = new qx.ui.table.celleditor.Dynamic(propertyCellEditorFactoryFunc);
				
				this.permissionPermissionTableModel = new qx.ui.table.model.Simple();
				this.permissionPermissionTableModel.setColumns(["Active","Permission Identifier","Permission Name"]);
				
				var rpc = new qx.io.remote.Rpc("http://"+this.user.getServer().getIp()+"/rpc/","scoville_admin.scvRpc");
                rpc.setCrossDomain(true);
                rpc.callAsync(this.updatePermissionList(this),"getRightsForUserPage",this.user.getName());
                
				this.permissionPermissionTable = new qx.ui.table.Table(this.permissionPermissionTableModel, {tableColumnModel : 
					                                                        function(obj){return (new qx.ui.table.columnmodel.Resize(obj));}});
				this.permissionPermissionTable.setColumnWidth(0,20);
                this.permissionPermissionTable.setColumnWidth(1,60);
                this.permissionPermissionTable.setColumnWidth(2,300);
                
                var permissionTCM = this.permissionPermissionTable.getTableColumnModel();
				permissionTCM.setDataCellRenderer(0, new qx.ui.table.cellrenderer.Boolean());
				permissionTCM.setCellEditorFactory(0, propertyCellEditorFactory);
				this.permissionPermissionTableModel.setColumnEditable(0,true);
                
				this.permissionPermissionLabel = new qx.ui.basic.Atom("Please choose the Permissions you want to assign to "+this.user.name+" here:", "scoville_admin/permission.png");
				this.permissionPermissionBox.add(this.permissionPermissionLabel);
				this.permissionPermissionBox.add(this.permissionPermissionTable);
				
				
				
				//Role-Table
				this.permissionRoleTableModel = new qx.ui.table.model.Simple();
				this.permissionRoleTableModel.setColumns(["Active","Role Identifier","Role Name"]);
				this.permissionRoleTableModel.setData([[false,"scoville.usermanager","The user can change every User attribute!"],
															 [true ,"scoville.rolemanager","The user can change any role"]]);
				this.permissionRoleTable = new qx.ui.table.Table(this.permissionRoleTableModel, {tableColumnModel : 
					                                                        function(obj){return (new qx.ui.table.columnmodel.Resize(obj));}});
				/*var roleTCM = this.permissionRoleTable.getTableColumnModel();
				roleTCM.setDataCellRenderer(0, new qx.ui.table.cellrenderer.Boolean());
				this.permission*/					                                                        
                this.permissionRoleTable.setColumnWidth(0,20);
                this.permissionRoleTable.setColumnWidth(1,60);
                this.permissionRoleTable.setColumnWidth(2,300);
				this.permissionRoleLabel = new qx.ui.basic.Atom("Please choose the Roles you want to assign to "+this.user.name+" here:","scoville_admin/role.png");
				this.permissionRoleBox.add(this.permissionRoleLabel);
				this.permissionRoleBox.add(this.permissionRoleTable);
				
				this.add(this.permissionbox);
			}
			
	    },
		
		
		heading:null,
		app:null,
		tabs:null,
		user:null,
		permissionTableInitialized:false
	}
	
});
