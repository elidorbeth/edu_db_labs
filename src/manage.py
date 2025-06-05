import os
from flask import Flask
from api.config import Config
from api.models import db
from api.swagger import init_api
from api.models import init_db  # функція для запуску SQL-скрипта
from api.resources.role import api as role_ns
from api.resources.user import api as user_ns
from api.resources.category import api as category_ns
from api.resources.quiz import api as quiz_ns
from api.resources.assignment import api as assignment_ns
from api.resources.question import api as question_ns
from api.resources.option import api as option_ns
from api.resources.answer import api as answer_ns
from api.resources.course import api as course_ns
from api.resources.module import api as module_ns
from api.resources.module_quiz import api as module_quiz_ns
from api.resources.result import api as result_ns
from api.resources.report import api as report_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

# Ініціалізація SQLAlchemy
    db.init_app(app)

# Ініціалізація Swagger / RESTX
    api = init_api(app)


    api.add_namespace(role_ns,        path='/roles')
    api.add_namespace(user_ns,        path='/users')
    api.add_namespace(category_ns,    path='/categories')
    api.add_namespace(quiz_ns,        path='/quizzes')
    api.add_namespace(assignment_ns,  path='/assignments')
    api.add_namespace(question_ns,    path='/questions')
    api.add_namespace(option_ns,      path='/options')
    api.add_namespace(answer_ns,      path='/answers')
    api.add_namespace(course_ns,      path='/courses')
    api.add_namespace(module_ns,      path='/modules')
    api.add_namespace(module_quiz_ns, path='/module-quizzes')
    api.add_namespace(result_ns,      path='/results')
    api.add_namespace(report_ns,      path='/reports')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
