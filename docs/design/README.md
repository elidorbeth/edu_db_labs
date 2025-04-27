# Проєктування бази даних

В рамках проекту розробляється: 
- модель бізнес-об'єктів 
@startuml

' --- Сутності ---
entity User #ffffff
entity User.id
entity User.first_name
entity User.last_name
entity User.email
entity User.role

entity Quiz
entity Quiz.id
entity Quiz.title
entity Quiz.description
entity Quiz.start_date
entity Quiz.end_date
entity Quiz.status

entity QuizAssignment
entity QuizAssignment.id
entity QuizAssignment.user_id
entity QuizAssignment.quiz_id

entity Question
entity Question.id
entity Question.quiz_id
entity Question.text
entity Question.question_type

entity Option
entity Option.id
entity Option.question_id
entity Option.text

entity Answer
entity Answer.id
entity Answer.user_id
entity Answer.quiz_id
entity Answer.question_id
entity Answer.option_id
entity Answer.text_answer

' --- Композиція атрибутів до сутностей ---
left to right direction
User *-u- User.id
User *-u- User.first_name
User *-u- User.last_name
User *-u- User.email
User *-u- User.role

Quiz *-u- Quiz.id
Quiz *-u- Quiz.title
Quiz *-u- Quiz.description
Quiz *-u- Quiz.start_date
Quiz *-u- Quiz.end_date
Quiz *-u- Quiz.status

QuizAssignment *-- QuizAssignment.id
QuizAssignment *-- QuizAssignment.user_id
QuizAssignment *-- QuizAssignment.quiz_id

Question *-u- Question.id
Question *-u- Question.quiz_id
Question *-u- Question.text
Question *-u- Question.question_type

Option *-u- Option.id
Option *-u- Option.question_id
Option *-u- Option.text

Answer *-- Answer.id
Answer *-- Answer.user_id
Answer *-- Answer.quiz_id
Answer *-- Answer.question_id
Answer *-- Answer.option_id
Answer *-- Answer.text_answer

' --- Зв'язки між основними сутностями з мультиплікацією ---
User "1,1" -- "0..*" QuizAssignment : assigns
Quiz "1,1" -- "0..*" QuizAssignment : assigned to

Quiz "1,1" -- "0..*" Question : contains
Question "1,1" -- "0..*" Option

User "1,1" -- "0..*" Answer
Quiz "1,1" -- "0..*" Answer
Question "1,1" -- "0..*" Answer : question answer
Option "0..1" -- "0..*" Answer : selected option

@enduml

- ER-модель
@startuml
' Налаштування вигляду
skinparam linetype ortho

' --- Сутності ---
entity "User" {
    + id : INT
    --
    first_name : STRING
    last_name : STRING
    email : STRING
    role : STRING
}

entity "Quiz" {
    + id : INT
    --
    title : STRING
    description : STRING
    start_date : DATE
    end_date : DATE
    status : STRING
}

entity "QuizAssignment" {
    + id : INT
    --
    user_id : INT
    quiz_id : INT
}

entity "Question" {
    + id : INT
    --
    quiz_id : INT
    text : STRING
    question_type : STRING
}

entity "Option" {
    + id : INT
    --
    question_id : INT
    text : STRING
}

entity "Answer" {
    + id : INT
    --
    user_id : INT
    quiz_id : INT
    question_id : INT
    option_id : INT
    text_answer : STRING
}

' --- Зв'язки між сутностями ---
"User" ||--o{ "QuizAssignment" : assigns
"Quiz" ||--o{ "QuizAssignment" : assigned to

"Quiz" ||--o{ "Question" : contains
"Question" ||--o{ "Option"

"User" ||--o{ "Answer"
"Quiz" ||--o{ "Answer"
"Question" ||--o{ "Answer" : question answer
"Option" |o--o{ "Answer" : selected option

@enduml

- реляційна схема

Table User {
  id int [pk]
  first_name varchar
  last_name varchar
  email varchar
  role varchar
}

Table Quiz {
  id int [pk]
  title varchar
  description text
  start_date date
  end_date date
  status varchar
}

Table QuizAssignment {
  id int [pk]
  user_id int
  quiz_id int
}

Table Question {
  id int [pk]
  quiz_id int
  text text
  question_type varchar
}

Table Option {
  id int [pk]
  question_id int
  text varchar
}

Table Answer {
  id int [pk]
  user_id int
  quiz_id int
  question_id int
  option_id int
  text_answer text
}

Ref: QuizAssignment.user_id > User.id
Ref: QuizAssignment.quiz_id > Quiz.id

Ref: Question.quiz_id > Quiz.id

Ref: Option.question_id > Question.id

Ref: Answer.user_id > User.id
Ref: Answer.quiz_id > Quiz.id
Ref: Answer.question_id > Question.id
Ref: Answer.option_id > Option.id
