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
import numpy as np

ip			= '10.2.111.34' #raw_input("Qual IP para comunicacao Telnet?\n")
#ip		= '10.2.111.52' #raw_input("Qual IP para comunicacao Telnet?\n")
porta_input		= '4747' #raw_input("Qual porta para comunicacao Telnet de entrada? Default: 4747 \n")
porta_output	= '5757' #raw_input("Qual porta para comunicacao Telnet? Default: 5757 \n")

log_flag	= raw_input("Deseja salvar os dados ? (s/n)\n")
if log_flag == 's':
	filename = raw_input("Qual nome do arquivo para salvar os dados? Ex.: log.txt\n")
	filepath = os.path.join('logs/', filename)
	file = open(filepath, 'w')
	file.write("Electrometer log file from "+str(datetime.datetime.now())+"\n\n")

tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("m0\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans
if log_flag == 's':
	file.write(ans)

rg	= raw_input("\nQual o range (r) selecionado? Opcoes: 0, 1, 2, 3, 4, 5, 6 e 7\n")
tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("r"+rg+"\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans
if log_flag == 's':
	file.write(ans)

n 	= raw_input("\nQual o numero de samples (n) selecionado? Opcoes: 1...4096\n")
tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("n"+n+"\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans
if log_flag == 's':
	file.write(ans)

Tint = raw_input("\nQual periodo de integracao (p) em us? Opcoes: 400...100000\n")
tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("p"+Tint+"\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans
if log_flag == 's':
	file.write(ans)

tn.close()
offset = [0,0,0,0]
rg = float(rg)
n = float(n)
Tint = float(Tint)	

off_adj = raw_input("\nDeseja zerar offset\n")
if off_adj == 's':
	ch_treated	=	[0,0,0,0]				#free vector to fill
	length = 10;
	arr = np.empty([length,4]);

	tn = telnetlib.Telnet(ip,porta_output) #open telnet output

	for j in range(length):
		data = tn.read_until('\n',5)
		fields = data.split(' ')
		try:
			for i in range(4):
				ch_treated[i] = 1e6*(((float(fields[i]))*50.2*rg)/(0xFFFFF) - 0.2*rg)/(Tint*n)-offset[i];
			print "%+.3f pA   %+.3f pA   %+.3f pA   %+.3f pA        \r\r" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
			arr[j,:] = fields;
			if log_flag == 's':
				file.write(str(datetime.datetime.now())+"\t\t%+.3f\t\t%+.3f\t\t%+.3f\t\t%+.3f\n" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])) 
			offset = offset + 1e6*(((ch_treated)*50.2*rg)/(0xFFFFF) - 0.2*rg)/Tint;
		except ValueError:
			pass
	tn.close()
	
print "\nOffset: " + "%+.3f pA   %+.3f pA   %+.3f pf   %+.3f pA        \n" % (offset[0], offset[1], offset[2], offset[3])
if log_flag == 's':
	file.write("\nOffset\t\tCH1\t\t\tCH2\t\t\tCH3\t\t\tCH4" + "\n%+.3f pA\t%+.3f pA\t%+.3f pf\t%+.3f pA\n" % (offset[0], offset[1], offset[2], offset[3]))

raw_input("\nPress Enter to Start\n")
	
print "O ip e : %s . A porta e %s . O range e %f . O numero de samples e %f . O periodo de integracao e %f  \n" %( ip, porta_output, rg, n, Tint)
if log_flag == 's':
	file.write("\nIP\t\t\t\tPorta" + "\n%s\t\t%s\n\n" %( ip, porta_output))

full_scale = 1e6*(rg*50)/(Tint*n) 		#datasheet pag. 9
resol = (rg*50.2*1e12/0xFFFFF)/(Tint*n)	#
if resol < 1000:
	unit_r = 'aA'
else:
	resol = resol/1000;
	unit_r = 'fA'

print "O fundo de escala e: %.3f pA\t A resolucao e: %.3f %s\n" %(full_scale,resol,unit_r)
if log_flag == 's':
	file.write("Full Scale: %.3f pA\t Resolution: %.3f %s\n\n" %(full_scale,resol,unit_r))
	
ch_treated	=	[0,0,0,0]				#free vector to fill

if log_flag == 's':
			file.write("Datetime\t\t\t\t\t\tCH1(pA)\t\tCH2(pA)\t\tCH3(pA)\t\tCH4(pA)\n") 
			
tn = telnetlib.Telnet(ip,porta_output) #open telnet output

#Tempo medio de execucao de uma iteracao: 70 us
while True:
	data = tn.read_until('\n',5)
	fields = data.split(' ')
	try:
		for i in range(4):
			ch_treated[i] = 1e6*(((float(fields[i]))*50.2*rg)/(0xFFFFF) - 0.2*rg)/(Tint*n)-offset[i];
		print "%+.3f pA   %+.3f pA   %+.3f pA   %+.3f pA        \r\r" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
		if log_flag == 's':
			file.write(str(datetime.datetime.now())+"\t\t%+.3f\t\t%+.3f\t\t%+.3f\t\t%+.3f\n" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])) 
	except ValueError:
		pass
	