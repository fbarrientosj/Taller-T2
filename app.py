from credentials import *
from responses import *
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import json

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

#  <------------------------------------------ START RELATIONSHIP ------------------------------------------>


# Relacionship
matchs = db.Table('matchs',
    db.Column('hamburguer_id', db.Integer, db.ForeignKey('hamburguer.hamburguer_id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.ingredient_id'))
)
#  <------------------------------------------ END RELATIONSHIP ------------------------------------------>


#  <------------------------------------------ START CLASS ------------------------------------------>


# Hamburguer Class/Model
class Hamburguer(db.Model):
  hamburguer_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=False)
  description = db.Column(db.String(300))
  price = db.Column(db.Float)
  picture = db.Column(db.String(300))
  # Relationship
  ing = db.relationship('Ingredient', secondary=matchs, backref=db.backref('ham'), lazy = 'dynamic')

  def __init__(self, name, description, price, picture):
    self.name = name
    self.description = description
    self.price = price
    self.picture = picture

class Ingredient(db.Model):
  ingredient_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=False)
  description = db.Column(db.String(300))

  def __init__(self, name, description):
    self.name = name
    self.description = description

#  <------------------------------------------ END CLASS ------------------------------------------>

#  <------------------------------------------ START SCHEMA ------------------------------------------>

# Hamburguer Schema
class HamburguerSchema(ma.Schema):
  class Meta:
    fields = ('hamburguer_id', 'name', 'description', 'price', 'picture')

hamburguer_schema = HamburguerSchema()
hamburguers_schema = HamburguerSchema(many=True)

# Hamburguer Schema
class IngredientSchema(ma.Schema):
  class Meta:
    fields = ('ingredient_id', 'name', 'description')

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

#  <------------------------------------------ END SCHEMA ------------------------------------------>

#  <------------------------------------------ START METHODS HAMBURGUER ------------------------------------------>

# Create a Hamburguer
@app.route('/hamburguesa', methods=['POST'])
def add_hamburguer():
  try: 
    name = request.json['nombre']
    description = request.json['descripcion']
    price = request.json['precio']
    picture = request.json['imagen']
    #ingredients = request.json['ingredientes']
    
    new_hamburguer = Hamburguer(name, description, price, picture)

    db.session.add(new_hamburguer)
    db.session.commit()

    return Response(json.dumps(response('hamburguer', new_hamburguer)), status=201)

  except:
    return Response('Input invalido', status=400)

  """for ingredient in ingredients:
    URL = ingredient['path']
    idIngredient = URL.split('/')[-1]
    ingredient = Ingredient.query.get(idIngredient)
    ingredient.ham.append(new_hamburguer)

  db.session.add(new_hamburguer)
  db.session.commit()

  return response('hamburguer', new_hamburguer)"""
  

# Get All Hamburguers
@app.route('/hamburguesa', methods=['GET'])
def get_hamburguers():
  all_products = Hamburguer.query.all()
  #result = hamburguers_schema.dump(all_products)
  #return jsonify(result)
  respons = response('hamburguers', all_products)
  return jsonify(respons)

# Get Single hamburguer
@app.route('/hamburguesa/<id>', methods=['GET'])
def get_hamburguer(id):

  try:
    if str(id).isnumeric():
      hamburguer = Hamburguer.query.get(id)
      respons = response('hamburguer', hamburguer)
      return jsonify(respons)
    else:
      return Response('Id invalido', status=400)
  except:
    return Response('Hamburguesa inexistente', status=404)
  
  
# Update a hamburguer
@app.route('/hamburguesa/<id>', methods=['PATCH'])
def update_hamburguer(id):

  if not(verifyRequest('updateHamburguer', request)) or not str(id).isnumeric():
    return Response('Parametros invalidos', status=400)

  try:
    hamburguer = Hamburguer.query.get(id)
    if 'nombre' in request.json.keys():
        name = request.json['nombre']
        hamburguer.name = name
    
    if 'descripcion' in request.json.keys():
        description = request.json['descripcion']
        hamburguer.description = description

    if 'precio' in request.json.keys():
        price = request.json['precio']
        hamburguer.price = price

    if 'imagen' in request.json.keys():
        image = request.json['imagen']
        hamburguer.image = image

    db.session.commit()
    respons = response('hamburguer', hamburguer)
    return Response(json.dumps(respons), status=200)

  except:
    return Response('Hamburguesa inexistente', status=404)


# Delete Hamburguer
@app.route('/hamburguesa/<id>', methods=['DELETE'])
def delete_hamburguer(id):

  try:
    hamburguer = Hamburguer.query.get(id)
    db.session.delete(hamburguer)
    db.session.commit()

    return hamburguer_schema.jsonify(hamburguer)
  except:
    return Response('Hamburguesa inexistente', status=404)



