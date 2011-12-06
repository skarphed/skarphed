qx.Class.define("scoville_admin.SitePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, site){
		this.app=app;
		this.base(arguments);
		this.site = site;
		this.setLabel(this.site.data.name);
		this.setIcon('scoville_admin/site.png');
		this.tabs = app.tabview;
		
		this.buildGui();
		this.buildToolbar();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		module:null,
		toolbarExtension:[],
		
		buildGui : function(){
			this.setLayout(new qx.ui.layout.VBox());
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Compositing of Site</span>",rich:true});
			
			var spaces = 0;
			for (var element in this.site.data.spaces){
				spaces++;
			}
			
			this.infoBox = new qx.ui.groupbox.GroupBox("Site-Info","scoville_admin/site.png");
			this.infoBox.setLayout(new qx.ui.layout.Basic());
			this.infoNameLabel = new qx.ui.basic.Label().set({value:"<b>Name</b>", rich:true});
			this.infoDescriptionLabel = new qx.ui.basic.Label().set({value:"<b>Description</b>",rich:true});
			this.infoSpacesLabel = new qx.ui.basic.Label().set({value:"<b>Spaces</b>",rich:true});
			this.infoNameDisplay = new qx.ui.basic.Label(this.site.data.name);
			this.infoDescriptionDisplay = new qx.ui.basic.Label(this.site.data.description);
			this.infoSpacesDisplay = new qx.ui.basic.Label(spaces.toString());
			this.infoBox.add(this.infoNameLabel,{top:10,left:10});
			this.infoBox.add(this.infoDescriptionLabel,{top:30,left:10});
			this.infoBox.add(this.infoSpacesLabel,{top:50,left:10});
			this.infoBox.add(this.infoNameDisplay,{top:10,left:100});
			this.infoBox.add(this.infoDescriptionDisplay,{top:30,left:100});
			this.infoBox.add(this.infoSpacesDisplay,{top:50,left:100});
			
			this.compBox = new qx.ui.groupbox.GroupBox("Widgets","scoville_admin/widget.png");
			this.compBox.setLayout(new qx.ui.layout.Basic());
			this.compLabel = new qx.ui.basic.Label("Please Drag a Widget into one of the empty Space-Slots to attach it to the Site");
			this.compList = new qx.ui.tree.Tree();
			this.compListRoot = new qx.ui.tree.TreeFolder();
			this.compList.setRoot(this.compListRoot);
			this.compList.setWidth(215);
			this.compList.setHeight(300);
			this.compList.setHideRoot(true);
			this.compListRoot.setOpen(true);
			this.compMinimap = new qx.ui.basic.Image();
			this.compBox.add(this.compLabel,{top:10, left:10});
			this.compBox.add(this.compList,{top:30, left:10});
			this.compBox.add(this.compMinimap,{top:30,left:235});
				
			for (element in this.site.data.spaces){
				this.compListRoot.add(new scoville_admin.SpaceWidgetWrap(this.app,element,this.site.data.spaces[element],this.compList, this.site));
			}
				
			this.add(this.heading);
			this.add(this.infoBox);
			this.add(this.compBox);
		},
		
		buildToolbar : function () {
			
		},
		
		getToolbarExtension : function(){
			return this.toolbarExtension;
		}	
	}
});
