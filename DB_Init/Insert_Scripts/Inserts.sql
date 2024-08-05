USE ALIE_DB;

-- Insertar datos de ejemplo en la tabla Carrera
INSERT INTO Carrera (id_carrera, nombre, descripcion) VALUES 
(1, 'Ingeniería en Sistemas', 'Carrera enfocada en el desarrollo de software y sistemas informáticos.'),
(2, 'Administración de Empresas', 'Carrera enfocada en la gestión y administración de organizaciones empresariales.'),
(3, 'Diseño Gráfico', 'Carrera enfocada en el diseño y la comunicación visual.')
ON CONFLICT (id_carrera) DO NOTHING;

-- Insertar datos de ejemplo en la tabla Estudiante
INSERT INTO Estudiante (id_estudiante, nombres, apellidos, fecha_nacimiento, id_carrera, email, telefono, direccion) VALUES 
(1, 'Juan', 'Pérez', '2000-05-15', 1, 'juan.perez@example.com', '123456789', 'Calle Falsa 123'),
(2, 'María', 'González', '1998-03-22', 2, 'maria.gonzalez@example.com', '987654321', 'Avenida Siempre Viva 456'),
(3, 'Luis', 'Martínez', '1999-11-11', 3, 'luis.martinez@example.com', '456789123', 'Boulevard Principal 789')
ON CONFLICT (id_estudiante) DO NOTHING;

-- Insertar datos de ejemplo en la tabla Profesor
INSERT INTO Profesor (id_profesor, nombres, apellidos, email, telefono) VALUES 
(1, 'Ana', 'Ramírez', 'ana.ramirez@example.com', '321654987'),
(2, 'Carlos', 'López', 'carlos.lopez@example.com', '654987321'),
(3, 'Laura', 'Hernández', 'laura.hernandez@example.com', '789321654')
ON CONFLICT (id_profesor) DO NOTHING;

-- Insertar datos de ejemplo en la tabla Curso
INSERT INTO Curso (id_curso, nombre, descripcion) VALUES 
(1, 'Curso de Programación', 'Curso básico de programación en diferentes lenguajes.'),
(2, 'Curso de Contabilidad', 'Curso básico de contabilidad para empresas.'),
(3, 'Curso de Diseño Gráfico', 'Curso básico de diseño gráfico y herramientas digitales.')
ON CONFLICT (id_curso) DO NOTHING;

-- Insertar datos de ejemplo en la tabla Clase
INSERT INTO Clase (id_clase, id_curso, periodo, fecha_inicio, fecha_final) VALUES 
(1, 1, '2023-1', '2023-01-10', '2023-06-10'),
(2, 2, '2023-1', '2023-01-15', '2023-06-15'),
(3, 3, '2023-2', '2023-08-01', '2023-12-01')
ON CONFLICT (id_clase) DO NOTHING;

-- Insertar datos de ejemplo en la tabla Nota
INSERT INTO Nota (id_nota, id_estudiante, id_curso, id_clase, nota) VALUES 
(1, 1, 1, 1, 9.5),
(2, 2, 2, 2, 8.7),
(3, 3, 3, 3, 7.8)
ON CONFLICT (id_nota) DO NOTHING;

-- Insertar datos de ejemplo en la tabla Estudiante_Clase
INSERT INTO Estudiante_Clase (id_estudiante, id_clase) VALUES 
(1, 1),
(2, 2),
(3, 3)
ON CONFLICT (id_estudiante, id_clase) DO NOTHING;
