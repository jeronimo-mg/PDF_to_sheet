#!/usr/bin/env bash
# Script para compilar o executável nativo do Linux (Ubuntu/Debian) usando PyInstaller

set -e

echo "=== Compilando PDF to Sheet Converter para Linux (Ubuntu) ==="

# Garante que o ambiente virtual está ativo ou dependências instaladas
pip install -q pyinstaller .

# Compila o binário independente do Linux
pyinstaller --noconfirm --onefile \
    --name pdf-to-sheet-linux \
    --distpath dist \
    --collect-all pdfplumber \
    --collect-all pypdfium2 \
    --collect-all rich \
    src/pdf_to_sheet/cli.py

chmod +x dist/pdf-to-sheet-linux

echo ""
echo "=== Compilação concluída com sucesso! ==="
echo "Executável gerado em: dist/pdf-to-sheet-linux"
