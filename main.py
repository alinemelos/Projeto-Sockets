from socket import socket, AF_INET, SOCK_DGRAM
import threading
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class CertificateAuthority:
    def __init__(self):
        self.public_keys = {}

    def register_node(self, node_id, public_key):
        self.public_keys[node_id] = public_key

    def get_public_key(self, node_id):
        return self.public_keys.get(node_id)

ca = CertificateAuthority()

def handle_request(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(2048)
            req = message.decode()
            print(f"Requisicao recebida de {client_address}")
            print(f"A requisicao foi: {req}")

            if req.startswith("REGISTER"):
                # Formato da mensagem: REGISTER|<node_id>|<public_key>
                _, node_id, public_key_bytes = req.split("|")
                public_key = serialization.load_pem_public_key(public_key_bytes.encode())
                ca.register_node(node_id, public_key)
                rep = "Node registrado na Autoridade Certificadora."
            else:
                rep = "Hey cliente!"

            server_socket.sendto(rep.encode(), client_address)
        except OSError as e:
            print(f"Erro ao lidar com a requisicao: {e}")

def main():
    server_port = 1234
    server_name = 'localhost'

    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((server_name, server_port))
    print("O servidor está pronto para receber")

    thread = threading.Thread(target=handle_request, args=(server_socket,))
    thread.start()

    thread.join()  # Espera a thread terminar antes de fechar o socket

    server_socket.close()

if __name__ == "__main__":
    main()
