import os
import re
import flask
import yagmail as yagmail
from flask import Flask, render_template, flash, request, redirect, session, url_for,  send_file, current_app, g, make_response
import utils
from formularios import*
from db import get_db, close_db
from  sqlite3  import Error
from flask_wtf import form
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.urandom(24)

#--------------------------------------------------------------------------------------------
#-----------------------------BASICOS--------------------------------------------------------
#--------------------------------------------------------------------------------------------
@app.route('/')
def login():
    return render_template("Principal/login.html")

@app.route('/formulario_registro', methods=['GET','POST'])
def formulario_registro():
    form=formregistro()
    return render_template("Principal/formulario_registro.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def log():
    form = formregistro( request.form )
    if request.method == 'POST':
        pri_nombre = request.form['pri_nombre']
        secu_nombre= request.form['secu_nombre']
        pri_apellido = request.form['pri_apellido']
        secu_apellido= request.form['secu_apellido']
        tipo_doc= request.form['tipo_doc']
        ndocumento= request.form['ndocumento']
        genero= request.form['genero']
        correo = request.form['correo']
        direccion= request.form['direccion']
        celular = request.form['celular']
        telefono= request.form['telefono']
        regimen= request.form['regimen']
        eps= request.form['eps']
        usuario = request.form['usuario']
        contrasena= request.form['contrasena']
        db = get_db()
        db.execute('INSERT INTO paciente (primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,tipo_documento,numero_documento,genero,correo,direccion,celular,telefono,regimen,eps,usuario,contrasena)   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (pri_nombre,secu_nombre,pri_apellido,secu_apellido,tipo_doc,ndocumento,genero,correo,direccion,celular,telefono,regimen,eps,usuario,generate_password_hash(contrasena) ))
        db.commit()
        #sql_insert_paciente(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tipo_doc,ndocumento,genero,correo,direccion,celular,telefono,regimen,eps,usuario,contrasena)
        #return "OK"
        flash('su   registro fue  exitoso, ya  puede ingresar')
        return render_template("Principal/login.html", form=form)
    # GET:
    
#--------------------------------------------------------------------------------------------
#----------------------------------LOGIN-----------------------------------------------------
#--------------------------------------------------------------------------------------------
@app.route('/inicio', methods=['GET','POST'])
def inicio():
    try:
        if request.method == 'POST':
            opcion=request.form['rol']
            username=request.form['usuario']
            password=request.form['password']
            
            if not username:
               error = 'Debes ingresar el usuario'
               flash( error )
               return render_template( 'login.html' )
            
            if not password:
                error = 'Contraseña requerida'
                flash( error )
        
            db = get_db()
            
            if (opcion=="paciente"):
                form=inicio_paciente()
                user = db.execute(
                        'SELECT * FROM paciente WHERE usuario=? and contrasena=? ', (username,password)
                        ).fetchone()
                store_password = user[14]
                result = check_password_hash(store_password, password)

                if result is None:
                    error = 'Usuario o contraseña inválidos'
                    flash( error )
                else:
                    session.clear()
                    session['rol']=opcion
                    session['pnombre'] = user[0]
                    session['user_id'] = user[5]
                    return render_template('Paciente/inicio.html', form=form)

            elif (opcion=="medico"):
                form=inicio_medico()
                user = db.execute(
                        'SELECT * FROM medico WHERE usuario=? and contrasena=? ', (username,password)
                        ).fetchone()
                store_password = user[13]
                result = check_password_hash(store_password, password)
                if result is None:
                    error = 'Usuario o contraseña inválidos'
                    flash( error )
                else:
                    session.clear()
                    session['user_id'] = user[5]
                    session['rol']=opcion
                    session['pnombre'] = user[0]
                    
                    return render_template('Medico/inicio.html',titulo='inicio', form=form)

            elif (opcion=="superAdministrador") :
                form=inicio_super()
                user = db.execute(
                        'SELECT * FROM super WHERE usuario=? and contrasena=? ', (username,password)
                        ).fetchone()
                store_password = user[10]
                result = check_password_hash(store_password, password)
                if result is None:
                    error = 'Usuario o contraseña inválidos'
                    flash( error )
                else:
                    session.clear()
                    session['user_id'] = user[5]
                    session['rol']=opcion
                    session['pnombre'] = user[0]
                    session['id'] = user[5]
                    return render_template('SuperAdministrador/inicio.html',titulo='inicio', form=form)
            
            else:
                return render_template("Principal/login.html")
                #return  "datos  invalidos"
        
        print("Llego al final")
        return render_template("Principal/login.html")
    except:
        #return  "aqui  estas"
        flash('credenciales incorectas, verifique  e intentelo  nuevamente')
        return  render_template("Principal/login.html")
        
#--------------------------------------------------------------------------------------------
#---------------------------------------paciente---------------------------------------------
#--------------------------------------------------------------------------------------------

@app.route('/principal_paciente')
def principal_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=inicio_paciente()
        return render_template('Paciente/inicio.html',titulo='inicio', form=form)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/configuraciones_paciente', methods=['GET','POST'])#3
def inicio_configuraciones_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_configuraciones_paciente(request.form)
        id = session['user_id']#de   la  sesion
        print("estas    aqui")
        print(id)
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id)
            ).fetchone()
        print (usuarios)
        return render_template('Paciente/configuraciones.html', form=form,  usuarios=usuarios)   
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/editar_configuraciones_paciente', methods=['GET','POST'])#3.1
def editar_configuraciones_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_configuraciones_paciente(request.form)
        #print ("ok")
        num_docum = session['user_id']
        db = get_db()
        usuarios = db.execute(
        'SELECT * FROM paciente WHERE numero_documento="{}" '.format(num_docum)
        ).fetchone()
        if  request.method=='POST':
            pri_nombre = request.form['pri_nombre']
            secu_nombre = request.form['secu_nombre']
            tdocumento = request.form['tdocumento']
            pri_apellido = request.form['pri_apellido']
            secu_apellido = request.form['secu_apellido']
            
            genero = request.form['genero']
            eps = request.form['eps']
            correo = request.form['correo']
            celular = request.form['telefono']
            direccion = request.form['direccion']
            regimen = request.form['regimen']
            usuario = request.form['usuario']
            contrasena = request.form['oculto']
            print(pri_nombre)
            db = get_db()
            db.execute(
                "UPDATE paciente SET primer_nombre= '{}',segundo_nombre= '{}',primer_apellido= '{}',segundo_apellido= '{}',tipo_documento= '{}',genero= '{}',correo= '{}',direccion= '{}',celular= '{}',regimen= '{}',eps= '{}',usuario= '{}',contrasena= '{}'  WHERE numero_documento= '{}' ".
                format(pri_nombre, secu_nombre, pri_apellido,secu_apellido,tdocumento,genero,correo,direccion,celular, regimen,eps,usuario,contrasena,num_docum)
                )

            
            #return render_template('/principal_paciente.html')
            flash("se realizo exitosamente su  actualizacion")
    
            return render_template('Paciente/configuraciones.html', form=form,  usuarios=usuarios)   
        return render_template('Paciente/configuraciones.html', form=form,  usuarios=usuarios)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/ver_HC_paciente')
