create domain nstring as varchar(64) not null;
create domain bool as smallint not null check (value = 0 or value = 1);