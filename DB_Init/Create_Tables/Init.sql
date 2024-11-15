-- Tabla Carrera
CREATE TABLE IF NOT EXISTS Carrera (
    id_carrera SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla Estudiante
CREATE TABLE IF NOT EXISTS Estudiante (
    id_estudiante SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    id_carrera INT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(30),
    direccion TEXT,
    FOREIGN KEY (id_carrera) REFERENCES Carrera(id_carrera)
);

-- Tabla Profesor
CREATE TABLE IF NOT EXISTS Profesor (
    id_profesor SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(30)
);

-- Tabla Curso
CREATE TABLE IF NOT EXISTS Curso (
    id_curso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INT NOT NULL,
    descripcion TEXT
);

-- Tabla Clase
CREATE TABLE IF NOT EXISTS Clase (
    id_clase SERIAL PRIMARY KEY,
    id_curso INT NOT NULL,
    periodo VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_final DATE NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
);

-- Tabla Nota
CREATE TABLE IF NOT EXISTS Nota (
    id_nota SERIAL PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    id_clase INT NOT NULL,
    nota DECIMAL(3, 2) NOT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiante(id_estudiante),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_clase) REFERENCES Clase(id_clase)
);

-- Tabla intermedia Estudiante_Clase para la relación muchos a muchos
CREATE TABLE IF NOT EXISTS Estudiante_Clase (
    id_estudiante INT NOT NULL,
    id_clase INT NOT NULL,
    PRIMARY KEY (id_estudiante, id_clase),
    FOREIGN KEY (id_estudiante) REFERENCES Estudiante(id_estudiante),
    FOREIGN KEY (id_clase) REFERENCES Clase(id_clase)
);


-- Tabla Prerrequisito_Curso
CREATE TABLE IF NOT EXISTS Prerrequisito_Curso(
    id_curso INT NOT NULL,
    id_prerrequisito_curso INT NOT NULL,
    PRIMARY KEY (id_curso, id_prerrequisito_curso),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_prerrequisito_curso) REFERENCES Curso(id_curso)
);

-- Tabla Horario_Clase
CREATE TABLE IF NOT EXISTS Horario_Clase (
    id_clase INT NOT NULL,
    dia VARCHAR(10) NOT NULL, 
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    PRIMARY KEY (id_clase, dia, hora_inicio, hora_fin),
    FOREIGN KEY (id_clase) REFERENCES Clase(id_clase)
);

-- Tabla Semestre_Sugerido
CREATE TABLE IF NOT EXISTS Semestre_Sugerido (
    id_curso INT NOT NULL,
    semestre INT NOT NULL,
    tipo_curso VARCHAR(50) NOT NULL CHECK (tipo_curso IN ('Núcleo de Formación Fundamental', 'Énfasis', 'Complementaria', 'Electiva')),
    PRIMARY KEY (id_curso, semestre),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
);
