from credentials import *

def response(what, Object):
    
    if what == 'hamburguer':
        response = {}
        response['id'] = Object.hamburguer_id
        response['nombre'] = Object.name
        response['precio'] = Object.price
        response['descripcion'] = Object.description 
        response['imagen'] = Object.picture
        ingredients = [ing.ingredient_id for ing in Object.ing]
        response['ingredientes'] = [{'path' : pageName + '/ingrediente/' + str(ID)} for ID in ingredients]
        return response
    
    elif what == 'hamburguers':

        finalResponse = []
        for hamburguer in Object:
            response = {}
            response['id'] = hamburguer.hamburguer_id
            response['nombre'] = hamburguer.name
            response['precio'] = hamburguer.price
            response['descripcion'] = hamburguer.description 
            response['imagen'] = hamburguer.picture
            ingredients = [ing.ingredient_id for ing in hamburguer.ing]
            response['ingredientes'] = [{'path' : pageName + '/ingrediente/' + str(ID)} for ID in ingredients]
            finalResponse.append(response)
        return finalResponse

    elif what == 'ingredient':
        response = {}
        response['id'] = Object.ingredient_id
        response['nombre'] = Object.name
        response['descripcion'] = Object.description 
        return response

    elif what == 'ingredients':
        response = []
        for ingrediente in Object:
            respon = {}
            respon['id'] = Object.ingredient_id
            respon['nombre'] = Object.name
            respon['descripcion'] = Object.description 
            response.append(respon)
        return response



def verifyRequest(what, request):

    if what == 'updateHamburguer':
        if 'precio' in request.json.keys():
            if not (str(request.json['precio']).isnumeric()):
                return False
        
        return True
    