def ver_hc_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_ver_hc_paciente()
        id = session['user_id']
        print(id)
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM citas WHERE id_paciente="{}" '.format(id)
            ).fetchall()
        print (usuarios)

        return render_template('Paciente/Ver_HC.html',form=form, usuarios=usuarios)
    
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/crear_cita_paciente',methods=['GET','POST'])#4
def crear_cita_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_crear_citas_paciente(request.form)
        db = get_db()
        especialidades = db.execute(
                'SELECT especialidad FROM especialidades' 
                ).fetchall()
        db.commit()
        close_db()
        if  request.method=='POST':
            id = session['user_id']#de   la  sesion
            especialidad=request.form['especialidad']
            print("estas    aqui")
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id)
                ).fetchone()
            medicos = db.execute(
                "SELECT primer_nombre,  primer_apellido,    numero_documento,  disponibilidad  FROM medico  WHERE   especialidad='{}'".format(especialidad) 
                ).fetchall()
            db.commit()
            close_db()
            print (usuarios)
            print(medicos)
            return render_template('Paciente/Crear_Citas.html', form=form,  usuarios=usuarios, medicos=medicos, especialidades=especialidades) 
        
        else:
            return render_template('Paciente/Crear_Citas.html', form=form,  usuarios=None, medicos=[None], especialidades=especialidades)  
        
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/efectuar_cita_paciente', methods=['GET','POST'])#4.1
def efectuar_cita_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_crear_citas_paciente(request.form)
        id = session['user_id']
        db = get_db()
        usuariosg = db.execute(
                'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id)
                ).fetchone()
        db.commit()
        close_db()
        if  request.method=='POST':        
            id_medico=request.form.get("medico", False)
            
            hora=request.form['hora']   
            fecha1=request.form['fecha']
            fecha=str(fecha1)    
            disponibilidad=request.form['disponibilidad']
            #especialidad="especialidad  de  prueba"
            dispoint=int(disponibilidad)
            comentarios=''
            db = get_db()
            usuarios = db.execute(
                "SELECT	count(*)	FROM	citas	WHERE	fecha='{}' AND  id_medico='{}'".format(fecha,id_medico)
                ).fetchone()
            db.commit()

            especialidad = db.execute(
                "SELECT especialidad FROM medico   WHERE	numero_documento='{}'".format(id_medico)
                ).fetchone()
            db.commit()

            fechascom = db.execute(
                "SELECT	count(*)	FROM	citas	WHERE	fecha='{}' AND  hora='{}'".format(fecha,hora)
                ).fetchone()
            db.commit()
            close_db()
            print(fechascom,'---')
            print(especialidad[0])
            if  (((usuarios[0]>=0)  and   (usuarios[0]<dispoint)) and  fechascom[0]==1):
                db = get_db()
                db.execute('INSERT INTO citas (id_paciente,id_medico,especialidad,fecha,hora,comentarios)   VALUES (?,?,?,?,?,?)', (id,id_medico,especialidad[0],fecha,hora,comentarios))
                db.commit()
                close_db()    
                print("------------------ok--------------------------------")
                flash("se realizo cita  exitosamente")
                return render_template('Paciente/inicio.html')
            else:
                flash("se copo la disponibilidad o tiene cita  asignada,  por  favor  verifique")
                return render_template('Paciente/inicio.html')
            
        #return "ok"#render_template('Paciente/Crear_Citas.html', form=form,  usuarios=usuarios)
        return render_template('Paciente/Crear_Citas.html', form=form,  usuarios=usuariosg)     
        
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/ver_cita_paciente', methods=['GET','POST'])
def ver_cita_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_ver_citas_paciente(request.form)
        if  request.method=='POST':
            id = session['user_id']
            fecha=request.form['fecha']
            print(id)
            print(fecha)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_paciente="{}" and fecha="{}"'.format(id,fecha)
                ).fetchall()
            print (usuarios)
            return render_template('Paciente/Ver_Citas.html',form=form, usuarios=usuarios)
        return render_template('Paciente/Ver_Citas.html',form=form)
            
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/evaluaciones_paciente',methods=['GET','POST'])
def evaluaciones_paciente():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_evaluaciones_paciente()
        db = get_db()
        especialidades = db.execute(
                'SELECT especialidad FROM especialidades' 
                ).fetchall()
        db.commit()
        close_db()
        if  request.method=='POST':
            especialidad=request.form["especialidad"]
            print("llego")
            db = get_db()
            medicos = db.execute(
                "SELECT primer_nombre,  primer_apellido, numero_documento, especialidad  FROM medico   WHERE	especialidad='{}'".format(especialidad)
                ).fetchall()
            db.commit()
            close_db()
            return render_template('Paciente/Evaluaciones.html',  especialidades=especialidades,  medicos=medicos)
        return render_template('Paciente/Evaluaciones.html',  especialidades=especialidades)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/evaluaciones_paciente_efectuar',methods=['GET','POST'])
