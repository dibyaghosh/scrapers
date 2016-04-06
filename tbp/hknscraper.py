from lxml import html
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

base_url = "https://tbp.berkeley.edu/"

class HKNScraper:
    def __init__(self):
        self.engine = create_engine('sqlite:///exams.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def parse(self):
        page = requests.get('https://hkn.eecs.berkeley.edu/exams')
        tree = html.fromstring(page.content)
        dep_links = tree.xpath('//*[@id="container"]/div/table/tbody/tr/td/a')
        print([(i.text,i.attrib['href']) for i in dep_links])
        for dep in dep_links:
            course_name = dep.text.split("-")[0].strip()
            print(repr(course_name))
            self.parse_page(course_name,dep.attrib['href'])
            self.session.commit()
        self.session.commit()


    def parse_page(self,name,url):
        course = get_course(name)
        base_url = "https://hkn.eecs.berkeley.edu"
        page = requests.get(base_url+url)
        tree = html.fromstring(page.content)
        crs_rows = tree.xpath('//*[@id="exams"]/tr')[1:]
        for row in crs_rows:
            self.get_row(course,row)

    def get_row(self,course,elem):
        time,ictors,mt1,mt2,mt3,final = elem.getchildren()
        time = time.text.strip()
        instructors = []
        for inst in ictors.getchildren():
            instructors.append(get_instructor(inst.text,inst.attrib['href']))
        insert_if_possible(mt1,course,time,"Midterm 1",instructors)
        insert_if_possible(mt2,course,time,"Midterm 2",instructors)
        insert_if_possible(mt3,course,time,"Midterm 3",instructors)
        insert_if_possible(final,course,time,"Final",instructors)


    def insert_if_possible(self,elem,course,time,examtype,instructors):
        if len(elem.getchildren())==0:
            return
        possibles = {url.text:url.attrib['href'] for url in elem.getchildren()}
        eurl = possibles['[pdf]'] if '[pdf]' in possibles else ""
        surl = possibles['[solution]'] if '[solution]' in possibles else ""
        exam = self.update_exam(course,time,examtype,eurl,surl,instructors)

    def update_exam(self,course,time,examtype,eurl,surl,instructors):

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

    def get_course(self,name):
        val = self.session.query(Class).filter(Class.name==name).first()
        if val == None:
            val = Course(name,"")
            self.session.add(val)
        return val

    def update_exam(self,course,time,examtype,eurl,surl,instructors):
        courseid = course.index
        alls = self.session.query(Exam).filter(Exam.course_id==courseid)
        alls = alls.filter(Exam.time==time).filter(Course.examtype==examtype)
        exm = alls.first()
        if not course:
            exm = Exam(time,examtype,eurl,surl)
            course.append(exm)
            for inst in instructors:
                exm.instructors.append(inst)
        else:
            exm.examurl = eurl
            exm.solutionurl = surl
        return exm


scraper = TBPScraper()
#scraper.parse()
scraper.list_exams()
#print(scraper.session.query(Exam).filter(Exam.course.name == "CS 70").all())
