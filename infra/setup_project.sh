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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Criando arquivo .env..."
echo "AIRFLOW_UID=$(id -u)" > "$PROJECT_DIR/.env"

echo "Inicializando Airflow..."
sudo docker compose -f "$PROJECT_DIR/docker-compose.yaml" up airflow-init

echo "Subindo containers..."
sudo docker compose -f "$PROJECT_DIR/docker-compose.yaml" up -d

echo "-------------------------------------"
echo "Airflow disponível em:"
echo "http://SEU_IP_PUBLICO:8080"
echo "-------------------------------------"
