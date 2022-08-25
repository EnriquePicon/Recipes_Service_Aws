
from flask_app.config.mysqlconnection import connectToMySQL

import re 
EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# importamos  expresiones regulares
#verificar emial con el formato requerido (caracteres)

from flask import flash

class User:

    def __init__(self, data):
        
        self.id = data['id']
        self.first_name = data['first_name']
        self.las_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(csl, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('recetas_recipes').query_db(query, formulario)
        return result # result es un resultado  de ID, una consulta SELET DEVUELVE SIEMPRE ID

#---------------------------------------------------------
#validacion de formulario

    @staticmethod
    def valida_usuario(formulario):

        es_valido = True
        if len(formulario['first_name']) < 3:
            flash("Nombre debe tener al menos 3 caracteres", 'registro')
            print("nombre")
            es_valido = False

        if len(formulario['last_name']) < 3:
            flash("Apellido debe tener al menos 3 caracteres", 'registro')
            print("apellido")
            es_valido = False

        if not EMAIL_REGEX.match(formulario['email']):
            flash('Emial invalido', 'registro')
            es_valido = False

        if len(formulario['password']) < 6:
            flash('Contrasena debe tener  al menos 6 caracteres.', 'registro')
            es_valido = False

        if formulario['password'] != formulario['confirm_password']:
            flash('Contrasena Incorrecta', 'registro')
            es_valido = False

            #Consultar  SI YA EXISTE  el correo en base o plataforma

        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recetas_recipes').query_db(query, formulario)
        if len(result) >= 1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False

        return es_valido
#---------------------------------------------------------------------------------

    @classmethod
    def  get_by_email(cls, formulario):

        query = "SELECT * FROM users WHERE  email = %(email)s"
        result = connectToMySQL('recetas_recipes').query_db(query, formulario)

        if len(result) < 1:
            return False
            
        else:
            # result  [{firsr_name, last_name, emial}]
            user = cls(result[0]) # haciendo una instancia de User  con los datos que recibimos dela base de datos dela consulta  result 
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users  WHERE id  = %(id)s"
        result = connectToMySQL('recetas_recipes').query_db(query,formulario )
        user = cls(result[0])
        return user