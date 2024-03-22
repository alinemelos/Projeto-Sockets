import socket
import threading

# Função para lidar com a comunicação de cada nó
def handle_connection(node_socket, node_id):
    print(f"Nó {node_id} pronto para receber mensagens.")
    while True:
        data, addr = node_socket.recvfrom(1024)
        print(f"Mensagem recebida de {addr} no nó {node_id}: {data.decode()}")
        # Processar a mensagem, se necessário

# Função para iniciar um nó
def start_node(node_id, port, neighbors):
    host = '127.0.0.1'
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    node_socket.bind((host, port))
    print(f"Nó {node_id} ouvindo na porta {port}")
    while True:
        data, addr = node_socket.recvfrom(1024)
        print(f"Mensagem recebida de {addr} no nó {node_id}: {data.decode()}")
        # Processar a mensagem, se necessário
        if addr[1] in neighbors:
            threading.Thread(target=handle_connection, args=(node_socket, node_id)).start()
        else:
            print(f"Conexão de um nó não autorizado com {addr} no nó {node_id}. Fechando conexão.")

# Definindo os detalhes de cada nó e seus vizinhos
nodes = {
    1: {'port': 5001, 'neighbors': [5002, 5006]},
    2: {'port': 5002, 'neighbors': [5001, 5003]},
    3: {'port': 5003, 'neighbors': [5002, 5004]},
    4: {'port': 5004, 'neighbors': [5003, 5005]},
    5: {'port': 5005, 'neighbors': [5004, 5006]},
    6: {'port': 5006, 'neighbors': [5001, 5005]},
    'Autoridade Certificadora': {'port': 6000, 'neighbors': []}  # A Autoridade Certificadora não tem vizinhos
}

# Iniciar os nós
for node_id, config in nodes.items():
    threading.Thread(target=start_node, args=(node_id, config['port'], config['neighbors'])).start()
