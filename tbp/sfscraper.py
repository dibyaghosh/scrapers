from lxml import html
import requests
from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker
from models import *
from utils import *

base_url = "http://studyfruit.com"

class SFScraper:

    switches = {'Biology':'Bio', 'Chemical Engineering':'ChemE',
                'CEE':'CE','Chemistry':'Chem'}

    def __init__(self):
        self.engine = create_engine('sqlite:///exams.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def parse(self):
        self.session.query(StudyGuide).delete()
        page = requests.get(base_url+'/doku.php')
        tree = html.fromstring(page.content)
        courses = tree.xpath('//*[@id="dokuwiki__aside"]/div/div[2]/div/p/a')[1:]
        [self.parse_class(i.text,i.attrib['href']) for i in courses]

    def parse_class(self,coursename,courseurl):
        course = self.find_closest(coursename)
        if not course:
            return
        page = requests.get(base_url+courseurl)
        tree = html.fromstring(page.content)
        links = tree.xpath('//*[@id="dokuwiki__content"]/div/div/div[4]/ul/li/div/p/a')
        for sg in links:
            studyguide = StudyGuide(sg.text,sg.attrib['href'])
            course.guides.append(studyguide)
        self.session.commit()
        print(course)

    def find_closest(self,coursename):
        coursename = fixCode(self.switches,coursename)
        course = self.session.query(Course).filter(func.lower(Course.name) == func.lower(coursename)).first()
        return course


s= SFScraper()
s.parse()
