#!/usr/bin/python

# ########	Software para testes do NSLS ELectrometer 	########
# ########	Autor : Guilherme Teixeira Semissatto		########
# ########	Grupo : GAE					########
# ########	Ultima modificao: 23/09/2016			########

import telnetlib
import datetime

# PyQtGraph Import
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
# End PyQtGraph Import


ip		= raw_input("Qual IP para comunicacao Telnet?\n")
porta 		= raw_input("Qual porta para comunicacao Telnet? Default: 5757 \n")
range_lido 	= raw_input("Qual o range (r) selecionado? Opcoes: 0, 1, 2, 3, 4, 5, 6 e 7\n")
n 		= raw_input("Qual o numero de samples (n) selecionado? Opcoes: 1...4096\n")
p 		= raw_input("Qual periodo de integracao (p) em us? Opcoes: 400...100000\n")
log_flag	= raw_input("Deseja salvar os dados ? (s/n)\n")
if log_flag == 's':
	filename	 = raw_input("Qual nome do arquivo para salvar os dados? Ex.: log.txt\n")
	file = open(filename, 'a')
	file.write("\n\n\n"+"NSLS Electrometer log file from "+str(datetime.datetime.now())+"\n\n\n")

print "O ip e : %s . A porta e %s . O range e %s . O numero de samples e %s . O periodo de integracao e %s  \n" %( ip, porta, range_lido, n, p)

tn = telnetlib.Telnet(ip, porta)
print "\n \nTelnet Communication On\n \n"


if	range_lido == '7':
	k	=	1.000888*2100*42.85/(100.15)			#gain para r = 7
elif	range_lido == '6':
	k	=	1.000888*2100*42.85*1050.55/(900.2*100.15)	#gain para r = 6
elif	range_lido == '5':
	k	=	1.0014*2100*42.85*1259.76/(900.2*100.15)	#gain para r = 5
elif	range_lido == '4':
	k	=	1.0014*2100*42.45*1590.2/(900.2*100.15)		#gain para r = 4
elif	range_lido == '3':
	k	=	1.00079*2100*42.85*2099.69/(900.2*100.15)	#gain para r = 3
elif	range_lido == '2':
	k	=	1.0005*2100*42.85*3151.18/(900.2*100.15)	#gain para r = 2
elif	range_lido == '1':
	k	=	1.0004991*2100*42.85*6295.55/(900.2*100.15)	#gain para r = 1
elif	range_lido == '0':
	k	=	2100*42.85*5953.53/(200.1*100.15)		#gain para r = 0

os			=	4430*float(n)				#offset
k_int			=	(float(p))/3000				#gain multiplo do periodo de integracao 3k us
samples			=	float(n)				#samples em float
ch_treated		=	[0,0,0,0]				#free vector to fill
ch0_treated_saved	=	[]					#array to save data to plot
ch1_treated_saved	=	[]					#array to save data to plot
ch2_treated_saved	=	[]					#array to save data to plot
ch3_treated_saved	=	[]					#array to save data to plot
#tempo			=	np.zeros(1000,dtype=float)		#array to save "time" to plot
k_new			=	10.4331606217616/1.04901384809064
auxiliar1		=	0					#aux variable to error filtering of reading data
auxiliar2		=	0					#aux variable that counts number of samples read

# PyQtGraph Setup
win = pg.GraphicsWindow(title="Current (nA) vs sample")
win.resize(1000,600)
win.setWindowTitle('Current (nA) vs sample')
p0 = win.addPlot(title="Ch0: Current (nA) vs sample")
p1 = win.addPlot(title="Ch1: Current (nA) vs sample")
win.nextRow()
p2 = win.addPlot(title="Ch2: Current (nA) vs sample")
p3 = win.addPlot(title="Ch3: Current (nA) vs sample")
# End PyQtGraph Setup

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
				ch_treated[i] = 0.9957777778*(float(fields[i])-os)/(k_int*k*samples*k_new)
			if i == 0:
				ch0_treated_saved.append(ch_treated[i])
			if i == 1:
				ch1_treated_saved.append(ch_treated[i])
			if i == 2:
				ch2_treated_saved.append(ch_treated[i])
			if i == 3:
				ch3_treated_saved.append(ch_treated[i])
			if (ch_treated[i] < 0):
				ch_treated[i] = 0		
		#tempo[auxiliar2]=auxiliar2
		auxiliar2 = auxiliar2+1
		
		#Dar uma olha em PlotDataItem http://www.pyqtgraph.org/documentation/graphicsItems/plotcurveitem.html
		#Dar uma olhada no esquema de update plot http://stackoverflow.com/questions/26994120/multiple-updating-plot-with-pyqtgraph-in-python
		# PyQtGraph Plots
		p0.plot(ch0_treated_saved, clear=True)
		p1.plot(ch1_treated_saved, clear=True)
		p2.plot(ch2_treated_saved, clear=True)
		p3.plot(ch3_treated_saved, clear=True)
		pg.QtGui.QApplication.processEvents()
		# End PyQtGraph Plots
		#print "%f	nA	%f	nA	%f	nA	%f	nA" % (ch_treated[0], ch_treated[1], ch_treated[2], ch_treated[3])
		if log_flag == 's':
			file.write(str(datetime.datetime.now())+"	"+str.format("{0:.9f}",ch_treated[0])+"	nA	"+str.format("{0:.9f}",ch_treated[1])+"	nA	"+str.format("{0:.9f}",ch_treated[2])+"	nA	"+str.format("{0:.9f}",ch_treated[3])+" nA\n" ) 
