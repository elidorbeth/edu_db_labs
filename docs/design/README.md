# Проєктування бази даних

В рамках проекту розробляється: 
- модель бізнес-об'єктів 
@startuml
left to right direction

' --- Сутності ---
entity User #ffffff
entity User.id
entity User.first_name
entity User.last_name
entity User.email
entity User.role

entity Role
entity Role.id
entity Role.name

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

entity Course
entity Course.id
entity Course.title
entity Course.description
entity Course.instructor_id
entity Course.duration_weeks

entity Module
entity Module.id
entity Module.course_id
entity Module.title
entity Module.order
entity Module.content

entity SurveyCategory
entity SurveyCategory.id
entity SurveyCategory.name
entity SurveyCategory.description

entity SurveyResult
entity SurveyResult.id
entity SurveyResult.quiz_id
entity SurveyResult.respondent_count
entity SurveyResult.created_at

entity Report
entity Report.id
entity Report.survey_result_id
entity Report.format
entity Report.content
entity Report.created_at

' --- Атрибути ---
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

Course *-- Course.id
Course *-- Course.title
Course *-- Course.description
Course *-- Course.instructor_id
Course *-- Course.duration_weeks

Module *-- Module.id
Module *-- Module.course_id
Module *-- Module.title
Module *-- Module.order
Module *-- Module.content

Role *-u- Role.id
Role *-u- Role.name

SurveyCategory *-u- SurveyCategory.id
SurveyCategory *-u- SurveyCategory.name
SurveyCategory *-u- SurveyCategory.description

SurveyResult *-- SurveyResult.id
SurveyResult *-- SurveyResult.quiz_id
SurveyResult *-- SurveyResult.respondent_count
SurveyResult *-- SurveyResult.created_at

Report *-u- Report.id
Report *-u- Report.survey_result_id
Report *-u- Report.format
Report *-u- Report.content
Report *-u- Report.created_at

' --- Зв’язки між сутностями ---
User "1,1" -- "0..*" QuizAssignment : assigns
Quiz "1,1" -- "0..*" QuizAssignment : assigned to

Quiz "1,1" -- "0..*" Question : contains
Question "1,1" -- "0..*" Option

User "1,1" -- "0..*" Answer
Quiz "1,1" -- "0..*" Answer
Question "1,1" -- "0..*" Answer : question answer
Option "0..1" -- "0..*" Answer : selected option

User "1,1" -- "0..*" Course : creates
Course "1,1" -- "1..*" Module : contains
Module "0..*" -- "0..*" Quiz : includes

Role "1,1" -- "0..*" User

SurveyCategory "1,1" -- "0..*" Quiz
Quiz "1,1" -- "0..1" SurveyResult
SurveyResult "1,1" -- "0..1" Report
User "1,1" -- "0..*" Report

@enduml

- ER-модель
@startuml
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

entity "Role" {
  + id : INT
  --
  name : STRING
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

entity "Course" {
  + id : INT
  --
  title : STRING
  description : STRING
  instructor_id : INT
  duration_weeks : INT
}

entity "Module" {
  + id : INT
  --
  course_id : INT
  title : STRING
  order : INT
  content : TEXT
}

entity "SurveyCategory" {
  + id : INT
  --
  name : STRING
  description : STRING
}

entity "SurveyResult" {
  + id : INT
  --
  quiz_id : INT
  respondent_count : INT
  created_at : DATE
}

entity "Report" {
  + id : INT
  --
  survey_result_id : INT
  format : STRING
  content : TEXT
  created_at : DATE
}

' --- Зв’язки ---
"User" ||--o{ "QuizAssignment"
"Quiz" ||--o{ "QuizAssignment"

"Quiz" ||--o{ "Question"
"Question" ||--o{ "Option"

"User" ||--o{ "Answer"
"Quiz" ||--o{ "Answer"
"Question" ||--o{ "Answer"
"Option" |o--o{ "Answer"

"User" ||--o{ "Course"
"Course" ||--o{ "Module"
"Module" ||--o{ "Quiz"

"Role" ||--o{ "User"
"SurveyCategory" ||--o{ "Quiz"
"Quiz" ||--o| "SurveyResult"
"SurveyResult" ||--o| "Report"
"User" ||--o{ "Report"

@enduml

- реляційна схема

```sql
Table User {
  id int [pk]
  first_name varchar
  last_name varchar
  email varchar
  role varchar
}

Table Role {
  id int [pk]
  name varchar
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

Table Course {
  id int [pk]
  title varchar
  description text
  instructor_id int
  duration_weeks int
}

Table Module {
  id int [pk]
  course_id int
  title varchar
  order int
  content text
}

Table SurveyCategory {
  id int [pk]
  name varchar
  description text
}

Table SurveyResult {
  id int [pk]
  quiz_id int
  respondent_count int
  created_at date
}

Table Report {
  id int [pk]
  survey_result_id int
  format varchar
  content text
  created_at date
}

Ref: QuizAssignment.user_id > User.id
Ref: QuizAssignment.quiz_id > Quiz.id

Ref: Question.quiz_id > Quiz.id
Ref: Option.question_id > Question.id

Ref: Answer.user_id > User.id
Ref: Answer.quiz_id > Quiz.id
Ref: Answer.question_id > Question.id
Ref: Answer.option_id > Option.id

Ref: Course.instructor_id > User.id
Ref: Module.course_id > Course.id
Ref: Module.id > Quiz.id

Ref: User.role > Role.id
Ref: Quiz.id > SurveyResult.quiz_id
Ref: SurveyCategory.id > Quiz.id
Ref: SurveyResult.id > Report.survey_result_id
Ref: Report.id > User.id
