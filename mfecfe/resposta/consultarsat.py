# -*- coding: utf-8 -*-
#
# satcfe/resposta/ativarsat.py
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

import base64

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from .padrao import RespostaSAT
from .padrao import analisar_retorno


STATUS_OK = '08000'


class RespostaConsultarSAT(RespostaSAT):

    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaConsultarSAT` a partir do retorno
        informado.

        :param unicode retorno: Retorno da função ``ConsultarSAT``.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ConsultarSAT',
                classe_resposta=RespostaConsultarSAT,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', unicode),
                        ('mensagem', unicode),
                        ('cod', unicode),
                        ('mensagemSEFAZ', unicode),
                        ('id_fila', unicode),
                    ),
                campos_alternativos=[
                        # se a ativação falhar espera-se o padrão de campos
                        # no retorno...
                        RespostaSAT.CAMPOS,
                        ('id_fila', unicode),
                    ]
            )
        if resposta.EEEEE != STATUS_OK:
            raise ExcecaoRespostaSAT(resposta)
        return resposta
