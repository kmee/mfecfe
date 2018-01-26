# -*- coding: utf-8 -*-
#
# satcfe/base.py
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

import collections
import ctypes
import os
import random
import time
import xmltodict

from ctypes import c_int
from ctypes import c_char_p

from satcomum import constantes
from xml import render_xml, sanitize_response
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MonitorIntegrador(PatternMatchingEventHandler):
    patterns = ["*.xml"]

    def __init__(self, observer):
        super(MonitorIntegrador, self).__init__()
        self.observer = observer

    def process(self, event):
        """ Realiza o processamento dos arquivos criados e modificados dentro da pasta de output do integrador

        E ao ler o arquivo notifica o observador do numero identificador do arquivo e seu caminho.

        :param event:
                event_type = None

                    The type of the event as a string.

                is_directory = False

                    True if event was emitted for a directory; False otherwise.

                src_path[source]

                    Source path of the file system object that triggered this event.

        :return:
        """
        with open(event.src_path, 'r') as xml_source:
            xml_string = xml_source.read()
            parsed = xmltodict.parse(xml_string)
            self.observer.src_path = event.src_path
            self.observer.resposta = \
                parsed.get('Integrador', {}).get('Resposta', {}).get('retorno') or \
                parsed.get('Integrador', {}).get('Resposta', {}).get('IdPagamento') or \
                parsed.get('Integrador', {}).get('Resposta', {})
            if not isinstance(self.observer.resposta, dict):
                self.observer.resposta += '|' + parsed.get('Integrador', {}).get('Identificador', {}).get('Valor')
            self.observer.numero_identificador = parsed.get('Integrador', {}).get('Identificador', {}).get('Valor')

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


class _Prototype(object):
    def __init__(self, argtypes, restype=c_char_p):
        self.argtypes = argtypes
        self.restype = restype


FUNCTION_PROTOTYPES = dict(
        AtivarSAT=_Prototype([c_int, c_int, c_char_p, c_char_p, c_int]),
        ComunicarCertificadoICPBRASIL=_Prototype([c_int, c_char_p, c_char_p]),
        EnviarDadosVenda=_Prototype([c_int, c_char_p, c_char_p]),
        CancelarUltimaVenda=_Prototype([c_int, c_char_p, c_char_p, c_char_p]),
        ConsultarSAT=_Prototype([c_int,]),
        TesteFimAFim=_Prototype([c_int, c_char_p, c_char_p]),
        ConsultarStatusOperacional=_Prototype([c_int, c_char_p]),
        ConsultarNumeroSessao=_Prototype([c_int, c_char_p, c_int]),
        ConfigurarInterfaceDeRede=_Prototype([c_int, c_char_p, c_char_p]),
        AssociarAssinatura=_Prototype([c_int, c_char_p, c_char_p, c_char_p]),
        AtualizarSoftwareSAT=_Prototype([c_int, c_char_p]),
        ExtrairLogs=_Prototype([c_int, c_char_p]),
        BloquearSAT=_Prototype([c_int, c_char_p]),
        DesbloquearSAT=_Prototype([c_int, c_char_p]),
        TrocarCodigoDeAtivacao=_Prototype([c_int, c_char_p, c_int, c_char_p, c_char_p])
    )


class BibliotecaSAT(object):
    """Configura a localização da biblioteca que efetivamente acessará o
    equipamento SAT. A biblioteca deverá ser uma DLL (*dynamic linked library*,
    em sistemas Microsoft Windows) ou uma *shared library* em sistemas baseados
    no UNIX ou GNU/Linux.

    :param string caminho: Caminho completo para a biblioteca SAT.

    :param integer convencao: Opcional. Indica a convenção de chamada da
        biblioteca, devendo ser uma das constantes definidas em
        :attr:`~satcomum.constantes.CONVENCOES_CHAMADA`. Se não for informado,
        a convenção de chamada será decidida conforme a extensão do nome do
        arquivo, assumindo :attr:`~satcomum.constantes.WINDOWS_STDCALL` para as
        extensões ``.DLL`` ou ``.dll``. Quaisquer outras extensões, assume a
        convenção de chamada :attr:`~satcomum.constantes.STANDARD_C`.

    """

    def __init__(self, caminho, convencao=None):
        self._libsat = None
        self._caminho = self.limpa_formatacao_caminho_integrador(caminho)
        self._convencao = convencao

    @property
    def ref(self):
        """Uma referência para a biblioteca SAT carregada."""
        return self._libsat


    @property
    def caminho(self):
        """Caminho completo para a biblioteca SAT."""
        return self._caminho


    @property
    def convencao(self):
        """Convenção de chamada para a biblioteca SAT. Deverá ser um dos valores
        disponíveis na contante :attr:`~satcomum.constantes.CONVENCOES_CHAMADA`.
        """
        return self._convencao

    def limpa_formatacao_caminho_integrador(self, caminho):
        if caminho[0] != '/':
            caminho = '/' + caminho
        if caminho[len(caminho)-1] != '/':
            caminho = caminho + '/'

        return caminho.replace('\\', '/')


