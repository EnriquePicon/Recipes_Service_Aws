from email import message
from flask import render_template, request, redirect, flash, session, jsonify
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

from flask_app import app
#importar models ....

#importar BCrypt
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/')
def index():

        return render_template('index.html')

#---------------------------------------------------------------------------------

    # pendiente crear una ruta para /register
@app.route('/register', methods=['POST'])
def register():

    if not User.valida_usuario(request.form):
        print("No validado")
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) # me ecripta la contrasena

    formulario = {

        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }


    id = User.save(formulario) # guardo el usuario y  recibo el ID  DE NUEVO  REGISTRO

    session ['user_id'] = id # Guardando  en session el identificador
    return redirect('/dashboard')

#------------------------------------------------------------------------------------------
#crear una ruta para /login

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        # flash('E-mail no corresponde', 'login')
        # return redirect('/')
        return jsonify(message="E-mail no encontrado")

    session ['user_id'] = user.id

        # COMPARACION DE CONTRASENAS
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # flash("Password Incorrecto", 'login')
        # return  redirect('/') 
        return jsonify(message="Password Incorrecto")

    # return redirect('/dashboard')
    return jsonify(message="correcto")

#-------------------------------------------------------------------------
# ruta de dashboard 

@app.route('/dashboard')
def dashhboard():
    if 'user_id' not in session :
        return redirect('/')

    formulario = {
    "id": session['user_id']

}
    user = User.get_by_id(formulario)

    recipe = Recipe.get_all() # recibimos lista de recetas 
    return render_template('/dashboard.html', user = user, recipe=recipe)


    #------------------------------------
    # crear ruta logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')