# Análise de Acidentes na BR-101/AL com Distribuição de Poisson

Este repositório contém um pipeline completo de análise estatística de acidentes graves na BR-101/AL, utilizando modelagem com Distribuição de Poisson e teste de aderência qui-quadrado, além da geração de gráficos comparativos entre dados observados e esperados.

## Estrutura do projeto


.
├── datatran2025.csv # Base bruta de dados (PRF)
├── output/ # Resultados gerados (CSV e resumo estatístico)
├── charts/ # Gráficos gerados automaticamente
├── script_analise.py # Processamento e teste estatístico
├── script_graficos.py # Geração dos gráficos


## Dependências

Instale as bibliotecas necessárias:

```bash
pip install pandas numpy matplotlib scipy holidays
```
Como executar o projeto
1. Rodar a análise estatística

Este script:

Filtra acidentes na BR-101/AL
Classifica dias normais vs. dias de alta sazonalidade
Calcula λ (lambda) empírico
Aplica teste qui-quadrado de aderência à Poisson
Gera arquivos CSV com resultados
python script_analise.py

Saída gerada em:

output/
├── poisson_dias_normais.csv
├── poisson_dias_sazonais.csv
├── summary.csv
2. Gerar os gráficos

Este script:

Lê os arquivos gerados no passo anterior
Compara dados observados vs esperados (Poisson)
Plota curva teórica
Exibe estatísticas do teste (λ, χ², p-valor)
Exporta gráficos em PNG e PDF
python script_graficos.py

Saída gerada em:

charts/
├── br101_dias_normais.png/pdf
├── br101_dias_sazonais.png/pdf
Metodologia
Classificação dos dias

Os dias são divididos em dois cenários:

Dias Normais
Dias de Alta Sazonalidade:
Finais de semana
Feriados nacionais (2025)
Dias com chuva/neblina/garoa
Modelagem estatística

Para cada cenário:

Estima-se o parâmetro λ (lambda), a média de acidentes por dia.
Calcula-se a distribuição de Poisson teórica.
Compara-se observado vs esperado.
Aplica-se o teste qui-quadrado de aderência.
Interpretação do teste
p-value > 0.05: não há evidência para rejeitar a aderência à Poisson
p-value ≤ 0.05: rejeita-se a aderência à Poisson
Fonte dos dados
PRF – DATATRAN 2025
Trecho: BR-101/AL
Apenas acidentes com feridos graves ou óbitos
Objetivo do projeto

Avaliar se a ocorrência de acidentes graves em rodovias pode ser modelada por um processo de Poisson e como fatores externos influenciam essa distribuição.

Licença

Este projeto está licenciado sob a Licença MIT.

Veja o arquivo LICENSE para mais detalhes.
