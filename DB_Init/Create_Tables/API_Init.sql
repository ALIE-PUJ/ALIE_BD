-- Tabla Categoria (Para almacenar las categorías disponibles)
CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE -- e.g., 'admin', 'student', 'supervisor'.
);

-- Tabla Usuario (Para login, categorías y asignación de categorías)
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario SERIAL PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    id_categoria INT, -- Se añade una columna para la categoría
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria) -- Clave foránea para la relación con la tabla Categoria
);

-- Tabla Chat (Para gestionar los chats)
CREATE TABLE IF NOT EXISTS Chat (
    memory_key VARCHAR(100) PRIMARY KEY,
    nombre VARCHAR(100),
    mensajes_agente TEXT[],
    mensajes_usuario TEXT[],
    mensajes_supervision TEXT[],
    user_id INT,
    archivado BOOLEAN DEFAULT FALSE,
    intervenido BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Usuario(id_usuario)
);

-- Tabla Archivo (Para subir, listar y eliminar archivos)
CREATE TABLE IF NOT EXISTS Archivo (
    id_archivo SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    archivo BYTEA NOT NULL
);
