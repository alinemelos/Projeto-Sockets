from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import datetime
import uuid

class AutoridadeCertificadora:
    def __init__(self):
        self.registered_nodes = {}  # Dicionário para armazenar os nós registrados
        self.dh_parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

    def register_node(self, node_id):
        """
        Registra um nó na Autoridade Certificadora.
        """
        if node_id not in self.registered_nodes:
            # Gera a chave privada e pública para o DH
            private_key = self.dh_parameters.generate_private_key()
            public_key = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            self.registered_nodes[node_id] = {"public_key": public_key, "dh_private_key": private_key}
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
    
    def generate_shared_secret(self, node_id):
        """
        Gera o segredo compartilhado entre a AC e o nó.
        """
        dh_private_key = self.registered_nodes[node_id]["dh_private_key"]
        public_key_bytes = self.registered_nodes[node_id]["public_key"]
        public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
        shared_key = dh_private_key.exchange(public_key)
        return shared_key

    def encrypt_private_key(self, node_id, private_key):
        """
        Criptografa a chave privada do nó com o segredo compartilhado.
        """
        shared_secret = self.generate_shared_secret(node_id)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_secret)
        cipher = AESGCM(derived_key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        return nonce, ciphertext
    
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
      