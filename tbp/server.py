from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,desc
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    """
    Serves the main page
    """
    f = open("index.html")
    return f.read()

@app.route('/get/courses')
def get_courses():
    courses = db.session.query(Course).all()
    return jsonify(data=[course.name for course in courses])
    return jsonify(data=[{'id':course.index, 'name':course.name} for course in courses])

@app.route('/get/exams/<int:course_id>')
def get_post(course_id):
    course = db.session.query(Course).get(course_id)
    exams = db.session.query(Exam).filter(Exam.course_id==course_id).all()
    return jsonify(course=course.to_dict(),exams=[e.to_dict() for e in exams])

if __name__ == '__main__':
    app.debug = True
    app.run()
