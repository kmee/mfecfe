# -*- coding: utf-8 -*-
from mfecfe import BibliotecaSAT
from mfecfe import ClienteSATLocal
from mfecfe import base

cliente = ClienteSATLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   codigo_ativacao='12345678'
)

# cliente2 = FuncoesSAT(
#     BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
#     codigo_ativacao='12345678'
# )

identificador = '99999'
resposta = cliente.consultar_sat(identificador)
print (resposta)

resposta = cliente.consultar_numero_sessao(identificador, '99999')
print (resposta)


resposta = cliente.associar_assinatura(identificador, '99999', '99999')
print (resposta)

resposta = cliente.ativar_sat(identificador, 'satcomum.constantes.CERTIFICADO_ACSAT_SEFAZ', '11111111111111', '35')
print (resposta)

resposta = cliente.atualizar_software_sat(identificador)
print (resposta)

resposta = cliente.bloquear_sat(identificador)
print (resposta)
