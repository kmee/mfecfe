# -*- coding: utf-8 -*-
import satcfe

from mfecfe import BibliotecaSAT
from mfecfe import ClienteSATLocal
from mfecfe import ClienteVfpeLocal

cliente = ClienteSATLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   codigo_ativacao='12345678'
)

resposta = cliente.consultar_sat()
resposta = cliente.consultar_numero_sessao('999999')
resposta = cliente.extrair_logs()
resposta = cliente.consultar_status_operacional()

XML_CFE_VENDA = """<?xml version="1.0" ?>
<CFe>
 <infCFe versaoDadosEnt="0.07">
 <ide>
 <CNPJ>16716114000172</CNPJ>
 <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
 <numeroCaixa>002</numeroCaixa>
 </ide>
 <emit>
 <CNPJ>08723218000186</CNPJ>
 <IE>562377111111</IE>
 <indRatISSQN>N</indRatISSQN>
 </emit>
 <dest/>
 <det nItem="1">
 <prod>
 <cProd>E-COM11</cProd>
 <xProd>Mouse, Optical</xProd>
 <NCM>84716053</NCM>
 <CFOP>5101</CFOP>
 <uCom>unid</uCom>
 <qCom>1.0000</qCom>
 <vUnCom>123.00</vUnCom>
 <indRegra>A</indRegra>
 </prod>
 <imposto>
 <vItem12741>18.56</vItem12741>
 <ICMS>
 <ICMSSN102>
 <Orig>0</Orig>
 <CSOSN>500</CSOSN>
 </ICMSSN102>
 </ICMS>
 <PIS>
 <PISSN>
 <CST>49</CST>
 </PISSN>
 </PIS>
 <COFINS>
 <COFINSSN>
 <CST>49</CST>
 </COFINSSN>
 </COFINS>
 </imposto>
 </det>
 <total>
 <vCFeLei12741>18.56</vCFeLei12741>
 </total>
 <pgto>
 <MP>
 <cMP>01</cMP>
 <vMP>123.00</vMP>
 </MP>
 </pgto>
 </infCFe>
</CFe>
"""


XML_CFE_CANCELAMENTO = """<?xml version="1.0" encoding="UTF-8"?>
<CFeCanc>
  <infCFe chCanc="CFe35150908723218000186599000040190000360539948">
    <ide>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <numeroCaixa>002</numeroCaixa>
    </ide>
    <emit/>
    <dest/>
    <total/>
    <infAdic/>
  </infCFe>
</CFeCanc>
"""


resposta = cliente.enviar_dados_venda(XML_CFE_VENDA)

# resposta = cliente.cancelar_ultima_venda(
#    'CFe35150908723218000186599000040190000360539948',
#    XML_CFE_CANCELAMENTO
# )


# TESTES INATIVOS
# resposta = cliente.associar_assinatura('99999', '99999')
# resposta = cliente.ativar_sat('satcomum.constantes.CERTIFICADO_ACSAT_SEFAZ', '11111111111111', '35')
# resposta = cliente.atualizar_software_sat()
# resposta = cliente.bloquear_sat()
# resposta = cliente.teste_fim_a_fim(u'CFeVenda')
# resposta = cliente.desbloquear_sat()
# resposta = cliente.configurar_interface_de_rede('tipoInter:')
# resposta = cliente.comunicar_certificado_icpbrasil('')


cliente2 = ClienteVfpeLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   chave_acesso_validador = '123456789'
)

resposta = cliente2.verificar_status_validador('1','1')
resposta = cliente2.enviar_pagamento('1','2','3','4','5','6','7','8','9','10',
                                      '11', '12','13','14','15')
resposta = cliente2.enviar_pagamentos_armazenamento_local()
resposta = cliente2.resposta_fiscal('1', '2', '3', '4', '5', '6', '7', '8', '9')


resposta = cliente2.enviar_status_pagamento('1','1','1','11/11/11','1','1',
                                            '1','1','1','1','1111')
print resposta

resposta = cliente2.recuperar_dados_locais_enviados()
print resposta