#  <------------------------------------------ END HAMBURGUER METHODS ------------------------------------------>

# Create a Ingredient
@app.route('/ingrediente', methods=['POST'])
def add_Ingredient():

  try:
    name = request.json['nombre']
    description = request.json['descripcion']

    new_Ingredient = Ingredient(name, description)

    db.session.add(new_Ingredient)
    db.session.commit()
    respon = response('ingredient', new_Ingredient)

    return Response(json.dumps(respon), status=201)

  except:
    return Response('Input invalido', status=400)

# Get All Ingredients
@app.route('/ingrediente', methods=['GET'])
def get_ingredients():
  all_products = Ingredient.query.all()
  result = ingredients_schema.dump(all_products)
  return jsonify(result)

# Get Single ingredient
@app.route('/ingrediente/<id>', methods=['GET'])
def get_ingredient(id):

  if not(str(id).isnumeric()):
    return Response('id invalido', status=400)

  try:
    ingredient = Ingredient.query.get(id)
    if not ingredient:
      return Response('ingrediente inexistente', status=404)

    return ingredient_schema.jsonify(ingredient)
  except:
    return Response('ingrediente inexistente', status=404)

# Update a ingredient
@app.route('/ingrediente/<id>', methods=['PATCH'])
def update_ingredient(id):
  if not(str(id).isnumeric()):
    return Response('id invalido', status=400)

  ingredient = Ingredient.query.get(id)

  if not(ingredient):
    return Response('Ingrediente inexistente', status=404)

  if 'nombre' in request.json.keys():
      name = request.json['nombre']
      ingredient.name = name
  
  if 'descripcion' in request.json.keys():
      description = request.json['descripcion']
      ingredient.description = description

  db.session.commit()
  return ingredient_schema.jsonify(ingredient)

# Delete Ingredient
@app.route('/ingrediente/<id>', methods=['DELETE'])
def delete_ingredient(id):
  
  ingredient = Ingredient.query.get(id)
  if not(ingredient): 
    return Response('ingrediente inexistente', status=404)

  records = db.session.query(matchs).filter_by(ingredient_id=id).all()
  if records: 
    return Response('Ingrediente no se puede borrar, se encuentra presente en una hamburguesa', status=409)

  db.session.delete(ingredient)
  db.session.commit()

  return ingredient_schema.jsonify(ingredient)

#  <------------------------------------------ END INGREDIENT'S METHODS ------------------------------------------>


#  <------------------------------------------ START MIDDLE TABLE METHODS ------------------------------------------>

@app.route('/hamburguesa/<idHamburguer>/ingrediente/<idIngredient>', methods=['PUT'])
def add_ingredient_to_hamburguer(idHamburguer, idIngredient):
  hamburguer = Hamburguer.query.get(idHamburguer)
  ingredient = Ingredient.query.get(idIngredient)
  if not hamburguer:
    return Response('Id de hamburguesa inválido', status=400)
  
  if not ingredient:
    return Response('Ingrediente inexistente', status=404)

  ingredient.ham.append(hamburguer)
  db.session.commit()
  return Response(f'Ingrediente: {ingredient.name} se ha metido en hamburguesa: {hamburguer.name}', status=201)

@app.route('/hamburguesa/<idHamburguer>/ingrediente/<idIngredient>', methods=['DELETE'])
def delete_ingredient_to_hamburguer(idHamburguer, idIngredient):
  try:
    hamburguer = Hamburguer.query.get(idHamburguer)
    ingredient = Ingredient.query.get(idIngredient)
    if not hamburguer:
      return Response('Id de hamburguesa inválido', status=400)

    if not ingredient:
      return Response('Ingrediente inexistente', status=404)

    #db.session.query(matchs).filter(idIngredient == ingredient.idIngredient, idHamburguer == hamburguer.idHamburguer).delete()
    #db.session.commit()
    effected_rows = hamburguer.ing.remove(ingredient)
    db.session.commit()

    return Response(f'Ingrediente: {ingredient.name} se ha eliminado en hamburguesa: {hamburguer.name}', status=201)
    
    
  except:
    return Response(f'Id ingrediente inexistente en la hamburguesa', status=404)

@app.route('/middle', methods=['GET'])
def get_middle():
  records = db.session.query(matchs).filter_by(ingredient_id=23).all()
  
  for record in records:
    print(record)

  return 'all good'


#  <------------------------------------------ END MIDDLE TABLE METHODS ------------------------------------------>



if __name__ == '__main__':

    app.run(debug=True)
