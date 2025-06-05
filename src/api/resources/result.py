from flask_restx import Namespace, Resource, fields
from api.models import db, QuizResult, Quiz

api = Namespace('results', description='Керування результатами опитувань (QuizResult)')

result_model = api.model('QuizResult', {
    'id':              fields.Integer(readOnly=True, description='ID результату'),
    'quiz_id':         fields.Integer(required=True, description='ID опитування'),
    'respondent_count': fields.Integer(required=True, description='Кількість респондентів'),
})

@api.route('/')
class ResultList(Resource):
    @api.marshal_list_with(result_model)
    def get(self):
        return QuizResult.query.all()

    @api.expect(result_model, validate=True)
    @api.marshal_with(result_model, code=201)
    def post(self):
        data = api.payload
        _ = Quiz.query.get_or_404(data['quiz_id'])
        new_res = QuizResult(
            quiz_id=data['quiz_id'],
            respondent_count=data['respondent_count']
        )
        db.session.add(new_res)
        db.session.commit()
        return new_res, 201

@api.route('/<int:id>')
@api.response(404, 'QuizResult not found')
@api.param('id', 'ID результату')
class ResultResource(Resource):
    @api.marshal_with(result_model)
    def get(self, id):
        return QuizResult.query.get_or_404(id)

    @api.expect(result_model, validate=True)
    @api.marshal_with(result_model)
    def put(self, id):
        res = QuizResult.query.get_or_404(id)
        data = api.payload
        _ = Quiz.query.get_or_404(data['quiz_id'])
        res.quiz_id = data['quiz_id']
        res.respondent_count = data['respondent_count']
        db.session.commit()
        return res

    @api.response(204, 'QuizResult deleted')
    def delete(self, id):
        res = QuizResult.query.get_or_404(id)
        db.session.delete(res)
        db.session.commit()
        return '', 204
