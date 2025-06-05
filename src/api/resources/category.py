from flask_restx import Namespace, Resource, fields
from api.models import db, QuizCategory

api = Namespace('categories', description='Керування категоріями опитувань')

category_model = api.model('QuizCategory', {
    'id':   fields.Integer(readOnly=True, description='ID категорії'),
    'name': fields.String(required=True, description='Назва категорії'),
})

@api.route('/')
class CategoryList(Resource):
    @api.marshal_list_with(category_model)
    def get(self):
        return QuizCategory.query.all()

    @api.expect(category_model, validate=True)
    @api.marshal_with(category_model, code=201)
    def post(self):
        data = api.payload
        new_cat = QuizCategory(name=data['name'])
        db.session.add(new_cat)
        db.session.commit()
        return new_cat, 201

@api.route('/<int:id>')
@api.response(404, 'Category not found')
@api.param('id', 'ID категорії')
class CategoryResource(Resource):
    @api.marshal_with(category_model)
    def get(self, id):
        return QuizCategory.query.get_or_404(id)

    @api.expect(category_model, validate=True)
    @api.marshal_with(category_model)
    def put(self, id):
        cat = QuizCategory.query.get_or_404(id)
        data = api.payload
        cat.name = data['name']
        db.session.commit()
        return cat

    @api.response(204, 'Category deleted')
    def delete(self, id):
        cat = QuizCategory.query.get_or_404(id)
        db.session.delete(cat)
        db.session.commit()
        return '', 204
