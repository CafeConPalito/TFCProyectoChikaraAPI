create schema if not exists chikara;

use chikara;

create table if not exists user_data(
id_user INT auto_increment not null,
user_name varchar(150) not null,
email varchar(300) not null,
pass varchar (300) not null,
first_name varchar(150) not null,
first_last_name varchar(150) not null,
second_last_name varchar(150),
birthdate date not null,

account_creation DATETIME default now(),

is_premium boolean default false,

primary key (id_user)
);

create table if not exists user_log(
id_log INT auto_increment not null,
id_user INT not null,
log_in DATETIME default now(),
log_out DATETIME,

primary key (id_log),
constraint fk_userData_userLog Foreign key (id_user) references user_data(id_user) on update cascade on delete cascade
);

-- si solo es uno = follower
create table if not exists user_nakama(
id_nakama INT auto_increment not null,
id_user_follower INT not null,
id_user_leader INT not null,
follow_creation DATETIME default now(),

nakama_creation DATETIME,

-- bloquear la amistad, solo lo puede quitar el que bloquea
is_blocked boolean default false,

-- me estan bloqueando, no lo ve el usuario
you_are_bloked boolean default false,

-- esta relacion es mutua
is_followed_back boolean default false,

primary key (id_nakama),
unique(id_user_follower,id_user_leader),
constraint fk_userData_userNakama_a Foreign key (id_user_follower) references user_data(id_user) on update cascade on delete cascade,
constraint fk_userData_userNakama_b Foreign key (id_user_leader) references user_data(id_user) on update cascade on delete cascade
);


-- OJO LOS TRIGERS DAN ERROR EL RESTO ESTA OK!


delimiter //
CREATE trigger make_nakama after update on user_nakama for each row

BEGIN

	if new.is_followed_back is true then
    
		insert into user_nakama (id_user_follower,id_user_leader,is_followed_back,nakama_creation) values(
		(new.id_user_leader,new.id_user_follower,true,now())
		);
        
        -- update user_nakama set is_followed_back = true, nakama_creation = now() where id_nakama = new.id_nakama;
        
	end if;

END//
delimiter ;

delimiter //
CREATE trigger block_nakama after update on user_nakama for each row

BEGIN
	
	-- bloquear
	if new.is_blocked is true then
		
		update user_nakama set is_followed_back = false where id_nakama = new.id_nakama;
		update user_nakama set is_followed_back = false, you_are_bloked = true where id_user_leader = new.id_user_follower and id_user_follower = new.id_user_leader;
		
	end if;

	-- desbloquear
	if new.is_blocked is false then
		
		update user_nakama set is_followed_back = false where id_nakama = new.id_nakama;
		update user_nakama set is_followed_back = false, you_are_bloked = false where id_user_leader = new.id_user_follower and id_user_follower = new.id_user_leader;
		
	end if;

END//
delimiter ;

