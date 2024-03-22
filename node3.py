import socket
import threading

class PC3:
    def __init__(self):
        self.node_id = 3
        self.neighbors = [2, 4]
        self.private_key = None 
        self.ac_address = ('127.0.0.1', 6000)  # Endereço da Autoridade Certificadora (AC)

    def send_message(self, message):
        # Simula o envio de mensagem para os vizinhos
        for neighbor in self.neighbors:
            print(f"Node {self.node_id} sending message to Node {neighbor}: {message}")

    def start_server(self):
        host = '127.0.0.1'
        port = 5003
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        node_socket.bind((host, port))
        print("PC3 ouvindo na porta 5003")
        while True:
            data, addr = node_socket.recvfrom(1024)
            if addr[1] in self.neighbors or addr == self.ac_address:
                print(f"Mensagem recebida de {addr} no PC3: {data.decode()}")
                # Processar a mensagem, se necessário
            else:
                print(f"Conexão de um nó não autorizado com {addr} no PC3. Ignorando mensagem.")

    def communicate_with_ac(self, message):
        # Implementar comunicação com a AC
        pass

    def main(self):
        # Iniciar servidor para receber mensagens
        threading.Thread(target=self.start_server).start()
        # Enviar mensagens para vizinhos e comunicar com a AC, conforme necessário
        pass

if __name__ == "__main__":
    pc3 = PC3()
    pc3.main()
