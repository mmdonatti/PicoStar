#!/usr/bin/python

####	Configuracao do NSLS ELectrometer 		
####	Mauricio Martins Donatti			
####	mauricio.donatti@lnls.br				
####	Ultima modificao: 23/10/2017						
####	Contribuicao: Guilherme Teixeira Semissatto	

import telnetlib
import datetime
import os.path

#ip		= '10.2.111.34' #raw_input("Qual IP para comunicacao Telnet?\n")
ip		= '10.2.111.52' #raw_input("Qual IP para comunicacao Telnet?\n")
porta 		= '4747' #raw_input("Qual porta para comunicacao Telnet? Default: 4747 \n")
log_flag	= raw_input("Deseja salvar os dados ? (s/n)\n")
if log_flag == 's':
	filename = raw_input("Qual nome do arquivo para salvar os dados? Ex.: log.txt\n")
	filepath = os.path.join('logs/', filename)
	file = open(filepath, 'a')
	file.write("\n\n\n"+"NSLS Electrometer log file from "+str(datetime.datetime.now())+"\n\n\n")

print "O ip e : %s . A porta e %s " %( ip, porta)

menu = {}
menu['h']=" - help" 
menu['i']=" - Integrator ID"
menu['m']=" - Mode"
menu['n']=" - Samples Count"
menu['p']=" - Period (us)"
menu['r']=" - Range: 1 to 7"
menu['s']=" - Return Settings"
menu['t']=" - Trigger Command (use with m=1)"
menu['v']=" - Return Firmware Version"
menu['e']=" - Exit"
while True: 
	print "\n\n"
	tn = telnetlib.Telnet(ip, porta,10)
	options=menu.keys()
	options.sort()
	for entry in options: 
		print entry, menu[entry]
	selection=raw_input("\nPlease Select:") 
	print "\n\n"
	if selection =='e':
		tn.close()
		if log_flag == 's':
			file.write(str(datetime.datetime.now())+": Exiting...\n")
			file.close()
		break 
	elif (selection in ['h','i','s','t','v']): 
		print "No Parameter Command"	
		tn.write(selection+"\r")
		ans = tn.read_until('\r', timeout=5)
		print "Answer: " + ans
		if log_flag == 's':
			file.write(str(datetime.datetime.now())+": Selection:"+menu[selection]+" Answer:"+ans+"\n")
	elif (selection in ['m','n','p','r']): 
		print "Parameter Command\n" 
		param=raw_input("\nSET (s) ou GET (g)?\n")
		if (param in ['s','S','set','SET','Set']):
			param=raw_input("\nDigite o valor do parametro: \n")
			tn.write(selection + param+"\r\r")
			ans = tn.read_until('\r', timeout=5)
			print "Answer: " + ans
			if log_flag == 's':
				file.write(str(datetime.datetime.now())+": Selection:"+menu[selection]+" mode: "+param+" Answer:"+ans+"\n")
		elif (param in ['g','G','get','GET','Get']):
			tn.write(selection+"\r")
			ans = tn.read_until('\r', timeout=5)
			print "Answer: " + ans
			if log_flag == 's':
				file.write(str(datetime.datetime.now())+": Selection:"+menu[selection]+" Answer:"+ans+"\n")
	else: 
		print "Unknown Option Selected!" 			