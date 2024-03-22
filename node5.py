import socket
import threading

class PC5:
    def __init__(self):
        self.node_id = 5
        self.neighbors = [4, 6]
        self.private_key = None 
        self.ac_address = ('127.0.0.1', 6000)  # Endereço da Autoridade Certificadora (AC)

    def send_message(self, message):
        # Simula o envio de mensagem para os vizinhos
        for neighbor in self.neighbors:
            print(f"Node {self.node_id} sending message to Node {neighbor}: {message}")

    def start_server(self):
        host = '127.0.0.1'
        port = 5005
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        node_socket.bind((host, port))
        print("PC5 ouvindo na porta 5005")
        while True:
            data, addr = node_socket.recvfrom(1024)
            if addr[1] in self.neighbors or addr == self.ac_address:
                print(f"Mensagem recebida de {addr} no PC5: {data.decode()}")
                # Processar a mensagem, se necessário
            else:
                print(f"Conexão de um nó não autorizado com {addr} no PC5. Ignorando mensagem.")

    def communicate_with_ac(self, message):
        # Implementar comunicação com a AC
        pass

    def main(self):
        # Iniciar servidor para receber mensagens
        threading.Thread(target=self.start_server).start()
        # Enviar mensagens para vizinhos e comunicar com a AC, conforme necessário
        pass

if __name__ == "__main__":
    pc5 = PC5()
    pc5.main()
