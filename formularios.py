from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.core import DateField
from wtforms.fields.html5 import EmailField
from wtforms import Form, StringField, SubmitField, validators, DateField 

#-----------------PRINCIPAL------------------------------------------------------------------------------------
#-----------------PRINCIPAL------------------------------------------------------------------------------------
#-----------------PRINCIPAL------------------------------------------------------------------------------------

class  formlogin(FlaskForm):
    usuario = StringField("Usuario", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    contrasena=PasswordField("contraseña", validators=[validators.DataRequired(message="Ingrese  contraseña")])
    login = SubmitField("Login")

class  formregistro(Form):
    #-----------------basicos----------------------------
    pri_nombre = StringField("Primer Nombre", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    secu_nombre=StringField("segundo Nombre")
    pri_apellido = StringField("Primer apellido", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    secu_apellido=StringField("segundo apellido")
    #tdocumento=StringField("tipo de documento", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    ndocumento=StringField("numero de documento", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    #genero=StringField("genero")
    #-----------------de contacto----------------------------
    correo = EmailField("Correo", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    direccion=StringField("Direccion", validators=[validators.DataRequired(message="Ingrese  contraseña")])
    celular = StringField("Celular", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    telefono=StringField("Telefono")
    #-----------------medico----------------------------
    #regimen=StringField("regimen")
    #eps=StringField("eps")
    #-----------------de sesion----------------------------
    usuario = StringField("Usuario", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    contrasena=PasswordField("contraseña", validators=[validators.DataRequired(message="Ingrese  contraseña")])

    #-----------------boton----------------------------
    enviar = SubmitField("Enviar")

#-----------------PACIENTE------------------------------------------------------------------------------------
#-----------------PACIENTE------------------------------------------------------------------------------------
#-----------------PACIENTE------------------------------------------------------------------------------------

class  inicio_paciente(FlaskForm):
    Nota = StringField("nota")

class  form_configuraciones_paciente(Form):

   
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

    #-----------------de contacto----------------------------
    #-----------------div 3----------------
    correo = EmailField("correo")
    eps=StringField("EPS")
    genero = StringField("genero")
    
    #-----------------div 4----------------
    direccion=StringField("Direccion")
    regimen = StringField("regimen")
    telefono=StringField("Telefono")
    
    #-----------------de sesion----------------------------
    #-----------------div 5----------------
    usuario = StringField("Usuario")
    contrasena=PasswordField("contraseña")

    #-----------------boton----------------------------
    

class  form_ver_hc_paciente(FlaskForm):
    
    id_paciente = StringField("ID Paciente")
    buscar=SubmitField("Buscar")
    imprimir = SubmitField("Imprimir reporte")

class  form_crear_citas_paciente(FlaskForm):
    #-----------------busqueda----------------------------
    
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

    #-----------------boton----------------------------
    crear = SubmitField("Creae")
    cancelar = SubmitField("Cancelar")

class  form_ver_citas_paciente(Form):
    buscar=SubmitField("Buscar  Citas", validators=[validators.DataRequired(message='No dejar vacío, completar')])

class  form_evaluaciones_paciente(FlaskForm):
    evaluar=SubmitField("Guardar evaluacion")

#-----------------MEDICO------------------------------------------------------------------------------------
#-----------------MEDICO------------------------------------------------------------------------------------
#-----------------MEDICO------------------------------------------------------------------------------------

class  inicio_medico(FlaskForm):
    Imagen = StringField("imagen")

class  form_configuraciones_medico(Form):
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

    #-----------------de contacto----------------------------
    #-----------------div 3----------------
    especialidad=StringField("Especialidad")
    correo = EmailField("correo")
    #genero = StringField("genero")
    
    #-----------------div 4----------------
    direccion=StringField("Direccion")
    disponibilidad = StringField("Disponibilidad")
    telefono=StringField("Telefono")
    
    #-----------------de sesion----------------------------
    #-----------------div 5----------------
    usuario = StringField("Usuario")
    contrasena=StringField("contraseña")

    #-----------------boton----------------------------
    
class  form_ver_hc_medico(Form):
    prueba = StringField("ID Paciente")
    buscar=SubmitField("Buscar")


class  form_citas_medico(FlaskForm):

    citas=DateField("citas del dia")
    #-----------------boton----------------------------
    buscar = SubmitField("Buscar citas")
    ejecutada = SubmitField("Marcar como ejecutada")
    cancelada = SubmitField("Marcar como cancelada")


#-----------------SUPER------------------------------------------------------------------------------------
#-----------------SUPER------------------------------------------------------------------------------------
#-----------------SUPER------------------------------------------------------------------------------------    

class  inicio_super(FlaskForm):
    Nota = StringField("nota")

class  administrar_citas_superad(Form):
    #-----------------busqueda----------------------------
    id= StringField("ID requerido")
    buscar=SubmitField("Buscar")
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

    #-----------------boton----------------------------
    eliminar = SubmitField("Eliminar cita  medica")
    editar = SubmitField("Editar cita medica")
    confirmar = SubmitField("confirmar edicion")

class  administrar_evaluaciones_super(FlaskForm):
    id_medico = StringField("ID Medico")
    buscar = SubmitField("buscar evaluaciones")
    imprimir = SubmitField("imprimir  reporte")

class  administrar_historias_super(Form):
    #-----------------busqueda----------------------------
    id_paciente = StringField("ID Paciente")
    buscar=SubmitField("Buscar")

    #-----------------boton----------------------------
    eliminar = SubmitField("Eliminar  historia  medica")
    imprimir = SubmitField("imprimir historia medica")

class  administrar_medico_superad(Form):
     #-----------------busqueda----------------------------
    id_medico = StringField("ID Paciente")
    buscar=SubmitField("Buscar")
    
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    #tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

    #-----------------de contacto----------------------------
    #-----------------div 3----------------
    correo = EmailField("correo")
    especialidad=StringField("Especialidad")
    genero = StringField("genero")
    
    #-----------------div 4----------------
    direccion=StringField("Direccion")
    disponibilidad = StringField("Disponibilidad")
    telefono=StringField("Telefono")
    #-----------------de sesion----------------------------
    #-----------------div 5----------------
    usuario = StringField("Usuario")
    contrasena=StringField("contraseña")
    #-----------------boton----------------------------
    editar = SubmitField("Editar medico")
    eliminar = SubmitField("Eliminar  medico")

class  administrar_paciente_superad(Form):
    #-----------------busqueda----------------------------
    id_paciente = StringField("ID Paciente")
    buscar=SubmitField("Buscar")
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    #tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

    #-----------------de contacto----------------------------
    #-----------------div 3----------------
    correo = EmailField("correo")
    eps=StringField("EPS")
    genero = StringField("genero")
    
    #-----------------div 4----------------
    direccion=StringField("Direccion")
    regimen = StringField("regimen")
    telefono=StringField("Telefono")
    
    #-----------------de sesion----------------------------
    #-----------------div 5----------------
    usuario = StringField("Usuario")#, validators=[validators.DataRequired(message='No dejar vacío, completar')])
    contrasena=StringField("contraseña")#, validators=[validators.DataRequired(message="Ingrese  contraseña")])

    #-----------------boton----------------------------
    editar = SubmitField("Editar paciente")
    eliminar = SubmitField("Eliminar  paciente")

class crear_cita_superad(Form):
    
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    #tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

class crear_cita_superad_busqueda(Form):
    #-----------------busqueda----------------------------
    id_paciente = StringField("ID Paciente")
    buscar=SubmitField("Buscar")
    pri_nombre=StringField("Primer nombre")
    secu_nombre=StringField("Segundo nombre")
    pri_apellido=StringField("Primer apellido")
    secu_apellido=StringField("Segundo apellido")
    tdocumento=StringField("Tipo de documento")
    ndocumento=StringField("Numero (#) de documento")
    #especialidad=StringField("especialidad")
    registrar=SubmitField("registrar")
    cancelar=SubmitField("cancelar")

class prueba(Form):#no  se  utiliza
    #-----------------busqueda--------------------------- 
    fecha=StringField("fecha")
    especialidad=StringField("especialidad")
   
   

class crear_cita_superad_cuerpo(Form):
    #-----------------busqueda----------------------------
    
    registrar=SubmitField("registrar")
    cancelar=SubmitField("cancelar")

class crear_medico_superad(Form):
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    secu_nombre=StringField("Segundo Nombre",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    pri_apellido = StringField("Primer apellido",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido",)
    #tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento",validators=[validators.DataRequired(message='No dejar vacío, completar')])

    #-----------------de contacto----------------------------
    #-----------------div 3----------------
    correo = EmailField("correo",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    especialidad=StringField("Especialidad",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    #genero = StringField("genero")
    
    #-----------------div 4----------------
    direccion=StringField("Direccion",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    disponibilidad = StringField("Disponibilidad",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    telefono=StringField("Telefono",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    #-----------------de sesion----------------------------
    #-----------------div 5----------------
    usuario = StringField("Usuario", validators=[validators.DataRequired(message='No dejar vacío, completar')])
    contrasena=PasswordField("contraseña", validators=[validators.DataRequired(message="Ingrese  contraseña")])
    #-----------------boton----------------------------
    registrar = SubmitField("Registrar medico")
    cancelar = SubmitField("cancelar  operacion")

class crear_paciente_superad(Form):
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    #tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento",validators=[validators.DataRequired(message='No dejar vacío, completar')])

    #-----------------de contacto----------------------------
    #-----------------div 3----------------
    correo = EmailField("correo",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    #eps=StringField("EPS")
    #genero = StringField("genero")
    
    #-----------------div 4----------------
    direccion=StringField("Direccion",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    regimen = StringField("regimen",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    telefono=StringField("Telefono",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    
    #-----------------de sesion----------------------------
    #-----------------div 5----------------
    usuario = StringField("Usuario",validators=[validators.DataRequired(message='No dejar vacío, completar')])
    contrasena=PasswordField("contraseña",validators=[validators.DataRequired(message='No dejar vacío, completar')])

    #-----------------boton----------------------------
    registrar = SubmitField("Registrar paciente")
    cancelar = SubmitField("cancelar operacion")

class ver_cita_superad(Form):
    #-----------------busqueda----------------------------
    id= StringField("ID requerido")
    buscar=SubmitField("Buscar")
    #-----------------basicos----------------------------inmodificables
    #-----------------div 1----------------
    pri_nombre = StringField("Primer Nombre")
    secu_nombre=StringField("Segundo Nombre")
    pri_apellido = StringField("Primer apellido")
    
    #-----------------div 2----------------
    secu_apellido=StringField("Segundo apellido")
    #tipo_docum=StringField("tipo de documento")
    num_docum=StringField("numero de documento")

