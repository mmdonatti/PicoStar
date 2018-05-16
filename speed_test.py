#!/usr/bin/python

import datetime
import os.path
from os import listdir
from os.path import isfile, join
import timeit

log_flag	= raw_input("Deseja salvar os dados ? (s/n)\n")
if log_flag == 's':
	filename = raw_input("Qual nome do arquivo para salvar os dados? Ex.: log.txt\n")
	filepath = os.path.join('logs/', filename)
	file = open(filepath, 'w')
	file.write("NSLS Electrometer log file from "+str(datetime.datetime.now())+"\n\n")

ch_treated = [0,0,0,0]

start_time = timeit.default_timer()

rg = 1
Tint = 1000000
offset = [-10,-10,-10,-10]
n = 1

for i in range(10000):
	data = "0000000000 0000000000 0000000000 0000000000"
	fields = data.split(' ')
	try:
		for i in range(4):
			ch_treated[i] = 1e6*(((float(fields[i]))*50.2*rg)/(0xFFFFF) - 0.2*rg)/(Tint*n)-offset[i];
		print "%+.3f pA   %+.3f pA   %+.3f pA   %+.3f pA        \r\r" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
		if log_flag == 's':
			file.write(str(datetime.datetime.now())+"\t\t%+.3f\t\t%+.3f\t\t%+.3f\t\t%+.3f\n" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])) 
	except ValueError:
		pass

elapsed = timeit.default_timer() - start_time	
print elapsed/10000