#imports
import subprocess
import re
from cryptography import x509
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# definicaco do caminho do arquivo .p12 do supervisor
p12_path = "supervisor.p12"

# usando openssl pkcs12 para extrair o certificado do .p12
# ignorando a ausência de MAC e sem fornecer senha (senha vazia)
subprocess.run([
    "openssl", "pkcs12", "-in", p12_path, "-nomacver",
    "-passin", "pass:", "-nokeys",
    "-out", "/tmp/supervisor_cert.pem"
], capture_output=True)

# 2. Carregar certificado e extrair número de série
# carregando o certificado PEM extraído do .p12
with open("/tmp/supervisor_cert.pem", "rb") as f:
    cert_pem = f.read()

match = re.search(b"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", cert_pem, re.DOTALL)
cert = x509.load_pem_x509_certificate(match.group(0))
serial_decimal = cert.serial_number

# 3. Usar o serial como senha para desbloquear a chave privada
# usando o serial decimal como senha para extrair a chave privada do .p12
subprocess.run([
    "openssl", "pkcs12", "-in", p12_path, "-nomacver",
    "-passin", f"pass:{serial_decimal}", "-nocerts", "-nodes",
    "-out", "/tmp/supervisor_key.pem"
], capture_output=True)

# secao de busca de certificados X.509 dentro do arquivo .p12, lendo o conteúdo binário do .p12 e procurando por estruturas que se assemelhem a certificados X.509 em DER
with open("/tmp/supervisor_key.pem", "rb") as f:
    key_pem = f.read()

match = re.search(b"-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----", key_pem, re.DOTALL)
privkey = load_pem_private_key(match.group(0), password=None)

# com isso temos o serial decimal, que é a senha para desbloquear a chave privada do .p12, e conseguimos extrair tanto o certificado quanto a chave privada usando esse serial como senha. O resultado final é o valor do serial decimal, que é a resposta para o desafio.
print(f"\nResposta: {serial_decimal}")
