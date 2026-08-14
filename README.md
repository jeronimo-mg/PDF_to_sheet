# 📊 PDF to Sheet Converter

> **Utilitário CLI e Servidor MCP de alta precisão para conversão local, offline e privada de tabelas em PDF para planilhas Excel (`.xlsx`).**

---

## 🌟 Visão Geral

O **PDF to Sheet Converter** é uma ferramenta desenvolvida em Python para extrair tabelas de documentos PDF (como faturas, extratos, notas fiscais e relatórios técnicos de engenharia LE/LI) e exportá-las em arquivos Excel (`.xlsx`) perfeitamente formatados, preservando alinhamentos, tipos de dados e cabeçalhos.

Toda a execução é realizada **100% localmente no seu computador**, sem dependência de serviços em nuvem ou vazamento de dados confidenciais.

---

## ✨ Principais Funcionalidades

* ⚡ **Engine Híbrida de Extração em 2 Níveis**:
  * **Nível 1 (Determinístico / Regras)**: Utiliza `pdfplumber` e `camelot` para extração rápida e precisa de tabelas vetoriais e com grades definidas.
  * **Nível 2 (IA Local / Visão - Fallback)**: Integração opcional com modelos locais de visão computacional via **Ollama** (ex: `llama3.2-vision`) para reconhecer tabelas complexas ou sem bordas quando a extração determinística falha.
* 🎯 **Perfis de Extração Selecionáveis (`--profile`)**:
  * `auto` *(Padrão Inteligente)*: Detecta automaticamente o formato do documento. Se encontrar termos de engenharia LE/LI (`SISTEMA`, `INSTRUM.`, `EQUIPAMENTO`), ativa o alinhamento de colunas especializado. Caso contrário, aplica a limpeza neutra universal.
  * `generic`: Força a extração universal neutra para qualquer tipo de tabela em PDF sem assumir regras de domínio.
  * `le_li`: Força o perfil otimizado para documentos técnicos de engenharia industrial (Listas de Equipamentos LE e Instrumentos LI).
* 🖥️ **Interface Gráfica Nativa (GUI)**:
  * Permite selecionar arquivos via caixa de diálogo do Windows com opção `--gui` ou dando duplo clique no executável `Converter_PDF_para_Excel.bat`.
* 🤖 **Servidor MCP Integrado (Model Context Protocol)**:
  * Permite que assistentes de IA (como Claude Desktop e Antigravity) inspecionem e convertam tabelas de PDFs diretamente via chamadas de ferramentas.
* 📈 **Exportação Rica em Excel**:
  * Formatação automática de colunas, quebra de texto (*wrap text*), ajuste de largura de células e separação em abas por página/tabela.

---

## 🛠️ Instalação

### Pré-requisitos
* **Python 3.10** ou superior instalado no Windows/Linux/macOS.

### Passo a Passo

1. **Clonar / Acessar o repositório**:
   ```bash
   cd H:/documents/pessoal/projetos/PDF_to_sheet
   ```

2. **Criar e ativar ambiente virtual (recomendado)**:
   ```bash
   python -m venv .venv
   # No Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # No Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instalar dependências e o pacote em modo editável**:
   ```bash
   pip install -e .
   ```

---

## 🚀 Como Usar

### 1. Converter um Arquivo PDF Único
```bash
# Usa a detecção automática de perfil (padrão inteligente)
pdf-to-sheet --file documento.pdf --output resultado.xlsx

# Ou usando o módulo python diretamente
python -m pdf_to_sheet.cli -f documento.pdf -o resultado.xlsx
```

### 2. Conversão em Lote (Diretório Completo)
Converte todos os arquivos `.pdf` contidos em uma pasta:
```bash
pdf-to-sheet --dir ./pasta_de_pdfs/ --output ./saida_excel/
```

### 3. Especificando Perfis de Extração (`--profile`)
```bash
# Modo Automático (Padrão: detecta LE/LI ou Genérico automaticamente)
pdf-to-sheet -f documento.pdf --profile auto

# Forçar Perfil Genérico (Universal para faturas, notas, relatórios financeiros, etc.)
pdf-to-sheet -f extrato.pdf --profile generic

# Forçar Perfil LE/LI (Documentos de Engenharia / Lista de Equipamentos e Instrumentos)
pdf-to-sheet -f R11.01-2151-LE-0001_2.pdf --profile le_li
```

### 4. Modo Interface Gráfica (GUI) & Executável Independente (.exe)
Você pode executar a conversão visual no Windows sem precisar de comandos no terminal:

* 📦 **Executável Independente (`.exe`)**:
  Localizado em `dist/Converter_PDF_para_Excel.exe`. Pode ser copiado e executado em qualquer computador com Windows, sem necessidade de instalar o Python!
  ```cmd
  dist\Converter_PDF_para_Excel.exe --gui
  ```
* ⚡ **Atalho via Arquivo Bat**:
  Basta dar um **duplo clique no arquivo `Converter_PDF_para_Excel.bat`** na raiz do projeto. Ele detectará o executável automaticamente e abrirá a caixa de seleção de arquivo.

---

## 🤖 Servidor MCP (Model Context Protocol)

O projeto inclui um servidor MCP compatível com assistentes de IA:

### Como Rodar o Servidor MCP
```bash
pdf-to-sheet-mcp
# Ou
python -m pdf_to_sheet.mcp_server
```

### Ferramentas MCP Disponíveis
* `inspect_pdf_tables(pdf_path)`: Retorna a estrutura, cabeçalhos e prévia de linhas das tabelas contidas no PDF.
* `convert_pdf(pdf_path, output_path, profile)`: Executa a conversão completa do PDF para `.xlsx`.

---

## 📂 Estrutura do Projeto

```text
PDF_to_sheet/
├── src/pdf_to_sheet/
│   ├── __init__.py
│   ├── cli.py             # Interface de linha de comando (Click + Rich)
│   ├── cleaner.py         # Limpeza de tabelas (perfis generic e le_li)
│   ├── merger.py          # Fusão de tabelas contínuas multipáginas
│   ├── models.py          # Dataclasses de modelos e interface BaseExtractor
│   ├── mcp_server.py      # Servidor MCP para integração com assistentes de IA
│   ├── extractors/
│   │   ├── rule_based.py  # Extrator determinístico (pdfplumber)
│   │   ├── local_ai.py    # Extrator de visão de IA local (Ollama)
│   │   └── hybrid.py      # Orquestrador híbrido com fallback
│   └── writers/
│       └── excel.py       # Gerador e formatador de arquivos XLSX (openpyxl)
├── tests/                 # Suíte de testes automatizados (pytest)
├── conductor/             # Especificações e planos de faixas de desenvolvimento
├── pyproject.toml         # Configuração do pacote e dependências
├── Converter_PDF_para_Excel.bat # Atalho executável para Windows GUI
└── README.md
```

---

## 🧪 Testes e Qualidade de Código

Para garantir a estabilidade do código, você pode rodar a suíte completa de verificação:

```bash
# Executar testes unitários e de integração
pytest

# Verificação de tipos estáticos
mypy .

# Análise estática de código e linting
ruff check .
```

---

## 📄 Licença

Este projeto é um software proprietário/privado desenvolvido para processamento local seguro de documentos.
