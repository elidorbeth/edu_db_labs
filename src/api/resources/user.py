from flask import request
from flask_restx import Resource, fields, Namespace
from api.models import db, User, Role

api = Namespace('users', description='Операції з користувачами')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'role_id': fields.Integer,
})

@api.route('/')
class UserListResource(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user, 201


@api.route('/<int:user_id>')
@api.response(404, 'Користувача не знайдено')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        db.session.refresh(user)
        return user

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Користувача видалено'}, 204
