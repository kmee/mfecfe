# -*- coding: utf-8 -*-
#
# satcfe/clientelocal.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from satcomum import constantes

from .base import FuncoesSAT
from .base import FuncoesVFPE

from .resposta import RespostaAtivarSAT
from .resposta import RespostaCancelarUltimaVenda
from .resposta import RespostaConsultarNumeroSessao
from .resposta import RespostaConsultarStatusOperacional
from .resposta import RespostaEnviarDadosVenda
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT
from .resposta import RespostaTesteFimAFim


class ClienteSATLocal(FuncoesSAT):
    """Fornece acesso ao equipamento SAT conectado na máquina local.

    As respostas às funções SAT serão trabalhadas resultando em objetos Python
    regulares cujos atributos representam as peças de informação conforme
    descrito, função por função, na ER SAT.
    """

    def __init__(self, *args, **kwargs):
        super(ClienteSATLocal, self).__init__(*args, **kwargs)

    def ativar_sat(self, tipo_certificado, cnpj, codigo_uf):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.ativar_sat`.

        :return: Uma resposta SAT especilizada em ``AtivarSAT``.
        :rtype: satcfe.resposta.ativarsat.RespostaAtivarSAT
        """

        retorno = super(ClienteSATLocal, self).ativar_sat(
            tipo_certificado, cnpj, codigo_uf)
        return RespostaAtivarSAT.analisar(retorno)

    def comunicar_certificado_icpbrasil(self, certificado):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.comunicar_certificado_icpbrasil`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self). \
            comunicar_certificado_icpbrasil(certificado)
        return RespostaSAT.comunicar_certificado_icpbrasil(retorno)

    def enviar_dados_venda(self, dados_venda):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.enviar_dados_venda`.

        :return: Uma resposta SAT especializada em ``EnviarDadosVenda``.
        :rtype: satcfe.resposta.enviardadosvenda.RespostaEnviarDadosVenda
        """
        retorno = super(ClienteSATLocal, self).enviar_dados_venda(dados_venda)
        return RespostaEnviarDadosVenda.analisar(retorno)

    def cancelar_ultima_venda(self, chave_cfe, dados_cancelamento):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.cancelar_ultima_venda`.

        :return: Uma resposta SAT especializada em ``CancelarUltimaVenda``.
        :rtype: satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda
        """
        retorno = super(ClienteSATLocal, self). \
            cancelar_ultima_venda(chave_cfe, dados_cancelamento)
        return RespostaCancelarUltimaVenda.analisar(retorno)

    def consultar_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).consultar_sat()
        return RespostaSAT.consultar_sat(retorno)

    def teste_fim_a_fim(self, dados_venda):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.teste_fim_a_fim`.

        :return: Uma resposta SAT especializada em ``TesteFimAFim``.
        :rtype: satcfe.resposta.testefimafim.RespostaTesteFimAFim
        """
        retorno = super(ClienteSATLocal, self).teste_fim_a_fim(dados_venda)
        return RespostaTesteFimAFim.analisar(retorno)

    def consultar_status_operacional(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_status_operacional`.

        :return: Uma resposta SAT especializada em ``ConsultarStatusOperacional``.
        :rtype: satcfe.resposta.consultarstatusoperacional.RespostaConsultarStatusOperacional
        """
        retorno = super(ClienteSATLocal, self).consultar_status_operacional()
        return RespostaConsultarStatusOperacional.analisar(retorno)

    def consultar_numero_sessao(self, numero_sessao):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_numero_sessao`.

        :return: Uma resposta SAT que irá depender da sessão consultada.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self). \
            consultar_numero_sessao(numero_sessao)
        return RespostaConsultarNumeroSessao.analisar(retorno)

    def configurar_interface_de_rede(self, configuracao):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.configurar_interface_de_rede`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self). \
            configurar_interface_de_rede(configuracao)
        return RespostaSAT.configurar_interface_de_rede(retorno)

    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.associar_assinatura`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self). \
            associar_assinatura(sequencia_cnpj, assinatura_ac)
        # (!) resposta baseada na redação com efeitos até 31-12-2016
        return RespostaSAT.associar_assinatura(retorno)

    def atualizar_software_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.atualizar_software_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).atualizar_software_sat()
        return RespostaSAT.atualizar_software_sat(retorno)

    def extrair_logs(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.extrair_logs`.

        :return: Uma resposta SAT especializada em ``ExtrairLogs``.
        :rtype: satcfe.resposta.extrairlogs.RespostaExtrairLogs
        """
        retorno = super(ClienteSATLocal, self).extrair_logs()
        return RespostaExtrairLogs.analisar(retorno)

    def bloquear_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.bloquear_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).bloquear_sat()
        return RespostaSAT.bloquear_sat(retorno)

    def desbloquear_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.desbloquear_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).desbloquear_sat()
        return RespostaSAT.desbloquear_sat(retorno)

    def trocar_codigo_de_ativacao(self, novo_codigo_ativacao,
                                  opcao=constantes.CODIGO_ATIVACAO_REGULAR,
                                  codigo_emergencia=None):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.trocar_codigo_de_ativacao`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).trocar_codigo_de_ativacao(
            novo_codigo_ativacao, opcao=opcao,
            codigo_emergencia=codigo_emergencia)
        return RespostaSAT.trocar_codigo_de_ativacao(retorno)


class ClienteVfpeLocal(FuncoesVFPE):
    def __init__(self, *args, **kwargs):
        super(ClienteVfpeLocal, self).__init__(*args, **kwargs)

    def verificar_status_validador(self, cpnj, id_fila):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.trocar_codigo_de_ativacao`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resposta = super(ClienteVfpeLocal, self). \
            verificar_status_validador(cpnj, id_fila)
        return RespostaEnviarDadosVenda.analisarVFPE(resposta)


    def enviar_pagamento(self, chave_requisicao, estabecimento, serial_pos,
                         cpnj, icms_base, vr_total_venda,
                         h_multiplos_pagamentos, h_anti_fraude,
                         cod_moeda, origem_pagemento):
        return super(ClienteVfpeLocal, self). \
            enviar_pagamento(chave_requisicao, estabecimento, serial_pos,
                         cpnj, icms_base, vr_total_venda,
                         h_multiplos_pagamentos, h_anti_fraude,
                         cod_moeda, origem_pagemento)

    def enviar_status_pagamento(self, codigo_autorizacao, bin, dono_cartao,
                                data_expiracao, instituicao_financeira, parcelas,
                                codigo_pagamento, valor_pagamento, id_fila,
                                tipo, ultimos_quatro_digitos):
        retorno = super(ClienteVfpeLocal, self). \
            enviar_status_pagamento(codigo_autorizacao,
                                    bin, dono_cartao, data_expiracao,
                                    instituicao_financeira, parcelas,
                                    codigo_pagamento, valor_pagamento,
                                    id_fila, tipo, ultimos_quatro_digitos)

    def recuperar_dados_locais_enviados(self):
        retorno = super(ClienteVfpeLocal, self). \
            recuperar_dados_locais_enviados()

    def enviar_pagamentos_armazenamento_local(self):
        retorno = super(ClienteVfpeLocal, self). \
            enviar_pagamentos_armazenamento_local()

    def resposta_fiscal(self, id_fila, chave_acesso, nsu, numero_aprovacao,
                        bandeira, adquirente, cnpj, impressao_fiscal,
                        numero_documento):
        retorno = super(ClienteVfpeLocal, self). \
            resposta_fiscal(id_fila, chave_acesso, nsu, numero_aprovacao,
                            bandeira, adquirente, cnpj, impressao_fiscal,
                            numero_documento)