qx.Class.define("scoville_admin.SpaceWidget",{
	extend: qx.ui.container.Composite,
	
	construct : function(app,number, initialdata, tree, site){
		this.app = app;
		this.data = initialdata;
		this.tree = tree;
		this.site = site;
		this.base(arguments);
		this.number = number;
		
		this.setLayout(new qx.ui.layout.VBox());
		
		this.label = new qx.ui.basic.Label().set({value:"<b>Space "+this.number.toString()+"</b>", rich:true});
		this.add(this.label);
		
		this.list = new qx.ui.tree.Tree();
		this.list.setHeight(35);
		this.add(this.list);
		
		this.removeButton = new qx.ui.form.Button("Remove Widget","scoville_admin/delete.png");
		this.add(this.removeButton);
		this.addListener("drop", this.dropHandler(this));
		this.addListener("dragover", this.preventDrop(this));
		this.setDroppable(true);
		this.removeButton.addListener("execute",this.removeWidget(this));
		
	},
	
	members:{
		app: false,
		tree: null,
		
		renderGui: function(){
			if (this.data == 0){
				this.removeButton.setEnabled(false);
			}else{
				this.removeButton.setEnabled(true);
			}
		}, 
		
		update : function(data){
			this.data = data;
			this.renderGui();
		},
		
		getData : function(){
			return this.data;
		},
		
		preventDrop : function(me){
			return function(evt){
				if(!this.data == 0 || !evt.supportsType("widget")){
					evt.preventDefault();
				}
			}
		},
		
		removeWidgetHandler : function(me){
			return function (result, exc){
				if (exc == null){
					me.list.resetRoot();
					me.data = 0;
					me.renderGui();
				}
			}
		},
		
		removeWidget : function(me){
			return function(e){
				if (me.data != 0){
					me.app.createRPCObject(me.site.getServer().getIp()).callAsync(me.removeWidgetHandler(me), "removeWidgetFromSpace", me.site.data.id, me.number);
				}
			} 
		},
		
		assignWidgetHandler: function(me, widget){
			return function(result, exc){
				if (exc == null){
					me.list.setRoot(widget);
					me.data = {"id":widget.id, "name":widget.name,"moduleId":widget.moduleId};
					me.renderGui();
				}
			}
		},
		
		dropHandler : function(me){
			return function(evt){
				if (this.data == 0){
					var widget = evt.getData("widget");
					me.app.createRPCObject(me.site.getServer().getIp()).callAsync(me.assignWidgetHandler(me,widget), "assignWidgetToSpace",me.site.data.id,me.number,widget.data.id);
				} 
			}
		}
		
	}
});