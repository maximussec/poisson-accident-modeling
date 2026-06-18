import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# CONFIGURAÇÃO

INPUT_DIR = "output"
CHARTS_DIR = "charts"

os.makedirs(CHARTS_DIR, exist_ok=True)

print("Iniciando geração de gráficos...")
print(f"Lendo arquivos de: {INPUT_DIR}")
print(f"Salvando gráficos em: {CHARTS_DIR}")

# FUNÇÃO DE GERAÇÃO DOS GRÁFICOS

def plot_distribuicao_dinamica(
    arquivo_csv,
    cenario,
    subtitulo,
    nome_saida
):

    caminho_csv = os.path.join(
        INPUT_DIR,
        arquivo_csv
    )

    caminho_resumo = os.path.join(
        INPUT_DIR,
        "summary.csv"
    )

    if not os.path.exists(caminho_csv):
        print(f"ERRO: Arquivo não encontrado: {caminho_csv}")
        return

    if not os.path.exists(caminho_resumo):
        print(f"ERRO: Arquivo não encontrado: {caminho_resumo}")
        return

    # =================================================
    # LEITURA DOS DADOS
    # =================================================

    df = pd.read_csv(
        caminho_csv,
        sep=';',
        decimal=','
    )

    resumo = pd.read_csv(
        caminho_resumo,
        sep=';',
        decimal=','
    )

    linha = resumo[
        resumo['cenario'] == cenario
    ].iloc[0]

    lambda_est = linha['lambda']
    chi2_stat = linha['chi2']
    p_value = linha['p_value']

    # =================================================
    # RESULTADO DO TESTE
    # =================================================

    if p_value > 0.05:
        resultado = "✓ Aderência à Distribuição de Poisson"
    else:
        resultado = "✗ Aderência Rejeitada"

    # =================================================
    # PREPARAÇÃO DOS DADOS
    # =================================================

    pos = np.arange(
        0,
        int(df['Qtd_Acidentes_no_Dia'].max()) + 1
    )

    df_plot = (
        df
        .set_index('Qtd_Acidentes_no_Dia')
        .reindex(pos)
        .fillna(0)
        .reset_index()
    )

    # =================================================
    # CRIAÇÃO DO GRÁFICO
    # =================================================

    plt.figure(figsize=(11, 6))

    largura_barra = 0.40

    # Dados observados

    plt.bar(
        pos - largura_barra / 2,
        df_plot['Dias_Observados'],
        largura_barra,
        label='Dados Observados',
        color='#4472C4',
        edgecolor='black'
    )

    # Distribuição esperada

    plt.bar(
        pos + largura_barra / 2,
        df_plot['Dias_Esperados'],
        largura_barra,
        label='Distribuição de Poisson Esperada',
        color='#D9D9D9',
        edgecolor='black',
        hatch='//'
    )

    # Curva teórica

    plt.plot(
        pos,
        df_plot['Dias_Esperados'],
        color='black',
        marker='o',
        markersize=7,
        markerfacecolor='black',
        markeredgecolor='black',
        linestyle='--',
        linewidth=2.2,
        label='Curva Teórica'
    )

    # =================================================
    # TÍTULOS
    # =================================================

    plt.suptitle(
        'Distribuição de Acidentes Graves na BR-101/AL',
        fontsize=16,
        fontweight='bold'
    )

    plt.title(
        subtitulo,
        fontsize=12
    )

    # =================================================
    # EIXOS
    # =================================================

    plt.xlabel(
        'Quantidade de Acidentes Graves por Dia',
        fontsize=11,
        fontweight='bold'
    )

    plt.ylabel(
        'Número de Dias',
        fontsize=11,
        fontweight='bold'
    )

    # Eixo X discreto (sem 0.5, 1.5, 2.5...)

    plt.xticks(
        pos,
        [str(i) for i in pos]
    )

    plt.xlim(
        -0.5,
        max(pos) + 0.5
    )

    # =================================================
    # CAIXA ESTATÍSTICA
    # =================================================

    texto_estatistico = (
        f"λ = {lambda_est:.3f}\n"
        f"χ² = {chi2_stat:.3f}\n"
        f"p-valor = {p_value:.4f}\n\n"
        f"{resultado}"
    )

    plt.text(
        0.98,
        0.96,
        texto_estatistico,
        transform=plt.gca().transAxes,
        horizontalalignment='right',
        verticalalignment='top',
        bbox=dict(
            facecolor='white',
            edgecolor='black',
            pad=6
        ),
        fontsize=11
    )

    # =================================================
    # GRADE
    # =================================================

    plt.grid(
        axis='y',
        linestyle=':',
        alpha=0.5
    )

    # =================================================
    # LEGENDA
    # =================================================

    plt.legend(
        loc='center right',
        frameon=True,
        fontsize=11
    )

    # =================================================
    # RODAPÉ
    # =================================================

    plt.figtext(
        0.01,
        0.01,
        (
            "Fonte: Polícia Rodoviária Federal (DATATRAN 2025)\n"
            "Trecho analisado: BR-101/AL\n"
            "Acidentes graves (feridos graves ou óbitos)"
        ),
        fontsize=8
    )

    # =================================================
    # EXPORTAÇÃO
    # =================================================

    caminho_png = os.path.join(
        CHARTS_DIR,
        nome_saida
    )

    caminho_pdf = caminho_png.replace(
        ".png",
        ".pdf"
    )

    plt.tight_layout()

    plt.savefig(
        caminho_png,
        dpi=600,
        bbox_inches='tight'
    )

    plt.savefig(
        caminho_pdf,
        bbox_inches='tight'
    )

    plt.close()

    print(f"✓ PNG salvo: {caminho_png}")
    print(f"✓ PDF salvo: {caminho_pdf}")

# EXECUÇÃO

plot_distribuicao_dinamica(
    arquivo_csv='poisson_dias_normais.csv',
    cenario='Dias Normais',
    subtitulo='Dias Normais',
    nome_saida='br101_dias_normais.png'
)

plot_distribuicao_dinamica(
    arquivo_csv='poisson_dias_sazonais.csv',
    cenario='Dias Sazonais',
    subtitulo='Alta Sazonalidade (Finais de Semana, Feriados e Chuva)',
    nome_saida='br101_dias_sazonais.png'
)

print("\nGráficos gerados com sucesso.")
print(f"Arquivos disponíveis em: {CHARTS_DIR}")