# valida-o_dodos
Pipeline de Validação de Ficheiro de Projetos
Este repositório contém um pipeline modular de validação de dados utilizado para garantir a qualidade do ficheiro de projetos antes de ser integrado em processos operacionais. O pipeline verifica colunas obrigatórias, corrige tipos de dados, identifica linhas com erros e gera um relatório final ordenado e colorido para facilitar a revisão.

📌 Objetivo
Garantir que o ficheiro de projetos cumpre os requisitos mínimos de qualidade antes de ser processado por automações ou carregado em sistemas internos. O pipeline:
- valida a existência do ficheiro
- confirma colunas obrigatórias
- converte tipos de dados
- deteta valores inválidos ou ausentes
- separa linhas limpas e linhas com erros
- gera um relatório final com formatação por cor
  🧩 Colunas obrigatórias
O ficheiro de projetos deve conter as seguintes colunas:
- ID (inteiro)
- Nome (texto)
- Estado (texto)
- Responsável (texto)

⚙️ Funcionalidades do Pipeline
- Verificação da existência do ficheiro
- Validação de colunas obrigatórias
- Conversão automática de tipos
- Identificação de linhas com erros
- Separação entre dados limpos e dados problemáticos
- Relatório final com:
- resultado de cada verificação
- detalhes dos erros
- coluna Estado (OK/ERRO)
- ordenação por criticidade
- formatação por cor (verde/vermelho)

▶️ Como Executar
1. Importar o pipeline
from pipeline_validacao import pipeline_principal

colunas = ['ID', 'Nome', 'Estado', 'Responsável']
tipos = {'ID': 'int', 'Nome': 'str', 'Estado': 'str', 'Responsável': 'str'}


2. Executar o pipeline
linhas_com_erros, linhas_sem_erros, relatorio, relatorio_colorido = pipeline_principal(
    'projetos.xlsx',
    colunas,
    tipos
)


3. Visualizar resultados
print(linhas_com_erros)
print(linhas_sem_erros)
print(relatorio)


4. Exportar relatório com cores (opcional)
relatorio_colorido.to_excel('relatorio_validacao.xlsx', index=False)


Linhas com ERRO aparecem a vermelho.
Linhas com OK aparecem a verde.


