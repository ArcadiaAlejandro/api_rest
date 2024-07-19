from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir el modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    datetimecreated = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.Column(db.Boolean, default=True)
    hasKey = db.Column(db.String(100), default="")

# Crear la tabla si no existe
with app.app_context():
    db.create_all()

# Endpoint para registrar un usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        datetimecreated=datetime.now(),
        state=data.get('state', True),
        hasKey=data.get('hasKey', "")
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

# Endpoint para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({"message": "Autenticación exitosa", "user": {"id": user.id, "username": user.username, "email": user.email}})
    else:
        return jsonify({"error": "Fallo en la autenticación"}), 401

# Endpoint para obtener todos los usuarios (opcional)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
