from dash import dcc, html
import plotly.express as px

def create_metric_selector():
    """Cria os botões de seleção de métrica lado a lado"""
    return html.Div([
        html.Label("Selecione a métrica para análise:", className="metric-selector-label"),
        dcc.RadioItems(
            id='metric-selector',
            options=[
                {'label': '⏱️ Média de Atraso', 'value': 'avg_delay'},
                {'label': '🔢 Quantidade de Atrasos', 'value': 'delay_count'},
                {'label': '❌ Quantidade de Cancelamentos', 'value': 'cancelled_count'},
                {'label': '🔄 Quantidade de Desvios', 'value': 'diverted_count'}
            ],
            value='avg_delay',
            labelStyle={'display': 'inline-block', 'margin-right': '15px', 'padding': '10px 15px'},
            className="metric-radio-items"
        )
    ], className="metric-selector-wrapper")

def create_charts_container():
    """Container para todos os gráficos"""
    return html.Div([
        # Linha 1
        html.Div([
            html.Div([dcc.Graph(id='top-airlines-chart')], className='chart-column'),
            html.Div([dcc.Graph(id='top-cities-chart')], className='chart-column'),
        ], className='charts-row'),
        
        # Linha 2
        html.Div([
            html.Div([dcc.Graph(id='top-states-chart')], className='chart-column'),
            html.Div([dcc.Graph(id='distance-chart')], className='chart-column'),
        ], className='charts-row'),
        
        # Linha 3
        html.Div([
            html.Div([dcc.Graph(id='day-of-month-chart')], className='chart-column'),
            html.Div([dcc.Graph(id='day-of-week-chart')], className='chart-column'),
        ], className='charts-row'),
        
        # Linha 4
        html.Div([
            html.Div([dcc.Graph(id='hour-chart')], className='chart-column'),
            html.Div([dcc.Graph(id='time-period-chart')], className='chart-column'),
        ], className='charts-row'),
    ], id='charts-container')

def create_map_container():
    """Container para o mapa"""
    return html.Div([
        html.H2("🗺️ Visualização Geográfica", className="section-title"),
        dcc.Graph(id='map-chart')
    ], className="map-container")