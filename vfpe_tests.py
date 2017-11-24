import uuid

import time

from mfecfe import ClienteVfpeLocal
from mfecfe import BibliotecaSAT

cliente = ClienteVfpeLocal(
   BibliotecaSAT('/opt/Integrador'), # Caminho do Integrador
   chave_acesso_validador = '25CFE38D-3B92-46C0-91CA-CFF751A82D3D'
)

resposta = cliente.enviar_pagamento(
                                    '26359854-5698-1365-9856-965478231456', # chave_requisicao
                                    '10', # estabecimento
                                    'TEF', # serial_pos
                                    '82373077000171', # cpnj
                                    '0.23', # icms_base
                                    '1530', # vr_total_venda
                                    '1674068', # id_fila_validador
                                    True, # h_multiplos_pagamentos
                                    False, # h_anti_fraude
                                    'BRL', # cod_moeda
                                    # '127.0.0.1', # endereco_ip
                                    'Mesa 1234', # origem_pagemento
                                    False, # cupom_nfce
                                    )
resposta = cliente.verificar_status_validador('82373077000171', '261833')
print (resposta.CodigoAutorizacao)
print (resposta.Bin)
print (resposta.DonoCartao)
print (resposta.DataExpiracao)
print (resposta.InstituicaoFinanceira)
print (resposta.Parcelas)
print (resposta.UltimosQuatroDigitos)
print (resposta.CodigoPagamento)
print (resposta.ValorPagamento)
print (resposta.IdFila)
print (resposta.Tipo)