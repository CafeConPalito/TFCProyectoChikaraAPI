-- drop database if exists chikara;

-- CREATE DATABASE chikara; -- Descomentar, ejecutar solo esta linea y volver a comentar

-- drop schema if exists chikara;

--CREATE schema if not exists chikara;


-- SET search_path TO chikara;

-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create table if not exists user_data(
id_user UUID, -- DEFAULT uuid_generate_v4(),
user_name varchar(150) not null unique,
email varchar(300) not null unique,
pwd varchar (300) not null,
first_name varchar(150) not null,
first_last_name varchar(150) not null,
second_last_name varchar(150),
birthdate date not null,

account_creation timestamptz default now(),

is_premium boolean default false,

primary key (id_user)
);

create table if not exists user_log(
id_log UUID ,--DEFAULT uuid_generate_v4(),
id_user UUID not null,
log_in timestamptz default now(),
log_out timestamptz,

primary key (id_log),
constraint fk_userData_userLog Foreign key (id_user) references user_data(id_user) on update cascade on delete cascade
);

create table if not exists user_device(
id_device UUID,
id_user UUID not null,
phone_id varchar(150) not null,
phone_model varchar(150) not null,
phone_brand varchar(150) not null,
block bool not null default false,

primary key (id_device),
constraint fk_userData_userDevice Foreign key (id_user) references user_data(id_user) on update cascade on delete cascade
);

-- si solo es uno = follower
create table if not exists user_nakama(
id_nakama UUID,-- DEFAULT uuid_generate_v4(),
id_user_follower UUID not null,
id_user_leader UUID not null,
follow_creation TIMESTAMP default now(),

nakama_creation TIMESTAMP,

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


/*
delimiter //
CREATE trigger control_nakama after insert on user_nakama for each row

BEGIN



	-- si se siguen mutuamente
	if new.is_followed_back is true then
	
        set new.is_followed_back = true;
        set new.nakama_creation = now();
       
       	call insert_nakama_followed_back(new.id_user_follower,new.id_user_leader);
       
	end if;


	-- bloquear
	if new.is_blocked is true then
		
		set new.is_followed_back = false;

		update user_nakama set is_followed_back = false, you_are_bloked = true where id_user_leader = new.id_user_follower and id_user_follower = new.id_user_leader;
		
	end if;

	-- desbloquear
	if new.is_blocked is false then
		
		set new.is_followed_back = false;

		update user_nakama set is_followed_back = false, you_are_bloked = false where id_user_leader = new.id_user_follower and id_user_follower = new.id_user_leader;
		
	end if;
*/


-- END//
-- delimiter ;


/*
DELIMITER //

CREATE PROCEDURE insert_nakama_followed_back (in follower int, in leader INT)
BEGIN
 
	insert into user_nakama (id_user_follower,id_user_leader,is_followed_back,nakama_creation) values
		(leader,follower,true,now());

END //

DELIMITER ;

*/

