from socket import socket, AF_INET, SOCK_DGRAM
import threading
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Definição da classe CertificateAuthority para representar a autoridade certificadora
class CertificateAuthority:
    def __init__(self):
        # Dicionário para armazenar as chaves públicas dos nós registrados
        self.public_keys = {}

    # Método para registrar um nó na autoridade certificadora
    def register_node(self, node_id, public_key):
        self.public_keys[node_id] = public_key

    # Método para obter a chave pública de um nó
    def get_public_key(self, node_id):
        return self.public_keys.get(node_id)

# Instanciação da autoridade certificadora
ca = CertificateAuthority()

# Função para lidar com as requisições recebidas pelo servidor
def handle_request(server_socket):
    while True:
        try:
            # Recebe a mensagem e o endereço do cliente que enviou a mensagem
            message, client_address = server_socket.recvfrom(2048)
            req = message.decode()
            print(f"Requisicao recebida de {client_address}")
            print(f"A requisicao foi: {req}")

            # Verifica se a requisição é para registrar um nó na autoridade certificadora
            if req.startswith("REGISTER"):
                # Formato da mensagem: REGISTER|<node_id>|<public_key>
                _, node_id, public_key_bytes = req.split("|")
                # Carrega a chave pública do nó a partir dos bytes recebidos
                public_key = serialization.load_pem_public_key(public_key_bytes.encode())
                # Registra o nó na autoridade certificadora
                ca.register_node(node_id, public_key)
                # Responde ao cliente confirmando o registro
                rep = "Node registrado na Autoridade Certificadora."
            else:
                # Responde ao cliente com uma mensagem genérica
                rep = "Hey cliente!"

            # Envia a resposta de volta para o cliente
            server_socket.sendto(rep.encode(), client_address)
        except OSError as e:
            print(f"Erro ao lidar com a requisicao: {e}")

# Função principal para executar o servidor
def main():
    server_port = 1234
    server_name = 'localhost'

    # Cria um socket UDP e o associa ao endereço e porta do servidor
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((server_name, server_port))
    print("O servidor está pronto para receber")

    # Cria uma thread para lidar com as requisições recebidas
    thread = threading.Thread(target=handle_request, args=(server_socket,))
    thread.start()

    # Aguarda a thread terminar antes de fechar o socket
    thread.join()

    # Fecha o socket do servidor
    server_socket.close()

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    # Chama a função principal para iniciar o servidor
    main()
