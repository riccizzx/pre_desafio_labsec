import hashlib

# ler pdf
with open("./instructions.pdf", "rb") as f:
    pdf = f.read()

matricula = b"25204746" # meu número de matrícula
 
h1 = hashlib.shake_256(pdf).digest(64) # hash do pdf usando shake_256 para gerar 64 bytes de saída
h2 = hashlib.shake_256(matricula).digest(64) # hash da matrícula usando shake_256 para gerar 64 bytes de saída

result = bytes([a ^ b for a, b in zip(h1, h2)]) # operação logica XOR entre os dois hashes para obter o resultado final
result = result.hex()

print("Flag: ",result)