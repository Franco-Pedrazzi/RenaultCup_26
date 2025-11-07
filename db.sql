
DROP DATABASE IF EXISTS Copa_Renault;
CREATE DATABASE Copa_Renault;
USE Copa_Renault;

CREATE TABLE `usuario` (
  `Nombre` VARCHAR(40) not NULL,
  `Email` VARCHAR(40) not NULL,
  `Contraseña` VARCHAR(200) not NULL,
  `rango`  VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`Email`)
);

CREATE TABLE `Verificacion` (
  `Email` VARCHAR(40) not NULL,
  `codigo` VARCHAR(20) not NULL,
  `contra_codificada`  VARCHAR(200) not null,
  `nombre` VARCHAR(40) not NULL,
  `rango` VARCHAR(20) not NULL,
  PRIMARY KEY (`codigo`)
);


CREATE TABLE `examples` (
  `id` INT AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL DEFAULT '-',
  PRIMARY KEY (`id`)
);
		
CREATE TABLE `Equipo` (
  `id` int AUTO_INCREMENT,
  `Deporte` VARCHAR(10) NULL DEFAULT '-',
  `Categoria` VARCHAR(10) NULL DEFAULT '-',
  `Sexo` VARCHAR(10) NULL DEFAULT '-',
  `Colegio` VARCHAR(50) NULL DEFAULT '-' COMMENT 'Agregar A o B si los demás campos son iguales',
  PRIMARY KEY (`id`)
);

CREATE TABLE `jugador` (
  `id` int AUTO_INCREMENT,
  `id_equipo` int NULL DEFAULT NULL,
  `Nombre` VARCHAR(50) NULL DEFAULT '-',
  `DNI` Varchar(10) NULL DEFAULT NULL,
  `Telefono` Varchar(15) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Comida_especial` VARCHAR(3) NULL DEFAULT 'N',
  `Fecha_nacimiento` DATE NULL DEFAULT NULL,
  `Infracciones` VARCHAR(10) NULL DEFAULT '0',
  PRIMARY KEY (`id`)
);
		
CREATE TABLE `Responsable` (
  `id`int AUTO_INCREMENT,
  `id_equipo` int NULL DEFAULT NULL,
  `Nombre` VARCHAR(50) NULL DEFAULT '-',
  `DNI` Varchar(10) NULL DEFAULT NULL,
  `Telefono` Varchar(15) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Comida_especial` VARCHAR(3) NULL DEFAULT 'N',
  `Fecha_nacimiento` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

		
CREATE TABLE `Partido` (
  `id`int AUTO_INCREMENT,
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
  `Puntaje_e1` int NULL DEFAULT 0,
  `Puntaje_e2` int NULL DEFAULT 0,
  `Resultado` int NULL DEFAULT NULL COMMENT '0 no jugado, 3 empate',
  `Infracciones_e1` int(3) NULL DEFAULT NULL,
  `Infracciones_e2` int(3) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

		
CREATE TABLE `Staff` (
  `id` int AUTO_INCREMENT,
  `Nombre` VARCHAR(40) NULL DEFAULT NULL,
  `DNI` int(8) NULL DEFAULT NULL,
  `Telefono` int(20) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Trabajo` VARCHAR(15) NULL DEFAULT NULL,
  `Sector` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Producto` (
  `id` int AUTO_INCREMENT,
  `Nombre` VARCHAR(40) NULL DEFAULT NULL,
  `Precio` int(8) NULL DEFAULT NULL,
  `tipo_img` VARCHAR(50),
  `tamaño_img` BIGINT,
  `pixel_img` LONGBLOB,
  PRIMARY KEY (`id`)
);

ALTER TABLE `jugador` ADD FOREIGN KEY (id_equipo) REFERENCES `Equipo` (`id`);
ALTER TABLE `Responsable` ADD FOREIGN KEY (id_equipo) REFERENCES `Equipo` (`id`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Arbitro) REFERENCES `Staff` (`id`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Planillero) REFERENCES `Staff` (`id`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Equipo_1) REFERENCES `Equipo` (`id`);
ALTER TABLE `Partido` ADD FOREIGN KEY (Equipo_2) REFERENCES `Equipo` (`id`);
