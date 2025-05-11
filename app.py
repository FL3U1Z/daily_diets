from flask import Flask, request, jsonify
from models.diet import Diet
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
#__name__ =__main__
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.daily_diets
diets_collection = db.diets
diets = []
diet_id_control = 1

@app.route("/diets", methods=['POST'])
def create_diet():
    global diet_id_control
    data = request.get_json()
    current_time = (datetime.now())
    new_recipe = Diet(id=diet_id_control, name=data['name'], description=data.get("description",""), time=current_time.strftime("%Y-%m-%d %H:%M:%S"), diet=data.get("diet",False))
    # Insere no MongoDB
    new_recipe_id = diets_collection.insert_one({
        'id': diet_id_control,
        'name': new_recipe.name,
        'description': new_recipe.description,
        'time': new_recipe.time,
        'diet': new_recipe.diet
    }).inserted_id
    diet_id_control += 1
     
    return jsonify({
        "message": "Nova receita criada com sucesso",
        "id": str(new_recipe_id)
    })

@app.route("/diets", methods=['GET'])
def get_all_diets():
    
    diets_from_db = diets_collection.find()
    
    
    diets_list = []
    for diet in diets_from_db:
        diets_list.append({
            "id": diet['id'],
            "name": diet['name'],
            "description": diet.get('description', ''),  
            "time": diet['time'],  
            "diet": diet['diet']  
        })
    
    return jsonify(diets_list)


@app.route("/diets/<diet_id>", methods=['GET'])
def get_one_diet(diet_id):
    try:
        diet = diets_collection.find_one({"id": int(diet_id)})
        
        if not diet:
            return jsonify({"message": "Dieta não encontrada"}), 404
        
        diet_dict = {
            "id": diet['id'],
            "name": diet['name'],  
            "description": diet.get('description', ''),
            "time": diet['time'],  
            "diet": diet['diet'] 
        }
        
        return jsonify(diet_dict)
    except Exception as e:
        return jsonify({"error": "ID inválido", "details": str(e)}), 400


@app.route("/diets/<diet_id>", methods=['PUT'])
def update_diet(diet_id):
    data = request.get_json()
    diet = diets_collection.find_one({"id": int(diet_id)})
    print(data)
    if not diet:
        return jsonify({"message": "Dieta não encontrada"}), 404
    
    
    current_time = (datetime.now())
    update_recipe = Diet(id=diet_id, name=data['name'], description=data.get("description",""), time=current_time.strftime("%Y-%m-%d %H:%M:%S"), diet=data.get("diet",False))
    update = diets_collection.update_one(
    {"id": 1},
    {"$set": {
        "name": update_recipe.name,  
        "description": diet.get(update_recipe.description, ''),
        "diet": update_recipe.diet
        }
    })
    if update.modified_count > 0:
        return jsonify({"message": "Dieta atualizada com sucesso"})
    else:
        return jsonify({"message": "Nenhuma alteração feita"}), 400

@app.route("/diets/<diet_id>", methods=['DELETE'])
def delete_diet(diet_id):
    diet = diets_collection.find_one({"id": int(diet_id)})
    
    if not diet:
        return jsonify({"message": "Dieta não encontrada"}), 404
    
    delete = diets_collection.delete_one({"_id": diet["_id"]})
    
    if delete.deleted_count > 0:
        return jsonify({"message": "Dieta apagada com sucesso"})
    else:
        return jsonify({"message": "Erro ao excluir dieta"}), 400

        
    

if __name__ == "__main__":
    app.run(debug=True)