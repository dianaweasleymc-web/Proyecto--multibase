--Creamos la tabla de estudiantes 
CREATE TABLE Estudiantes(
id_Alumno SERIAL PRIMARY KEY,
numeroControl VARCHAR(20),
nombre VARCHAR(100),
apellidoPaterno VARCHAR(100),
apellidoMaterno VARCHAR(100),
carrera TEXT, 
);

