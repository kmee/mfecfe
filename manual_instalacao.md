
ATENcaO !
EXECUTE O COMANDO ldd --version no shell antes de instala o drive MFE!
Se o resultado for 2.12 ou inferior o drive do MFE nao funciona nesta distribuicao

x86
https://integrador.blob.core.windows.net/integrador/instalador-ce-sefaz-driver-linux-x86-02.04.07.tar.gz

Após a instalacao do drive MFE Fornecido pela SEFAZ
Verificacoes necessarias antes de preseguir com a instalacao do integrador

ldd --version
se for  2.12 ou menor o Drive do MFE nao funciona.

Verificar se a porta 9015 existe, se aparecer alguma das saidas abaixo esta ok, caso nao o Drive do MFE nao funciona.
netstat -t -l -p --numeric-ports
Saida
"tcp        0      0 127.0.0.1:9015          0.0.0.0:*               OUcA       26263  /mfe-https"
"tcp        0      0 0.0.0.0:9015            0.0.0.0:*               OUcA       3053   /mfehttps"
"tcp        0      0 *:9015                        *:*               OUcA       1556/ ./mfehttps"

Verificar se o servico existe, se aparecer alguma das 2 saidas abaixo esta ok, caso nao o Drive do MFE nao funciona.
ps aux | grep mfehttps
Saida
"root     12424  0.0  0.0   3580   780 pts/0    S+   13:43   0:00 grep mfe-https"
"root     12424  0.0  0.0   3580   780 pts/0    S+   13:43   0:00 grep mfehttps"

tem que conter duas linhas do mfe-https, caso nao o Drive do MFE nao funciona.


Caso o Drive do MFE nao funcine contato do reponsavel da empresa COMPSIS
12 99197-7324 -> Carlos Doria / Carlos.Doria@compsis.com.br
suporte.mfe@sefaz.ce.gov.br SEFAZ


Linux x86 com Integrador + Drive MFE imagens disponiveis
Para todos:
usuario root     senha gizmin
usuario gizmin   senha gizmin



Configuracao do ambiente para o INTEGRADOR.

- Kernel minimo 2.6.x
- Compilador minimo GCC 4.4.7
  Utilize o gerenciador de pacotes de sua distribuicao ou faca o download, link na lista abaixo
  GCC 4.4.7
  https://gcc.gnu.org/gcc-4.4/

- Mono 4.2.4 (versao minima para funcionamento)
  Realize a compilacao desta versao do mono ou faca a instalacao via gerenciador de pacotes
  *Utilizando o genrencido de pacotes faca a instalacao do mono-complete
  **A versao do mono recomendada e esta 4.2.4, segue link para download abaixo
  ***Caso o MONO esteja consumindo muito a CPU segue a seguinte solucao
    http://archive.is/nDqZH#selection-287.0-299.19

Mono (para compilacao)
https://integrador.blob.core.windows.net/linuxwithoutui/mono-4.2.4.4.tar.bz2
Pagina oficial do mono, pode-se instalar e usar pelo gerenciado de pacotes
http://www.mono-project.com/download/#download-lin
faca a intalação completa caso use o repositorio
sudo apt-get install mono-complete / sudo yum install mono-complete

*Caso o MONO esteja consumindo muito a CPU segue a seguinte solucao
http://archive.is/nDqZH#selection-287.0-299.19


- SQLite.Interop.so mono 5 > ou superior
  Segue link do  source para compilacao e link do distribuidor
  https://system.data.sqlite.org/index.html/doc/preRelease/www/downloads.wiki

Link do sources
https://integrador.blob.core.windows.net/linuxwithoutui/sqlite-netFx-full-source-1.0.105.2.zip
*Case seja instalado o mono 4.2.x < , link para o source ser compiado
https://integrador.blob.core.windows.net/linuxwithoutui/sqlite-netFx-full-source-1.0.104.0.zip

- uuidgen
  Verificar se na sua distribuicao tem este pacote instalado, se nao tiver realizar a instalacao


Após as verificacoes feitas presegue-se com a instalacao do integrador

Portas a serem liberadas no firewall para comunicacao entre o Integrador Servidor e Integrador Terminal

Portas : 11119 e 11118

Enderecos:
http://apiintegrador.azurewebsites.net
http://integrador.blob.core.windows.net/integrador/

Ex:
/home/pdv/IntegradorLinuxServidor
/home/pdv/IntegradorLinuxTerminal

Instalacao INTEGRADOR SERVIDOR
Copie libSQLite.Interop.so e SQLite.Interop.dll para a pasta onde foi descompactado o integrador

URL para download: https://integrador.blob.core.windows.net/linuxwithoutui/IntegradorLinuxServidor.zip
Faca o download do integrador para ser usado no servidor, onde o aparelho MFE devera estar instalado,
descompacte o arquivo e coloque na pasta onde deseja que ele seja executado.

Passos 1o. execucao:
$ mono IntegradorLinux.exe
Como alguns arquivos de configuracao que ele gera nao exisem ele vai dar a seguinte mensagem:

