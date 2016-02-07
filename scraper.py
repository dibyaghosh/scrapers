import requests
from bs4 import BeautifulSoup
import csv

def convert_as_necessary(s):
	try:
		if int(s) == float(s):
			return int(s)
		return float(s)
	except:
		return s

def get_page(page_num):
	assert 0<page_num<139
	page = requests.get('http://www.boxofficemojo.com/alltime/domestic.htm?page=%d'%page_num)
	soup = BeautifulSoup(page.content, 'html.parser')
	table = soup.find("table",{"cellpadding":5})
	rows = table.find_all('tr')
	data = []
	for row in rows[1:]:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([convert_as_necessary(ele) for ele in cols if ele])
	return data


def save_to_csv(data,location="output.csv"):
	with open(location, "w") as f:
   		writer = csv.writer(f)
   		writer.writerows(data)

def get_all(num=139):
	data = []
	for i in range(1,num):
		data.extend(get_page(i))
		print(i)
	return data

