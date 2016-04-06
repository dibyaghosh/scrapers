from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base
from utils import *

Base = declarative_base()

instructor_table = Table('instructor_tags', Base.metadata,
                  Column('instructor', Integer, ForeignKey('instructors.index')),
                  Column('exam', Integer, ForeignKey('exams.index'))
                  )


class Course(Base):
    __tablename__ = "courses"

    index = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    department_id = Column(Integer, ForeignKey('departments.index'))
    exams = relationship("Exam", backref="course")
    guides = relationship("StudyGuide", backref="course")

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return "Course<%s>"%self.name

    def to_dict(self):
        d = dict()
        d['name'] = self.name
        d['url'] = self.url
        d['guides'] = [sg.todict() for sg in self.guides]
        return d

class Department(Base):
    __tablename__ = "departments"

    index = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String, unique=True)
    courses = relationship("Course", backref="department")

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return "Department<%s>"%self.name

class StudyGuide(Base):
    __tablename__ = "studyguides"

    index = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    course_id = Column(Integer, ForeignKey('courses.index'))

    def __init__(self,name,url):
        self.url = url
        self.name = name

    def __repr__(self):
        return "Guide<%s>"%self.name

    def todict(self):
        return {'name':self.name,'url':self.url}

class Exam(Base):
    __tablename__ = "exams"

    index = Column(Integer, primary_key=True)
    examurl = Column(String)
    solutionurl = Column(String)
    course_id = Column(Integer, ForeignKey('courses.index'))
    time = Column(String)
    examtype = Column(String)
    instructors = relationship("Instructor", secondary=instructor_table)

    def __init__(self, time, examtype="Final", examurl="", solutionurl=""):
        self.time = time
        self.examtype = examtype
        self.solutionurl = solutionurl
        self.examurl = examurl

    def __repr__(self):
        return "Exam< %s %s %s>"%(str(self.course), self.time, self.examtype)

    def to_dict(self):
        d = dict()
        d['url'] = self.examurl
        d['solutionurl'] = self.solutionurl
        d['eexists'] = len(self.examurl) > 1
        d['sexists'] = len(self.solutionurl) > 1
        d['time'] = self.time
        type_dict = {'Midterm 1':'First Midterm', 'Midterm 2':'Second Midterm'}
        d['exam'] = fixCode(type_dict,self.examtype)
        d['instructors'] = [inst.name for inst in self.instructors]
        return d


class Instructor(Base):
    __tablename__ = "instructors"

    index = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String, unique=True)
    exams = relationship("Exam", secondary=instructor_table)

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return "Instructor<%s>"%self.name

def nothing():
    pass

if __name__ == "__main__":
    engine = create_engine('sqlite:///exams.db', echo=False)
    Base.metadata.create_all(engine)
    print("Created Database")
