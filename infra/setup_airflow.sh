#!/bin/bash
set -e

echo "Atualizando a lista de pacotes do APT..."
sudo apt update && sudo apt upgrade -y

echo "Instalando dependências..."
sudo apt install -y ca-certificates curl gnupg lsb-release

echo "Configurando repositório oficial do Docker..."
sudo mkdir -p /etc/apt/keyrings   

if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg   
fi

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

echo "Instalando Docker..."
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "Criando diretório do Airflow..."
mkdir -p ~/airflow
cd ~/airflow

echo "Baixando docker-compose do Airflow..."
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.7/docker-compose.yaml'

echo "Criando diretórios..."
mkdir -p ./dags ./logs ./plugins ./config   

echo "Criando arquivo .env..."
echo "AIRFLOW_UID=$(id -u)" > .env

echo "Inicializando Airflow..."
sudo docker compose up airflow-init

echo "Subindo containers..."
sudo docker compose up -d