class NumeroSessaoMemoria(object):
    """Implementa um numerador de sessão simples, baseado em memória, não
    persistente, que irá gerar um número de sessão (seis dígitos) diferente
    entre os ``n`` últimos números de sessão gerados. Conforme a ER SAT, um
    número de sessão não poderá ser igual aos últimos ``100`` números.

    .. sourcecode:: python

        >>> numerador = NumeroSessaoMemoria(tamanho=5)
        >>> n1 = numerador()
        >>> 100000 <= n1 <= 999999
        True
        >>> n1 in numerador
        True
        >>> n2 = numerador()
        >>> n3 = numerador()
        >>> n4 = numerador()
        >>> n5 = numerador()
        >>> len(set([n1, n2, n3, n4, n5]))
        5
        >>> n6 = numerador()
        >>> n1 in numerador
        False

    """

    def __init__(self, tamanho=100):
        super(NumeroSessaoMemoria, self).__init__()
        self._tamanho = tamanho
        self._memoria = collections.deque(maxlen=tamanho)


    def __contains__(self, item):
        return item in self._memoria


    def __call__(self, *args, **kwargs):
        while True:
            numero = random.randint(100000, 999999)
            if numero not in self._memoria:
                self._memoria.append(numero)
                break
        return numero


class FuncoesSAT(object):
    """Estabelece a interface básica para acesso às funções da biblioteca SAT.

    A intenção é que esta classe seja a base para classes mais especializadas
    capazes de trabalhar as respostas, resultando em objetos mais úteis, já que
    os métodos desta classe invocam as funções da biblioteca SAT e retornam o
    resultado *verbatim*.

    As funções implementadas estão descritas na ER SAT, item 6.1.

    +---------+-----------------------------------+-----------------------------------------+
    | Item ER | Função                            | Método                                  |
    +=========+===================================+=========================================+
    | 6.1.1   | ``AtivarSAT``                     | :meth:`ativar_sat`                      |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.2   | ``ComunicarCertificadoICPBRASIL`` | :meth:`comunicar_certificado_icpbrasil` |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.3   | ``EnviarDadosVenda``              | :meth:`enviar_dados_venda`              |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.4   | ``CancelarUltimaVenda``           | :meth:`cancelar_ultima_venda`           |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.5   | ``ConsultarSAT``                  | :meth:`consultar_sat`                   |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.6   | ``TesteFimAFim``                  | :meth:`teste_fim_a_fim`                 |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.7   | ``ConsultarStatusOperacional``    | :meth:`consultar_status_operacional`    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.8   | ``ConsultarNumeroSessao``         | :meth:`consultar_numero_sessao`         |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.9   | ``ConfigurarInterfaceDeRede``     | :meth:`configurar_interface_de_rede`    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.10  | ``AssociarAssinatura``            | :meth:`associar_assinatura`             |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.11  | ``AtualizarSoftwareSAT``          | :meth:`atualizar_software_sat`          |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.12  | ``ExtrairLogs``                   | :meth:`extrair_logs`                    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.13  | ``BloquearSAT``                   | :meth:`bloquear_sat`                    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.14  | ``DesbloquearSAT``                | :meth:`desbloquear_sat`                 |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.15  | ``TrocarCodigoDeAtivacao``        | :meth:`trocar_codigo_de_ativacao`       |
    +---------+-----------------------------------+-----------------------------------------+

    :param biblioteca: Uma instância de :class:`BibliotecaSAT`.

    :param string codigo_ativacao: Código de ativação. Senha definida pelo
        contribuinte no software de ativação, conforme item 2.1.1 da ER SAT.

    :param numerador_sessao: Opcional. Um ``callable`` capaz de gerar um
        número de sessão conforme descrito no item 6, alínea "a", "Funções do
        Equipamento SAT", da ER SAT. Se não for especificado, será utilizado
        um :class:`NumeroSessaoMemoria`.

    """

    def __init__(self, biblioteca, codigo_ativacao=None, numerador_sessao=None):
        self._biblioteca = biblioteca
        self._codigo_ativacao = codigo_ativacao
        self._numerador_sessao = numerador_sessao or NumeroSessaoMemoria()
        self._path = os.path.join(os.path.dirname(__file__), 'templates')


    @property
    def biblioteca(self):
        return self._biblioteca


    @property
    def codigo_ativacao(self):
        return self._codigo_ativacao


    def gerar_numero_sessao(self):
        """Gera o número de sessão para a próxima invocação de função SAT."""
        return self._numerador_sessao()

    def __getattr__(self, name):
        if name.startswith('invocar__'):
            metodo_sat = name.replace('invocar__', '')
            proto = FUNCTION_PROTOTYPES[metodo_sat]
            fptr = getattr(self._biblioteca.ref, metodo_sat)
            fptr.argtypes = proto.argtypes
            fptr.restype = proto.restype
            return fptr
        raise AttributeError('{!r} object has no attribute {!r}'.format(
                self.__class__.__name__, name))

    def comando_sat(self, template, **kwargs):
        if kwargs['consulta']['numero_identificador'] != 'False':
            numero_identificador = kwargs.get(
                'numero_sessao',
                kwargs['consulta']['numero_identificador'],
            )
        else:
            numero_identificador = kwargs.get(
                'numero_sessao',
                self.gerar_numero_sessao(),
            )

        kwargs['numero_identificador'] = numero_identificador
        path_file = self.biblioteca.caminho+'input/' + str(numero_identificador) + '-' + template.lower()
        # remove arquivo se ele existir
        if os.path.isfile(path_file):
            os.remove(path_file)

        observer = Observer()
        observer.numero_identificador = False
        observer.src_path = False
        observer.schedule(MonitorIntegrador(observer), path=self.biblioteca.caminho+'output')
        observer.start()

        xml = render_xml(self._path, template, True, **kwargs)
        xml.write(
            path_file,
            xml_declaration=True,
            encoding='UTF-8'
        )

        cont_time = 0
        while True:
            # Analisa a pasta a cada um segundo.
            # entra10 vezes e sai da verificacao
            time.sleep(1)
            cont_time = cont_time + 1
            if (str(numero_identificador) == str(observer.numero_identificador) and \
                observer.src_path):
                # Ao encontrar um arquivo de retorno com o mesmo numero identificador da remessa sai do loop.
                break
            if  cont_time == 10:
                observer.resposta = str(numero_identificador)+'|'+str(numero_identificador)+'|'+'0'+'|'+'Erro interno'+'|'+'0'+'|'+'ERRO'
                # Ao nao encontrar um arquivo de retorno com o mesmo numero identificador
                break
        observer.stop()
        observer.join()
        return observer.resposta


    def ativar_sat(self, tipo_certificado, cnpj, codigo_uf):
        """Função ``AtivarSAT`` conforme ER SAT, item 6.1.1.
        Ativação do equipamento SAT. Dependendo do tipo do certificado, o
        procedimento de ativação é complementado enviando-se o certificado
        emitido pela ICP-Brasil (:meth:`comunicar_certificado_icpbrasil`).

        :param int tipo_certificado: Deverá ser um dos valores
            :attr:`satcomum.constantes.CERTIFICADO_ACSAT_SEFAZ`,
            :attr:`satcomum.constantes.CERTIFICADO_ICPBRASIL` ou
            :attr:`satcomum.constantes.CERTIFICADO_ICPBRASIL_RENOVACAO`, mas
            nenhuma validação será realizada antes que a função de ativação
            seja efetivamente invocada.

        :param str cnpj: Número do CNPJ do estabelecimento contribuinte,
            contendo apenas os dígitos. Nenhuma validação do número do CNPJ
            será realizada antes que a função de ativação seja efetivamente
            invocada.

        :param int codigo_uf: Código da unidade federativa onde o equipamento
            SAT será ativado (eg. ``35`` para o Estado de São Paulo). Nenhuma
            validação do código da UF será realizada antes que a função de
            ativação seja efetivamente invocada.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'tipo_certificado': tipo_certificado,
            'codigo_ativacao': self._codigo_ativacao,
            'cnpj': cnpj,
            'codigo_uf': codigo_uf,
        }
        return self.comando_sat('AtivarSat.xml', consulta=consulta)

    def comunicar_certificado_icpbrasil(self, certificado):
        """Função ``ComunicarCertificadoICPBRASIL`` conforme ER SAT, item 6.1.2.
        Envio do certificado criado pela ICP-Brasil.

        :param str certificado: Conteúdo do certificado digital criado pela
            autoridade certificadora ICP-Brasil.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            'certificado': certificado,
        }
        return self.comando_sat('ComunicarCertificadoICPBRASIL.xml', consulta=consulta)

    def enviar_dados_venda(self, dados_venda, numero_identificador):
        """Função ``EnviarDadosVenda`` conforme ER SAT, item 6.1.3. Envia o
        CF-e de venda para o equipamento SAT, que o enviará para autorização
        pela SEFAZ.

        :param dados_venda: Uma instância de :class:`~satcfe.entidades.CFeVenda`
            ou uma string contendo o XML do CF-e de venda.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_venda = dados_venda \
            if isinstance(dados_venda, basestring) \
            else dados_venda.documento()
        if isinstance(self._numerador_sessao, basestring):
            numero_sessao = self._numerador_sessao
        else:
            numero_sessao = self.gerar_numero_sessao()
        consulta = {
            'numero_sessao': numero_sessao,
            'codigo_ativacao': self._codigo_ativacao,
            'cfe_venda': cfe_venda,
            'numero_documento': 10,  # FIXME
            'numero_identificador': numero_identificador,  # FIXME
        }
        return self.comando_sat('EnviarDadosVenda.xml', consulta=consulta)

    def cancelar_ultima_venda(self, chave_cfe, dados_cancelamento):
        """Função ``CancelarUltimaVenda`` conforme ER SAT, item 6.1.4. Envia o
        CF-e de cancelamento para o equipamento SAT, que o enviará para
        autorização e cancelamento do CF-e pela SEFAZ.

        :param chave_cfe: String contendo a chave do CF-e a ser cancelado,
            prefixada com o literal ``CFe``.

        :param dados_cancelamento: Uma instância
            de :class:`~satcfe.entidades.CFeCancelamento` ou uma string
            contendo o XML do CF-e de cancelamento.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_canc = dados_cancelamento \
                if isinstance(dados_cancelamento, basestring) \
                else dados_cancelamento.documento()

        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            'chave_cfe': chave_cfe,
            'cfe_canc': cfe_canc,
        }
        return self.comando_sat('CancelarUltimaVenda.xml', consulta=consulta)


    def consultar_sat(self):
        """Função ``ConsultarSAT`` conforme ER SAT, item 6.1.5. Usada para
        testes de comunicação entre a AC e o equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """

        consulta = {
                'numero_sessao': self.gerar_numero_sessao(),
            }
        return self.comando_sat('ConsultarSAT.xml', consulta=consulta)

    def teste_fim_a_fim(self, dados_venda):
        """Função ``TesteFimAFim`` conforme ER SAT, item 6.1.6. Teste de
        comunicação entre a AC, o equipamento SAT e a SEFAZ.

        :param dados_venda: Uma instância de :class:`~satcfe.entidades.CFeVenda`
            ou uma string contendo o XML do CF-e de venda de teste.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_venda = dados_venda \
            if isinstance(dados_venda, basestring) \
            else dados_venda.documento()

        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            'cfe_venda': cfe_venda,
            }
        return self.comando_sat('TesteFimAFim.xml', consulta=consulta)

    def consultar_status_operacional(self):
        """Função ``ConsultarStatusOperacional`` conforme ER SAT, item 6.1.7.
        Consulta do status operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            }
        return self.comando_sat('ConsultarStatusOperacional.xml', consulta=consulta)

    def consultar_numero_sessao(self, numero_sessao):
        """Função ``ConsultarNumeroSessao`` conforme ER SAT, item 6.1.8.
        Consulta o equipamento SAT por um número de sessão específico.

        :param int numero_sessao: Número da sessão que se quer consultar.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'codigo_ativacao': self._codigo_ativacao,
            'numero_sessao': numero_sessao,
            }
        return self.comando_sat('ConsultarNumeroSessao.xml', consulta=consulta)

    def configurar_interface_de_rede(self, configuracao):
        """Função ``ConfigurarInterfaceDeRede`` conforme ER SAT, item 6.1.9.
        Configurção da interface de comunicação do equipamento SAT.

        :param configuracao: Instância de :class:`~satcfe.rede.ConfiguracaoRede`
            ou uma string contendo o XML com as configurações de rede.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        conf_xml = configuracao \
                if isinstance(configuracao, basestring) \
                else configuracao.documento()

        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            'configuracao': conf_xml,
        }
        return self.comando_sat('ConfigurarInterfaceDeRede.xml', consulta=consulta)

    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        """Função ``AssociarAssinatura`` conforme ER SAT, item 6.1.10.
        Associação da assinatura do aplicativo comercial.

        :param sequencia_cnpj: Sequência string de 28 dígitos composta do CNPJ
            do desenvolvedor da AC e do CNPJ do estabelecimento comercial
            contribuinte, conforme ER SAT, item 2.3.1.

        :param assinatura_ac: Sequência string contendo a assinatura digital do
            parâmetro ``sequencia_cnpj`` codificada em base64.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            'sequencia_cnpj': sequencia_cnpj,
            'assinatura_ac': assinatura_ac,
        }
        return self.comando_sat('AssociarAssinatura.xml', consulta=consulta)

    def atualizar_software_sat(self):
        """Função ``AtualizarSoftwareSAT`` conforme ER SAT, item 6.1.11.
        Atualização do software do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
        }
        return self.comando_sat('AtualizarSoftwareSAT.xml', consulta=consulta)


    def extrair_logs(self):
        """Função ``ExtrairLogs`` conforme ER SAT, item 6.1.12. Extração dos
        registros de log do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
        }
        return self.comando_sat('ExtrairLogs.xml', consulta=consulta)

    def bloquear_sat(self):
        """Função ``BloquearSAT`` conforme ER SAT, item 6.1.13. Bloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
        }
        return self.comando_sat('BloquearSAT.xml', consulta=consulta)

    def desbloquear_sat(self):
        """Função ``DesbloquearSAT`` conforme ER SAT, item 6.1.14. Desbloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
        }
        return self.comando_sat('DesbloquearSAT.xml', consulta=consulta)

    def trocar_codigo_de_ativacao(self, novo_codigo_ativacao,
            opcao=constantes.CODIGO_ATIVACAO_REGULAR,
            codigo_emergencia=None):
        """Função ``TrocarCodigoDeAtivacao`` conforme ER SAT, item 6.1.15.
        Troca do código de ativação do equipamento SAT.

        :param str novo_codigo_ativacao: O novo código de ativação escolhido
            pelo contribuinte.

        :param int opcao: Indica se deverá ser utilizado o código de ativação
            atualmente configurado, que é um código de ativação regular,
            definido pelo contribuinte, ou se deverá ser usado um código de
            emergência. Deverá ser o valor de uma das constantes
            :attr:`satcomum.constantes.CODIGO_ATIVACAO_REGULAR` (padrão) ou
            :attr:`satcomum.constantes.CODIGO_ATIVACAO_EMERGENCIA`.
            Nenhuma validação será realizada antes que a função seja
            efetivamente invocada. Entretanto, se opção de código de ativação
            indicada for ``CODIGO_ATIVACAO_EMERGENCIA``, então o argumento que
            informa o ``codigo_emergencia`` será checado e deverá avaliar como
            verdadeiro.

        :param str codigo_emergencia: O código de ativação de emergência, que
            é definido pelo fabricante do equipamento SAT. Este código deverá
            ser usado quando o usuário perder o código de ativação regular, e
            precisar definir um novo código de ativação. Note que, o argumento
            ``opcao`` deverá ser informado com o valor
            :attr:`satcomum.constantes.CODIGO_ATIVACAO_EMERGENCIA` para que
            este código de emergência seja considerado.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string

        :raises ValueError: Se o novo código de ativação avaliar como falso
            (possuir uma string nula por exemplo) ou se o código de emergencia
            avaliar como falso quando a opção for pelo código de ativação de
            emergência.

        .. warning::

            Os argumentos da função ``TrocarCodigoDeAtivacao`` requerem que o
            novo código de ativação seja especificado duas vezes (dois
            argumentos com o mesmo conteúdo, como confirmação). Este método irá
            simplesmente informar duas vezes o argumento
            ``novo_codigo_ativacao`` na função SAT, mantendo a confirmação do
            código de ativação fora do escopo desta API.

        """
        if not novo_codigo_ativacao:
            raise ValueError('Novo codigo de ativacao invalido: {!r}'.format(
                    novo_codigo_ativacao))

        codigo_ativacao = self._codigo_ativacao

        if opcao == constantes.CODIGO_ATIVACAO_EMERGENCIA:
            if codigo_emergencia:
                codigo_ativacao = codigo_emergencia
            else:
                raise ValueError('Codigo de ativacao de emergencia invalido: '
                        '{!r} (opcao={!r})'.format(codigo_emergencia, opcao))

        consulta = {
            'numero_sessao': self.gerar_numero_sessao(),
            'codigo_ativacao': self._codigo_ativacao,
            'opcao': self.opcao,
            'novo_codigo_ativacao': self.novo_codigo_ativacao,
        }
        return self.comando_sat('TrocarCodigoDeAtivacao.xml', consulta=consulta)


class FuncoesVFPE(object):
    def __init__(self, biblioteca, chave_acesso_validador=None, numerador_sessao=None):
        self._biblioteca = biblioteca
        self._chave_acesso_validador = chave_acesso_validador
        self._numerador_sessao = numerador_sessao or NumeroSessaoMemoria()
        self._path = os.path.join(os.path.dirname(__file__), 'templates/')


    @property
    def biblioteca(self):
        return self._biblioteca

    def gerar_numero_sessao(self):
        """Gera o número de sessão para a próxima invocação de função SAT."""
        return self._numerador_sessao()

    @property
    def chave_acesso_validador(self):
        return self._chave_acesso_validador


    def __getattr__(self, name):
        if name.startswith('invocar__'):
            metodo_vfpe = name.replace('invocar__', '')
            proto = FUNCTION_PROTOTYPES[metodo_vfpe]
            fptr = getattr(self._biblioteca.ref, metodo_vfpe)
            fptr.argtypes = proto.argtypes
            fptr.restype = proto.restype
            return fptr
        raise AttributeError('{!r} object has no attribute {!r}'.format(
                self.__class__.__name__, name))

    def comando_vfpe(self, template, **kwargs):
        if kwargs['numero_identificador'] != 'False':
            numero_identificador = kwargs.get(
                'numero_sessao',
                kwargs['numero_identificador'],
            )
        else:
            numero_identificador = kwargs.get(
                'numero_sessao',
                self.gerar_numero_sessao(),
            )

        kwargs['numero_identificador'] = numero_identificador
        path_file = self.biblioteca.caminho+'input/' + str(numero_identificador) + '-' + template.lower()
        # remove arquivo se ele existir
        if os.path.isfile(path_file):
            os.remove(path_file)

        observer = Observer()
        observer.numero_identificador = False
        observer.src_path = False
        observer.schedule(MonitorIntegrador(observer), path=self.biblioteca.caminho+'output')
        observer.start()

        xml = render_xml(self._path, template, True, **kwargs)
        xml.write(
            path_file,
            xml_declaration=True,
            encoding='UTF-8'
        )

        cont_time = 0
        while True:
            # Analisa a pasta a cada um segundo.
            # entra10 vezes e sai da verificacao
            time.sleep(1)
            cont_time = cont_time + 1
            if (str(numero_identificador) == str(observer.numero_identificador) and \
                observer.src_path):
                # Ao encontrar um arquivo de retorno com o mesmo numero identificador da remessa sai do loop.
                break
            if  cont_time == 10:
                observer.resposta = str(numero_identificador)+'|'+str(numero_identificador)+'|'+'0'+'|'+'Erro interno'+'|'+'0'+'|'+'ERRO'
                # Ao nao encontrar um arquivo de retorno com o mesmo numero identificador
                break
        observer.stop()
        observer.join()
        return observer.resposta

    def verificar_status_validador(self, cpnj, id_fila):
        """Função ``VerificarStatusValidador`` conforme ER SAT, item 6.1.14. Desbloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
            'chave_acesso_validador': self._chave_acesso_validador,
            'id_fila': id_fila,
            'cnpj': cpnj,
        }

        return self.comando_vfpe('VerificarStatusValidador.xml', consulta=consulta)

    def enviar_pagamentos_armazenamento_local(self):
        """Função ``VerificarStatusValidador`` conforme ER SAT,
        item 6.1.14. Desbloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        consulta = {
        }
        return self.comando_vfpe('EnviarPagamentosEmArmazenamentoLocal.xml',
                                 consulta=consulta)

    def enviar_pagamento(self, chave_requisicao, estabecimento, serial_pos,
                         cpnj, icms_base, vr_total_venda,
                         h_multiplos_pagamentos, h_anti_fraude,
                         cod_moeda, origem_pagemento, numero_identificador):
        consulta = {
            'chave_acesso_validador': self._chave_acesso_validador,
            'chave_requisicao': chave_requisicao,
            'estabecimento': estabecimento,
            'serial_pos': serial_pos,
            'cpnj': cpnj,
            'icms_base': icms_base,
            'vr_total_venda': vr_total_venda,
            'h_multiplos_pagamentos': h_multiplos_pagamentos,
            'h_anti_fraude': h_anti_fraude,
            'cod_moeda': cod_moeda,
            'origem_pagemento': origem_pagemento,
            'numero_identificador': numero_identificador
        }
        return self.comando_vfpe('EnviarPagamento.xml', consulta=consulta)


    def enviar_status_pagamento(self, codigo_autorizacao, bin, dono_cartao,
                                data_expiracao, instituicao_financeira, parcelas,
                                codigo_pagamento, valor_pagamento, id_fila,
                                tipo, ultimos_quatro_digitos):

        consulta = {
            'chave_acesso_validador': self._chave_acesso_validador,
            'codigo_autorizacao': codigo_autorizacao,
            'bin': bin,
            'dono_cartao':dono_cartao,
            'data_expiracao':data_expiracao,
            'instituicao_financeira':instituicao_financeira,
            'parcelas':parcelas,
            'codigo_pagamento':codigo_autorizacao,
            'valor_pagamento':valor_pagamento,
            'id_fila':id_fila,
            'tipo':tipo,
            'ultimos_quatro_digitos':ultimos_quatro_digitos
        }
        return self.comando_vfpe('EnviarStatusPagamento.xml', consulta=consulta)

    def recuperar_dados_locais_enviados(self):

        consulta = {
            'chave_acesso_validador': self._chave_acesso_validador,
        }
        return self.comando_vfpe('RecuperarDadosLocaisEnviadosParaValidadorFiscal.xml', consulta=consulta)

    def resposta_fiscal(self, id_fila, chave_acesso, nsu, numero_aprovacao,
                        bandeira, adquirente, cnpj, impressao_fiscal,
                        numero_documento):

        consulta = {
            'chave_acesso_validador': self._chave_acesso_validador,
            'id_fila': id_fila,
            'chave_acesso': chave_acesso,
            'nsu': nsu,
            'numero_aprovacao': numero_aprovacao,
            'bandeira': bandeira,
            'adquirente': adquirente,
            'cnpj': cnpj,
            'impressao_fiscal': impressao_fiscal,
            'numero_documento': numero_documento,
        }
        return self.comando_vfpe("RespostaFiscal.xml", consulta=consulta)

