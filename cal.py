#!/usr/bin/python

####	Configuracao do NSLS ELectrometer 		
####	Mauricio Martins Donatti			
####	mauricio.donatti@lnls.br				
####	Ultima modificao: 23/10/2017						
####	Contribuicao: Guilherme Teixeira Semissatto	

import telnetlib
import datetime
import os.path
import numpy as np

ip				= '10.2.111.34' #raw_input("Qual IP para comunicacao Telnet?\n")
porta_input		= '4747' #raw_input("Qual porta para comunicacao Telnet de entrada? Default: 4747 \n")
porta_output	= '5757' #raw_input("Qual porta para comunicacao Telnet? Default: 5757 \n")

tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("i\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans
		
filepath = os.path.join("./cal/",str(datetime.date.today())+"_ID"+ans[9:-2]+".cal")
#filepath = os.path.join("./cal/",str(datetime.date.today())+"_TESTE_ID"+ans[9:-2]+".cal")
file = open(filepath, 'w')

tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("m0\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans

tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("n1\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans

tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("r1\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans

tn = telnetlib.Telnet(ip,porta_input,10)
tn.write("p1000000\r\r")
ans = tn.read_until('\r', timeout=5)
print "\nAnswer: " + ans

tn.close()

try:
	tn_o = telnetlib.Telnet(ip, porta_output,10)
except:
	print "\nTelnet Error"
length = 100;

arr = np.empty([length,4]);

ch_treated	=	[0,0,0,0]				#free vector to fill
rg = 1
Tint = 1000000

for j in range(5):
	data = tn_o.read_until('\n',5)
	fields = data.split(' ')
	for i in range(4):
		fields[i] = float(fields[i])
		try:
			ch_treated[i] = 1e6*(((fields[i])*50.2*rg)/(0xFFFFF) - 0.2*rg)/Tint;
		except ValueError:
			print "Receive Error\n\r"
	print "%+.3f pA   %+.3f pA   %+.3f pf   %+.3f pA        \r\r" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])

for j in range(length):
	data = tn_o.read_until('\n',5)
	fields = data.split(' ')
	for i in range(4):
		fields[i] = float(fields[i])
		try:
			ch_treated[i] = 1e6*(((fields[i])*50.2*rg)/(0xFFFFF) - 0.2*rg)/Tint;
		except ValueError:
			print "Receive Error\n\r"
	print "%+.3f pA   %+.3f pA   %+.3f pf   %+.3f pA        \r\r" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
	arr[j,:] = fields;

media = np.mean(arr, axis=0)
offset = 1e6*(((media.astype(np.float))*50.2*rg)/(0xFFFFF) - 0.2*rg)/Tint;

print "Valores de Offset Calculados: %+.3f pA   %+.3f pA  %+.3f pA  %+.3f pA       \n" % (offset[0], offset[1], offset[2], offset[3])

file.write(str(datetime.datetime.now())+" - Offset Currents per channel\n")
file.write("%f %f %f %f \n" % (offset[0], offset[1], offset[2], offset[3]))

tn_o.close()
file.close()