from modules.factoria import crear_repositorio_usuarios, crear_repositorio_reclamos
from modules.sistema import SistemaGestionReclamos
from modules.inicializacion import DATOS_PERSONAL # Datos para inicializar personal
from modules.roles import JefeDepartamento, SecretarioTecnico # Clases específicas
from modules.excepciones import UsuarioExistenteError # Para manejar errores al inicializar
from flask import render_template, request, redirect, url_for, session, flash
from modules.config import app, login_manager # Importamos app y login_manager
from modules.formularios import FormRegistro, FormLogin, FormCrearReclamo # Importamos los formularios
from modules.gestor_login import GestorDeLogin # Importamos el gestor
from modules.excepciones import UsuarioInexistenteError, UsuarioExistenteError
from modules.usuario import Usuario # Para el chequeo de contraseñas


repo_usuarios = crear_repositorio_usuarios()
repo_reclamos = crear_repositorio_reclamos()
sistema = SistemaGestionReclamos(repo_usuarios, repo_reclamos)

print("Creando gestor de login...")
gestor_login = GestorDeLogin(login_manager, repo_usuarios)

@app.context_processor
def inject_gestor_login():
    """
    Inyecta la variable 'gestor_login' en el contexto de todas las plantillas.
    Esto es necesario para que 'base.html' pueda usarla en la barra de navegación.
    """
    return dict(gestor_login=gestor_login)

# --- Inicialización del personal (SIN HASHING) ---
print("Inicializando personal...")
for datos_persona in DATOS_PERSONAL:
    try:
        usuario_existente = repo_usuarios.obtener_por_filtro(nombre_usuario=datos_persona["nombre_usuario"])
        if usuario_existente:
            print(f"Usuario '{datos_persona['nombre_usuario']}' ya existe, omitiendo creación inicial.")
            continue

        if datos_persona["rol"] == "jefe":
            nuevo_personal = JefeDepartamento(
                nombre=datos_persona["nombre"], apellido=datos_persona["apellido"], email=datos_persona["email"],
                nombre_usuario=datos_persona["nombre_usuario"],
                contrasena=datos_persona["contrasena"], # Contraseña en texto plano
                departamento_asignado=datos_persona["departamento_asignado"]
            )
        elif datos_persona["rol"] == "secretario":
            nuevo_personal = SecretarioTecnico(
                nombre=datos_persona["nombre"], apellido=datos_persona["apellido"], email=datos_persona["email"],
                nombre_usuario=datos_persona["nombre_usuario"],
                contrasena=datos_persona["contrasena"] # Contraseña en texto plano
            )
        else:
            continue

        repo_usuarios.guardar(nuevo_personal)
        print(f"Usuario '{nuevo_personal.nombre_usuario}' ({datos_persona['rol']}) creado.")

    except KeyError as e:
        print(f"Error al inicializar personal: falta la clave {e} en los datos.")
    except UsuarioExistenteError as e:
         print(f"Error al guardar personal: {e}")
    except Exception as e:
         print(f"Error inesperado al inicializar personal '{datos_persona.get('nombre_usuario', 'Desconocido')}': {e}")

print("Inicialización de personal completada.")


@app.route("/")
def inicio():
    """
    Ruta principal. Redirige al panel si el usuario está logueado,
    o muestra la página de inicio pública si no lo está.
    """
    if gestor_login.usuario_autenticado:
        return redirect(url_for('panel_principal'))
    
    return render_template("inicio.html")

# --- RUTAS DE AUTENTICACIÓN ---

