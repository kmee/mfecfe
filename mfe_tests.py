# -*- coding: utf-8 -*-
from mfecfe import BibliotecaSAT
from mfecfe import ClienteSATLocal

cliente = ClienteSATLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   codigo_ativacao='12345678'
)

resposta = cliente.consultar_sat()
print (resposta)

resposta = cliente.consultar_numero_sessao('99999')
print (resposta)

resposta = cliente.associar_assinatura('99999', '99999')
print (resposta)

resposta = cliente.ativar_sat('satcomum.constantes.CERTIFICADO_ACSAT_SEFAZ', '11111111111111', '35')
print (resposta)

resposta = cliente.atualizar_software_sat()
print (resposta)

resposta = cliente.bloquear_sat()
print (resposta)

resposta = cliente.extrair_logs()
print (resposta)

# resposta = cliente.teste_fim_a_fim(identificador)
# print (resposta)

# resposta = cliente.enviar_dados_venda(identificador, )
# print (resposta)

resposta = cliente.desbloquear_sat()
print (resposta)

# resposta = cliente.consultar_status_operacional(identificador)
# print (resposta)

