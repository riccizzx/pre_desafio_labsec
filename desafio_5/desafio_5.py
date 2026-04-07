
# PRECISO FAZER A EXTRACAO DAS ASSINATURAS DIGITAIS DO PDF, PROCURAR POR CERTIFICADOS X.509
# DENTRO DOS DADOS DE ASSINATURA (PKCS#7) E EXTRAIR OS NUMEROS DE SERIE PARA CONCATENAR COMO RESPOSTA FINAL.
# O DESAFIO É QUE AS ASSINATURAS PODEM ESTAR EM FORMATO PKCS#7, ONDE OS CERTIFICADOS SÃO EMBUTIDOS COMO BLOB BINÁRIO, ENTÃO PRECISO LER ESSE BLOB, PROCURAR POR ESTRUTURAS 
# QUE SE ASSEMELHEM A CERTIFICADOS X.509 EM DER (QUE COMEÇAM COM 0x30 SEQUENCE) E EXTRAIR O NUMERO DE SERIE DE CADA UM PARA CONCAT

# para resolver bastou abrir o arquivo com text-editor para filtrar todas as possiveis serial-keys,
# encontrei os valores hexadecimais dos seriais, converti para decimal e concatenei para obter a resposta final. O processo de extração manual foi mais rápido do que escrever um script para isso, dado o formato complexo dos dados de assinatura PKCS#7. O resultado final é a concatenação dos números de série em decimal, que é a resposta para o desafio.
