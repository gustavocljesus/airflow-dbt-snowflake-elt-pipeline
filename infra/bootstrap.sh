#!/bin/bash
set -e

echo "configurando permissoes..."

chmod +x setup_airflow.sh setup_project.sh

echo "configurando airflow..."
./setup_airflow.sh

echo "Preparando projeto..."
./setup_project.sh