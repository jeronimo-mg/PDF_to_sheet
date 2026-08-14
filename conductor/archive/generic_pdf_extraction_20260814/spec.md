# Specification: Suporte a Extração Genérica de Tabelas em PDF (`generic_pdf_extraction`)

## 1. Overview
Adicionar suporte a um modo de extração de tabelas genérico e universal para qualquer arquivo PDF com camada de texto. Atualmente, o limpador e extrator (`cleaner.py` e `rule_based.py`) possuem regras fixas (*hardcoded*) voltadas para listas de equipamentos e instrumentos industriais (LE/LI), tais como alteração da coluna 0 assumindo "Revisão", propagação de TAGs na coluna 2 e filtro de rodapés industriais.
Com esta atualização, o extrator passará a utilizar o modo **Genérico / Universal como padrão**, reservando o tratamento de LE/LI para quando a flag `--profile le_li` for informada.

## 2. Functional Requirements
- **Modo Genérico Padrão (`generic`)**:
  - Por padrão, a ferramenta processará qualquer PDF sem assumir estruturas de colunas específicas (sem assumir coluna 0 como "Rev." ou coluna 2 como "TAG").
  - Aplicará apenas sanitização neutra: remoção de quebras de linha (`\n`), normalização de espaços duplos e remoção de linhas vazias.
  - Filtrará apenas rodapés genéricos comuns (ex: `"Página X de Y"`, `"Page X of Y"` ou números de página soltos no final).
- **Modo Perfil Específico (`--profile le_li` ou `--profile generic`)**:
  - Permitir a passagem de parâmetro de perfil via CLI (ex: `--profile le_li` para ativar as regras industriais de LE/LI existentes em `cleaner.py`).
  - Manter retrocompatibilidade total com as extrações de arquivos LE/LI (`R11.01-2151-LE-0001_2.pdf` e `R11.01-2151-LI-0001_3-1.pdf`).
- **Configuração e Arquitetura**:
  - Refatorar `cleaner.py` para separar as funções de limpeza em `clean_generic_table_rows` e `clean_le_li_table_rows` (ou via estratégias/perfis extensíveis).
  - Atualizar `models.py` e `cli.py` para aceitar a opção `--profile` (valores aceitos: `generic`, `le_li`).

## 3. Non-Functional Requirements
- **Manutenibilidade**: Código desacoplado permitindo incluir novos perfis de extração no futuro.
- **Desempenho**: Nenhuma regressão de tempo na extração `pdfplumber`.
- **Integridade de Dados**: Garantir que tabelas de PDFs não industriais não sofram corrupção de valores em colunas genéricas.

## 4. Acceptance Criteria
- [ ] Extração de PDF genérico preserva integralmente os dados de todas as colunas.
- [ ] `--profile le_li` mantém o comportamento de mesclagem e sanitização industrial.
- [ ] Todos os testes automatizados (`pytest`) passam com sucesso.
