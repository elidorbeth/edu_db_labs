from flask_restx import Namespace, Resource, fields
from api.models import db, Module, Course

api = Namespace('modules', description='Керування модулями (Module)')

module_model = api.model('Module', {
    'id':        fields.Integer(readOnly=True, description='ID модуля'),
    'course_id': fields.Integer(required=True, description='ID курсу'),
    'title':     fields.String(required=True, description='Заголовок модуля'),
    'content':   fields.String(description='Контент модуля'),
})

@api.route('/')
class ModuleList(Resource):
    @api.marshal_list_with(module_model)
    def get(self):
        return Module.query.all()

    @api.expect(module_model, validate=True)
    @api.marshal_with(module_model, code=201)
    def post(self):
        data = api.payload
        _ = Course.query.get_or_404(data['course_id'])
        new_mod = Module(
            course_id=data['course_id'],
            title=data['title'],
            content=data.get('content')
        )
        db.session.add(new_mod)
        db.session.commit()
        return new_mod, 201

@api.route('/<int:id>')
@api.response(404, 'Module not found')
@api.param('id', 'ID модуля')
class ModuleResource(Resource):
    @api.marshal_with(module_model)
    def get(self, id):
        return Module.query.get_or_404(id)

    @api.expect(module_model, validate=True)
    @api.marshal_with(module_model)
    def put(self, id):
        mod = Module.query.get_or_404(id)
        data = api.payload
        _ = Course.query.get_or_404(data['course_id'])
        mod.course_id = data['course_id']
        mod.title = data['title']
        mod.content = data.get('content')
        db.session.commit()
        return mod

    @api.response(204, 'Module deleted')
    def delete(self, id):
        mod = Module.query.get_or_404(id)
        db.session.delete(mod)
        db.session.commit()
        return '', 204
