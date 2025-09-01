DROP DATABASE IF EXISTS Copa_Renault;
CREATE DATABASE Copa_Renault;
USE Copa_Renault;

CREATE TABLE `examples` (
  `id_example` INT AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL DEFAULT '-',
  PRIMARY KEY (`id_example`)
);
		
CREATE TABLE `Equipo` (
  `id_equipo` int AUTO_INCREMENT,
  `Deporte` VARCHAR(10) NULL DEFAULT '-',
  `Categoria` VARCHAR(10) NULL DEFAULT '-',
  `Sexo` VARCHAR(10) NULL DEFAULT '-',
  `Colegio` VARCHAR(50) NULL DEFAULT '-' COMMENT 'Agregar A o B si los demás campos son iguales',
  PRIMARY KEY (`id_equipo`)
);

CREATE TABLE `jugador` (
  `id_jugador` int AUTO_INCREMENT,
  `id_equipo` int NULL DEFAULT NULL,
  `Nombre` VARCHAR(50) NULL DEFAULT '-',
  `DNI` Varchar(10) NULL DEFAULT NULL,
  `Telefono` Varchar(15) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Comida_especial` VARCHAR(3) NULL DEFAULT 'N',
  `Fecha_nacimiento` DATE NULL DEFAULT NULL,
  `Infracciones` VARCHAR(10) NULL DEFAULT '0',
  PRIMARY KEY (`id_jugador`)
);
		
CREATE TABLE `Responsable` (
  `id_profesor`int AUTO_INCREMENT,
  `id_equipo` int NULL DEFAULT NULL,
  `Nombre` VARCHAR(50) NULL DEFAULT '-',
  `DNI` Varchar(10) NULL DEFAULT NULL,
  `Telefono` Varchar(15) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Comida_especial` VARCHAR(3) NULL DEFAULT 'N',
  `Fecha_nacimiento` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`id_profesor`)
);

		
CREATE TABLE `Partido` (
  `id_partido`int AUTO_INCREMENT,
  `Deporte` VARCHAR(1) NULL DEFAULT NULL,
  `Categoria` VARCHAR(3) NULL DEFAULT NULL,
  `Sexo` VARCHAR(1) NULL DEFAULT NULL,
  `Arbitro` int NULL DEFAULT NULL,
  `Planillero` int NULL DEFAULT NULL,
  `Equipo_1` int NULL DEFAULT NULL,
  `Equipo_2` int NULL DEFAULT NULL,
  `Fase` VARCHAR(25) NULL DEFAULT NULL,
  `Horario_inicio` TIME NULL DEFAULT NULL,
  `Horario_final` TIME NULL DEFAULT NULL,
  PRIMARY KEY (`id_partido`)
);

CREATE TABLE `Resultado` (
  `id_partido` int AUTO_INCREMENT,
  `Puntaje_e1` int NULL DEFAULT 0,
  `Puntaje_e2` int NULL DEFAULT 0,
  `Resultado` int NULL DEFAULT NULL COMMENT '0 no jugado, 3 empate',
  `Infracciones_e1` int(3) NULL DEFAULT NULL,
  `Infracciones_e2` int(3) NULL DEFAULT NULL,
  PRIMARY KEY (`id_partido`)
);

		
CREATE TABLE `Cuenta_habilitada` (
  `Nombre` VARCHAR(40) not NULL,
  `Email` VARCHAR(40) not NULL,
  `Contraseña` VARCHAR(200) not NULL,
  `rango`  VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`Email`)
);

		
CREATE TABLE `Staff` (
  `id_staff` int AUTO_INCREMENT,
  `Nombre` VARCHAR(40) NULL DEFAULT NULL,
  `DNI` int(8) NULL DEFAULT NULL,
  `Telefono` int(20) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Trabajo` VARCHAR(15) NULL DEFAULT NULL,
  `Sector` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id_staff`)
);

CREATE TABLE `Verificacion` (
  `id` int not NULL auto_increment,
  `Email` VARCHAR(40) not NULL,
  `codigo` VARCHAR(20) not NULL,
  `contra_codificada`  VARCHAR(200) not null,
  `nombre` VARCHAR(40) not NULL,
  `rango` VARCHAR(20) not NULL,
  PRIMARY KEY (`id`)
);

ALTER TABLE `jugador` ADD FOREIGN KEY (id_equipo) REFERENCES `Equipo` (`id_equipo`);
ALTER TABLE `Responsable` ADD FOREIGN KEY (id_equipo) REFERENCES `Equipo` (`id_equipo`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Arbitro) REFERENCES `Staff` (`id_staff`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Planillero) REFERENCES `Staff` (`id_staff`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Equipo_1) REFERENCES `Equipo` (`id_equipo`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Equipo_2) REFERENCES `Equipo` (`id_equipo`);
ALTER TABLE `Resultado` ADD FOREIGN KEY (id_partido) REFERENCES `Partido` (`id_partido`);