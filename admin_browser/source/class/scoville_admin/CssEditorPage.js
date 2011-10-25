qx.Class.define("scoville_admin.CssEditorPage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, server, data){
		this.app=app;
		this.base(arguments);
		this.server = server;
		this.setLabel("Configure CSS Data");
		this.setIcon('scoville_admin/css.png');
		
		this.tabs = app.tabview;
		
		this.buildGui();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
	},
	
	members: {
		buttonEnter:null,
		buttonCancel:null,
		label:null,
		ipentry:null,
		server:null,
		infobox:null,
		infolabel:null,
		heading:null,
		
		buildGui : function (){
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Edit CSS properties of </span>",rich:true});
			
			this.cssbox = new qx.ui.groupbox.GroupBox("CSS Properties", "scoville_admin/css.png");
			this.cssbox.setLayout(new qx.ui.layout.Basic());
			this.setLayout(new qx.ui.layout.VBox());
			this.buttonEnter.addListener("execute", this.enterNewServerCallback(this));
			this.buttonCancel.addListener("execute", this.cancelCallback(this));
			
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