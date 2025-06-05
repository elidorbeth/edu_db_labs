from flask_restx import Namespace, Resource, fields
from api.models import db, Option, Question

api = Namespace('options', description='Керування варіантами відповідей (Option)')

option_model = api.model('Option', {
    'id':          fields.Integer(readOnly=True, description='ID варіанта'),
    'question_id': fields.Integer(required=True, description='ID питання'),
    'text':        fields.String(required=True, description='Текст варіанта'),
})

@api.route('/')
class OptionList(Resource):
    @api.marshal_list_with(option_model)
    def get(self):
        return Option.query.all()

    @api.expect(option_model, validate=True)
    @api.marshal_with(option_model, code=201)
    def post(self):
        data = api.payload
        _ = Question.query.get_or_404(data['question_id'])
        new_opt = Option(
            question_id=data['question_id'],
            text=data['text']
        )
        db.session.add(new_opt)
        db.session.commit()
        return new_opt, 201

@api.route('/<int:id>')
@api.response(404, 'Option not found')
@api.param('id', 'ID варіанта')
class OptionResource(Resource):
    @api.marshal_with(option_model)
    def get(self, id):
        return Option.query.get_or_404(id)

    @api.expect(option_model, validate=True)
    @api.marshal_with(option_model)
    def put(self, id):
        opt = Option.query.get_or_404(id)
        data = api.payload
        _ = Question.query.get_or_404(data['question_id'])
        opt.question_id = data['question_id']
        opt.text = data['text']
        db.session.commit()
        return opt

    @api.response(204, 'Option deleted')
    def delete(self, id):
        opt = Option.query.get_or_404(id)
        db.session.delete(opt)
        db.session.commit()
        return '', 204