def evaluaciones_paciente_efectuar():
    if  'user_id' in session  and  session['rol']=="paciente":
        form=form_evaluaciones_paciente()
        
        if  request.method=='POST':
            medico=request.form.get("medico",False)
            db = get_db()
            especialidad = db.execute(
                "SELECT  especialidad  FROM medico   WHERE	numero_documento='{}'".format(medico)
                ).fetchone()
            db.commit()
           
            id = session['user_id']
            comentario=request.form["comentario"]
            #medico=request.form["medico"]
            #especialidad=request.form["especialidad"]
            id_evaluacion="5"
            
            db.execute('INSERT INTO evaluaciones (id_evaluacion,id_paciente,especialidad,id_medico,comentario)   VALUES (?,?,?,?,?)', (id_evaluacion,id,especialidad[0],medico,comentario))
            db.commit()
            close_db()
            flash("evaluacion  exitosa")
            return render_template('Paciente/Evaluaciones.html')
        
    else:
        session.clear()
        return  redirect(url_for('login'))


#--------------------------------------------------------------------------------------------
#---------------------------------------MEDICO---------------------------------------------
#--------------------------------------------------------------------------------------------

@app.route('/principal_medico')
def principal_medico():
    if  'user_id' in session  and  session['rol']=="medico":
        form=inicio_medico()
        return  render_template('Medico/inicio.html') 
    else:
        session.clear()
        return redirect(url_for('login'))

