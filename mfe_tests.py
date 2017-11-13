from mfecfe import BibliotecaSAT
from mfecfe import ClienteSATLocal

cliente = ClienteSATLocal(
    BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
    codigo_ativacao='12345678'
)

identificador = '99999'
resposta = cliente.consultar_sat(identificador)

print resposta