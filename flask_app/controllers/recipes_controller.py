

from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.recipes import Recipe
from flask_app.models.users import User

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session :
        return redirect('/')

    formulario = {
        "id": session['user_id']
    }
    user = User.get_by_id(formulario)

    return render_template('new_recipe.html', user = user)


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session :  #solo puede ver la pagina si ya inicio sesion
        return redirect('/')
    
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    Recipe.save(request.form)
    return redirect('/dashboard')

    #---------------------------------------------------------------------------
    #Ruta '/edit/recipe/<int:id>

@app.route('/edit/recipe/<int:id>') #Recibo el identificador de la receta que quiero editar
def edit_recipe(id):
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario) #Usuario que inició sesión

    formulario_receta = { "id": id }
    #llamar a una función y debo de recibir la receta
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

    #-----------------------------------------------------
    #ruta update


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id']) #/edit/recipe/1

    Recipe.update(request.form)

    return redirect('/dashboard')