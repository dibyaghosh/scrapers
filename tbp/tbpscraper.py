from lxml import html
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

base_url = "https://tbp.berkeley.edu/"

class TBPScraper:
    def __init__(self):
        self.engine = create_engine('sqlite:///exams.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def parse(self):
        page = requests.get(base_url+'courses')
        tree = html.fromstring(page.content)
        dep_links = tree.xpath('//*[@id="content"]/ul/li/a')
        for dep in dep_links:
            department = Department(dep.text,dep.attrib['href'])
            self.parse_department(department)
            self.session.add(department)
            self.session.commit()
        self.session.commit()

    def parse_department(self, department):
        print(department)
        page = requests.get(base_url+department.url)
        tree = html.fromstring(page.content)
        course_links = tree.xpath('//*[@id="content"]/ul/li/a')
        for c in course_links:
            course = Course(c.text, c.attrib['href'])
            department.courses.append(course)
            self.parse_course(course)

    def parse_course(self, course):
        page = requests.get(base_url+course.url)
        tree = html.fromstring(page.content)
        rows = tree.xpath('//*[@id="content"]/table[1]/tbody/tr')
        for exam in rows:
            if(len(exam.getchildren()) < 5): 
                break
            inst, examtype, time, eurl,surl = exam.getchildren()[:-1]
            eurl = base_url+eurl.getchildren()[0].attrib['href'] if any(eurl.getchildren()) else ""
            surl = base_url+surl.getchildren()[0].attrib['href'] if any(surl.getchildren()) else ""
            time, examtype = time.text,examtype.text
            exam = Exam(time, examtype, eurl,surl)
            for i in inst:
                instructor = self.get_instructor(i.text, i.attrib['href'])
                exam.instructors.append(instructor)
            course.exams.append(exam)

    def list_courses(self):
        for course in self.session.query(Course):
            print(course)

    def list_exams(self):
        for exam in self.session.query(Exam):
            print(exam)

    def get_instructor(self,name,url):
        instructor = self.session.query(Instructor).filter(Instructor.name==name).first()
        if instructor == None:
            instructor = Instructor(name,url)
            self.session.add(instructor)
        return instructor

scraper = TBPScraper()
#scraper.parse()
scraper.list_exams()
#print(scraper.session.query(Exam).filter(Exam.course.name == "CS 70").all())
