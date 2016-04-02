from lxml import html
import requests

base_url = "http://studyfruit.com"

page = requests.get('http://guide.berkeley.edu/courses/')
tree = html.fromstring(page.content)
courses = tree.xpath('//*[@id="atozindex"]/ul/li/a')
[print(i.text,i.attrib['href']) for i in courses]
"""
page = requests.get(base_url+courses[0].attrib['href'])
tree2 = html.fromstring(page.content)
others = tree2.xpath('//*[@id="dokuwiki__content"]/div/div/div[4]/ul/li/div/p/a')
[print(i.text,i.attrib['href']) for i in others]
"""
