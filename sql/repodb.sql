create domain nstring as varchar(64) not null;

create generator mod_gen;

create generator dep_gen;

create table modules
(
  mod_id integer not null,
  mod_name nstring,
  mod_displayname varchar(64),
  mod_versionmajor integer not null,
  mod_versionminor integer not null,
  mod_versionrev integer not null,
  mod_md5 varchar(32),
  mod_data blob sub_type 0 not null,
  constraint mod_pk primary key (mod_id)
);

create table dependencies
(
  dep_id integer,
  dep_mod_id integer not null,
  dep_mod_dependson integer not null,
  constraint dep_pk primary key (dep_id),
  constraint dep_fk_mod foreign key (dep_mod_id) references modules (mod_id) on delete cascade on update cascade
);