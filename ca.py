from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid


one_day = datetime.timedelta(1, 0, 0)
private_key = rsa.generate_private_key( #gera a  chave privada RSA
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key() #extrai a chave publica que corresponde a privada gerada
builder = x509.CertificateBuilder() #construtor de certificados
builder = builder.subject_name(x509.Name([ # define o nome do certificado
    x509.NameAttribute(NameOID.COMMON_NAME, u'openstack-ansible Test CA'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'openstack-ansible'),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'Default CA Deployment'),
]))
builder = builder.issuer_name(x509.Name([ #nome do emissor
    x509.NameAttribute(NameOID.COMMON_NAME, u'openstack-ansible Test CA'),
]))
#pode seguir sem colocar uma data de validação, mas isso representa uma falha de segurança
builder = builder.not_valid_before(datetime.datetime.today() - one_day)
builder = builder.not_valid_after(datetime.datetime(2024, 8, 2))
builder = builder.serial_number(int(uuid.uuid4())) # criando um numero de serie
builder = builder.public_key(public_key) #chave publica
builder = builder.add_extension( #marcando como CA
    x509.BasicConstraints(ca=True, path_length=None), critical=True,
) 
certificate = builder.sign( # Assina o certificado usando a chave privada especificada e o algoritmo de hash SHA256.
    private_key=private_key, algorithm=hashes.SHA256(),
    backend=default_backend()
)
print(isinstance(certificate, x509.Certificate)) #verifica se é uma instância da classe
with open("ca.key", "wb") as f: # escreve a chave gerada
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
    ))
with open("ca.crt", "wb") as f: #escreve o certificado
    f.write(certificate.public_bytes(
        encoding=serialization.Encoding.PEM,
    ))

