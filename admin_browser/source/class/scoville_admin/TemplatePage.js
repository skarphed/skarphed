qx.Class.define("scoville_admin.TemplatePage",{
	extend: qx.ui.tabview.Page,
	
	construct : function(app, template){
		this.app=app;
		this.base(arguments);
		this.template = template;
		this.setLabel("Template");
		this.setIcon('scoville_admin/template.png');
		
		this.tabs = app.tabview;
		this.buildGui();
		this.buildToolbar();
		
		this.setShowCloseButton(true);
		this.tabs.add(this);
		
	},
	
	members: {
		label:null,
		template:null,
		infobox:null,
		infolabel:null,
		heading:null,
		toolbarExtension:[],
		uploadRunning:false,
		
		buildGui : function(){
			this.setLayout(new qx.ui.layout.VBox());
			this.heading = new qx.ui.basic.Label().set({value:"<span style='font-size:18px; font-weight:bold;'>Authentication</span>",rich:true});
			
			this.currentBox = new qx.ui.groupbox.GroupBox("Currently Installed", "scoville_admin/template.png");
			this.currentBox.setLayout(new qx.ui.layout.Basic());
			this.currentNameLabel = new qx.ui.basic.Label().set({value:"<b>Name:</b>",rich:true});
			this.currentDescriptionLabel = new qx.ui.basic.Label().set({value:"<b>Description:</b>",rich:true});
			this.currentAuthorLabel = new qx.ui.basic.Label().set({value:"<b>Author:</b>",rich:true});
			this.currentNameDisplay = new qx.ui.basic.Label();
			this.currentDescriptionDisplay = new qx.ui.basic.Label();
			this.currentAuthorDisplay = new qx.ui.basic.Label();
			this.currentBox.add(this.currentNameLabel,{top:10,left:10});
			this.currentBox.add(this.currentDescriptionLabel,{top:30,left:10});
			this.currentBox.add(this.currentAuthorLabel,{top:50,left:10});
			this.currentBox.add(this.currentNameDisplay,{top:10,left:100});
			this.currentBox.add(this.currentDescriptionDisplay,{top:30,left:100});
			this.currentBox.add(this.currentAuthorDisplay,{top:50,left:100});
			
			
			this.uploadBox = new qx.ui.groupbox.GroupBox("Upload new Template", "scoville_admin/template.png");
			this.uploadBox.setLayout(new qx.ui.layout.VBox());
			this.uploadForm = new uploadwidget.UploadForm('uploadfrm',"http://"+this.template.getServer().getIp()+"/rpc/upload.php");
			this.uploadForm.setLayout(new qx.ui.layout.Basic());
			this.uploadForm.setParameter('rm','upload');
			this.uploadButton = new uploadwidget.UploadButton('uploadfile','Choose Template-Archive',"scoville_admin/template.png");
			this.uploadForm.add(this.uploadButton);
			this.uploadForm.addListener("completed",this.uploadListener(this));
			this.uploadSubmit = new qx.ui.form.Button("Upload and Install");
			this.uploadSubmit.addListener("execute",this.sendListener(this));
			this.uploadBox.add(this.uploadForm);
			this.uploadBox.add(this.uploadSubmit);			
			
			this.repoBox = new qx.ui.groupbox.GroupBox("Search in Repository", "scoville_admin/repo.png");
			this.repoInfoBox = new qx.ui.groupbox.GroupBox("Template-Info", "scoville_admin/template.png");
			this.repoBox.setLayout(new qx.ui.layout.HBox());
			this.repoInfoBox.setLayout(new qx.ui.layout.Basic());
			this.repoVcontainer = new qx.ui.container.Composite();
			this.repoVcontainer.setLayout( new qx.ui.layout.VBox());
			this.repoList = new qx.ui.form.List();
			this.repoInstall = new qx.ui.form.Button("Install");
			this.repoVcontainer.add(this.repoList);
			this.repoVcontainer.add(this.repoInstall);
			this.repoNameLabel = new qx.ui.basic.Label().set({value:"<b>Name:</b>",rich:true});
			this.repoDescriptionLabel = new qx.ui.basic.Label().set({value:"<b>Description:</b>",rich:true});
			this.repoAuthorLabel = new qx.ui.basic.Label().set({value:"<b>Author:</b>",rich:true});
			this.repoNameDisplay = new qx.ui.basic.Label();
			this.repoDescriptionDisplay = new qx.ui.basic.Label();
			this.repoAuthorDisplay = new qx.ui.basic.Label();
			this.repoInfoBox.add(this.repoNameLabel,{top:10,left:10});
			this.repoInfoBox.add(this.repoDescriptionLabel,{top:30,left:10});
			this.repoInfoBox.add(this.repoAuthorLabel,{top:50,left:10});
			this.repoInfoBox.add(this.repoNameDisplay,{top:10,left:100});
			this.repoInfoBox.add(this.repoDescriptionDisplay,{top:30,left:100});
			this.repoInfoBox.add(this.repoAuthorDisplay,{top:50,left:100});
			this.repoBox.add(this.repoVcontainer);
			this.repoBox.add(this.repoInfoBox);
			
			this.add(this.heading);
			this.add(this.currentBox);
			this.add(this.uploadBox);
			this.add(this.repoBox);
		},
		
		sendListener : function(me){
			return function(e){
				me.uploadForm.send();
			}
		},
		
		uploadListener : function(me){
			return function(e){
				alert("KOMPLETTT!");
				me.uploadForm.clear();
				var response = me.uploadForm.getIframeTextContent();
				alert("RESPONSE: "+response);
			}
		},
		
		buildToolbar : function () {
			
		},
		
		getToolbarExtension : function(){
			return this.toolbarExtension;
		}	
		
		
	}
});