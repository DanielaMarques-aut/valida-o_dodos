import os
import pandas as pd

# ============================================================
# 1. Carregar ficheiro
#    - Verifica se o ficheiro existe
#    - Tenta ler o Excel
# ============================================================
def carregar_ficheiro(caminho):
    if not os.path.exists(caminho):
        return None, False
    try:
        df = pd.read_excel(caminho)
        return df, True
    except:
        return None, False


# ============================================================
# 2. Validar colunas obrigatórias
#    - Compara colunas esperadas com as colunas reais
# ============================================================
def validar_colunas(df, colunas_esperadas):
    colunas_faltam = [c for c in colunas_esperadas if c not in df.columns]
    return colunas_faltam


# ============================================================
# 3. Corrigir tipos de dados
#    - ID → inteiro (valores inválidos viram NaN)
#    - Outras colunas → texto
# ============================================================
def corrigir_tipos(df, tipos_esperados):
    for coluna, tipo in tipos_esperados.items():
        if coluna in df.columns:
            if tipo == "int":
                df[coluna] = pd.to_numeric(df[coluna], errors="coerce").astype("Int64")
            elif tipo == "str":
                df[coluna] = df[coluna].astype(str)
    return df


# ============================================================
# 4. Detetar erros por linha
#    - Marca linhas que têm pelo menos um NaN
# ============================================================
def detetar_erros_linha(df):
    df["Tem_Erros"] = df.isna().any(axis=1)
    return df


# ============================================================
# 5. Gerar relatório de validação
#    - Cria tabela com verificações, resultados e detalhes
#    - Adiciona coluna Estado (OK/ERRO)
# ============================================================
def gerar_relatorio(ficheiro_existe, colunas_faltam, df):
    linhas = [
        {
            "Verificação": "Ficheiro existe",
            "Resultado": ficheiro_existe,
            "Detalhes": "" if ficheiro_existe else "Ficheiro não encontrado"
        },
        {
            "Verificação": "Colunas em falta",
            "Resultado": len(colunas_faltam) == 0,
            "Detalhes": ", ".join(colunas_faltam) if colunas_faltam else "Nenhuma"
        },
        {
            "Verificação": "Valores nulos",
            "Resultado": df.isna().sum().sum() == 0,
            "Detalhes": str(df.isna().sum().to_dict())
        }
    ]

    relatorio = pd.DataFrame(linhas)
    relatorio["Estado"] = relatorio["Resultado"].apply(lambda x: "OK" if x else "ERRO")
    return relatorio


# ============================================================
# 6. Ordenar relatório
#    - Coloca linhas com ERRO primeiro
# ============================================================
def ordenar_relatorio(relatorio):
    return relatorio.sort_values(by="Estado", ascending=True)


# ============================================================
# 7. Aplicar cores ao relatório
#    - ERRO → vermelho
#    - OK → verde
# ============================================================
def aplicar_cores_relatorio(relatorio):
    def colorir_estado(row):
        if row["Estado"] == "ERRO":
            return ["background-color: #ff9999"] * len(row)
        else:
            return ["background-color: #b3ffb3"] * len(row)

    return relatorio.style.apply(colorir_estado, axis=1)


# ============================================================
# 8. Pipeline principal
#    - Junta todas as etapas
#    - Devolve:
#         • linhas com erros
#         • linhas sem erros
#         • relatório final (DataFrame)
#         • relatório colorido (Styler)
# ============================================================
def pipeline_principal(caminho, colunas_esperadas, tipos_esperados):
    df, ficheiro_existe = carregar_ficheiro(caminho)

    if not ficheiro_existe:
        print("Erro: ficheiro não encontrado.")
        return None, None, None, None

    colunas_faltam = validar_colunas(df, colunas_esperadas)
    df = corrigir_tipos(df, tipos_esperados)
    df = detetar_erros_linha(df)

    linhas_com_erros = df[df["Tem_Erros"]]
    linhas_sem_erros = df[~df["Tem_Erros"]]

    relatorio = gerar_relatorio(ficheiro_existe, colunas_faltam, df)
    relatorio = ordenar_relatorio(relatorio)
    relatorio_colorido = aplicar_cores_relatorio(relatorio)

    return linhas_com_erros, linhas_sem_erros, relatorio, relatorio_colorido