@app.route("/register", methods=["GET", "POST"])
def register():
    """Ruta para registrar un nuevo usuario final."""
    form = FormRegistro()
    
    if form.validate_on_submit():
        # Si el formulario es válido, intentamos registrar al usuario
        try:
            sistema.registrar_usuario(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                email=form.email.data,
                nombre_usuario=form.nombre_usuario.data,
                claustro=form.claustro.data,
                contrasena=form.password.data
                # No pasamos la 'confirmacion', ya fue validada por el formulario
            )
            # Si tiene éxito, mostramos un mensaje y lo mandamos a loguearse
            flash("¡Registro exitoso! Por favor, inicia sesión.", "success")
            return redirect(url_for('login'))
        except UsuarioExistenteError as e:
            # Si falla (ej. email ya existe), mostramos el error
            flash(str(e), "danger")
        except Exception as e:
            flash(f"Error inesperado al registrar: {e}", "danger")
            
    # Si es GET o el formulario no es válido, mostramos la plantilla de registro
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Ruta para iniciar sesión (todos los roles)."""
    form = FormLogin()
    
    if form.validate_on_submit():
        try:
            # 1. Buscar al usuario
            usuario_entidad = sistema.buscar_usuario(form.nombre_usuario.data)
            
            # 2. Validar la contraseña (SIN HASHING)
            if not usuario_entidad.validar_contrasena(form.password.data):
                raise ValueError("Contraseña incorrecta.")
                
            # 3. Iniciar sesión
            gestor_login.login(usuario_entidad)
            flash(f"Bienvenido, {usuario_entidad.nombre}!", "success")
            
            # 4. Redirigir al panel principal
            return redirect(url_for('panel_principal'))
            
        except (UsuarioInexistenteError, ValueError) as e:
            flash(f"Error al iniciar sesión: {e}", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@gestor_login.se_requiere_login # Protegemos esta ruta
def logout():
    """Ruta para cerrar sesión."""
    gestor_login.logout()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('inicio'))


# --- RUTA PRINCIPAL (LOGUEADO) ---

@app.route("/panel")
@gestor_login.se_requiere_login # Esta es la protección de Flask-Login
def panel_principal():
    """
    Panel principal al que accede el usuario tras iniciar sesión.
    Aquí se mostrarán distintas cosas según el rol.
    """
    flash("Esta es una prueba de flash DESDE el panel.", "warning")
    mensaje_prueba = session.pop('prueba_manual', None)
    print(f"VALOR DE PRUEBA EN SESIÓN: {mensaje_prueba}")
    usuario_actual = gestor_login.usuario_actual
    
    # (Aún no hemos creado esta plantilla, lo haremos ahora)
    return render_template("panel_usuario.html", usuario=usuario_actual, mensaje_prueba=mensaje_prueba)

@app.route("/crear_reclamo", methods=["GET", "POST"])
@gestor_login.se_requiere_login
def crear_reclamo():
    """
    Paso 1 del flujo de creación:
    - Muestra el formulario para escribir el reclamo.
    - Al enviar (POST), clasifica el contenido y busca similares.
    - Muestra la lista de similares para que el usuario decida.
    """
    form = FormCrearReclamo()

    if form.validate_on_submit():
        # El formulario es válido, procesamos el contenido
        contenido = form.contenido.data

        # Usamos el método del sistema para clasificar y buscar
        reclamos_similares = sistema.buscar_reclamos_similares(contenido)

        if not reclamos_similares:
            # No se encontraron similares
            try:
                # Creamos el reclamo directamente
                nuevo_reclamo = sistema.crear_reclamo(
                    usuario_creador=gestor_login.usuario_actual.entidad,
                    contenido=contenido
                )
                flash(f"Reclamo #{nuevo_reclamo.id_reclamo} creado exitosamente y derivado a '{nuevo_reclamo.departamento}'.", "success")
                return redirect(url_for('panel_principal')) # Volvemos al panel
            except Exception as e:
                flash(f"Error al crear el reclamo: {e}", "danger")

        else:
            # ¡Se encontraron reclamos similares!
            # Guardamos el contenido temporalmente en la sesión
            session['reclamo_temporal'] = contenido

            # Mostramos la página de "confirmación"
            return render_template("confirmar_reclamo.html", 
                                   reclamos_similares=reclamos_similares, 
                                   contenido_nuevo=contenido)

    # Si es GET (o el form no es válido), solo mostramos el formulario
    return render_template("crear_reclamo.html", form=form)


# server.py

# ... (después de la ruta @app.route("/crear_reclamo", ...)) ...

@app.route("/crear_reclamo_confirmado", methods=["POST"])
@gestor_login.se_requiere_login
def crear_reclamo_confirmado():
    """
    Ruta que procesa la decisión final de crear un reclamo nuevo
    después de haber visto los similares.
    """
    # Recuperamos el contenido del reclamo que guardamos temporalmente en la sesión
    contenido = session.pop('reclamo_temporal', None) 
    
    if not contenido:
        flash("Error: No hay un reclamo temporal para crear. Por favor, intente de nuevo.", "danger")
        return redirect(url_for('crear_reclamo'))
        
    try:
        # Usamos el método 'crear_reclamo' del sistema
        nuevo_reclamo = sistema.crear_reclamo(
            usuario_creador=gestor_login.usuario_actual.entidad,
            contenido=contenido
        )
        session['prueba_manual'] = 'ESTO ES UNA PRUEBA DE SESION'
        flash(f"Reclamo #{nuevo_reclamo.id_reclamo} creado exitosamente y derivado a '{nuevo_reclamo.departamento}'.", "success")
    except Exception as e:
        flash(f"Error al crear el reclamo: {e}", "danger")

    # Siempre redirigimos al panel principal después de la acción
    return redirect(url_for('panel_principal'))


@app.route("/adherir/<int:id_reclamo>", methods=["POST"])
@gestor_login.se_requiere_login
def adherir_reclamo(id_reclamo):
    """
    Ruta para adherir el usuario actual a un reclamo existente.
    """
    # Borramos el reclamo temporal de la sesión, ya que no lo vamos a crear
    session.pop('reclamo_temporal', None) 
    
    try:
        # Obtenemos la entidad del usuario actual
        usuario_actual = gestor_login.usuario_actual.entidad
        
        # Llamamos al método del sistema para adherir
        sistema.adherir_a_reclamo(usuario_actual, id_reclamo)
        flash(f"Te has adherido exitosamente al reclamo #{id_reclamo}.", "success")
    
    except Exception as e:
        flash(f"Error al adherirse al reclamo: {e}", "danger")

    return redirect(url_for('panel_principal'))

@app.route("/listar_reclamos")
@gestor_login.se_requiere_login
def listar_reclamos():
    """
    Ruta para la Opción 2: Listar todos los reclamos pendientes,
    con opción de filtrar por departamento.

    """
    # Obtenemos el departamento del filtro (si existe en la URL)
    filtro_depto = request.args.get('departamento', None)

    lista_reclamos = []
    if filtro_depto:
        # Si hay un filtro, buscamos por ese departamento
        lista_reclamos = sistema.buscar_reclamos_pendientes_por_departamento(filtro_depto)
    else:
        # Si no hay filtro, traemos todos los pendientes
        lista_reclamos = sistema.buscar_reclamos_pendientes_todos()

    # Lista de departamentos para armar los botones de filtro
    departamentos_posibles = ["soporte informático", "secretaría técnica", "maestranza"]

    return render_template("listar_reclamos.html", 
                           reclamos=lista_reclamos,
                           departamentos=departamentos_posibles,
                           filtro_actual=filtro_depto)


@app.route("/mis_reclamos")
@gestor_login.se_requiere_login
def mis_reclamos():
    """
    Ruta para la Opción 3: Mostrar solo los reclamos del usuario logueado.
    (Implementación pendiente)
    """
    # TODO: Implementar la lógica de búsqueda
    flash("La página 'Mis Reclamos' aún está en construcción.", "info")
    return redirect(url_for('panel_principal'))

# --- Punto de entrada para ejecutar la aplicación ---
if __name__ == "__main__":
    # debug=True reinicia el servidor automáticamente con cada cambio
    # host='0.0.0.0' permite que sea accesible desde tu red
    app.run(debug=True, host='0.0.0.0', port=5000)