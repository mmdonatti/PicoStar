#!/usr/bin/python

import telnetlib

ip = raw_input("Qual IP para comunicacao Telnet?\n")
porta = raw_input("Qual porta para comunicacao Telnet?\n")
ranged = raw_input("Qual o range (r) selecionado? Opcoes: 0, 1, 2, 3, 4, 5, 6 e 7\n")
n = raw_input("Qual o numero de samples (n) selecionado? Opcoes: 1...4095\n")
p = raw_input("Qual periodo de integracao em us? Opcoes: 3000...100000\n")
print "O ip e : %s . A porta e %s . O range e %s . O numero de samples e %s . O periodo de integracao e %s  \n" %( ip, porta, ranged, n, p)

tn = telnetlib.Telnet(ip, porta)
print "\n \nTelnet Communication OK\n \n"

k	=	(2100*42.85)/100.15	#gain
os	=	4400*float(n)		#offset
k_int	=	(float(p))/3000		#gain multiplo do periodo de integracao 3k us
samples	=	float(n)		#samples em float
os_emp	=	0.27			#offset para calibracao

while True:
	if len(tn.read_some()) == 44:
		data = tn.read_some()
		fields = data.split(' ')
		ch1 = (float(fields[0])-os)/(k_int*k*samples)
		ch2 = (float(fields[1])-os)/(k_int*k*samples)
		ch3 = (float(fields[2])-os)/(k_int*k*samples)
		if len(fields[3]) == 11:					#gambiarra, necessita estudo de non printing characters
			ch4 = (float(fields[3]-os)/(k_int*k*samples)-os_emp
			ch5 = (float[fields[3]-os)/(k_int*k*samples)-os_emp-ch4*0.0025
			print "%f	nA	%f	nA	%f	nA	%f	nA" % (ch1, ch2, ch3, ch5)
