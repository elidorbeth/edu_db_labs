# Реалізація інформаційного та програмного забезпечення

В рамках проекту розробляється: 
- SQL-скрипт для створення на початкового наповнення бази даних
- RESTfull сервіс для управління даними


CREATE TABLE Role (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE User (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Role(id)
);


CREATE TABLE quizCategory (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE Quiz (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES quizCategory(id)
);


CREATE TABLE QuizAssignment (
    id INT PRIMARY KEY,
    user_id INT,
    quiz_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);


CREATE TABLE Question (
    id INT PRIMARY KEY,
    quiz_id INT,
    text TEXT,
    question_type VARCHAR(50),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);


CREATE TABLE Option (
    id INT PRIMARY KEY,
    question_id INT,
    text TEXT,
    FOREIGN KEY (question_id) REFERENCES Question(id)
);


CREATE TABLE Answer (
    id INT PRIMARY KEY,
    user_id INT,
    quiz_id INT,
    question_id INT,
    option_id INT,
    text_answer TEXT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id),
    FOREIGN KEY (question_id) REFERENCES Question(id),
    FOREIGN KEY (option_id) REFERENCES Option(id)
);


CREATE TABLE Course (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    duration_weeks INT
);


CREATE TABLE Module (
    id INT PRIMARY KEY,
    course_id INT,
    title VARCHAR(255),
    content TEXT,
    FOREIGN KEY (course_id) REFERENCES Course(id)
);


CREATE TABLE Module_Quiz (
    module_id INT,
    quiz_id INT,
    PRIMARY KEY (module_id, quiz_id),
    FOREIGN KEY (module_id) REFERENCES Module(id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);


CREATE TABLE quizResult (
    id INT PRIMARY KEY,
    quiz_id INT,
    respondent_count INT,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);


CREATE TABLE Report (
    id INT PRIMARY KEY,
    quiz_result_id INT,
    user_id INT,
    format VARCHAR(50),
    content TEXT,
    created_at DATE,
    FOREIGN KEY (quiz_result_id) REFERENCES quizResult(id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);
