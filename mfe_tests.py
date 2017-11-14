# -*- coding: utf-8 -*-
import satcfe

from mfecfe import BibliotecaSAT
from mfecfe import ClienteSATLocal
from mfecfe import ClienteVfpeLocal

cliente = ClienteSATLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   codigo_ativacao='12345678'
)

# resposta = cliente.consultar_sat()
# print (resposta)
#
# resposta = cliente.consultar_numero_sessao('99999')
# print (resposta)
#
# resposta = cliente.extrair_logs()
# print (resposta)
#
# resposta = cliente.consultar_status_operacional()
# print (resposta)

XML_CFE_VENDA = """<?xml version="1.0"?>
<CFe>
  <infCFe versaoDadosEnt="0.06">
    <ide>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <numeroCaixa>002</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>08723218000186</CNPJ>
      <IE>149626224113</IE>
      <IM>123123</IM>
      <cRegTribISSQN>3</cRegTribISSQN>
      <indRatISSQN>N</indRatISSQN>
    </emit>
    <dest/>
    <det nItem="1">
      <prod>
        <cProd>7894321722016</cProd>
        <xProd>TODDYNHO 200 ML</xProd>
        <CFOP>5102</CFOP>
        <uCom>UN</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>2.00</vUnCom>
        <indRegra>A</indRegra>
      </prod>
      <imposto>
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
    <total/>
    <pgto>
      <MP>
        <cMP>01</cMP>
        <vMP>2.00</vMP>
      </MP>
    </pgto>
    <infAdic>
      <infCpl>Valores aproximados dos tributos:
Fed R$   0,23 / Est R$   0,36
Fonte: IBPT (9oi3aC)
 Balcao: Venda Balcao
 TK: 100296906  SS: 100001680  VND: PATRI  OP
</infCpl>
    </infAdic>
  </infCFe>
</CFe>
"""

resposta = cliente.enviar_dados_venda(XML_CFE_VENDA)


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

resposta = cliente.cancelar_ultima_venda(
   'CFe35150908723218000186599000040190000360539948',
   XML_CFE_CANCELAMENTO
)

# resposta = cliente.associar_assinatura('99999', '99999')
# print (resposta)
#
# resposta = cliente.ativar_sat('satcomum.constantes.CERTIFICADO_ACSAT_SEFAZ', '11111111111111', '35')
# print (resposta)
#
# resposta = cliente.atualizar_software_sat()
# print (resposta)
#
# resposta = cliente.bloquear_sat()
# print (resposta)
#
# resposta = cliente.teste_fim_a_fim(u'CFeVenda')
# print (resposta)
#
# resposta = cliente.enviar_dados_venda(u'CFeVenda')
# print (resposta)
#
# resposta = cliente.desbloquear_sat()
# print (resposta)
#
# resposta = cliente.configurar_interface_de_rede('tipoInter:')
# print resposta

# resposta = cliente.cancelar_ultima_venda('CFe11087746478373757726265545868587463856478463', 'segundo')
# print resposta

# resposta = cliente.comunicar_certificado_icpbrasil('')
# print resposta

cliente2 = ClienteVfpeLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   chave_acesso_validador = '123456789'
)

resposta = cliente2.verificar_status_validador('1','1')
print resposta

resposta = cliente2.enviar_pagamento('1','1','1','1','1','1','1','1','1','1',
                                     '1', '1','1','1','1')
print resposta


