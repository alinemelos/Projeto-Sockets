# Importando os módulos necessários da biblioteca cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pickle
import os

# Definição da classe CertificateAuthority para representar a autoridade certificadora
class CertificateAuthority:
    # Método inicializador da classe
    def __init__(self):
        # Gera uma chave privada RSA de 2048 bits
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    # Método para obter a chave pública da CA
    def get_public_key(self):
        # Retorna a chave pública da CA no formato PEM
        return self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    # Método para assinar uma mensagem usando a chave privada da CA
    def sign_message(self, message):
        # Assina a mensagem usando a chave privada da CA e o algoritmo de hash SHA256
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # Retorna a assinatura gerada
        return signature

# Função principal para execução do código
def main():
    # Instanciação da classe CertificateAuthority para representar a CA
    ca = CertificateAuthority()

    # Salva a chave privada da CA em um arquivo no formato PEM
    with open("ca_private_key.pem", "wb") as f:
        f.write(ca.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Salva a chave pública da CA em um arquivo no formato PEM
    with open("ca_public_key.pem", "wb") as f:
        f.write(ca.get_public_key())

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    # Chama a função principal para iniciar a execução do código
    main()
