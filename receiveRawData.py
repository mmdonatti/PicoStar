#!/usr/bin/python

####	Configuracao do NSLS ELectrometer 		
####	Mauricio Martins Donatti			
####	mauricio.donatti@lnls.br				
####	Ultima modificao: 23/10/2017						
####	Contribuicao: Guilherme Teixeira Semissatto	

import telnetlib
import datetime
import os.path
from os import listdir
from os.path import isfile, join

ip			= "10.2.111.52"#10.2.111.34' #raw_input("Qual IP para comunicacao Telnet?\n")
porta_input		= '4747' #raw_input("Qual porta para comunicacao Telnet de entrada? Default: 4747 \n")
porta_output	= '5757' #raw_input("Qual porta para comunicacao Telnet? Default: 5757 \n")

log_flag	= raw_input("Deseja salvar os dados ? (s/n)\n")
if log_flag == 's':
	filename = raw_input("Qual nome do arquivo para salvar os dados? Ex.: log.txt\n")
	filepath = os.path.join('logs/', filename)
	file = open(filepath, 'w')
	file.write("NSLS Electrometer log file from "+str(datetime.datetime.now())+"\n\n")

rg	= 1

n 	= 1
Tint = 1000000

offset = [0,0,0,0]

rg = float(rg)
n = float(n)
Tint = float(Tint)	

full_scale = 1e6*(rg*50)/(Tint*n) 		#datasheet pag. 9
resol = (rg*50.2*1e12/0xFFFFF)/(Tint*n)	#
if resol < 1000:
	unit_r = 'aA'
else:
	resol = resol/1000;
	unit_r = 'fA'
	
tn = telnetlib.Telnet(ip,porta_output) #open telnet output

ch_treated	=	[0,0,0,0]				#free vector to fill

if log_flag == 's':
			file.write("Datetime\t\t\t\t\t\tCH1(pA)\t\tCH2(pA)\t\tCH3(pA)\t\tCH4(pA)\n") 

#Tempo medio de execucao de uma iteracao: 70 us
while True:
	data = tn.read_until('\n',5)
	fields = data.split(' ')
	print fields
	try:
		for i in range(4):
			ch_treated[i] = 1e6*(((float(fields[i]))*50.2*rg)/(0xFFFFF) - 0.2*rg)/(Tint*n)-offset[i];
		print "%+.3f pA   %+.3f pA   %+.3f pA   %+.3f pA        \r\r" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
		if log_flag == 's':
			file.write(str(datetime.datetime.now())+"\t\t%+.3f\t\t%+.3f\t\t%+.3f\t\t%+.3f\n" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])) 
	except ValueError:
		pass
	