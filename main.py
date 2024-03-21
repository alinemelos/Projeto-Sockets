from ca import AutoridadeCertificadora  # Importa a classe AutoridadeCertificadora do arquivo ca.py

class Node:
    def __init__(self, node_id, neighbors):
        self.node_id = node_id
        self.neighbors = neighbors
        self.private_key = None

    def send_message(self, message):
        # Simula o envio de mensagem para os vizinhos
        for neighbor in self.neighbors:
            print(f"Node {self.node_id} sending message to Node {neighbor}: {message}")

    def store_private_key(self, private_key):
        """
        Armazena a chave privada associada a este nó.
        """
        self.private_key = private_key

# Criando uma instância da Autoridade Certificadora
ac = AutoridadeCertificadora()

# Definindo os nós (PCs) da topologia
nodes = {
    1: Node(node_id=1, neighbors=[2, 6]),
    2: Node(node_id=2, neighbors=[1, 3]),
    3: Node(node_id=3, neighbors=[2, 4]),
    4: Node(node_id=4, neighbors=[3, 5]),
    5: Node(node_id=5, neighbors=[4, 6]),
    6: Node(node_id=6, neighbors=[1, 5]),
}

# Registrando os nós (PCs) na AC e gerando certificados
for node_id in nodes:
    private_key = ac.register_node(node_id)
    if private_key:
        nodes[node_id].store_private_key(private_key)
    ac.generate_certificate(node_id)

# Verificando os nós registrados
print("Nodes registrados na Autoridade Certificadora:")
for node_id in ac.registered_nodes:
    print(f"Node {node_id}")

# Simulando a comunicação entre os nós
for node_id, node in nodes.items():
    message = f"Hello from Node {node_id}!"
    node.send_message(message)

# Simulando a comunicação com a Autoridade Certificadora (AC)
ac_message = "Hello from Autoridade Certificadora!"
print(f"AC sending message: {ac_message}")

for node_id in nodes:
    public_key = ac.get_public_key(node_id)
    if public_key:
        print(f"Chave pública para Node {node_id}: {public_key}")
    else:
        print(f"Nenhuma chave pública encontrada para Node {node_id}.")
