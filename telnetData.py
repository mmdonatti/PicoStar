#!/usr/bin/python

# ########	Software para testes do NSLS ELectrometer 	########
# ########	Autor : Guilherme Teixeira Semissatto		########
# ########	Grupo : GAE					########
# ########	Ultima modificao: 06/09/2016			########

import telnetlib
import datetime

ip = raw_input("Qual IP para comunicacao Telnet?\n")
porta = raw_input("Qual porta para comunicacao Telnet? Default: 5757 \n")
range_lido = raw_input("Qual o range (r) selecionado? Opcoes: 0, 1, 2, 3, 4, 5, 6 e 7\n")
n = raw_input("Qual o numero de samples (n) selecionado? Opcoes: 1...4096\n")
p = raw_input("Qual periodo de integracao (p) em us? Opcoes: 400...100000\n")
filename = raw_input("Qual nome do arquivo para salvar os dados? Ex.: log.txt\n")
print "O ip e : %s . A porta e %s . O range e %s . O numero de samples e %s . O periodo de integracao e %s  \n" %( ip, porta, range_lido, n, p)

tn = telnetlib.Telnet(ip, porta)
print "\n \nTelnet Communication On\n \n"

file = open(filename, 'a')

if	range_lido == '7':
	k	=	2100*42.85/(100.15)			#gain para r = 7
elif	range_lido == '6':
	k	=	2100*42.85*1050.55/(900.2*100.15)	#gain para r = 6
elif	range_lido == '5':
	k	=	2100*42.85*1259.76/(900.2*100.15)	#gain para r = 5
elif	range_lido == '4':
	k	=	2100*42.45*1590.2/(900.2*100.15)	#gain para r = 4
elif	range_lido == '3':
	k	=	2100*42.85*2099.69/(900.2*100.15)	#gain para r = 3
elif	range_lido == '2':
	k	=	2100*42.85*3151.18/(900.2*100.15)	#gain para r = 2
elif	range_lido == '1':
	k	=	2100*42.85*6295.55/(900.2*100.15)	#gain para r = 1
elif	range_lido == '0':
	k	=	2100*42.85*5953.53/(200.1*100.15)	#gain para r = 0

os		=	4430*float(n)				#offset
k_int		=	(float(p))/3000				#gain multiplo do periodo de integracao 3k us
samples		=	float(n)				#samples em float
#os_emp		=	2*float(p)/(1000000)+ 0.23		#offset para calibracao
os_emp		=	0
ch_treated	=	[0,0,0,0]				#free vector to fill
k_new		=	10.4331606217616/1.04901384809064
while True:
	if len(tn.read_some()) == 44:
		data = tn.read_some()
		fields = data.split(' ')
		for i in range(4):
			auxiliar = 0
			try:
				float(fields[i])
			except ValueError:
				auxiliar = 1
			if (auxiliar == 0 and float(fields[i]) > 0 and len(fields[3]) == 11):			# necessita melhorar o comparador == 11
				ch_treated[i] = (float(fields[i])-os)/(k_int*k*samples*k_new)-os_emp
				ch_treated[i] = 0.9957777778*ch_treated[i]
			else:
				ch_treated[i] = 0
		print "%f	nA	%f	nA	%f	nA	%f	nA" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
		file.write( str(datetime.datetime.now())+" "+str(ch_treated[0])+"	nA\n	" ) 
