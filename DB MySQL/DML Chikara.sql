use chikara;

INSERT INTO user_data (user_name, email, pwd, first_name, first_last_name, second_last_name, birthdate, account_creation, is_premium) VALUES
('@usuario1', 'usuario1@example.com', md5('pass1'), 'Nombre1', 'Apellido1', 'Apellido2', '1990-01-01', NOW(), true),
('@usuario2', 'usuario2@example.com', md5('pass2'), 'Nombre2', 'Apellido3', 'Apellido4', '1985-05-15', NOW(), false),
('@usuario3', 'usuario3@example.com', md5('pass3'), 'Nombre3', 'Apellido5', 'Apellido6', '1992-11-30', NOW(), true),
('@usuario4', 'usuario4@example.com', md5('pass4'), 'Nombre4', 'Apellido7', 'Apellido8', '1988-09-22', NOW(), false),
('@usuario5', 'usuario5@example.com', md5('pass5'), 'Nombre5', 'Apellido9', 'Apellido10', '1995-07-12', NOW(), true),
('@usuario6', 'usuario6@example.com', md5('pass6'), 'Nombre6', 'Apellido11', 'Apellido12', '1982-03-05', NOW(), false),
('@usuario7', 'usuario7@example.com', md5('pass7'), 'Nombre7', 'Apellido13', 'Apellido14', '1998-06-28', NOW(), true),
('@usuario8', 'usuario8@example.com', md5('pass8'), 'Nombre8', 'Apellido15', 'Apellido16', '1987-12-17', NOW(), false),
('@usuario9', 'usuario9@example.com', md5('pass9'), 'Nombre9', 'Apellido17', 'Apellido18', '1994-04-03', NOW(), true),
('@usuario10', 'usuario10@example.com', md5('pass10'), 'Nombre10', 'Apellido19', 'Apellido20', '1980-08-09', NOW(), false);

/*
-- Suponiendo que los usuarios 1, 2 y 3 ya han iniciado sesión y el usuario 1 ha cerrado sesión.
INSERT INTO user_log (id_user, log_out) VALUES
(1, NOW()),
(2, NULL),
(3, NULL),
(4, NULL),
(5, NOW()),
(6, NOW()),
(7, NOW()),
(8, NULL),
(9, NOW()),
(10, NULL);
*/

-- Estableciendo algunas relaciones de "nakama" entre usuarios.
/*INSERT INTO user_nakama (id_user_follower, id_user_leader) VALUES
(1, 2),
(2, 3),
(3, 1),
(4, 5),
(5, 6),
(6, 7),
(8, 9),
(9, 10),
(10, 1),
(1, 3);*/