ARQUIVO EXEMPLO PARA : CONFIGURACAO SERVIDOR

{
   "ie":"06.501148-2",
   "cnpj":"22.295.347/0001-41",
   "cnpjSh":"72.618.748/0001-63",
   "nomeAc":"NOME DO SEU AC",
   "acFile":"/PATHDOAC/EXECUTAVELAC",
   "IsServer":"True",
   "ServerIp":"127.0.0.1",
   "chaveAcesso":"!==MD2Nof/O0tQMPKiYeeAydSjYt7YV9kU0nWKZGXHVdYIzR2W9Z6tgXni/Y5bnjmUAk8MkqlBJIiOOIskKCjJ086k7vAP0EU5cBRYj/nzHUiRdu9AVD7WRfVs00BDyb5fsnnKg7gAXXH6SBgCxG9yjAkxJ0l2E2idsWBAJ5peQEBZqtHytRUC+FLaSfd3+66QNxIBlDwQIRzUGPaU6fvErVDSfMUf8WpkwnPz36fCQnyLypqe/5mbox9pt3RCbbXcYqnR/4poYGr9M9Kymj4/PyX9xGeiXwbgzOOHNIU5M/aAs0rulXz948bZla0eXABgEcp6mDkTzweLPZTbmOhX+eA==",
   "inputFolder":"/home/gizmin/Integrador/input/",
   "outputFolder":"/home/gizmin/Integrador/output/",
   "inputFolderTerminal":"/home/gizmin/Integrador/input/",
   "outputFolderTerminal":"/home/gizmin/Integrador/output/",
   "Info":"Este dados sao todos ficticios, utilizados apenas para exemplos de configuracoes, CNPJ, IE (inscricao estadual), CNPJSH, CHAVEACESSO sao invalidos. CNPJ e IE devem ser do comercio, CNPJSH e o CNPJ da Softwarehouse do AC, chaveAcesso e a chave de ativacao do MFE informada no ativado da SEFAZ",
   "port1": "11119",
   "port2": "11118",
   "usarproxy": "NAO",
   "ipproxy" : "127.0.0.1",
   "portproxy" : "80",
   "proxyuser" : "semusuario",
   "proxysenha" : "semsenha"
}

Salvar o arquivo como: integrador.ooo
Após a configuracao do integrador, deve-se criar um servico junto com a inicializacao do LINUX


Caso for utilizar 1 equipamento MFE para cada PDV nao e necessario utilizar o IntegradorTerminal.

ARQUIVO EXEMPLO PARA : CONFIGURACAO TERMINAL
*Os campos devem permanecer em branco mesmo, somente os campos de portas devem estar preenchidos.

{
   "ie":"",
   "cnpj":"",
   "cnpjSh":"",
   "nomeAc":"",
   "acFile":"",
   "IsServer":"",
   "ServerIp":"",
   "chaveAcesso":"",
   "inputFolder":"",
   "outputFolder":"",
   "inputFolderTerminal":"",
   "outputFolderTerminal":"",
   "Info":"",
   "port1": "11119",
   "port2": "11118",
   "usarproxy": "",
   "ipproxy" : "",
   "portproxy" : "",
   "proxyuser" : "",
   "proxysenha" : ""
}


Instalacao INTEGRADOR TERMINAL
URL para download: https://integrador.blob.core.windows.net/linuxwithoutui/IntegradorLinuxTerminal.zip
faca o download do integrador para ser usado no terminal, onde o aparelho MFE devera estar instalado,
descompacte o arquivo e coloque na pasta onde deseja que ele seja executado, deve-se criar um servico
junto com a inicializacao do LINUX

execucao:
$ mono IntegradorLinuxTerminal.exe


OBS:
Copie a libSQLite.Interop.so para a pasta onde for descompactado o integrador
Caso nao funcione o integrador e seja criado uma pasta com um arquivo ex:
LOG/06072017/LOG_06072017.log

Contendo uma mensagem como esta:
 System.TypeInitializationException: The type initializer for 'A.^L^V' threw an exception. ---> System.DllNotFoundException: SQLite.Interop.dll
  at (wrapper managed-to-native) System.Data.SQLite.UnsafeNativeMethods:sqlite3_config_none (System.Data.SQLite.SQLiteConfigOpsEnum)
  at System.Data.SQLite.SQLite3.StaticIsInitialized () <0xb70178f8 + 0x0004f> in <filename unknown>:0
  at System.Data.SQLite.SQLiteLog.Initialize () <0xb7017620 + 0x00017> in <filename unknown>:0
  at System.Data.SQLite.SQLiteConnection..ctor (System.String connectionString, Boolean parseViaFramework) <0xb7038bf0 + 0x0003b> in <filename unknown>:0
  at System.Data.SQLite.SQLiteConnection..ctor (System.String connectionString) <0xb7038bc0 + 0x0001f> in <filename unknown>:0
  at (wrapper remoting-invoke-with-check) System.Data.SQLite.SQLiteConnection:.ctor (string)
  at (wrapper dynamic-method) A.^B : (string)
  at A.^B .
 (System.String ) <0xb7038a00 + 0x00023> in <filename unknown>:0
  at A.^L^V..cctor () <0xb7038900 + 0x00047> in <filename unknown>:0
  --- End of inner exception stack trace ---
  at A.^V^V.^N () <0xb7290c68 + 0x00053> in <filename unknown>:0
