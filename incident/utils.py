from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, incidents, tasks):
		incidents_per_day = incidents.filter(timestamp__day=day)
		tasks_per_day = tasks.filter(due_date__day=day)
		d = ''
		for incident in incidents_per_day:
			d += '<li> {subject} </li>'.format(subject=incident.subject)

		for task in tasks_per_day:
			d += '<li> {subject} </li>'.format(subject=task.task_subject)

		if day != 0:
			return "<td><span class='date'>{day}</span><ul> {d} </ul></td>".format(day=day, d=d)
		return '<td></td>'
		return d

	# formats a week as a tr 
	def formatweek(self, theweek, incidents, tasks):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, incidents, tasks)
		return "<tr> {week} </tr>".format(week=week)

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		incidents =  Incident.objects.filter(timestamp__year=self.year, timestamp__month=self.month)
		tasks =  Task.objects.filter(due_date__year=self.year, due_date__month=self.month)

		cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		# cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		# cal += f'{self.formatweekheader()}\n'
		# for week in self.monthdays2calendar(self.year, self.month):
		# 	cal += f'{self.formatweek(week, incidents, tasks)}\n'
		return cal


def get_filename(filename, request):
    return filename.upper()
