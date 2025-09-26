# Dashboard de Análise de Voos

Este dashboard foi desenvolvido em Python usando Dash e Plotly para análise interativa de dados de voos.

## Funcionalidades

### 📊 Parte 1 - Big Numbers

- **Total de Voos**: Número total de voos na base de dados
- **Atraso Médio**: Tempo médio de atraso em minutos
- **Voos com Atraso**: Percentual de voos que tiveram atraso
- **Voos Cancelados**: Percentual de voos cancelados
- **Voos Desviados**: Percentual de voos desviados

### 📈 Parte 2 - Análise de Distribuições

Seletor interativo de métricas com as seguintes opções:

- **Média de Atraso**: Atraso médio em minutos
- **Quantidade de Atrasos**: Número total de atrasos
- **Quantidade de Cancelamentos**: Número total de cancelamentos
- **Quantidade de Desvios**: Número total de desvios

Para cada métrica selecionada, são exibidos gráficos de:

- Top 10 Companhias
- Top 10 Cidades de Origem
- Top 10 Estados de Origem
- Distribuição por Faixa de Distância
- Variação por Dia do Mês
- Variação por Dia da Semana
- Variação por Hora do Dia
- Variação por Período do Dia

### 🗺️ Parte 3 - Visualização Geográfica

Mapa interativo que mostra:

- Localização dos aeroportos de origem
- Tamanho dos pontos proporcional ao número de voos
- Cor dos pontos baseada na métrica selecionada
- Informações detalhadas no hover

## Estrutura dos Dados

O dashboard utiliza o arquivo `df_view.csv` com as seguintes colunas:

- `FL_DATE`: Data do voo
- `FL_DAY`: Dia do voo
- `ORIGIN_CITY`: Cidade de origem
- `ORIGIN_STATE`: Estado de origem
- `DEST_CITY`: Cidade de destino
- `CANCELLED`: Voo cancelado (binário)
- `DIVERTED`: Voo desviado (binário)
- `DELAY`: Voo atrasado (binário)
- `DISTANCE`: Distância percorrida
- `AIRLINE_Description`: Nome da companhia
- `DELAY_OVERALL`: Atraso em minutos
- `TIME_PERIOD`: Período do dia
- `DAY_OF_WEEK`: Dia da semana
- `TIME_HOUR`: Hora do voo
- `ORIGIN_LAT`, `ORIGIN_LON`: Coordenadas do aeroporto de origem
- `DEST_LAT`, `DEST_LON`: Coordenadas do aeroporto de destino

## Como Executar

1. Instale as dependências:

```bash
pip install dash plotly pandas
```

2. Execute o dashboard:

```bash
python dashboard_app.py
```

3. Acesse no navegador:

```
http://localhost:8050
```

## Arquivos

- `dashboard_app.py`: Código principal do dashboard
- `dataset/created/df_view.csv`: Dados
- `README.md`: Esta documentação

## Características Técnicas

- **Framework**: Dash (Python)
- **Visualizações**: Plotly
- **Responsividade**: Layout adaptável
- **Interatividade**: Callbacks para atualização dinâmica dos gráficos
- **Estilo**: CSS customizado para visual profissional
- **Performance**: Otimizado para datasets grandes com amostragem

## Personalização

Para usar com seus próprios dados:

1. Substitua o arquivo `dataset/created/df_view_sample.csv` pelo seu dataset
2. Ajuste o caminho no código se necessário
3. Verifique se as colunas estão no formato esperado

O dashboard é totalmente customizável e pode ser adaptado para diferentes tipos de análise de dados de transporte.
