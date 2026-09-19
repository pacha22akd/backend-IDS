CREATE TABLE IF NOT EXISTS deportes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL
);

CREATE TABLE IF NOT EXISTS canchas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

CREATE TABLE IF NOT EXISTS socios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL,
    email VARCHAR(100) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_cancha INT NOT NULL,
    id_socio INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    estado ENUM('confirmada','cancelada','finalizada') NOT NULL DEFAULT 'confirmada',
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,
    FOREIGN KEY (id_cancha) REFERENCES canchas(id),
    FOREIGN KEY (id_socio) REFERENCES socios(id)
);

--INSERT DE ARCHIVOS DE PRUEBA--

INSERT INTO deportes (nombre) VALUES
("Futbol"),
("Tenis"),
("Padel");

INSERT INTO canchas (id_deporte, nombre, precio_hora, activa) VALUES
    (1, 'Cancha Futbol 1', 1000000, TRUE),   
    (1, 'Cancha Futbol 2', 1200000, TRUE),   
    (2, 'Cancha Tenis 1',   800000, TRUE),   
    (2, 'Cancha Tenis 2',   800000, TRUE),
    (3, 'Cancha Padel 1',   900000, TRUE),
    (3, 'Cancha Padel 2',   900000, FALSE);  

INSERT INTO socios (nombre, email, activo) VALUES
    ('Ana Gómez', 'ana.gomez@example.com', TRUE),
    ('Bruno Díaz', 'bruno.diaz@example.com', TRUE),
    ('Carla Fernández', 'carla.fernandez@example.com', FALSE),
    ('Diego López', 'diego.lopez@example.com', FALSE);

INSERT INTO reservas (id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, estado, tarifa_historica, importe_total) VALUES
    (1, 1, '2026-10-15 18:00:00', '2026-10-15 20:00:00', 'confirmada', 1000000, 2000000),
    (3, 2, '2026-10-16 09:00:00', '2026-10-16 10:00:00', 'confirmada',  800000,  800000),
    (5, 3, '2026-10-17 20:00:00', '2026-10-17 22:00:00', 'cancelada',   900000, 1800000);
