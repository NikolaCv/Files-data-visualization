import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import datetime
import time
from matplotlib import ticker as mticker

style.use("classic")
#print(plt.style.available)

def pretvori_st_u_broj(st):
	i = 2
	b = 0

	while i < len(st) - 1:
		if st[i] != ',':
			b = b*10 + int(st[i])
		i += 1
	return b

def obrada_fajla(f):
	st = ''
	b = []
	bn = []
	dates = []
	full_dates = []
	full_dates_n = []
	while True:
		st = f.readline()
		if st == 'DATE\n':
			break

	while True:
		st = f.readline()
		if st == 'HOME  COMMUNITY  PLAYERS\n':
			break

		if st[0] == '+':
			b.append(pretvori_st_u_broj(st))
			f.readline()
			f.readline()
			st = f.readline()

			full_st = st.replace('\n','')
			full_st = datetime.datetime.strptime(full_st,'%d/%m/%Y %H:%M')
			full_dates.append(full_st)

			st = st[0:10]
			st = datetime.datetime.strptime(st,'%d/%m/%Y')
			if st not in dates:
				dates.append(st)
		elif st[0] == '-':
			bn.append(pretvori_st_u_broj(st))
			f.readline()
			f.readline()
			st = f.readline()

			full_st = st.replace('\n','')
			full_st = datetime.datetime.strptime(full_st,'%d/%m/%Y %H:%M')
			full_dates_n.append(full_st)

			st = st[0:10]
			st = datetime.datetime.strptime(st,'%d/%m/%Y')
			if st not in dates:
				dates.append(st)

	dates.reverse()
	full_dates.sort()
	b.reverse()
	bn.reverse()
	bn = [x*(-1) for x in bn]
	full_dates_n.reverse()

	return dates, full_dates, full_dates_n, b, bn

def sumiraj_po_danima(b,st_set,dates_full,dates):
	i = 0
	suma = []
	prvi = datetime.datetime(2019,1,21)
	poslednji = datetime.datetime(2019,2,3)
	d = (poslednji-prvi).days

	for i in range (0,d+1):
		suma.append(0)

	i = 0
	while i < len(b):
		new = dates_full[i].replace(hour=0,minute=0)
		if new in st_set:
			suma[(dates_full[i] - prvi).days] += b[i]
		i += 1

	return suma

def uredi_datume(dates, full_dates, full_dates_n, b, bn):
	dates.sort()
	full_dates.sort()
	full_dates_n.sort()

	pocetak = datetime.datetime(2019,1,21)
	kraj = datetime.datetime(2019,2,3)

	st_set = set(pocetak + datetime.timedelta(x) for x in range(0, (kraj-pocetak).days+1))

	suma = sumiraj_po_danima(b,st_set,full_dates,dates)
	suman = sumiraj_po_danima(bn,st_set,full_dates_n,dates)

	for i in st_set:
		if i not in dates:
			dates.append(i)

	dates.sort()

	dates1 = []

	for i in st_set:
		dates1.append(i + datetime.timedelta(days=1))
	dates1.sort()

	return dates1, full_dates, suma, suman

def graph(igrac):
	f = open("%s.txt" %igrac,"r")

	dates, full_dates, full_dates_n, b, bn = obrada_fajla(f)

	dates, full_dates, suma, suman = uredi_datume(dates, full_dates, full_dates_n, b, bn)

	plt.figure(2,figsize=(15, 8))
	ax1 = plt.subplot(121)
	ax2 = plt.subplot(122,sharex=ax1)

	bar1 = ax1.bar(dates, suma, color='b',alpha=0.9, width = -0.8, align='edge')
	ax1.set_title("Suma",fontsize=20,pad=10)
	ax1.set_ylabel('Broj Poena',rotation=45,fontsize=15,labelpad=25)
	ax1.grid(True)
	ax1.axis([min(dates) - datetime.timedelta(days=1), max(dates) + datetime.timedelta(hours=4.8), 1.1*min(suman), 1.1*max(suma)])
	ax1.tick_params(axis='y', which='major', pad=10)

	bar2 = ax1.bar(dates, suman, color='r',alpha=0.9, width = -0.8, align='edge')
	ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=1))

	for rect in bar1:
		height = rect.get_height()
		ax1.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % height, ha='center', va='bottom')

	for rect in bar2:
		height = rect.get_height()
		if height != 0:
			ax1.text(rect.get_x() + rect.get_width()/2.0, height+min(suman)*0.018, '%d' % height, ha='center', va='top')

	ax2.plot_date(full_dates, b, '.')
	ax2.set_title("Po borbi",fontsize=20,pad=10)
	ax2.set_ylabel('Broj Poena',rotation=45,fontsize=15,labelpad=25)
	ax2.grid(True)
	ax2.set_ylim([0,1.1*max(b)])
	ax2.tick_params(axis='y', which='major', pad=10)
	ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=25))

	plt.gcf().autofmt_xdate(rotation=45)
	plt.suptitle(igrac, fontsize=25)
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')

	plt.show()


def main():

	graph('Alcohero')
	graph('Joseph')
	graph('Magma')

main()