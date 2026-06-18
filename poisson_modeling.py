import pandas as pd
import numpy as np
import holidays
import os
from scipy.stats import poisson, chisquare

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

resumo_resultados = []

# Ajuste o caminho se necessário
caminho_arquivo = r'datatran2025.csv'

df_bruto = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
df_bruto['br'] = pd.to_numeric(df_bruto['br'], errors='coerce')
df_bruto['data_inversa'] = pd.to_datetime(df_bruto['data_inversa'], errors='coerce')
df_bruto = df_bruto.dropna(subset=['data_inversa'])

rodovia_alvo = 101
estado_alvo = 'AL'

df_base = df_bruto[(df_bruto['br'] == rodovia_alvo) & (df_bruto['uf'] == estado_alvo)].copy()

calendario = pd.DataFrame({
    'data_inversa': pd.date_range('2025-01-01', '2025-12-31', freq='D')
})

condicoes_chuva = ['Chuva', 'Garoa/Chuvisco', 'Nevoeiro/Neblina']
dias_com_chuva = df_base[df_base['condicao_metereologica'].isin(condicoes_chuva)]['data_inversa'].dt.normalize().unique()

calendario['is_fds'] = calendario['data_inversa'].dt.dayofweek.isin([5,6])
feriados_br = holidays.Brazil(years=[2025])
calendario['is_feriado'] = calendario['data_inversa'].dt.date.isin(feriados_br.keys())
calendario['is_chuva'] = calendario['data_inversa'].dt.normalize().isin(dias_com_chuva)
calendario['alta_sazonalidade'] = calendario['is_fds'] | calendario['is_feriado'] | calendario['is_chuva']

df_graves = df_base[(df_base['feridos_graves'] > 0) | (df_base['mortos'] > 0)].copy()

contagem = df_graves.groupby('data_inversa').size().reset_index(name='qtd_acidentes')

df_final = calendario.merge(contagem, on='data_inversa', how='left')
df_final['qtd_acidentes'] = df_final['qtd_acidentes'].fillna(0).astype(int)

def testar_aderencia_poisson(df_cenario, nome_cenario):
    total_dias = len(df_cenario)
    lambda_empirico = df_cenario['qtd_acidentes'].mean()

    max_acidentes = int(df_cenario['qtd_acidentes'].max())
    categorias = pd.DataFrame({'Qtd_Acidentes_no_Dia': np.arange(0, max_acidentes + 1)})

    observados = df_cenario['qtd_acidentes'].value_counts().sort_index().reset_index()
    observados.columns = ['Qtd_Acidentes_no_Dia', 'Dias_Observados']

    freq = categorias.merge(observados, on='Qtd_Acidentes_no_Dia', how='left')
    freq['Dias_Observados'] = freq['Dias_Observados'].fillna(0).astype(int)

    freq['Probabilidade_Poisson'] = poisson.pmf(freq['Qtd_Acidentes_no_Dia'], lambda_empirico)
    freq['Dias_Esperados'] = freq['Probabilidade_Poisson'] * total_dias

    freq.loc[freq.index[-1], 'Dias_Esperados'] += total_dias - freq['Dias_Esperados'].sum()

    freq_teste = freq.copy()
    while len(freq_teste) > 2 and freq_teste['Dias_Esperados'].min() < 5:
        freq_teste.iloc[-2, freq_teste.columns.get_loc('Dias_Observados')] += freq_teste.iloc[-1]['Dias_Observados']
        freq_teste.iloc[-2, freq_teste.columns.get_loc('Dias_Esperados')] += freq_teste.iloc[-1]['Dias_Esperados']
        freq_teste = freq_teste.iloc[:-1]

    f_obs = freq_teste['Dias_Observados'].values
    f_esp = freq_teste['Dias_Esperados'].values
    f_esp = f_esp * (f_obs.sum() / f_esp.sum())

    chi2_stat, p_value = chisquare(f_obs=f_obs, f_exp=f_esp)

    resumo_resultados.append({
        'cenario': nome_cenario,
        'lambda': lambda_empirico,
        'chi2': chi2_stat,
        'p_value': p_value,
        'total_dias': total_dias,
        'total_acidentes': int(df_cenario['qtd_acidentes'].sum())
    })

    freq.to_csv(
        os.path.join(OUTPUT_DIR, f"poisson_{nome_cenario.lower().replace(' ', '_')}.csv"),
        sep=';', decimal=',', index=False
    )

testar_aderencia_poisson(df_final[df_final['alta_sazonalidade'] == False], "Dias Normais")
testar_aderencia_poisson(df_final[df_final['alta_sazonalidade'] == True], "Dias Sazonais")

pd.DataFrame(resumo_resultados).to_csv(
    os.path.join(OUTPUT_DIR, "summary.csv"),
    sep=';', decimal=',', index=False
)

print("Concluído.")
