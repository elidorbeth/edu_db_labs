from flask_restx import Namespace, Resource, fields
from api.models import db, ModuleQuiz, Module, Quiz

api = Namespace('module_quizzes', description='Керування зв’язками Module_Quiz')

module_quiz_model = api.model('ModuleQuiz', {
    'module_id': fields.Integer(required=True, description='ID модуля'),
    'quiz_id':   fields.Integer(required=True, description='ID опитування'),
})

@api.route('/')
class ModuleQuizList(Resource):
    @api.marshal_list_with(module_quiz_model)
    def get(self):
        return ModuleQuiz.query.all()

    @api.expect(module_quiz_model, validate=True)
    @api.marshal_with(module_quiz_model, code=201)
    def post(self):
        data = api.payload
        _ = Module.query.get_or_404(data['module_id'])
        _ = Quiz.query.get_or_404(data['quiz_id'])
        new_link = ModuleQuiz(module_id=data['module_id'], quiz_id=data['quiz_id'])
        db.session.add(new_link)
        db.session.commit()
        return new_link, 201

@api.route('/<int:module_id>/<int:quiz_id>')
@api.response(404, 'ModuleQuiz not found')
@api.param('module_id', 'ID модуля')
@api.param('quiz_id',   'ID опитування')
class ModuleQuizResource(Resource):
    @api.marshal_with(module_quiz_model)
    def get(self, module_id, quiz_id):
        link = ModuleQuiz.query.get_or_404((module_id, quiz_id))
        return link

    @api.response(204, 'ModuleQuiz deleted')
    def delete(self, module_id, quiz_id):
        link = ModuleQuiz.query.get_or_404((module_id, quiz_id))
        db.session.delete(link)
        db.session.commit()
        return '', 204
