#!/usr/bin/python

# ########	Software para testes do NSLS ELectrometer 	########
# ########	Autor : Guilherme Teixeira Semissatto		########
# ########	Grupo : GAE					########
# ########	Ultima modificao: 06/09/2016			########

import telnetlib

ip = raw_input("Qual IP para comunicacao Telnet?\n")
porta = raw_input("Qual porta para comunicacao Telnet? Default: 5757 \n")
range_lido = raw_input("Qual o range (r) selecionado? Opcoes: 0, 1, 2, 3, 4, 5, 6 e 7\n")
n = raw_input("Qual o numero de samples (n) selecionado? Opcoes: 1...4095\n")
p = raw_input("Qual periodo de integracao (p) em us? Opcoes: 3000...100000\n")
print "O ip e : %s . A porta e %s . O range e %s . O numero de samples e %s . O periodo de integracao e %s  \n" %( ip, porta, range_lido, n, p)

tn = telnetlib.Telnet(ip, porta)
print "\n \nTelnet Communication OK\n \n"

k		=	(2100*42.85)/100.15		#gain para r = 7
#k		=	1
os		=	4430*float(n)			#offset
k_int		=	(float(p))/3000			#gain multiplo do periodo de integracao 3k us
samples		=	float(n)			#samples em float
os_emp		=	2*float(p)/(1000000)+ 0.23	#offset para calibracao
ch		=	[0,0,0,0]			#free vector to fill
ch_treated	=	[0,0,0,0]			#free vector to fill

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
				ch[i] = (float(fields[i])-os)/(k_int*k*samples)-os_emp
				ch_treated[i] = 0.997*ch[i]
			else:
				ch_treated[i] = 0
		print "%f	nA	%f	nA	%f	nA	%f	nA" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
