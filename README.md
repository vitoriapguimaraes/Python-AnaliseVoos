# Dashboard de Análise de Voos

> Análise aprofundada de padrões problemáticos de voos (Janeiro/2023). O projeto envolveu segmentação de dados, validação de hipóteses, cálculo de risco relativo e aplicação de modelos de regressão para identificar fatores de atraso. Resultado: Dashboard interativo (deploy) e notebook de análise completo.

Desenvolvido em parceria com [Ianna Lise Castro de Paiva](https://github.com/iannacastro).

![Demonstração do sistema](https://github.com/vitoriapguimaraes/Python-AnaliseVoos/blob/main/project_development/results/display_notebook.gif)

## Funcionalidades Principais

O dashboard é dividido em três seções principais para uma análise abrangente:

- **Big Numbers**: Visão geral com as principais métricas de voos, como total de voos, atraso médio, percentual de voos com atraso, cancelados e desviados.
- **Análise de Distribuições**: Seção interativa que permite ao usuário selecionar uma métrica (Média de Atraso, Quantidade de Atrasos, Quantidade de Cancelamentos, Quantidade de Desvios) e visualizar sua distribuição em relação a diversas categorias, como companhias aéreas, cidades, estados, distância, dia do mês, dia da semana e hora do dia.
- **Visualização Geográfica**: Um mapa interativo que exibe rotas de voos, com pontos de origem e destino, onde o tamanho e a cor dos pontos podem representar a métrica selecionada, oferecendo insights geográficos sobre as operações.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Dash**: Framework para construção de aplicações web analíticas.
- **Plotly**: Biblioteca para criação de gráficos interativos e visualizações de dados.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **CSS**: Estilização customizada para um design moderno e responsivo.

## Como Executar

Para configurar e executar o dashboard localmente, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/vitoriapguimaraes/Python-AnaliseVoos
    cd Python-AnaliseVoos
    ```

2.  **Instale as dependências:**
    Certifique-se de ter o `pip` instalado. Em seguida, instale as bibliotecas necessárias:
    ```bash
    pip install requirements.txt
    ```

> Versão dash
3.  **Execute o projeto:**
    Navegue até o diretório raiz do projeto e execute o arquivo principal da aplicação:
    ```bash
    python app.py
    ```

4.  **Acesse o dashboard:**
    Após a execução, o dashboard estará disponível no seu navegador. Abra a seguinte URL:
    ```
    http://localhost:8050
    ```
> Versão em notebook
5. Configura o **notebook do dashboard** em `app_notebook_version.ipynb.ipynb`

## Como Usar

Ao acessar o dashboard, você encontrará:

-   **Big Numbers**: Na parte superior, um resumo das principais métricas de voos.
-   **Seleção de Métricas**: Abaixo dos Big Numbers, há quatro botões retangulares (`⏱️ Média de Atraso`, `🔢 Quantidade de Atrasos`, `❌ Quantidade de Cancelamentos`, `🔄 Quantidade de Desvios`). Clique em um deles para alterar a métrica que será visualizada nos gráficos de distribuição e no mapa.
-   **Gráficos de Distribuição**: Uma série de gráficos de barras e linhas que se atualizam dinamicamente com base na métrica selecionada, mostrando a distribuição por diversas categorias.
-   **Mapa Geográfico**: Na parte inferior, um mapa interativo que visualiza as rotas de voos e a intensidade da métrica selecionada por localização.

## Estrutura de Diretórios

```
/repo
├── app_notebook_version        # Dashboard em versão notebook
├── project_development/        # Arquivos notebook do desenvolvimento e resultados das análises
├── app_deploy/
│   ├── app.py                  # Aplicação principal Dash
│   ├── assets/
│   │   ├── custom.js           # JavaScript customizado
│   │   └── style.css           # Estilos CSS do dashboard
│   ├── callbacks/
│   │   └── chart_callbacks.py  # Lógica dos callbacks para atualização dos gráficos
│   ├── components/
│   │   ├── big_numbers.py      # Componente para os cartões de grandes números
│   │   ├── charts.py           # Componentes para gráficos e seleção de métricas
│   │   ├── header.py           # Componente do cabeçalho
│   │   └── layout.py           # Layout principal do dashboard
│   └── utils/
│       └── data_processing.py  # Funções de processamento e preparação de dados
├── LICENSE
└── README.md
```

## Status

- 🚧 Em desenvolvimento

## Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.
