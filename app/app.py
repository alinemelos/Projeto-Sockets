from os import getenv
import socket
host = getenv('HOST')
print(host)

#definindo com quem cada host vai se relacionar (rotas)
route_1 = ['host6', 'host2']
route_2 = ['host1', 'host3']
route_3 = ['host2', 'host4']
route_4 = ['host3', 'host5']
route_5 = ['host4', 'host6']
route_6 = ['host5', 'host1']

# certificate_auth = Certificate_Authority() 

# definir com quem cada host vai se relacionar
if host == 'host1':
