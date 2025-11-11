from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Optional, NumberRange



# Formulario para el registro de usuarios finales
# Basado en los requisitos de la consigna
class FormRegistro(FlaskForm):
    nombre = StringField(label="Nombre", validators=[DataRequired()])
    apellido = StringField(label="Apellido", validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    nombre_usuario = StringField(label="Nombre de Usuario", validators=[DataRequired()])

    # Opciones para el campo 'claustro'
    claustro_opciones = [('estudiante', 'Estudiante'), ('docente', 'Docente'), ('PAYS', 'PAYS')]
    claustro = SelectField(label='Claustro', choices=claustro_opciones, validators=[DataRequired()])

    password = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=4)])
    # La consigna pide 'contraseña repetida'
    confirmacion = PasswordField(label='Repetir Contraseña', 
                                 validators=[DataRequired(), 
                                             EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField(label='Registrarse')

# Formulario para el Login (común a todos los usuarios)
class FormLogin(FlaskForm):
    nombre_usuario = StringField(label='Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField(label='Contraseña', validators=[DataRequired()])
    submit = SubmitField(label='Ingresar')

class FormCrearReclamo(FlaskForm):
    """
    Formulario para que el usuario final cree un nuevo reclamo.

    """
    contenido = TextAreaField(
        label='Detalle su reclamo', 
        validators=[DataRequired(), Length(min=10, max=1000)], # Pedimos al menos 10 caracteres
        render_kw={"rows": 5} # Para que la caja de texto sea más grande
    )
    submit = SubmitField(label='Buscar reclamos similares')

class FormEditarEstado(FlaskForm):
    """
    Formulario para que el admin cambie el estado de un reclamo.

    """
    # Lista de los 4 estados posibles
    opciones_estado = [
        ('pendiente', 'Pendiente'),
        ('en proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('inválido', 'Inválido')
    ]
    estado = SelectField(label='Nuevo Estado', 
                         choices=opciones_estado, 
                         validators=[DataRequired()])

    # Campo para el tiempo de resolución. Es opcional,
    # porque solo se usa si el estado es 'en proceso'.
    #
    tiempo_resolucion = IntegerField(
        label='Tiempo de Resolución (en días, 1-15)',
        validators=[
            Optional(), # Permite que el campo esté vacío
            NumberRange(min=1, max=15, message="Debe estar entre 1 y 15 días")
        ],
        render_kw={"placeholder": "Solo si está 'En Proceso'"}
    )

    submit = SubmitField(label='Actualizar Estado')


class FormDerivarReclamo(FlaskForm):
    """
    Formulario para que Secretaría Técnica derive un reclamo.

    """
    # Lista de los 3 departamentos válidos
    opciones_depto = [
        ('soporte informático', 'Soporte Informático'),
        ('maestranza', 'Maestranza'),
        ('secretaría técnica', 'Secretaría Técnica')
    ]
    departamento = SelectField(label='Nuevo Departamento', 
                               choices=opciones_depto, 
                               validators=[DataRequired()])

    submit = SubmitField(label='Derivar Reclamo')

    