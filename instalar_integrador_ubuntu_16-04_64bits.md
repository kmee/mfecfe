Instalando o Integrador do Ceará no Linux Ubuntu 16.04 64 bits
==============================================================

Importante: Se vc executar em outra ordem não vai funcionar

1. ldd: Deve ser maior que > 2.12

```
ldd --version
```

2. Mono

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/ubuntu xenial main" | sudo tee /etc/apt/sources.list.d/mono-official.list
sudo apt update
apt list --upgradable
sudo apt-get update
sudo apt-get install mono-complete uuid-runtime axel
```

3. Downloads

```
cd ~/Downloads
axel https://integrador.blob.core.windows.net/integrador/instalador-ce-sefaz-driver-linux-x64-02.04.07.tar.gz
axel https://integrador.blob.core.windows.net/linuxwithoutui/sqlite-netFx-full-source-1.0.105.2.zip
axel https://integrador.blob.core.windows.net/linuxwithoutui/IntegradorLinuxServidor.zip
```

4. Driver

```
tar -zxvf instalador-ce-sefaz-driver-linux-x64-02.04.07.tar.gz
cd instalador-ce-sefaz-driver-linux-x64-02.04.07
sudo su
#Rodar como root!
./instala-driver-mfe.sh
reboot
```

5. Extraindo o integrador

```
cd ~/Downloads
unzip IntegradorLinuxServidor.zip
mv Debug ~/IntegradorServer
```

6. Compilando o libSQLite.Interop.so
```
unzip sqlite-netFx-full-source-1.0.105.2.zip -d sqlite-netFx-full-source-1.0.105.2
cd sqlite-netFx-full-source-1.0.105.2/Setup
chmod +x compile-interop-assembly-release.sh
./compile-interop-assembly-release.sh
cd ~/Downloads/sqlite-netFx-full-source-1.0.105.2/bin/2013/Release/bin
chmod -x libSQLite.Interop.so
cp libSQLite.Interop.so ~/IntegradorServer
```

7. Criando os diretórios de input e output:
- Atenção não coloque nada neles antes de iniciar o Integrador server pela primeira vez, senão vai dar problema

```
mkdir -p ~/Integrador/input
mkdir -p ~/Integrador/output
```

8. Crie o arquivo se configuração
```
nano ~/IntegradorServer/integrador.ooo
```

Exemplo arquivo Tanca, cuidado pois isto é um json!!! não tem vilgula na ultima linha.

```
{
   "ie":"06.591148-2",
   "cnpj":"30.146.465/0001-16",
   "cnpjSh":"98.155.757/0001-59",
   "nomeAc":"Odoo",
   "IsServer":"True",
   "ServerIp":"127.0.0.1",
   "chaveAcesso":"MD2Nof/O0tQMPKiYeeAydSjYt7YV9kU0nWKZGXHVdYIzR2W9Z6tgXni/Y5bnjmUAk8MkqlBJIiOOIskKCjJ086k7vAP0EU5cBRYj/nzHUiRdu9AVD7WRfVs00BDyb5fsnnKg7gAXXH6SBgCxG9yjAkxJ0l2E2idsWBAJ5peQEBZqtHytRUC+FLaSfd3+66QNxIBlDwQIRzUGPaU6fvErVDSfMUf8WpkwnPz36fCQnyLypqe/5mbox9pt3RCbbXcYqnR/4poYGr9M9Kymj4/PyX9xGeiXwbgzOOHNIU5M/aAs0rulXz948bZla0eXABgEcp6mDkTzweLPZTbmOhX+eA==",
   "inputFolder":"/home/kmee/Integrador/input/",
   "outputFolder":"/home/kmee/Integrador/output/",
   "inputFolderTerminal":"/home/kmee/Integrador/input/",
   "outputFolderTerminal":"/home/kmee/Integrador/output/"
}
```

9. Execute o servidor pela primeira vez!

Você não precisa executar o servidor como root, desde que o mesmo tenha acesso a todos os arquivos. Na primeira vez são realizados alguns downloads então este procedimento pode demorar um pouco dependendo da sua internet.

Espere alguns minutos antes de continuar. No momento na minha instalação listo os seguintes arquivos:

```
mileo@mileo-XPS-L421X:/opt/integrador/server$ ls -1 && ls | wc -l
ComponenteConsultaNSessao.cp
dataupdate
easync.dll
GizminNetworks.dll
IntegracaoComIntegradorSefaz.zip
Integrador.cnf
integradorcore.dll
integradorcoreterminal.dll
integradorData.itr
IntegradorLinux.exe
IntegradorLinux.vshost.exe
integradorMFE.dll
integradorMFE.jar
integrador.ooo
libSQLite.Interop.so
LOG
Newtonsoft.Json.dll
Newtonsoft.Json.xml
RestSharp.dll
RestSharp.xml
ServiceStack.Text.dll
ServiceStack.Text.xml
SQLite.Interop.dll
SQLite.Interop.so
System.Data.SQLite.dll
System.Data.SQLite.xml
System.Management.dll
System.Management.Instrumentation.dll
ValidadorFiscal.Integracao.dll
```

Total de arquivos 29.

Executando o integrador pela primeira vez

```
cd ~/IntegradorServer
mono IntegradorLinux.exe
```

10. Coloque seu primeiro arquivo na pasta input

Não edite aquivos lá dentro, apenas salve arquivos finalizados.

```
nano /tmp/consultaMfe.xml
```

Cole o conteudo

```
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
```
Copie o arquivo
```
cp /tmp/consultaMfe.xml ~/Integrador/input
```
