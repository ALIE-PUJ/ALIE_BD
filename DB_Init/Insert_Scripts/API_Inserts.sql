-- Insertar categorías en la tabla Categoria
INSERT INTO Categoria (id_categoria, nombre) VALUES
(1, 'Student'),
(2, 'Admin');

-- Insertar administradores en la tabla Usuario
INSERT INTO Usuario (usuario, contrasena, email, id_categoria) VALUES
('Luis Bravo', 'contrasena_segura_luis', 'luis.bravo@javeriana.edu.com', 2), -- Admin
('Ana Ortegon', 'contrasena_segura_ana', 'ana.ortegon@javeriana.edu.com', 2), -- Admin
('Maria Avellaneda', 'contrasena_segura_maria', 'maria.avellaneda@javeriana.edu.com', 2), -- Admin
('Juan Sanchez', 'contrasena_segura_juan', 'juan.sanchez@javeriana.edu.com', 2); -- Admin

-- Insertar estudiantes en la tabla Usuario
INSERT INTO Usuario (usuario, contrasena, email, id_categoria) VALUES
('Pepito perez', 'contrasena_segura_pepito', 'pepito@javeriana.edu.com', 1); -- Student

-- Insertar un chat de ejemplo en la tabla Chat
INSERT INTO Chat (memory_key, nombre, mensajes_agente, mensajes_usuario, mensajes_supervision, user_id, archivado, intervenido) VALUES
(
    'chat_12345',  -- memory_key
    'Chat de Prueba',  -- nombre
    ARRAY['{"texto": "Hola, ¿en qué puedo ayudarte hoy?"}', '{"texto": "¿Necesitas ayuda con algún tema específico?"}']::TEXT[],  -- mensajes_agente
    ARRAY['{"texto": "Estoy buscando información sobre mi cuenta."}', '{"texto": "Sí, tengo algunas preguntas sobre las funcionalidades."}']::TEXT[],  -- mensajes_usuario
    ARRAY['{"texto": "Revisar la solicitud del usuario y proporcionar asistencia."}']::TEXT[],  -- mensajes_supervision
    1,  -- user_id (debe coincidir con un id_usuario válido en la tabla Usuario)
    FALSE,  -- archivado
    FALSE   -- intervenido
);
