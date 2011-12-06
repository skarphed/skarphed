create table users (
  usr_id int,
  usr_name nstring,
  usr_password varchar(40) not null,
  constraint usr_pk primary key (usr_id),
  constraint usr_uni_name unique (usr_name)
);

create table rights (
  rig_id int,
  rig_name nstring,
  constraint rig_pk primary key (rig_id),
  constraint rig_uni_name unique (rig_name)
);

create table roles (
  rol_id int,
  rol_name nstring,
  constraint rol_pk primary key (rol_id),
  constraint rol_uni_name unique (rol_name)
);

create table userrights (
  uri_usr_id int,
  uri_rig_id int,
  constraint uri_pk primary key (uri_usr_id, uri_rig_id),
  constraint uri_fk_usr foreign key (uri_usr_id) references users (usr_id) on update cascade on delete cascade,
  constraint uri_fk_rig foreign key (uri_rig_id) references rights (rig_id) on update cascade on delete cascade
);

create table rolerights (
  rri_rol_id int,
  rri_rig_id int,
  constraint rri_pk primary key (rri_rol_id, rri_rig_id),
  constraint rri_fk_rol foreign key (rri_rol_id) references roles (rol_id) on update cascade on delete cascade,
  constraint rri_fk_rig foreign key (rri_rig_id) references rights (rig_id) on update cascade on delete cascade
);

create table userroles (
  uro_usr_id int,
  uro_rol_id int,
  constraint uro_pk primary key (uro_usr_id, uro_rol_id),
  constraint uro_fk_usr foreign key (uro_usr_id) references users (usr_id) on update cascade on delete cascade,
  constraint uro_fk_rol foreign key (uro_rol_id) references roles (rol_id) on update cascade on delete cascade
);

create table repositories (
  rep_id int,
  rep_name nstring,
  rep_ip varchar(32),
  rep_port int default 80,
  rep_lastupdate timestamp,
  constraint rep_pk primary key (rep_id),
  constraint rep_uni_ipport unique (rep_id,rep_port)
);

create table modules (
  mod_id int,
  mod_name nstring,
  mod_rep_id int,
  mod_displayname varchar(64),
  mod_versionmajor int,
  mod_versionminor int,
  mod_versionrev int,
  mod_md5 varchar(32),
  /*mod_html blob sub_type text,
  mod_javascript blob sub_type text,
  mod_css blob sub_type text,*/
  constraint mod_pk primary key (mod_id),
  constraint mod_uni_name unique (mod_name, mod_versionmajor, mod_versionminor, mod_versionrev),
  constraint mod_fk_rep foreign key (mod_rep_id) references repositories (rep_id) on update cascade on delete set null
);

create table moduletables (
  mdt_id int,
  mdt_name nstring,
  mdt_mod_id int,
  constraint mdt_pk primary key (mdt_id),
  constraint mdt_uni_name unique (mdt_name),
  constraint mdt_fk_mod foreign key (mdt_mod_id) references modules (mod_id) on update cascade on delete cascade
);

create table menus (
  mnu_id int,
  mnu_name nstring,
  constraint mnu_pk primary key (mnu_id),
  constraint mnu_uni_name unique (mnu_name)
);

create table widgets (
  wgt_id int,
  wgt_name nstring,
  wgt_sit_id int,
  wgt_mod_id int,
  wgt_space int,
  constraint wgt_pk primary key (wgt_id),
  constraint wgt_fk_sit foreign key (wgt_sit_id) references sites (sit_id) on update cascade on delete cascade,
  constraint wgt_fk_mod foreign key (wgt_mod_id) references modules (mod_id) on update cascade on delete cascade
);

create table actionlists (
  atl_id int,
  atl_name nstring,
  constraint atl_pk primary key (atl_id)
);

