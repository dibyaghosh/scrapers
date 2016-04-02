from lxml import html
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

base_url = "http://guide.berkeley.edu"
class GuideScraper:
    def __init__(self):
        self.engine = create_engine('sqlite:///courses.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_courses(self):
        page = requests.get(base_url+'/courses/')
        tree = html.fromstring(page.content)
        courses = tree.xpath('//*[@id="atozindex"]/ul/li/a')
        [self.parse_department(i.attrib['href']) for i in courses]

    def parse_department(self,url):
        print(url)
        department = requests.get(base_url+url)
        tree = html.fromstring(department.content)
        classes = tree.xpath('//div[@class="courseblock"]')
        [self.session.add(self.elementToClass(e)) for e in classes if self.elementToClass(e)]
        self.session.commit()

    def elementToClass(self,e):
        try:
            name  = e.xpath(".//span[@class='title']")[0].text
            code  = e.xpath(".//span[@class='code']")[0].text
            units = e.xpath(".//span[@class='hours']")[0].text

            coursedetails = e.xpath(".//p[@class='courseblockdesc']")[0]
            desc = '\n'.join(coursedetails.itertext())

            tpw = e.xpath('.//*[text()[contains(.,"Fall and/or spring:")]]')[0].tail
            prereqs = e.xpath('.//*[text()[contains(.,"Prerequisites")]]')[0].tail

            sbcl = e.xpath('.//*[text()[contains(.,"Course Level")]]')[0].tail
            sub, clevel = sbcl.split('/')

            gf = e.xpath('.//*[text()[contains(.,"Grading")]]')[0].tail
            grading, finals = gf.split('.')[:2]
            print(name)
            return Course(name, code, units, desc, tpw, prereqs, sub, clevel, grading, finals)
        except:
            return

g = GuideScraper()
g.get_courses()