@app.route('/configuraciones_medico', methods=['GET','POST'])#5
def inicio_configuraciones_medico():
    if  'user_id' in session  and  session['rol']=="medico":
        form=form_configuraciones_medico(request.form)
        id = session['user_id']#de   la  sesion
        print("estas    aqui")
        print(id)
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM medico WHERE numero_documento="{}" '.format(id)
            ).fetchone()
        #print (usuarios)
        
        return render_template('Medico/configuraciones_medi.html', form=form,  usuarios=usuarios)      
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/editar_configuraciones_medico', methods=['GET','POST'])#5.1
def editar_configuraciones_medico():
    if  'user_id' in session  and  session['rol']=="medico":
        form=form_configuraciones_medico(request.form)
        num_docum = session['user_id']
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM medico WHERE numero_documento="{}" '.format(num_docum)
            ).fetchone()
        close_db()
        if  request.method=='POST':
                        
            genero = request.form['genero']
            especialidad = request.form['especialidad']
            correo = request.form['correo']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            disponibilidad = request.form['disponibilidad']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            print(genero)
            db = get_db()
            db.execute(
                "UPDATE medico SET genero= '{}',especialidad= '{}',correo= '{}',telefono= '{}',direccion= '{}',disponibilidad= '{}',usuario= '{}',contrasena= '{}'  WHERE numero_documento= '{}' ".
                format(genero,especialidad,correo,telefono,direccion,disponibilidad,usuario,contrasena,num_docum)
                )
            db.commit()
            close_db()
            flash("actializacion   exitosa")
            return render_template('Medico/inicio.html')   
        return render_template('Medico/configuraciones.html', form=form,  usuarios=usuarios)
    else:
        session.clear()
        return redirect(url_for('login'))

@app.route('/ver_hc_medico', methods=['GET','POST'])
def ver_hc_medico():
    if  'user_id' in session  and  session['rol']=="medico":
        form=form_ver_hc_medico(request.form)
        if request.method == 'POST':
            id = request.form["id_paciente"]
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_paciente="{}" '.format(id)
                ).fetchall()
            db.commit()
            print (usuarios)
            
            return render_template('Medico/Ver_HC_medi.html', usuarios=usuarios)
        else:
            return render_template('Medico/Ver_HC_medi.html', form=form,usuarios=[None])       
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/ver_cita_medico', methods=['GET','POST'])
def ver_cita_medico():
    if  'user_id' in session  and  session['rol']=="medico":
        form=form_citas_medico(request.form)
        if  request.method=='POST':
            id = session['user_id']
            fecha=request.form['fecha']
            print(fecha)
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_medico="{}" and fecha="{}"'.format(id,fecha)
                ).fetchall()
            print (usuarios)
            return render_template('Medico/Ver_Citas_medi.html',form=form, usuarios=usuarios)
        return render_template('Medico/Ver_Citas_medi.html',form=form)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/evaluaciones_medico')
def evaluaciones_medico():
    if  'user_id' in session  and  session['rol']=="medico":
        form=form_configuraciones_medico()
        id = session['user_id']
        print(id)
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM evaluaciones WHERE id_medico="{}" '.format(id)
            ).fetchall()
        print (usuarios)
        return render_template('Medico/Evaluaciones_medi.html',form=form, usuarios=usuarios)
        
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/gestion', methods=['GET','POST'])
def gestion():
    if  'user_id' in session  and  session['rol']=="medico":
        if  request.method=='POST':
            uno=request.form['paciente']
            dos=request.form['fecha']
            tres=request.form['hora']
            print(tres)
            
            return render_template('Medico/gestion.html', uno=uno,dos=dos,tres=tres)
        
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/reporte', methods=['GET','POST'])
def reporte():
    if  'user_id' in session  and  session['rol']=="medico":
        #if  request.method=='POST':
        uno=request.form['id']
        dos=request.form['fecha']
        tres=request.form['hora']
        comentario=request.form['reporte']
        print(comentario)
        
        db = get_db()
        db.execute(
            "UPDATE citas SET comentarios='{}' WHERE  hora='{}' AND fecha='{}'  AND id_paciente='{}'".format(comentario,tres,dos,uno)
            ).fetchone()
        db.commit()
        close_db()
        print("lohizo")
        flash('ha gestionado  esta cita exitosamente')
        return render_template('Medico/gestion.html', uno=uno,dos=dos,tres=tres)      
    else:
        session.clear()
        return  redirect(url_for('login'))

