--Tablas para el sistema de Bibloteca
--Creamos la tabla de estudiantes 
CREATE TABLE Estudiantes(
	id_Alumno SERIAL PRIMARY KEY,
	numeroControl VARCHAR(20),
	nombre VARCHAR(100),
	apellidoPaterno VARCHAR(100),
	apellidoMaterno VARCHAR(100),
	carrera TEXT 
);

--Creamos la tabla de Libros
CREATE TABLE Libros (
    id_Libro SERIAL PRIMARY KEY,
    nombre TEXT, 
    autor TEXT, 
    editorial VARCHAR(100),
    id_Genero INT,
    FOREIGN KEY (id_Genero) REFERENCES Genero(id_Genero)
);

--Creamos la tabla de Prestamo 
CREATE TABLE Prestamo(
	 id_Prestamo SERIAL PRIMARY KEY, 
	 id_Alumno INT,
	 id_Libro INT,
	 FOREIGN KEY (id_Libro) REFERENCES Libros(id_Libro),
	 FOREIGN KEY (id_Alumno) REFERENCES Estudiantes(id_Alumno),
	 fechaPrestamo DATE, 
	 fechaEntrega DATE
);

--Creamos la tabla de catalogo 
CREATE TABLE Genero(
	id_Genero SERIAL PRIMARY KEY,
	tipoGenero VARCHAR(100)
);

CREATE TABLE Autores (
    id_Autor SERIAL PRIMARY KEY,
    nombre VARCHAR(150),
    nacionalidad VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Editoriales (
    id_Editorial SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    pais VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);
INSERT INTO Genero(tipoGenero) VALUES 
	('CienciaFiccion'),
	('Novelas'),
	('Fantacia');

INSERT INTO Estudiantes(numeroControl, nombre, apellidoPaterno, apellidoMaterno, carrera) VALUES
	(23290660, 'Diana Guadalupe', 'Moreno', 'Cisneros', 'Ingeneria Informatica'),
	(24290701, 'Jonathan Ulises', 'Moreno', 'Cisneros', 'Ingeneria en Sistemas Computacionales'),
	(23290551, 'Daniel Hassael',  'Mendiola', 'Alonsso', 'Ingeneria Informatica'),
	(23290364, 'Harry James', 'Potter', 'Granger', 'Ingeneria en Sistemas Computacionales');

INSERT INTO Libros(nombre, autor, editorial, id_Genero) VALUES
('Cien Años de Soledad', 'Gabriel García Márquez', 'Editorial Sudamericana', 1),
('Harry Potter y la priedra filosofal', 'J.K Rowling ', 'Salamandra', 2),
('Las Cronicas de Narnia(El león, la bruja y el ropero)', 'C. S. Lewis', 'Editorial Destino', 3);

-- Insertar datos en Autores
INSERT INTO Autores (nombre, nacionalidad, activo) VALUES 
('Gabriel García Márquez', 'Colombiana', TRUE),
('J.K. Rowling', 'Británica', TRUE),
('C.S. Lewis', 'Británica', TRUE);

-- Insertar datos en Editoriales
INSERT INTO Editoriales (nombre, pais, activo) VALUES 
('Editorial Sudamericana', 'Argentina', TRUE),
('Salamandra', 'España', TRUE),
('Editorial Destino', 'España', TRUE);

--Borrador logico-->borra el redistro donde ejecuta el update lo cual cambia el estado
UPDATE Libros SET activo = FALSE WHERE id_Libro = $s;

--Consultas con el GET 
SELECT * FROM Libros WHERE activo = TRUE;
	