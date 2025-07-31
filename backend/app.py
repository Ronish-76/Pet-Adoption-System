from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import base64
import os

app = Flask(__name__)
CORS(app)

DATABASE = '../pet_adoption.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/pets', methods=['GET'])
def get_pets():
    conn = get_db_connection()
    pets = conn.execute('SELECT * FROM pets WHERE status = "Available"').fetchall()
    conn.close()
    
    pets_list = []
    for pet in pets:
        pets_list.append({
            'id': pet['id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'image': pet['image'],
            'shelter': pet['shelter'],
            'status': pet['status']
        })
    
    return jsonify(pets_list)

@app.route('/api/pets', methods=['POST'])
def add_pet():
    data = request.json
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO pets (name, species, breed, age, gender, size, description, image, shelter, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['species'], 
        data['breed'],
        data['age'],
        data['gender'],
        data['size'],
        data['description'],
        data['image'],
        data['shelter'],
        'Available'
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Pet added successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)