#--------------------------------------------------------------------------------------------
#---------------------------------------SuperAdministrador-----------------------------------
#--------------------------------------------------------------------------------------------

@app.route('/principal_super')
def principal_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=inicio_super()
        return render_template('SuperAdministrador/inicio.html',titulo='inicio', form=form)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/crear_paciente_super', methods=['GET','POST'])
def crear_paciente_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=crear_paciente_superad(request.form)
        if request.method == 'POST':
            pri_nombre =  request.form['pri_nombre']
            secu_nombre= request.form['secu_nombre']
            pri_apellido =  request.form['pri_apellido']
            secu_apellido= request.form['secu_apellido']
            tipo_doc= request.form['tipo_doc']
            num_docum= request.form['num_docum']
            correo =  request.form['correo']
            eps= request.form['eps']
            genero =  request.form['genero']
            direccion= request.form['direccion']
            regimen =  request.form['regimen']
            telefono= request.form['telefono']
            usuario =  request.form['usuario']
            contrasena= request.form['contrasena']
                
            sql_insert_paciente(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tipo_doc,num_docum,genero,correo,direccion,telefono,telefono,regimen,eps,usuario,contrasena)
            flash("registro exitoso")
        #return "OK"
        return render_template('SuperAdministrador/Crear_Paciente.html', form=form)
    else:
        session.clear()
        return  redirect(url_for('login'))
 
def sql_insert_paciente(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tdocumento,ndocumento,genero,correo,direccion,celular,telefono,regimen,eps,usuario,contrasena):
    try:
        sql = "INSERT INTO paciente (primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,tipo_documento,numero_documento,genero,correo,direccion,celular,telefono,regimen,eps,usuario,contrasena) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tdocumento,ndocumento,genero,correo,direccion,celular,telefono,regimen,eps,usuario,contrasena)       
        print(sql)
        conn = get_db()        
        cursorObj = conn.cursor()  
        cursorObj.execute(sql) #usar para evitar vulnerabilidad
        print("Aquí.")
        conn.commit() 
        conn.close()
    except Error:
        print(Error)

@app.route('/administrar_paciente_super', methods=['GET','POST'])#1
def administrar_paciente_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_paciente_superad(request.form)
        if request.method == 'POST':
            id_paciente = request.form['id_paciente']
            print(id_paciente)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id_paciente)
                ).fetchone()
            print (usuarios)
            return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=usuarios)
        else:
            return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=None)

    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/APS_actualizar', methods=['GET','POST'])#1.1
def actualizar_PS():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_paciente_superad(request.form)
        if request.method == 'POST':
                
            pri_nombre = request.form['pri_nombre']
            secu_nombre = request.form['secu_nombre']
            tdocumento = request.form['tdocumento']
            pri_apellido = request.form['pri_apellido']
            secu_apellido = request.form['secu_apellido']
            num_docum = request.form['num_docum']
            genero = request.form['genero']
            eps = request.form['eps']
            correo = request.form['correo']
            celular = request.form['telefono']
            direccion = request.form['direccion']
            regimen = request.form['regimen']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            print(pri_nombre)
            db = get_db()
            db.execute(
                "UPDATE paciente SET primer_nombre= '{}',segundo_nombre= '{}',primer_apellido= '{}',segundo_apellido= '{}',tipo_documento= '{}',genero= '{}',correo= '{}',direccion= '{}',celular= '{}',regimen= '{}',eps= '{}',usuario= '{}',contrasena= '{}'  WHERE numero_documento= '{}' ".
                format(pri_nombre, secu_nombre, pri_apellido,secu_apellido,tdocumento,genero,correo,direccion,celular, regimen,eps,usuario,contrasena,num_docum)
                )
            db.commit()
            close_db()
            print ("ok")
            flash("actualizacion exitosa")
            return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=None)
        else:
            return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=None)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/APS_eliminar', methods=['GET','POST'])#1.2
def APS_eliminar():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_paciente_superad(request.form)
    #if request.method == 'POST': 
        
        num_docum = request.form['oculto']
        
        print(num_docum)
        db = get_db()
        db.execute(
            "DELETE	FROM	paciente	WHERE	numero_documento='{}'".format(num_docum)
            )
        db.commit()
        close_db()
        print ("ok")
        flash('elimino paciente exitosamente')
        return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=None)
    #else:
        #return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=None)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/administrar_historias_medicas', methods=['GET','POST'])
