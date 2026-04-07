#!/usr/bin/env python3
"""
Desafio 2 - O Desleixo do Assalariado
Descriptografia RSA com certificado PKCS#12
"""

import os
import subprocess
import re
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Caminhos
script_dir = os.path.dirname(os.path.abspath(__file__))
p12_path = os.path.join(script_dir, "employee.p12")
enc_path = os.path.join(script_dir, "access_code.enc")
password = "AVoiceFromBeyondTheGrave-1352463911"

# 1. Extrair chave privada RSA do certificado PKCS#12
subprocess.run([
    "openssl", "pkcs12", "-in", p12_path, "-nomacver",
    "-passin", f"pass:{password}", "-nocerts", "-nodes",
    "-out", "/tmp/key.pem"
], capture_output=True)

# 2. Carregar a chave privada
with open("/tmp/key.pem", "rb") as f:
    pem_data = f.read()

match = re.search(b"-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----", pem_data, re.DOTALL)
private_key = load_pem_private_key(match.group(0), password=None)

# 3. Descriptografar access_code.enc
with open(enc_path, "rb") as f:
    ciphertext = f.read()

plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 4. Extrar e exibir o código de acesso
texto = plaintext.decode("utf-8")
codigo = re.search(r"\d+", texto).group()

print(f"Plaintext: {texto}")
print(f"ACCESS CODE: {codigo}")
