from flask_restx import Namespace, Resource, fields
from api.models import db, QuizAssignment, User, Quiz

api = Namespace('assignments', description='Керування призначеннями опитувань (QuizAssignment)')

assignment_model = api.model('QuizAssignment', {
    'id':      fields.Integer(readOnly=True, description='ID запису призначення'),
    'user_id': fields.Integer(required=True, description='ID користувача'),
    'quiz_id': fields.Integer(required=True, description='ID опитування'),
})

@api.route('/')
class AssignmentList(Resource):
    @api.marshal_list_with(assignment_model)
    def get(self):
        return QuizAssignment.query.all()

    @api.expect(assignment_model, validate=True)
    @api.marshal_with(assignment_model, code=201)
    def post(self):
        data = api.payload
        _ = User.query.get_or_404(data['user_id'])
        _ = Quiz.query.get_or_404(data['quiz_id'])

        new_asg = QuizAssignment(user_id=data['user_id'], quiz_id=data['quiz_id'])
        db.session.add(new_asg)
        db.session.commit()
        return new_asg, 201

@api.route('/<int:id>')
@api.response(404, 'Assignment not found')
@api.param('id', 'ID призначення')
class AssignmentResource(Resource):
    @api.marshal_with(assignment_model)
    def get(self, id):
        return QuizAssignment.query.get_or_404(id)

    @api.expect(assignment_model, validate=True)
    @api.marshal_with(assignment_model)
    def put(self, id):
        asg = QuizAssignment.query.get_or_404(id)
        data = api.payload
        _ = User.query.get_or_404(data['user_id'])
        _ = Quiz.query.get_or_404(data['quiz_id'])
        asg.user_id = data['user_id']
        asg.quiz_id = data['quiz_id']
        db.session.commit()
        return asg

    @api.response(204, 'Assignment deleted')
    def delete(self, id):
        asg = QuizAssignment.query.get_or_404(id)
        db.session.delete(asg)
        db.session.commit()
        return '', 204
