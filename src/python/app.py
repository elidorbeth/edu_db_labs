import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_restx import Api, Resource, fields

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_db_file = os.path.join(BASE_DIR, 'formsys.db')
print("Using database at:", _db_file)

# Конфігурація SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{_db_file}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_EXPIRE_ON_COMMIT'] = False

db = SQLAlchemy(app)
api = Api(
    app,
    version='1.0',
    title='FORMSYS API',
    description='REST API для системи опитувань експертів',
    doc='/docs'
)

# Swagger-моделі
role_model = api.model('Role', {
    'id': fields.Integer(description='ID ролі'),
    'name': fields.String(required=True, description='Назва ролі')
})
user_model = api.model('User', {
    'id': fields.Integer(description='ID користувача'),
    'email': fields.String(required=True, description='Email'),
    'first_name': fields.String(required=True, description='Ім’я'),
    'last_name': fields.String(required=True, description='Прізвище'),
    'role_id': fields.Integer(required=True, description='ID ролі')
})

# ORM-моделі
class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))
    role = db.relationship('Role')

ns_role = api.namespace('roles', description='Операції з ролями')
ns_user = api.namespace('users', description='Операції з користувачами')

# Role endpoints
@ns_role.route('')
class RoleList(Resource):
    @ns_role.marshal_list_with(role_model)
    def get(self):
        return Role.query.all()

    @ns_role.expect(role_model)
    @ns_role.response(201, 'Role created')
    @ns_role.response(400, 'Validation Error')
    def post(self):
        data = request.json or {}
        name = data.get('name')
        if not name:
            api.abort(400, 'Missing field: name')

        if 'id' in data and data['id'] is not None:
            new_role = Role(id=data['id'], name=name)
        else:
            new_role = Role(name=name)

        db.session.add(new_role)
        try:
            db.session.flush()
            role_id = new_role.id
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            api.abort(400, 'Integrity error: можливо, id вже існує')

        return {'id': role_id, 'name': new_role.name}, 201

@ns_role.route('/<int:id>')
class RoleItem(Resource):
    @ns_role.marshal_with(role_model)
    @ns_role.response(404, 'Role not found')
    def get(self, id):
        return Role.query.get_or_404(id)

    @ns_role.expect(role_model)
    @ns_role.response(200, 'Role updated')
    @ns_role.response(400, 'Validation Error')
    @ns_role.response(404, 'Role not found')
    def put(self, id):
        data = request.json or {}
        name = data.get('name')
        if not name:
            api.abort(400, 'Missing field: name')
        role = Role.query.get_or_404(id)
        role.name = name
        try:
            db.session.flush()
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            api.abort(400, 'Integrity error')
        return {'id': role.id, 'name': role.name}

    @ns_role.response(204, 'Role deleted')
    @ns_role.response(404, 'Role not found')
    def delete(self, id):
        role = Role.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        return '', 204

# User endpoints
@ns_user.route('')
class UserList(Resource):
    @ns_user.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @ns_user.expect(user_model)
    @ns_user.response(201, 'User created')
    @ns_user.response(400, 'Validation Error')
    def post(self):
        data = request.json or {}
        missing = [f for f in ('email','first_name','last_name','role_id') if f not in data]
        if missing:
            api.abort(400, f'Missing fields: {missing}')

        if 'id' in data and data['id'] is not None:
            new_user = User(
                id=data['id'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                role_id=data['role_id']
            )
        else:
            new_user = User(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                role_id=data['role_id']
            )

        db.session.add(new_user)
        try:
            db.session.flush()
            user_id = new_user.id
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            api.abort(400, 'Integrity error: id уже існує або email неунікальний')

        return {
            'id': user_id,
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'role_id': new_user.role_id
        }, 201

@ns_user.route('/<int:id>')
class UserItem(Resource):
    @ns_user.marshal_with(user_model)
    @ns_user.response(404, 'User not found')
    def get(self, id):
        return User.query.get_or_404(id)

    @ns_user.expect(user_model)
    @ns_user.response(200, 'User updated')
    @ns_user.response(400, 'Validation Error')
    @ns_user.response(404, 'User not found')
    def put(self, id):
        data = request.json or {}
        user = User.query.get_or_404(id)
        for field in ('email','first_name','last_name','role_id'):
            if field in data:
                setattr(user, field, data[field])
        try:
            db.session.flush()
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            api.abort(400, 'Integrity error: email неунікальний')
        return {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'role_id': user.role_id}

@app.route('/', methods=['GET'])
def index():
    return {'message': 'Welcome to FORMSYS API. Use /roles or /users.'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
