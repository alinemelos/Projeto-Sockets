import socket
import threading

class PC6:
    def __init__(self):
        self.node_id = 6
        self.neighbors = [1, 5]
        self.private_key = None 
        self.ac_address = ('127.0.0.1', 6000)  # Endereço da Autoridade Certificadora (AC)

    def send_message(self, message):
        # Simula o envio de mensagem para os vizinhos
        for neighbor in self.neighbors:
            print(f"Node {self.node_id} sending message to Node {neighbor}: {message}")

    def start_server(self):
        host = '127.0.0.1'
        port = 5006
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        node_socket.bind((host, port))
        print("PC6 ouvindo na porta 5006")
        while True:
            data, addr = node_socket.recvfrom(1024)
            if addr[1] in self.neighbors or addr == self.ac_address:
                print(f"Mensagem recebida de {addr} no PC6: {data.decode()}")
                # Processar a mensagem, se necessário
            else:
                print(f"Conexão de um nó não autorizado com {addr} no PC6. Ignorando mensagem.")

    def communicate_with_ac(self, message):
        # Implementar comunicação com a AC
        pass

    def main(self):
        # Iniciar servidor para receber mensagens
        threading.Thread(target=self.start_server).start()
        # Enviar mensagens para vizinhos e comunicar com a AC, conforme necessário
        pass

if __name__ == "__main__":
    pc6 = PC6()
    pc6.main()
