from lxml import html
import requests


page = requests.get('http://guide.berkeley.edu/courses/')
tree = html.fromstring(page.content)
courses = tree.xpath('//*[@id="atozindex"]/ul/li/a')
[print(i.text,i.attrib['href']) for i in courses]

<<<<<<< HEAD
"""
page = requests.get(base_url+courses[0].attrib['href'])
tree2 = html.fromstring(page.content)
others = tree2.xpath('//*[@id="dokuwiki__content"]/div/div/div[4]/ul/li/div/p/a')
[print(i.text,i.attrib['href']) for i in others]
"""
=======

eecs = requests.get('http://guide.berkeley.edu/courses/eecs/')
tree = html.fromstring(eecs.content)
classes = tree.xpath('//div[@class="courseblock"]')
[print(i.text) for i in classes]
>>>>>>> 7509be4d80fe8eaabd8459e0540706b398a6df84
