import telnetlib

ip = raw_input("Qual IP para comunicacao Telnet?")
porta = raw_input("Qual porta para comunicacao Telnet?")
ranged = raw_input("Qual o range (r) selecionado? Opcoes: 0, 1, 2, 3, 4, 5, 6 e 7")
n = raw_input("Qual o numero de samples (n) selecionado? Opcoes: 1...4095")
print "O ip e : %s . A porta e %s . O range e %s . O numero de samples e %s " %( ip, porta, ranged, n)

tn = telnetlib.Telnet(ip, porta)
sess_op = tn.read_all()
print sess_op
