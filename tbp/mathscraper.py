from lxml import html
import requests
from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker
from models import *
from utils import *

class MathScraper:
    def __init__(self):
        self.engine = create_engine('sqlite:///exams.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def get_courses(self):
        url = "https://math.berkeley.edu/courses/archives/exams"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        course_links = tree.xpath('//*[@id="node-923"]/div/div/p/a')[1:]
        [self.parse_course(i.text,i.attrib['href']) for i in course_links]
        #print([(i.text,i.attrib['href']) for i in course_links])

    def parse_course(self,name,url):
        print(name)
        course = self.foc_course(name,url)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        examlinks = tree.xpath('//*[@id="content-area"]/div/div/div[2]/div[2]/div/div/a')
        [self.parse_exam(e.text,e.attrib['href'],course) for e in examlinks]
        self.session.commit()

    def parse_exam(self,ename,eurl,course):
        surl = ""
        time_switch = {'Sp':'Spring ','F':'Fall ','Su':'Summer '}
        time,ename = ename[:ename.find(' ')],ename[ename.find(' ')+1:]
        time = fixCode(time_switch,time)
        try:
            num = int(time[-2:])
            if num > 50:
                time = time[:-2]+"19"+time[-2:]
            else:
                time = time[:-2]+"20"+time[-2:]
        except:
            pass
        examtype,instructor = ename[:ename.find('-')],ename[ename.find('-')+1:]
        instructor = instructor.split(' ')[-1]
        solornot = " Solution" in examtype
        if solornot:
            examtype = examtype[:examtype.rfind(" ")]
            eurl,surl = "",eurl
        exam_switch = {'First Midterm':'Midterm 1', 'Second Midterm':'Midterm 2','Final Exam':'Final'}
        examtype = fixCode(exam_switch,examtype)
        exam = Exam(time,examtype,eurl,surl)
        exam.instructors.append(self.get_instructor(instructor,""))
        course.exams.append(exam)

    def foc_course(self,coursename,url):
        found = self.session.query(Course).filter(func.lower(Course.name) == func.lower(coursename)).first()
        if not found:
            found = Course(coursename,url)
            self.session.add(found)
        return found

    def find_exam(self,courseid,etype,time,teacher):
        found = self.session.query(Exam).filter(Exam.course_id==courseid).filter(func.lower(Exam.examtype)==func.lower(etype))
        found = found.filter(func.lower(Exam.time) == func.lower(time)).all()
        if found:
            print(found)

    def get_instructor(self,name,url):
        instructor = self.session.query(Instructor).filter(func.lower(Instructor.name)==func.lower(name)).first()
        if instructor == None:
            instructor = Instructor(name,url)
            self.session.add(instructor)
        return instructor

scrapers = MathScraper()
#m.get_courses()