1. Autenticacion
2. Guardar chats (Registros de usuario, agente y si hay, intervencion)
3. Guardar archivos que se suban, a la BD

Endpoints:

JUAN
/login recibe (Usuario y contraseña) Express.js (JWT). Retorna un token, y la informacion del usuario mas el rol
/asignar_rol recibe (Usuario, rol) retorna True si se asigno, False si no.

LUIS
/alie (Recibe un user_prompt, memory_key, priority) retorna un mensaje (Respuesta del agente). En caso de ser un retry, poner Priority = "True". Por defecto, priority = "False"

MAJO
/chat/guardar recibe memory_key y nombre(String), recibe mensajes_agente[], mensajes_usuario[], mensajes_supervision[] retorna True si se guardo, False si no. Se puede reutilizar para editar chats.
/chat/get recibe memory_key (String), retorna JSON del chat.
/chat/list recibe user_id (String), retorna una lista de memory_keys y nombres correspondientes a los chats de un usuario.
/chat/list_all retorna una lista de memory_keys y nombres correspondientes a TODOS los chats
/chat/delete recibe el memory_key de un chat y lo borra. Retorna true si se borro, False si no.
/chat/archive recibe el memory_key de un chat y lo archiva. Retorna true si se archivo, False si no.

ANA
/files/list_all retorna una lista con los IDs y nombres de todos los archivos subidos.
/files/submit recibe la categoria del archivo, agrega un archivo a la base de datos (Blob), retorna True si fue exitoso, false si no.
/files/delete borra un archivo de la base de datos (Blob), retorna True si fue exitoso, false si no.
Para editar, se borra y se sube otro.

LUIS
/tag recibe el ultimo mensaje del usuario y el ultimo mensaje del agente, ademas de el estado=pos o neg, retorna True si fue exitoso, False si no.


Funcion general de auth, que se llama siempre que llega un request antes de enviar una respuesta al cliente.