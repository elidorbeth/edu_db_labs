import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sql_path = os.path.join(BASE_DIR, 'sql', 'lab6.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        script = f.read()

    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        print("Ініціалізація бази завершена")
    finally:
        cursor.close()
        conn.close()


class Role(db.Model):
    __tablename__ = 'Role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    users = db.relationship('User', back_populates='role', cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))

    role = db.relationship('Role', back_populates='users')
    assignments = db.relationship('QuizAssignment', back_populates='user', cascade="all, delete-orphan")
    answers = db.relationship('Answer', back_populates='user', cascade="all, delete-orphan")
    reports = db.relationship('Report', back_populates='user', cascade="all, delete-orphan")


class QuizCategory(db.Model):
    __tablename__ = 'quizCategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    quizzes = db.relationship('Quiz', back_populates='category', cascade="all, delete-orphan")


class Quiz(db.Model):
    __tablename__ = 'Quiz'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('quizCategory.id'))

    category = db.relationship('QuizCategory', back_populates='quizzes')
    assignments = db.relationship('QuizAssignment', back_populates='quiz', cascade="all, delete-orphan")
    questions = db.relationship('Question', back_populates='quiz', cascade="all, delete-orphan")
    answers = db.relationship('Answer', back_populates='quiz', cascade="all, delete-orphan")
    module_links = db.relationship('ModuleQuiz', back_populates='quiz', cascade="all, delete-orphan")
    results = db.relationship('QuizResult', back_populates='quiz', cascade="all, delete-orphan")


class QuizAssignment(db.Model):
    __tablename__ = 'QuizAssignment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))

    user = db.relationship('User', back_populates='assignments')
    quiz = db.relationship('Quiz', back_populates='assignments')


class Question(db.Model):
    __tablename__ = 'Question'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    text = db.Column(db.Text)
    question_type = db.Column(db.String(50))

    quiz = db.relationship('Quiz', back_populates='questions')
    options = db.relationship('Option', back_populates='question', cascade="all, delete-orphan")
    answers = db.relationship('Answer', back_populates='question', cascade="all, delete-orphan")


class Option(db.Model):
    __tablename__ = 'Option'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    text = db.Column(db.Text)

    question = db.relationship('Question', back_populates='options')
    answers = db.relationship('Answer', back_populates='option', cascade="all, delete-orphan")


class Answer(db.Model):
    __tablename__ = 'Answer'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('Option.id'), nullable=True)
    text_answer = db.Column(db.Text)

    user = db.relationship('User', back_populates='answers')
    quiz = db.relationship('Quiz', back_populates='answers')
    question = db.relationship('Question', back_populates='answers')
    option = db.relationship('Option', back_populates='answers')


class Course(db.Model):
    __tablename__ = 'Course'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer)

    modules = db.relationship('Module', back_populates='course', cascade="all, delete-orphan")


class Module(db.Model):
    __tablename__ = 'Module'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

    course = db.relationship('Course', back_populates='modules')
    module_quizzes = db.relationship('ModuleQuiz', back_populates='module', cascade="all, delete-orphan")


class ModuleQuiz(db.Model):
    __tablename__ = 'Module_Quiz'

    module_id = db.Column(db.Integer, db.ForeignKey('Module.id'), primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'), primary_key=True)

    module = db.relationship('Module', back_populates='module_quizzes')
    quiz = db.relationship('Quiz', back_populates='module_links')


class QuizResult(db.Model):
    __tablename__ = 'quizResult'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    respondent_count = db.Column(db.Integer)

    quiz = db.relationship('Quiz', back_populates='results')
    reports = db.relationship('Report', back_populates='quiz_result', cascade="all, delete-orphan")


class Report(db.Model):
    __tablename__ = 'Report'

    id = db.Column(db.Integer, primary_key=True)
    quiz_result_id = db.Column(db.Integer, db.ForeignKey('quizResult.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    format = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.Date)

    quiz_result = db.relationship('QuizResult', back_populates='reports')
    user = db.relationship('User', back_populates='reports')
