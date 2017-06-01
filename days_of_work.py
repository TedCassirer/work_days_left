#!/usr/bin/python3

import datetime as dt
import sys
from bs4 import BeautifulSoup as bs
import requests
from collections import namedtuple

holiday_source = "https://www.kalender.se/helgdagar/"

holidays = dict()
WORKDAY, WEEKEND, HOLIDAY, HALFDAY = range(4)
WorkDays = namedtuple("WorkDays", ["workdays", "weekends", "holidays", "half_days"])

def parse_date(dateStr, deliminiter='-'):
	datePara = map(int, dateStr.split(deliminiter))
	return dt.date(*datePara)

def get_holidays(source, start_year, end_year):
	holidays = {}
	for year in range(start_year, end_year+1):
		soup = bs(requests.get(source + str(year)).text, 'html.parser')
		table = soup.find('table', class_='table table-striped').find_all('tr')
		for holiday in table[1:]:
			data = holiday.find_all('td')
			date = parse_date(data[0].text.strip())
			holiday_name = data[1].text.strip()
			holidays[date] = holiday_name
	return holidays

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)

def get_type_of_day(date):
	if date.weekday() >= 5:
		return WEEKEND
	if date in holidays:
		return HOLIDAY
	if (date + dt.timedelta(1)) in holidays:
		return HALFDAY
	return WORKDAY

def get_work_days(start_date, end_date):
	work = [[], [], [], []]
	for date in daterange(start_date, end_date):
		work[get_type_of_day(date)].append(str(date)) 
	res = WorkDays._make(work)		
	return res

if __name__	== "__main__":
	td = dt.date.today()
	target = parse_date(sys.argv[1])
	holidays = get_holidays(holiday_source, td.year, target.year)	
	work = get_work_days(td, target)
	res = list(map(len, work))
	print(WorkDays._make(res))
	print("Days left: %i" % (sum(res)))		
	print("Next halfday is:", work.half_days[0])
	print("Next holiday is:", work.holidays[0], holidays[parse_date(work.holidays[0])])	
