from flask_restx import Namespace, Resource, fields
from api.models import db, Course

api = Namespace('courses', description='Керування курсами (Course)')

course_model = api.model('Course', {
    'id':             fields.Integer(readOnly=True, description='ID курсу'),
    'title':          fields.String(required=True, description='Назва курсу'),
    'description':    fields.String(description='Опис курсу'),
    'duration_weeks': fields.Integer(required=True, description='Тривалість (тижнів)'),
})

@api.route('/')
class CourseList(Resource):
    @api.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()

    @api.expect(course_model, validate=True)
    @api.marshal_with(course_model, code=201)
    def post(self):
        data = api.payload
        new_course = Course(
            title=data['title'],
            description=data.get('description'),
            duration_weeks=data['duration_weeks']
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course, 201

@api.route('/<int:id>')
@api.response(404, 'Course not found')
@api.param('id', 'ID курсу')
class CourseResource(Resource):
    @api.marshal_with(course_model)
    def get(self, id):
        return Course.query.get_or_404(id)

    @api.expect(course_model, validate=True)
    @api.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get_or_404(id)
        data = api.payload
        course.title          = data['title']
        course.description    = data.get('description')
        course.duration_weeks = data['duration_weeks']
        db.session.commit()
        return course

    @api.response(204, 'Course deleted')
    def delete(self, id):
        course = Course.query.get_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return '', 204
