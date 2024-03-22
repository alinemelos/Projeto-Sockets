import socket
import threading
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid

class Node:
    def __init__(self, node_id, neighbors):
        self.node_id = node_id
        self.neighbors = neighbors
        self.private_key= None

    def send_message(self, message, dest_address):
        # Simula o envio de mensagem para o destinatário
        self.node_socket.sendto(message.encode(), dest_address)

    def receive_message(self):
        # Função para receber mensagens
        while True:
            data, addr = self.node_socket.recvfrom(1024)
            print(f"Mensagem recebida por Node {self.node_id} de {addr}: {data.decode()}")

class AutoridadeCertificadora:
    def __init__(self):
        self.registered_nodes = {}  # Dicionário para armazenar os nós registrados

    def register_node(self, node_id):
        """
        Registra um nó na Autoridade Certificadora.
        """
        if node_id not in self.registered_nodes:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            self.registered_nodes[node_id] = public_key
            print(f"Node {node_id} registrado com sucesso.")
            return private_key
        else:
            print(f"Node {node_id} já está registrado.")
            return None

    def get_public_key(self, node_id):
        """
        Retorna a chave pública do nó registrado.
        """
        return self.registered_nodes.get(node_id)

    def generate_certificate(self, node_id):
        """
        Gera um certificado para o nó registrado.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        validity_period = datetime.timedelta(days=365)  # Um ano de validade

        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, f"Node {node_id}"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "openstack-ansible"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Default CA Deployment"),
        ]))
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, "openstack-ansible Test CA"),
        ]))
        builder = builder.serial_number(int(uuid.uuid4()))
        builder = builder.public_key(public_key)
        builder = builder.not_valid_before(datetime.datetime.utcnow())
        builder = builder.not_valid_after(datetime.datetime.utcnow() + validity_period)
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        certificate = builder.sign(
            private_key=private_key, algorithm=hashes.SHA256(),
            backend=default_backend()
        )

        #with open(f"node_{node_id}_cert.pem", "wb") as f:
         #   f.write(certificate.public_bytes(serialization.Encoding.PEM))
          #  print(f"Certificado para Node {node_id} gerado e salvo como node_{node_id}_cert.pem")

# Criando uma instância da Autoridade Certificadora
ac = AutoridadeCertificadora()

# Definindo os nós (PCs) da topologia
nodes = {
    1: {'neighbors': [2, 6], 'address': ('127.0.0.1', 5001)},
    2: {'neighbors': [1, 3], 'address': ('127.0.0.1', 5002)},
    3: {'neighbors': [2, 4], 'address': ('127.0.0.1', 5003)},
    4: {'neighbors': [3, 5], 'address': ('127.0.0.1', 5004)},
    5: {'neighbors': [4, 6], 'address': ('127.0.0.1', 5005)},
    6: {'neighbors': [1, 5], 'address': ('127.0.0.1', 5006)},
}

# Registrando os nós (PCs) na AC e gerando certificados
for node_id, node_info in nodes.items():
    private_key = ac.register_node(node_id)
    ac.generate_certificate(node_id)
    node_info['private_key'] = private_key

# Verificando os nós registrados
print("Nodes registrados na Autoridade Certificadora:")
for node_id in ac.registered_nodes:
    print(f"Node {node_id}")

# Simulando a comunicação entre os nós
for node_id, node_info in nodes.items():
    message = f"Hello from Node {node_id}!"
    for neighbor_id in node_info['neighbors']:
        neighbor_address = nodes[neighbor_id]['address']
        threading.Thread(target=node_info['private_key'].send_message, args=(message, neighbor_address)).start()

# Simulando a comunicação com a Autoridade Certificadora (AC)
ac_message = "Hello from Autoridade Certificadora!"
for node_id, node_info in nodes.items():
    threading.Thread(target=node_info['private_key'].send_message, args=(ac_message, ('127.0.0.1', 6000))).start()

# Verificar se a CA está guardando as chaves públicas corretamente
for node_id in nodes:
    public_key = ac.get_public_key(node_id)
    if public_key:
        print(f"Chave pública para Node {node_id}: {public_key}")
    else:
        print(f"Nenhuma chave pública encontrada para Node {node_id}.")