def administrarHM_paciente_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_historias_super()
        if request.method == 'POST':
            id = request.form['id_paciente']
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_paciente="{}" '.format(id)
                ).fetchall()
            db.commit()
            close_db()
            print (usuarios)
            return render_template('SuperAdministrador/Administrar_Historias.html', form=form, usuarios=usuarios)
        else:
            return render_template('SuperAdministrador/Administrar_Historias.html', form=form,  usuarios=[None])
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/crear_medico_super', methods=['GET','POST'])
def crear_medico_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=crear_medico_superad(request.form)
        db = get_db()
        especialidades = db.execute(
                'SELECT especialidad FROM especialidades' 
                ).fetchall()
        db.commit()
        close_db()
        if request.method == 'POST':
            pri_nombre =  request.form['pri_nombre']
            secu_nombre= request.form['secu_nombre']
            pri_apellido =  request.form['pri_apellido']
            secu_apellido= request.form['secu_apellido']
            tipo_doc= request.form['tipo_doc']
            num_docum= request.form['num_docum']
            genero =  request.form['genero']
            especialidad= request.form['especialidad']
            correo =  request.form['correo']
            telefono= request.form['telefono']
            direccion= request.form['direccion']
            disponibilidad =  request.form['disponibilidad']
            usuario =  request.form['usuario']
            contrasena= request.form['contrasena']
            perfil= request.form['perfil']
                
            sql_insert_medico(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tipo_doc,num_docum,genero,especialidad,correo,telefono,direccion,disponibilidad,usuario,contrasena,perfil)
        #return "OK"
            flash('registro exitoso')
        return render_template('SuperAdministrador/Crear_Medico.html', form=form,   especialidades=especialidades    )
    else:
        session.clear()
        return  redirect(url_for('login'))

def sql_insert_medico(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tipo_doc,num_docum,genero,especialidad,correo,telefono,direccion,disponibilidad,usuario,contrasena,perfil):
    try:
        sql = "INSERT INTO medico (primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,tipo_documento,numero_documento,genero,especialidad,correo,telefono,direccion,disponibilidad,usuario,contrasena,perfil) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(pri_nombre,secu_nombre,pri_apellido,secu_apellido,tipo_doc,num_docum,genero,especialidad,correo,telefono,direccion,disponibilidad,usuario,contrasena,perfil)       
        print(sql)
        conn = get_db()        
        cursorObj = conn.cursor()  
        cursorObj.execute(sql) #usar para evitar vulnerabilidad
        print("Aquí.")
        conn.commit() 
        conn.close()
    except Error:
        print(Error)

@app.route('/administrar_medico', methods=['GET','POST'])#2
def administrar_medico_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_medico_superad(request.form)
        if request.method == 'POST':
            id_medico = request.form['id_medico']
            print(id_medico)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM medico WHERE numero_documento="{}" '.format(id_medico)
                ).fetchone()
            db.commit()
            print (usuarios)
            return render_template('SuperAdministrador/Administrar_Medico.html', form=form,    usuarios=usuarios)
        else:
            return render_template('SuperAdministrador/Administrar_Medico.html', form=form,    usuarios=None)
    else:
        session.clear()
        return  redirect(url_for('login'))
    
@app.route('/AMS_actualizar', methods=['GET','POST'])#2.1
def AMS_actualizar():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_medico_superad(request.form)
        if request.method == 'POST':   
            pri_nombre = request.form['pri_nombre']
            secu_nombre = request.form['secu_nombre']
            tdocumento = request.form['tdocumento']
            pri_apellido = request.form['pri_apellido']
            secu_apellido = request.form['secu_apellido']
            num_docum = request.form['num_docum']
            genero = request.form['genero']
            eps = request.form['eps']
            correo = request.form['correo']
            celular = request.form['telefono']
            direccion = request.form['direccion']
            regimen = request.form['regimen']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            print(pri_nombre)
            db = get_db()
            db.execute(
                "UPDATE paciente SET primer_nombre= '{}',segundo_nombre= '{}',primer_apellido= '{}',segundo_apellido= '{}',tipo_documento= '{}',genero= '{}',correo= '{}',direccion= '{}',celular= '{}',regimen= '{}',eps= '{}',usuario= '{}',contrasena= '{}'  WHERE numero_documento= '{}' ".
                format(pri_nombre, secu_nombre, pri_apellido,secu_apellido,tdocumento,genero,correo,direccion,celular, regimen,eps,usuario,contrasena,num_docum)
                )
            db.commit()
            close_db()
            print ("ok")
            flash('actualizacion exitosa')
            return render_template('SuperAdministrador/Administrar_Medico.html', form=form,    usuarios=None)
        else:
            return render_template('SuperAdministrador/Administrar_Medico.html', form=form,    usuarios=None)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/AMS_eliminar', methods=['GET','POST'])#2.2
