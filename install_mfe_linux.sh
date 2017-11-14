#!/usr/bin/env bash


sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/ubuntu xenial main" | sudo tee /etc/apt/sources.list.d/mono-official.list
sudo apt update
apt list --upgradable
sudo apt-get update
sudo apt-get install mono-complete uuid-runtime
mono
mono  --version # Mono JIT compiler version 5.2.0.224 (tarball Tue Oct  3 19:49:47 UTC 2017)

ldd --version # Deve ser maior que > 2.12

wget https://integrador.blob.core.windows.net/integrador/instalador-ce-sefaz-driver-linux-x64-02.04.07.tar.gz
# x86
#https://integrador.blob.core.windows.net/integrador/instalador-ce-sefaz-driver-linux-x86-02.04.07.tar.gz
# Instalar

netstat -t -l -p --numeric-ports | grep -i 9015
ps aux | grep mfehttps



wget https://integrador.blob.core.windows.net/linuxwithoutui/sqlite-netFx-full-source-1.0.105.2.zip

Copie libSQLite.Interop.so e SQLite.Interop.dll para a pasta onde foi descompactado o integrador

Processo descompacte o arquivo
cd sqlite-netFx-full-source-1.0.104.0/Setup
chmod +x compile-interop-assembly-release.sh
./compile-interop-assembly-release.sh
cd ..

cd /sqlite-netFx-full-source-1.0.104.0/bin/2013/Release/bin
cp libSQLite.Interop.so /home/USUARIO_SERVIDOR/PATH_INTEGRADOR_SERVER



axel https://integrador.blob.core.windows.net/linuxwithoutui/IntegradorLinuxServidor.zip

Passos 1o. execucao:
$ mono IntegradorLinux.exe
Como alguns arquivos de configuracao que ele gera nao exisem ele vai dar a seguinte mensagem:

Instalacao INTEGRADOR TERMINAL
URL para download: https://integrador.blob.core.windows.net/linuxwithoutui/IntegradorLinuxTerminal.zip


