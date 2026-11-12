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
	