from flask_restx import Namespace, Resource, fields
from api.models import db, Question, Quiz

api = Namespace('questions', description='Керування питаннями (Question)')

question_model = api.model('Question', {
    'id':            fields.Integer(readOnly=True, description='ID питання'),
    'quiz_id':       fields.Integer(required=True, description='ID опитування'),
    'text':          fields.String(required=True, description='Текст питання'),
    'question_type': fields.String(required=True, description='Тип питання (single_choice, multiple_choice, text)'),
})

@api.route('/')
class QuestionList(Resource):
    @api.marshal_list_with(question_model)
    def get(self):
        return Question.query.all()

    @api.expect(question_model, validate=True)
    @api.marshal_with(question_model, code=201)
    def post(self):
        data = api.payload
        _ = Quiz.query.get_or_404(data['quiz_id'])
        new_q = Question(
            quiz_id=data['quiz_id'],
            text=data['text'],
            question_type=data['question_type']
        )
        db.session.add(new_q)
        db.session.commit()
        return new_q, 201

@api.route('/<int:id>')
@api.response(404, 'Question not found')
@api.param('id', 'ID питання')
class QuestionResource(Resource):
    @api.marshal_with(question_model)
    def get(self, id):
        return Question.query.get_or_404(id)

    @api.expect(question_model, validate=True)
    @api.marshal_with(question_model)
    def put(self, id):
        q = Question.query.get_or_404(id)
        data = api.payload
        _ = Quiz.query.get_or_404(data['quiz_id'])
        q.quiz_id = data['quiz_id']
        q.text = data['text']
        q.question_type = data['question_type']
        db.session.commit()
        return q

    @api.response(204, 'Question deleted')
    def delete(self, id):
        q = Question.query.get_or_404(id)
        db.session.delete(q)
        db.session.commit()
        return '', 204
