from lxml import html
import requests


page = requests.get('http://guide.berkeley.edu/courses/')
tree = html.fromstring(page.content)
courses = tree.xpath('//*[@id="atozindex"]/ul/li/a')
[print(i.text,i.attrib['href']) for i in courses]

eecs = requests.get('http://guide.berkeley.edu/courses/eecs/')
tree = html.fromstring(eecs.content)
classes = tree.xpath('//div[@class="courseblock"]')
[print(i.text) for i in classes]
