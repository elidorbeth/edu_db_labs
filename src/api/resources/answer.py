from flask_restx import Namespace, Resource, fields
from api.models import db, Answer, User, Quiz, Question, Option

api = Namespace('answers', description='Керування відповідями (Answer)')

answer_model = api.model('Answer', {
    'id':          fields.Integer(readOnly=True, description='ID відповіді'),
    'user_id':     fields.Integer(required=True, description='ID користувача'),
    'quiz_id':     fields.Integer(required=True, description='ID опитування'),
    'question_id': fields.Integer(required=True, description='ID питання'),
    'option_id':   fields.Integer(description='ID вибраного варіанта (якщо є)'),
    'text_answer': fields.String(description='Текстова відповідь (якщо є)'),
})

@api.route('/')
class AnswerList(Resource):
    @api.marshal_list_with(answer_model)
    def get(self):
        return Answer.query.all()

    @api.expect(answer_model, validate=True)
    @api.marshal_with(answer_model, code=201)
    def post(self):
        data = api.payload
        _ = User.query.get_or_404(data['user_id'])
        _ = Quiz.query.get_or_404(data['quiz_id'])
        _ = Question.query.get_or_404(data['question_id'])
        if data.get('option_id') is not None:
            _ = Option.query.get_or_404(data['option_id'])

        new_ans = Answer(
            user_id=data['user_id'],
            quiz_id=data['quiz_id'],
            question_id=data['question_id'],
            option_id=data.get('option_id'),
            text_answer=data.get('text_answer')
        )
        db.session.add(new_ans)
        db.session.commit()
        return new_ans, 201

@api.route('/<int:id>')
@api.response(404, 'Answer not found')
@api.param('id', 'ID відповіді')
class AnswerResource(Resource):
    @api.marshal_with(answer_model)
    def get(self, id):
        return Answer.query.get_or_404(id)

    @api.expect(answer_model, validate=True)
    @api.marshal_with(answer_model)
    def put(self, id):
        ans = Answer.query.get_or_404(id)
        data = api.payload
        _ = User.query.get_or_404(data['user_id'])
        _ = Quiz.query.get_or_404(data['quiz_id'])
        _ = Question.query.get_or_404(data['question_id'])
        if data.get('option_id') is not None:
            _ = Option.query.get_or_404(data['option_id'])

        ans.user_id     = data['user_id']
        ans.quiz_id     = data['quiz_id']
        ans.question_id = data['question_id']
        ans.option_id   = data.get('option_id')
        ans.text_answer = data.get('text_answer')
        db.session.commit()
        return ans

    @api.response(204, 'Answer deleted')
    def delete(self, id):
        ans = Answer.query.get_or_404(id)
        db.session.delete(ans)
        db.session.commit()
        return '', 204
