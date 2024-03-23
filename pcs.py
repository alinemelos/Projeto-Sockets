from socket import socket, AF_INET, SOCK_DGRAM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def send_request(node_id, port, server_address, public_key):
    client_socket = socket(AF_INET, SOCK_DGRAM)

    # Envia a solicitação apenas uma vez
    message = f"Solicitacao do Node {node_id}"
    client_socket.sendto(message.encode(), server_address)

    # Recebe a resposta do servidor uma vez
    data, _ = client_socket.recvfrom(2048)
    reply = data.decode()
    print(f"Resposta recebida pelo Node {node_id}: {reply}")

    client_socket.close()

def main():
    nodes = {
        'PC1': {'port': 5001, 'public_key': None},
        'PC2': {'port': 5002, 'public_key': None},
        'PC3': {'port': 5003, 'public_key': None},
        'PC4': {'port': 5004, 'public_key': None},
        'PC5': {'port': 5005, 'public_key': None},
        'PC6': {'port': 5006, 'public_key': None},
    }

    # Gerar chaves públicas para os nós
    for node_id, config in nodes.items():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        config['public_key'] = private_key.public_key()

    # Registro dos nós na Autoridade Certificadora
    ac_address = ('localhost', 1234)
    for node_id, config in nodes.items():
        client_socket = socket(AF_INET, SOCK_DGRAM)
        public_key_bytes = config['public_key'].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        register_message = f"REGISTER|{node_id}|{public_key_bytes.decode()}"
        client_socket.sendto(register_message.encode(), ac_address)
        data, _ = client_socket.recvfrom(2048)
        reply = data.decode()
        print(f"Resposta recebida pelo Node {node_id}: {reply}")
        client_socket.close()

    # Envio de mensagens entre os nós
    for node_id, config in nodes.items():
        send_request(node_id, config['port'], ac_address, config['public_key'])

if __name__ == "__main__":
    main()
