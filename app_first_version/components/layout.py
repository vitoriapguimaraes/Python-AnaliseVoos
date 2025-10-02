from dash import html, dcc
from components.header import create_header
from components.big_numbers import create_big_numbers
from components.charts import create_metric_selector, create_charts_container, create_map_container

def create_layout(df):
    return html.Div([
        create_header(),
        create_big_numbers(df),
        
        html.Div([
            html.H2("📈 Análise de Distribuições", className="section-title"),
            create_metric_selector(),
            create_charts_container(),
        ], className="charts-section"),
        
        create_map_container(),
        
        # Componente hidden para callbacks (removido, não é mais necessário)
        # dcc.Store(id='selected-metric', data='avg_delay')
        
    ], className="main-container")