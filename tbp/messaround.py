from lxml import html
import requests
from models import *
from utils import *


"""
page = requests.get('https://hkn.eecs.berkeley.edu/exams')
tree = html.fromstring(page.content)
dep_links = tree.xpath('//*[@id="container"]/div/table/tbody/tr/td/a')
print([(i.text,i.attrib['href']) for i in dep_links])
"""
page = requests.get('https://hkn.eecs.berkeley.edu/exams/course/ee/40')
tree = html.fromstring(page.content)
dep_links = tree.xpath('//*[@id="exams"]/tr')[1:]

