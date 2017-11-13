# -*- coding: utf-8 -*-
import satcfe

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

resposta = cliente.teste_fim_a_fim(u'CFeVenda')
print (resposta)

resposta = cliente.enviar_dados_venda(u'CFeVenda')
print (resposta)

resposta = cliente.desbloquear_sat()
print (resposta)

resposta = cliente.consultar_status_operacional()
print (resposta)

resposta = cliente.consultar_sat()
print resposta

resposta = cliente.configurar_interface_de_rede('tipoInter:')
print resposta

resposta = cliente.cancelar_ultima_venda('CFe11087746478373757726265545868587463856478463', 'segundo')
print resposta

# resposta = cliente.comunicar_certificado_icpbrasil('')
# print resposta

