from flask_restx import Namespace, Resource, fields
from api.models import db, Role

api = Namespace('roles', description='Керування ролями користувачів')

role_model = api.model('Role', {
    'id':   fields.Integer(readOnly=True, description='ID ролі'),
    'name': fields.String(required=True, description='Назва ролі'),
})

@api.route('/')
class RoleList(Resource):
    @api.marshal_list_with(role_model)
    def get(self):
        return Role.query.all()

    @api.expect(role_model, validate=True)
    @api.marshal_with(role_model, code=201)
    def post(self):
        data = api.payload
        new_role = Role(name=data['name'])
        db.session.add(new_role)
        db.session.commit()
        return new_role, 201

@api.route('/<int:id>')
@api.response(404, 'Role not found')
@api.param('id', 'ID ролі')
class RoleResource(Resource):
    @api.marshal_with(role_model)
    def get(self, id):
        role = Role.query.get_or_404(id)
        return role

    @api.expect(role_model, validate=True)
    @api.marshal_with(role_model)
    def put(self, id):
        role = Role.query.get_or_404(id)
        data = api.payload
        role.name = data['name']
        db.session.commit()
        return role

    @api.response(204, 'Role deleted')
    def delete(self, id):
        role = Role.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        return '', 204
