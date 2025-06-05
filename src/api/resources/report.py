from flask_restx import Namespace, Resource, fields
from api.models import db, Report, QuizResult, User
from datetime import datetime

api = Namespace('reports', description='Керування звітами (Report)')

report_model = api.model('Report', {
    'id':             fields.Integer(readOnly=True, description='ID звіту'),
    'quiz_result_id': fields.Integer(required=True, description='ID результату (quizResult)'),
    'user_id':        fields.Integer(required=True, description='ID користувача, що створив звіт'),
    'format':         fields.String(required=True, description='Формат звіту (наприклад: PDF, DOCX)'),
    'content':        fields.String(description='Вміст звіту'),
    'created_at':     fields.Date(required=True, description='Дата створення (YYYY-MM-DD)'),
})

@api.route('/')
class ReportList(Resource):
    @api.marshal_list_with(report_model)
    def get(self):
        return Report.query.all()

    @api.expect(report_model, validate=True)
    @api.marshal_with(report_model, code=201)
    def post(self):
        data = api.payload
        _ = QuizResult.query.get_or_404(data['quiz_result_id'])
        _ = User.query.get_or_404(data['user_id'])
        try:
            created_dt = datetime.strptime(data['created_at'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, "Невірний формат дати. Очікується YYYY-MM-DD.")
        new_r = Report(
            quiz_result_id=data['quiz_result_id'],
            user_id=data['user_id'],
            format=data['format'],
            content=data.get('content'),
            created_at=created_dt
        )
        db.session.add(new_r)
        db.session.commit()
        return new_r, 201

@api.route('/<int:id>')
@api.response(404, 'Report not found')
@api.param('id', 'ID звіту')
class ReportResource(Resource):
    @api.marshal_with(report_model)
    def get(self, id):
        return Report.query.get_or_404(id)

    @api.expect(report_model, validate=True)
    @api.marshal_with(report_model)
    def put(self, id):
        rep = Report.query.get_or_404(id)
        data = api.payload
        _ = QuizResult.query.get_or_404(data['quiz_result_id'])
        _ = User.query.get_or_404(data['user_id'])
        try:
            created_dt = datetime.strptime(data['created_at'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, "Невірний формат дати. Очікується YYYY-MM-DD.")
        rep.quiz_result_id = data['quiz_result_id']
        rep.user_id        = data['user_id']
        rep.format         = data['format']
        rep.content        = data.get('content')
        rep.created_at     = created_dt
        db.session.commit()
        return rep

    @api.response(204, 'Report deleted')
    def delete(self, id):
        rep = Report.query.get_or_404(id)
        db.session.delete(rep)
        db.session.commit()
        return '', 204