[06/07/2017 12:07:29] "The type initializer for 'A.\f\u0016' threw an exception."

Deve-se fazer o processo de compilacao link do source para download:

https://integrador.blob.core.windows.net/linuxwithoutui/sqlite-netFx-full-source-1.0.104.0.zip

Processo descompacte o arquivo
cd sqlite-netFx-full-source-1.0.104.0/Setup
chmod +x compile-interop-assembly-release.sh
./compile-interop-assembly-release.sh
cd ..

cd /sqlite-netFx-full-source-1.0.104.0/bin/2013/Release/bin
cp libSQLite.Interop.so /home/USUARIO_SERVIDOR/PATH_INTEGRADOR_SERVER

Segue um teste basico para verificar se o integrador esta consumindo os arquivos XML
Crie um arquivo XML e coloque este conteúdo, salve como ConsultaMFE.xml
<?xml version="1.0" encoding="utf-8"?>
<Integrador>
    <Identificador>
        <Valor>808060</Valor>
    </Identificador>
    <Componente Nome="MF-e">
        <Metodo Nome="ConsultarMFe">
            <Parametros>
                <Parametro>
                    <Nome>numeroSessao</Nome>
                    <Valor>808060</Valor>
                </Parametro>
            </Parametros>
        </Metodo>
    </Componente>
</Integrador>

Erros de drive devido a ldd <= 2.12
 [24/07/2017 22:39:24] System.Net.WebException: Error: SendFailure (Error writing headers) ---> System.Net.WebException: Error writing headers ---> System.IO.IOException: The authentication or decryption has failed. ---> Mono.Security.Protocol.Tls.TlsException: Invalid certificate received from server. Error code: 0xffffffff800b010a

  at Mono.Security.Protocol.Tls.RecordProtocol.EndReceiveRecord (IAsyncResult asyncResult) <0x5cc610 + 0x000db> in <filename unknown>:0

  at Mono.Security.Protocol.Tls.SslClientStream.SafeEndReceiveRecord (IAsyncResult ar, Boolean ignoreEmpty) <0x5cc568 + 0x0001f> in <filename unknown>:0

  at Mono.Security.Protocol.Tls.SslClientStream.NegotiateAsyncWorker (IAsyncResult result) <0xa8a088 + 0x0019f> in <filename unknown>:0

  --- End of inner exception stack trace ---

  at System.Net.WebConnection.EndWrite (System.Net.HttpWebRequest request, Boolean throwOnError, IAsyncResult result) <0x569d40 + 0x00183> in <filename unknown>:0

  at System.Net.WebConnectionStream+<SetHeadersAsync>c__AnonStorey1.<>m__0 (IAsyncResult r) <0x569788 + 0x000eb> in <filename unknown>:0

  --- End of inner exception stack trace ---

  --- End of inner exception stack trace ---

  at System.Net.HttpWebRequest.EndGetResponse (IAsyncResult asyncResult) <0x5615a0 + 0x00187> in <filename unknown>:0

  at System.Net.HttpWebRequest.GetResponse () <0x55e670 + 0x0004c> in <filename unknown>:0

  at (wrapper dynamic-method) A.__: (object)

  at A.__.

(System.Object ) <0xa7d870 + 0x00023> in <filename unknown>:0

  at A._.

(System.String ) <0xa7ccf0 + 0x0015b> in <filename unknown>:0



-Integrador para windows para auxilio em relação aos XML´s
https://integrador.blob.core.windows.net/releases/Integrador%20Setup%201.6.86.exe

Dados de configuração

--Dados para trabalho comercio
--CNPJ  22295347000141
--IE    065911482

--Dados para trabalho SoftwareHouse
--      !==MD2Nof/O0tQMPKiYeeAydSjYt7YV9kU0nWKZGXHVdYIzR2W9Z6tgXni/Y5bnjmUAk8MkqlBJIiOOIskKCjJ086k7vAP0EU5cBRYj/nzHUiRdu9AVD7WRfVs00BDyb5fsnnKg7gAXXH6SBgCxG9yjAkxJ0l2E2idsWBAJ5peQEBZqtHytRUC+FLaSfd3+66QNxIBlDwQIRzUGPaU6fvErVDSfMUf8WpkwnPz36fCQnyLypqe/5mbox9pt3RCbbXcYqnR/4poYGr9M9Kymj4/PyX9xGeiXwbgzOOHNIU5M/aAs0rulXz948bZla0eXABgEcp6mDkTzweLPZTbmOhX+eA==
--CNPJ  72618748000163

*Não esquecer de marcar a opção servidor antes de salvar as configurações

Em aplictivos contem todos os componentes e neles os respectivos XML com exemplos de envio e exemplos de retorno