def AMS_eliminar():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_medico_superad(request.form)
    #if request.method == 'POST': 
        
        num_docum = request.form['oculto']
        
        print(num_docum)
        db = get_db()
        db.execute(
            "DELETE	FROM    medico	WHERE	numero_documento='{}'".format(num_docum)
            )
        db.commit()
        print ("ok")
        flash('elimino  registro  satisfactoriamente')
        return render_template('SuperAdministrador/Administrar_Medico.html', form=form,    usuarios=None)
    #else:
        #return render_template('SuperAdministrador/Administrar_Paciente.html', form=form,    usuarios=None)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/crear_citas_super', methods=['GET','POST'])#3
def crear_citas_supera():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=crear_cita_superad_busqueda(request.form)
        db = get_db()
        especialidades = db.execute(
                'SELECT especialidad FROM especialidades' 
                ).fetchall()
        db.commit()
        close_db()

        if request.method == 'POST':
            id_paciente = request.form['id_paciente']
            especialidades=request.form['especialidad']
            print(especialidades)
            print(id_paciente)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id_paciente)
                ).fetchone()
            medicos = db.execute(
                "SELECT primer_nombre,  primer_apellido, numero_documento, especialidad,  disponibilidad  FROM medico   WHERE	especialidad='{}'".format(especialidades)
                ).fetchall()
            db.commit()
            close_db()
            print (usuarios)
            print(medicos)
            print('--------------------------------------')
            return render_template('SuperAdministrador/Crear_Citas.html', usuarios=usuarios,  form=form,  medicos=medicos)
        else:
            return render_template('SuperAdministrador/Crear_Citas.html', form=form,    usuarios=None,  medicos=[None],   especialidades=especialidades   )
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/asignar_cita', methods=['GET','POST'])#3.1
def asignar_cita():
    #form=prueba(request.form)
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=crear_cita_superad_busqueda(request.form)
        if  request.method=='POST':
            db = get_db()
            id_medico=request.form["medico"]
            especialidad = db.execute(
                "SELECT especialidad FROM medico   WHERE	numero_documento='{}'".format(id_medico)
                ).fetchone()
            db.commit()
            #fecha=request.form["fecha"]
            fecha1=request.form["fecha"]
            fecha=str(fecha1)
            id_medico=request.form["medico"]
            hora=request.form["hora"]
            
            print(especialidad[0])
            print("------------------------------------------")
            
            id_paciente=request.form['oculto']
            disponibilidad=request.form['disponibilidad']
            dispoint=int(disponibilidad)
            comentarios=''
            db = get_db()
            citasdis = db.execute(
                "SELECT	count(*)	FROM	citas	WHERE	fecha='{}' AND  id_medico='{}'".format(fecha,id_medico)
                ).fetchone()
            db.commit()

            fechascom = db.execute(
                "SELECT	count(*)	FROM	citas	WHERE	fecha='{}' AND  hora='{}'".format(fecha,hora)
                ).fetchone()
            db.commit()
            close_db()
            if  (((citasdis[0]>=0)  and   (citasdis[0]<dispoint)) and fechascom[0]==0):
                db = get_db()
                db.execute('INSERT INTO citas (id_paciente,id_medico,especialidad,fecha,hora,comentarios)   VALUES (?,?,?,?,?,?)', (id_paciente,id_medico,especialidad[0],fecha,hora,comentarios))
                db.commit()
                close_db()    
                print("------------------ok--------------------------------")
                flash('cita creada exitosamente')
                return render_template('SuperAdministrador/inicio.html')
            else:
                #return  "se copo   la   disponibilidad"
                flash('capacidad diaria del medico copada  o  usted ya tiene  cita, intente de  nuevo')
                return render_template('SuperAdministrador/inicio.html')
    else:
        session.clear()
        return  redirect(url_for('login'))
            
