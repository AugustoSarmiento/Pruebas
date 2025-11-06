# Datos para usuarios finales
USUARIOS_INICIALES = [
    {
        "nombre": "Juan", "apellido": "Perez", "email": "juan@mail.com",
        "nombre_usuario": "juanperez", "claustro": "estudiante", "contrasena": "pass123"
    },
    {
        "nombre": "Maria", "apellido": "Lopez", "email": "maria@mail.com",
        "nombre_usuario": "marialopez", "claustro": "docente", "contrasena": "pass456"
    },
    {
        "nombre": "Carlos", "apellido": "Sanchez", "email": "carlos@mail.com",
        "nombre_usuario": "carlossanchez", "claustro": "PAyS", "contrasena": "pass789"
    }
]

# Datos para reclamos

RECLAMOS_INICIALES = [
    {
        "creador_username": "juanperez",
        "contenido": "El aula 5 no tiene tizas ni borrador.",
        # El departamento lo asignará automáticamente nuestro clasificador
    },
    {
        "creador_username": "marialopez",
        "contenido": "No funciona la red wifi en la biblioteca.",
    },
    {
        "creador_username": "carlossanchez",
        "contenido": "El proyector del aula magna no enciende.",
    },
    {
        "creador_username": "juanperez",
        "contenido": "Los baños del primer piso están siempre sucios.",
    }
]