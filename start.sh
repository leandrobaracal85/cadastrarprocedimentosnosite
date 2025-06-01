#!/bin/bash

PROJETO_DIR="/root/automacoes/cadastrarprocedimentosnosite"
cd "$PROJETO_DIR"

source venv/bin/activate

while true; do
    echo "[Atualizando o repositório Git]"
    git pull

    echo "[Instalando dependências]"
    pip install -r requirements.txt

    echo "[Iniciando API Flask]"
    python3 api.py

    echo "[API encerrada. Reiniciando em 10 segundos...]"
    sleep 10
done
