# Lista de diccionarios que contiene los datos del personal a precargar en el sistema.
# Para añadir un nuevo jefe, simplemente se agrega un nuevo diccionario a esta lista.
# modules/inicializacion.py
DATOS_PERSONAL = [
    {
        "rol": "jefe", "nombre": "Laura", "apellido": "García", "email": "laura.garcia@uner.edu.ar",
        "nombre_usuario": "lauragarcia", "contrasena": "jefe123", 
        "departamento_asignado": "soporte informático" 
    },
    {
        "rol": "jefe", "nombre": "Carlos", "apellido": "Martínez", "email": "carlos.martinez@uner.edu.ar",
        "nombre_usuario": "carlosmartinez", "contrasena": "jefe456", 
        "departamento_asignado": "maestranza"  
    },
    {
        "rol": "secretario", "nombre": "Ana", "apellido": "López", "email": "ana.lopez@uner.edu.ar",
        "nombre_usuario": "analopez", "contrasena": "sec123"
        # Secretaría Técnica no necesita 'departamento_asignado' porque es un rol especial
    }
]