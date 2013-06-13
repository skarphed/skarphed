insert into roles values (gen_id(rol_gen,1),'Skarphed Core Admin');

insert into rights values (gen_id(rig_gen,1),'skarphed.manageserverdata');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.users.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.users.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.users.modify');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.users.grant_revoke');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.roles.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.roles.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.roles.modify');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'skarphed.modules.install');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.modules.uninstall');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.modules.enter_repo');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.modules.erase_repo');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.sites.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.sites.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.sites.modify');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.widget.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.widget.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.widget.modify');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'skarphed.css.edit');

insert into users values (gen_id(usr_gen,1),'zigapeda','test');
insert into users values (gen_id(usr_gen,1),'grindhold','test');
insert into users values (gen_id(usr_gen,1),'chefpflaume','test');
