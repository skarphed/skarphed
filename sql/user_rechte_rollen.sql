insert into roles values (gen_id(rol_gen,1),'Scoville Core Admin');

insert into rights values (gen_id(rig_gen,1),'scoville.manageserverdata');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.users.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.users.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.users.modify');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.users.grant_revoke');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.roles.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.roles.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.roles.modify');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1),'scoville.modules.install');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.modules.uninstall');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.modules.enter_repo');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.modules.erase_repo');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.sites.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.sites.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.sites.modify');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.widget.create');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.widget.delete');
INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.widget.modify');

INSERT INTO RIGHTS VALUES (gen_id(rig_gen,1), 'scoville.css.edit');

insert into users values (gen_id(usr_gen,1),'zigapeda','test');
insert into users values (gen_id(usr_gen,1),'grindhold','test');
insert into users values (gen_id(usr_gen,1),'chefpflaume','test');