@app.route('/administrar_citas', methods=['GET','POST'])#6
def administrar_citas_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_citas_superad(request.form)
        if request.method == 'POST'   and   (request.form['opcionvista']=="paciente"):
            id = request.form['id']
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_paciente="{}" '.format(id)
                ).fetchall()
            otro = db.execute(
                'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id)
                ).fetchone()
            print (usuarios)
            print (otro)
            return render_template('SuperAdministrador/Administrar_cita.html',form=form, usuarios=usuarios, otro=otro)
            
        elif request.method == 'POST'   and   (request.form['opcionvista']=="medico"):
            id = request.form['id']
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_medico="{}" '.format(id)
                ).fetchall()
            otro = db.execute(
                'SELECT * FROM medico WHERE numero_documento="{}" '.format(id)
                ).fetchone()
            print (usuarios)
            print (otro)
            return render_template('SuperAdministrador/Administrar_cita.html',form=form, usuarios=usuarios, otro=otro)
        else:
            return render_template('SuperAdministrador/Administrar_cita.html', form=form,  usuarios=[None], otro=None)
    else:
        session.clear()
        return  redirect(url_for('login'))      

@app.route('/administrar_citas_eliminar', methods=['GET','POST'])#6.1
def administrar_citas_super_eliminar():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_citas_superad(request.form)
        medico = request.form['medico']
        paciente = request.form['paciente']
        especialidad = request.form['especialidad']
        fecha = request.form['fecha']
        hora = request.form['hora']
        db = get_db()
        db.execute(
            "DELETE	FROM    citas	WHERE	id_paciente='{}' AND   id_medico='{}'   AND especialidad='{}' AND  fecha='{}'   AND   hora='{}'".format(medico,paciente,especialidad,fecha,hora)
            )
        db.commit()
        close_db()
        print ("ok")
        flash('registro eliminado exitosamente')
        #  "se ha  logrado"
        return  render_template('inicio.html')

    else:
        session.clear()
        return  redirect(url_for('login'))


@app.route('/ver_citas_super', methods=['GET','POST'])
def ver_citas_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=ver_cita_superad()
        
        if request.method == 'POST'   and   (request.form['opcionvista']=="paciente"):
            id = request.form['id']
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_paciente="{}" '.format(id)
                ).fetchall()
            otro = db.execute(
                'SELECT * FROM paciente WHERE numero_documento="{}" '.format(id)
                ).fetchone()
            print (usuarios)
            print (otro)
            return render_template('SuperAdministrador/Ver_citas.html',form=form, usuarios=usuarios, otro=otro)
        elif request.method == 'POST'   and   (request.form['opcionvista']=="medico"):
            id = request.form['id']
            print(id)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM citas WHERE id_medico="{}" '.format(id)
                ).fetchall()
            otro = db.execute(
                'SELECT * FROM medico WHERE numero_documento="{}" '.format(id)
                ).fetchone()
            print (usuarios)
            print (otro)
            return render_template('SuperAdministrador/Ver_citas.html',form=form, usuarios=usuarios, otro=otro)
        else:
            return render_template('SuperAdministrador/Ver_citas.html', form=form,  usuarios=[None], otro=None)
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/evaluaciones_super', methods=['GET','POST'])
def evaluaciones_super():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_evaluaciones_super()
        if request.method == 'POST':
            id_medico = request.form['id_medico']
            print(id_medico)
            db = get_db()
            usuarios = db.execute(
                'SELECT * FROM evaluaciones WHERE id_medico="{}" '.format(id_medico)
                ).fetchall()
            print (usuarios)
            return render_template('SuperAdministrador/Administrar_Evaluaciones.html',form=form, usuarios=usuarios)
        else:
            return render_template('SuperAdministrador/Administrar_Evaluaciones.html', form=form,  usuarios=[None])
    else:
        session.clear()
        return  redirect(url_for('login'))

@app.route('/evaluaciones_super_eliminar', methods=['GET','POST'])#6.1
def evaluaciones_super_eliminar():
    if  'user_id' in session  and  session['rol']=="superAdministrador":
        form=administrar_evaluaciones_super()
        if request.method == 'POST':
            medico = request.form['medico']
            paciente = request.form['paciente']
            comentario = request.form['comentario']
            print(comentario)
            print(medico)
            print('---------------------------------')
            db = get_db()
            db.execute(
                "DELETE	FROM    evaluaciones	WHERE	id_paciente='{}' AND  id_medico='{}'  AND comentario='{}'".format(medico,paciente,comentario)
                )
            db.commit()
            close_db()
            print ("ok")
            flash('registro eliminado exitosamente')
            return render_template('SuperAdministrador/Administrar_Evaluaciones.html', form=form,  usuarios=[None])

    else:
        session.clear()
        return  redirect(url_for('login'))


@app.route( '/logout',methods=['POST'] )
def logout():
    session.clear()
    return redirect(url_for('login'))