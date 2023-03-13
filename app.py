from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate('firebase\key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apipsp-a8ed6-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Initialize reference to Firebase database
ref = db.reference('Mangas')

# Metodo para sacar todos los mangas
@app.route('/mangas', methods=['GET'])
def get_all_mangas():
    Mangas = ref.get()
    return jsonify(Mangas)

# Metodo para buscar un manga por el título
@app.route('/get-manga/<title>', methods=['GET'])
def get_manga(title):
    manga = ref.order_by_child('titulo').equal_to(title).get()
    if manga:
        return jsonify(manga)
    else:
        return jsonify({'error': 'Manga not found'}), 404

# Metodo para añadir un nuevo manga
@app.route('/new-manga', methods=['POST'])
def add_manga():
    manga = request.json
    new_manga_ref = ref.push()  # crea una nueva referencia en la lista de Mangas
    new_manga_ref.set(manga)   # establece los datos del nuevo manga en la referencia creada
    return jsonify({'message': 'Manga added successfully', 'data': manga}), 201

# Metodo para borrar un manga
@app.route('/delete-manga/<title>', methods=['DELETE'])
def delete_manga(title):
    mangas_ref = ref.order_by_child('titulo').equal_to(title).get()
    if not mangas_ref:
        return jsonify({'error': 'Manga not found'}), 404
    else:
        for manga_id in mangas_ref:
            ref.child(manga_id).delete()
        return jsonify({'message': 'Manga deleted successfully'}), 200

# Metodo para actualizar la información de la valoración de un manga
@app.route('/update-manga-score/<title>', methods=['PATCH'])
def update_manga_score(title):
    manga_ref = ref.order_by_child('titulo').equal_to(title).get()
    if not manga_ref:
        return jsonify({'error': 'Manga not found'}), 404
    else:
        manga_id = next(iter(manga_ref))
        manga = manga_ref[manga_id]
        new_score = request.json.get('score')
        if not new_score:
            return jsonify({'error': 'New score not provided'}), 400
        manga['valoracion'] = new_score
        ref.child(manga_id).update(manga)
        return jsonify({'message': 'Manga score updated successfully', 'data': manga}), 200

