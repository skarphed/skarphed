qx.Class.define("scoville_admin.CssEditorPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, server, data){
		this.app=app;
		this.base(arguments);
		this.server = server;
		this.setLabel("Configure CSS Data");
		this.setIcon('scoville_admin/css.png');
		
		this.tabs = app.tabview;
		
		this.data = qx.lang.Json.parse(data);
		
		this.buildGui();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
	},
	
	members: {
		data:null,
		server:null,
		heading:null,
		cssbox:null,
		tabs:null,
		
		fillCssTable : function(){
			var newdata = [];
			for (var element in this.data.properties){
				var identifier = element.split("?");
				newdata.push([identifier[0],identifier[1],this.data.properties[element].v, this.data.properties[element].i,false]);
			}
			this.cssboxTableModel.setData(newdata);
		},
		
		saveDone : function(me){
			return function (result,exc){
				if (exc==null){
					var data = me.cssboxTableModel.getData();
					var newdata = [];
					for (var i = 0; i < data.length; i++){
						if (data[i][4] === false){
							newdata.push(data[i]);
						}
					}
					me.cssboxTableModel.setData(newdata);
				}else{
					alert(exc);
				}
			}
		},
		
		saveCSScallback: function(me){
			return function(){
				var data = me.cssboxTableModel.getData();
				
				me.data.properties = {};
				
				for (var i = 0; i < data.length; i++){
					if (data[i][4] === false){
						me.data.properties[data[i][0]+"?"+data[i][1]] = {'v':data[i][2],'i':data[i][3]};
					}
				}
				
				
			    //var senddata = qx.lang.Json.stringify(me.data)
				
				me.app.createRPCObject(me.server.getIp()).callAsync(me.saveDone(me),"setCssPropertySet",me.data)
			}
			
		},
		
		addNewPropertyCallback: function(me){
			return function(){
				me.cssboxTableModel.addRows([['','','',false,false]]);
			}
		},
		
		buildGui : function (){
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Edit CSS properties of </span>",rich:true});
			
			this.cssbox = new qx.ui.groupbox.GroupBox("CSS Properties", "scoville_admin/css.png");
			this.cssbox.setLayout(new qx.ui.layout.VBox());
			this.setLayout(new qx.ui.layout.VBox());
			
			var propertyCellEditorFactoryFunc = function (cellInfo)
		    {
		    	switch(cellInfo.col){
		    		case 0:
		    			return new qx.ui.table.celleditor.TextField();
		    		case 1:
		    			return new qx.ui.table.celleditor.TextField();
		    		case 2:
		    			//TODO: Implement Celleditors for different types of tags.
		    			return new qx.ui.table.celleditor.TextField();
		    			
		    		case 4:
		    			return new qx.ui.table.celleditor.CheckBox();
		    			
		    	}
		    }
		    
			var cssCellEditorFactory = new qx.ui.table.celleditor.Dynamic(propertyCellEditorFactoryFunc);
			
			this.cssboxTableModel = new qx.ui.table.model.Simple();
			this.cssboxTableModel.setColumns(["Selector","CSS-Property","Value", "Inherited", "Delete"]);
			
            this.fillCssTable();
            
			this.cssboxTable = new qx.ui.table.Table(this.cssboxTableModel, {tableColumnModel : 
				            function(obj){return (new qx.ui.table.columnmodel.Resize(obj));}});
			this.cssboxTable.setColumnWidth(0,20);
            this.cssboxTable.setColumnWidth(1,60);
            this.cssboxTable.setColumnWidth(2,300);
            
            var cssTCM = this.cssboxTable.getTableColumnModel();
            cssTCM.setCellEditorFactory(0, cssCellEditorFactory);
			cssTCM.setCellEditorFactory(1, cssCellEditorFactory);
			cssTCM.setCellEditorFactory(2, cssCellEditorFactory);
			cssTCM.setCellEditorFactory(4, cssCellEditorFactory);
			cssTCM.setDataCellRenderer(3, new qx.ui.table.cellrenderer.Boolean());
			cssTCM.setDataCellRenderer(4, new qx.ui.table.cellrenderer.Boolean());
			this.cssboxTableModel.setColumnEditable(0,true);
			this.cssboxTableModel.setColumnEditable(1,true);
			this.cssboxTableModel.setColumnEditable(2,true);
			this.cssboxTableModel.setColumnEditable(4,true);
			
			this.savebutton = new qx.ui.form.Button("Save CSS");
			this.savebutton.addListener("execute", this.saveCSScallback(this));
			
			this.addrowbutton = new qx.ui.form.Button("Insert new CSS property");
			this.addrowbutton.addListener("execute", this.addNewPropertyCallback(this));
			
			this.cssbox.add(this.cssboxTable);
			this.cssbox.add(this.addrowbutton);
			this.cssbox.add(this.savebutton);
			
			this.add(this.heading);
			this.add(this.cssbox);
		},
		
		cancelCallback: function(me){
			return function(){}
			/*return function(){
				me.tabs.remove(me);
			}*/
		}
		
			
	}
});