create table actions (
  act_id int,
  act_name nstring,
  act_atl_id int not null,
  act_order int not null,
  act_sit_id int,
  act_space int,
  act_wgt_id int,
  act_url varchar(1024),
  constraint act_pk primary key (act_id),
  constraint act_uni_order unique (act_atl_id,act_order),
  constraint act_fk_atl foreign key (act_atl_id) references actionlists (atl_id) on update cascade on delete cascade,
  constraint act_fk_sit foreign key (act_sit_id) references sites (sit_id) on update cascade on delete cascade,
  constraint act_fk_wgt foreign key (act_wgt_id) references widgets (wgt_id) on update cascade on delete cascade
);

create table sites (
  sit_id int,
  sit_name nstring,
  sit_mnu_id int,
  sit_html blob sub_type text,
  constraint sit_pk primary key (sit_id),
  constraint sit_uni_name unique (sit_name),
  constraint sit_fk_mnu foreign key (sit_mnu_id) references menus (mnu_id) on update cascade on delete set null
);

create table menuitems (
  mni_id int,
  mni_name nstring,
  mni_mnu_id int not null,
  mni_order int not null,
  mni_mni_id int,
  mni_atl_id int,
  constraint mni_pk primary key (mni_id),
  constraint mni_uni_name unique (mni_name),
  constraint mni_uni_order unique (mni_mnu_id, mni_order),
  constraint mni_fk_mnu foreign key (mni_mnu_id) references menus (mnu_id) on update cascade on delete cascade,
  constraint mni_fk_mni foreign key (mni_mni_id) references menuitems (mni_id) on update cascade on delete cascade,
  constraint mni_fk_atl foreign key (mni_atl_id) references actionlists (atl_id) on update cascade on delete set null
);

create table css
(
  css_id int,
  css_selector varchar(15) not null,
  css_mod_id int,
  css_wgt_id int,
  css_session varchar(32),
  css_tag varchar(20) not null,
  css_value varchar(50) not null,
  constraint css_pk primary key (css_id),
  constraint css_uni_selector unique (css_selector,css_mod_id,css_wgt_id,css_session,css_tag),
  constraint css_fk_mod foreign key (css_mod_id) references modules (mod_id) on update cascade on delete cascade,
  constraint css_fk_wgt foreign key (css_wgt_id) references widgets (wgt_id) on update cascade on delete cascade
);

create table csssession
(
  cse_session varchar(32) not null,
  cse_file varchar(50) not null,
  cse_outdated bool,
  constraint cse_pk primary key (cse_session,cse_file)
);

CREATE TABLE OPERATIONS
(
  OPE_ID Integer NOT NULL,
  OPE_OPE_PARENT Integer,
  OPE_INVOKED Timestamp NOT NULL,
  OPE_TYPE Varchar(64) NOT NULL,
  OPE_ACTIVE BOOL DEFAULT 0,
  CONSTRAINT PK_OPERATIONS PRIMARY KEY (OPE_ID)
);

CREATE TABLE OPERATIONDATA
(
  OPD_OPE_ID Integer NOT NULL,
  OPD_KEY Varchar(64) NOT NULL,
  OPD_VALUE Varchar(512) NOT NULL,
  OPD_TYPE Varchar(16) NOT NULL,
  CONSTRAINT PK_OPERATIONDATA PRIMARY KEY (OPD_OPE_ID,OPD_KEY),
  constraint fk_operationdata_1 foreign key (opd_ope_id) references operaions (ope_id) on update cascade on delete cascade
);

create table binarys
(
  bin_id int,
  bin_mime varchar(64),
  bin_usr_id_owner int,
  bin_usr_id_lastchange int,
  bin_date_lastchange timestamp,
  bin_rig_id int,
  bin_md5 varchar(32),
  bin_data blob sub_type 0,
  constraint bin_pk primary key (bin_id),
  constraint bin_fk_usr_owner foreign key (bin_usr_id_owner) references users (usr_id) on update cascade on delete set null,
  constraint bin_fk_usr_lastchange foreign key (bin_usr_id_lastchange) references users (usr_id) on update cascade on delete set null,
  constraint bin_fk_rig foreign key (bin_rig_id) references rights (rig_id) on update cascade on delete cascade
);

create table dual (
    d varchar(1)
);