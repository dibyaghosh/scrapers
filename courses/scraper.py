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

def elementToClass(e):
    name  = e.xpath(".//span[@class='title']")[0].text
    code  = e.xpath(".//span[@class='code']")[0].text
    units = e.xpath(".//span[@class='hours']")[0].text

    coursedetails = e.xpath(".//p[@class='courseblockdesc']")[0]
    desc = '\n'.join(v.itertext())

    tpw = c.xpath('.//*[text()[contains(.,"Fall and/or spring:")]]')[0].tail
    prereqs = c.xpath('.//*[text()[contains(.,"Prerequisites")]]')[0].tail

    sbcl = c.xpath('.//*[text()[contains(.,"Course Level")]]')[0].tail
    sub, clevel = sbcl.split('/')

    gf = c.xpath('.//*[text()[contains(.,"Grading")]]')[0].tail
    grading, finals = gf.split('.')

    return Course(name, code, units, desc, tpw, prereqs, sub, clevel, grading, finals)
