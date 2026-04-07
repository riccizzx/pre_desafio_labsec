import re
import subprocess
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# definicao dos caminhos dos arquivos e senha do .p12
P12_PATH    = "supervisor.p12"
SENHA_P12   = "693020395"
NUMBER_HEX  = "12594ad17"

subprocess.run(
    [
        "openssl", "pkcs12",
        "-in", P12_PATH,
        "-nomacver",
        "-passin", f"pass:{SENHA_P12}",
        "-nocerts", "-nodes",
        "-out", "/tmp/supervisor_key.pem"
    ],
    capture_output=True
)

with open("/tmp/supervisor_key.pem", "rb") as f:
    pem_data = f.read()

match = re.search(
    b"-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----",
    pem_data, re.DOTALL
)
if not match:
    raise RuntimeError("chave privada não encontrada.")
 
private_key = load_pem_private_key(match.group(0), password=None)
nums = private_key.private_numbers()

# parâmetros RSA
n = nums.public_numbers.n   # módulo (2048 bits)
d = nums.d                  # expoente privado
e = nums.public_numbers.e   # expoente público (65537)

m = int(NUMBER_HEX, 16)   # converte hex → inteiro

# calculando a assinatura RSA manualmente (sem padding)
# formula para abordagem m ^d mod n
sig = pow(m, d, n)
  
# verificação: sig^e mod n deve retornar m
verificacao = pow(sig, e, n)
assert verificacao == m, "ERRO: verificação falhou!"
 
# converter resultado final para hexadecimal e removendo 0x do prefixo
sig_hex = hex(sig)[2:]   # remove o '0x' do prefixo

print(f"Assinatura (hex) :\n  {sig_hex}")
print(f"\nTamanho: {len(sig_hex)} caracteres hex ({len(sig_hex)*4} bits)") 
