from flask_restx import Namespace, Resource, fields
from api.models import db, Quiz, QuizCategory
from datetime import datetime

api = Namespace('quizzes', description='Керування опитуваннями (Quiz)')

quiz_model = api.model('Quiz', {
    'id':          fields.Integer(readOnly=True, description='ID опитування'),
    'title':       fields.String(required=True, description='Заголовок'),
    'description': fields.String(description='Опис'),
    'start_date':  fields.Date(required=True, description='Дата початку (YYYY-MM-DD)'),
    'end_date':    fields.Date(required=True, description='Дата завершення (YYYY-MM-DD)'),
    'status':      fields.String(description='Статус (Наприклад: Заплановано, Чернетка тощо)'),
    'category_id': fields.Integer(required=True, description='ID категорії'),
})

@api.route('/')
class QuizList(Resource):
    @api.marshal_list_with(quiz_model)
    def get(self):
        return Quiz.query.all()

    @api.expect(quiz_model, validate=True)
    @api.marshal_with(quiz_model, code=201)
    def post(self):
        data = api.payload
        _ = QuizCategory.query.get_or_404(data['category_id'])

        try:
            start_dt = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_dt   = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, "Невірний формат дати. Очікується YYYY-MM-DD.")

        new_quiz = Quiz(
            title=data['title'],
            description=data.get('description'),
            start_date=start_dt,
            end_date=end_dt,
            status=data.get('status'),
            category_id=data['category_id']
        )
        db.session.add(new_quiz)
        db.session.commit()
        return new_quiz, 201

@api.route('/<int:id>')
@api.response(404, 'Quiz not found')
@api.param('id', 'ID опитування')
class QuizResource(Resource):
    @api.marshal_with(quiz_model)
    def get(self, id):
        return Quiz.query.get_or_404(id)

    @api.expect(quiz_model, validate=True)
    @api.marshal_with(quiz_model)
    def put(self, id):
        quiz = Quiz.query.get_or_404(id)
        data = api.payload

        _ = QuizCategory.query.get_or_404(data['category_id'])

        try:
            start_dt = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_dt   = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, "Невірний формат дати. Очікується YYYY-MM-DD.")

        quiz.title       = data['title']
        quiz.description = data.get('description')
        quiz.start_date  = start_dt
        quiz.end_date    = end_dt
        quiz.status      = data.get('status')
        quiz.category_id = data['category_id']
        db.session.commit()
        return quiz

    @api.response(204, 'Quiz deleted')
    def delete(self, id):
        quiz = Quiz.query.get_or_404(id)
        db.session.delete(quiz)
        db.session.commit()
        return '', 204
