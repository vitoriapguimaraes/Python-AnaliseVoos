import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Carregando os dados
print("Carregando dados...")
df = pd.read_csv("dataset/created/df_view.csv")
print(f"Dados carregados: {len(df)} registros")

# Inicializando o app Dash
app = dash.Dash(__name__)

# Função para calcular big numbers
def calculate_big_numbers(df):
    total_flights = len(df)
    avg_delay = df['DELAY_OVERALL'].mean()
    delay_percentage = (df['DELAY'].sum() / total_flights) * 100
    cancelled_percentage = (df['CANCELLED'].sum() / total_flights) * 100
    diverted_percentage = (df['DIVERTED'].sum() / total_flights) * 100
    
    return {
        'total_flights': total_flights,
        'avg_delay': avg_delay,
        'delay_percentage': delay_percentage,
        'cancelled_percentage': cancelled_percentage,
        'diverted_percentage': diverted_percentage
    }

# Função para criar o mapa
def create_map(df, metric='avg_delay'):
    if metric == 'avg_delay':
        agg_dict = {'DELAY_OVERALL': 'mean'}
        color_col = 'DELAY_OVERALL'
        title = "Atraso Médio por Aeroporto de Origem"
        color_title = "Atraso Médio (min)"
    elif metric == 'delay_count':
        agg_dict = {'DELAY': 'sum'}
        color_col = 'DELAY'
        title = "Quantidade de Atrasos por Aeroporto de Origem"
        color_title = "Quantidade de Atrasos"
    elif metric == 'cancelled_count':
        agg_dict = {'CANCELLED': 'sum'}
        color_col = 'CANCELLED'
        title = "Quantidade de Cancelamentos por Aeroporto de Origem"
        color_title = "Quantidade de Cancelamentos"
    elif metric == 'diverted_count':
        agg_dict = {'DIVERTED': 'sum'}
        color_col = 'DIVERTED'
        title = "Quantidade de Desvios por Aeroporto de Origem"
        color_title = "Quantidade de Desvios"
    
    # Agregar dados por aeroporto de origem
    agg_dict.update({
        'ORIGIN_LAT': 'first',
        'ORIGIN_LON': 'first',
        'FL_DATE': 'count'  # Total de voos
    })
    
    airport_data = (df.groupby('ORIGIN_CITY')
                   .agg(agg_dict)
                   .rename(columns={'FL_DATE': 'TOTAL_VOOS'})
                   .reset_index())
    
    # Filtrar apenas aeroportos com dados válidos
    airport_data = airport_data.dropna(subset=['ORIGIN_LAT', 'ORIGIN_LON'])
    
    # Criar o mapa
    fig = px.scatter_mapbox(
        airport_data,
        lat="ORIGIN_LAT",
        lon="ORIGIN_LON",
        size="TOTAL_VOOS",
        color=color_col,
        hover_name="ORIGIN_CITY",
        hover_data={
            color_col: ":.1f" if metric == 'avg_delay' else True,
            "TOTAL_VOOS": True,
            "ORIGIN_LAT": False,
            "ORIGIN_LON": False
        },
        color_continuous_scale="RdYlGn_r",
        size_max=15,
        zoom=3,
        height=600,
        title=title
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(
            title=color_title,
            thickness=15
        )
    )
    
    return fig

# Calculando os big numbers
print("Calculando métricas...")
big_numbers = calculate_big_numbers(df)

# Estilos CSS customizados
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Dashboard de Análise de Voos", 
                style={
                    'textAlign': 'center', 
                    'color': '#2c3e50', 
                    'marginBottom': '30px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '2.5em',
                    'fontWeight': 'bold'
                })
    ]),
    
    # PARTE 1 - BIG NUMBERS
    html.Div([
        html.H2("📊 Resumo Geral", 
                style={
                    'color': '#34495e', 
                    'marginBottom': '20px',
                    'fontFamily': 'Arial, sans-serif'
                }),
        
        # Primeira linha de métricas
        html.Div([
            # Total de voos
            html.Div([
                html.H3(f"{big_numbers['total_flights']:,}", 
                        style={
                            'fontSize': '2.5em', 
                            'color': '#3498db', 
                            'margin': '0',
                            'fontWeight': 'bold'
                        }),
                html.P("Total de Voos", 
                       style={
                           'fontSize': '1.2em', 
                           'color': '#7f8c8d',
                           'margin': '5px 0'
                       })
            ], style={
                'textAlign': 'center', 
                'padding': '20px', 
                'backgroundColor': '#ecf0f1', 
                'borderRadius': '10px', 
                'margin': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '30%',
                'display': 'inline-block'
            }),
            
            # Média de atrasos
            html.Div([
                html.H3(f"{big_numbers['avg_delay']:.1f} min", 
                        style={
                            'fontSize': '2.5em', 
                            'color': '#e74c3c', 
                            'margin': '0',
                            'fontWeight': 'bold'
                        }),
                html.P("Atraso Médio", 
                       style={
                           'fontSize': '1.2em', 
                           'color': '#7f8c8d',
                           'margin': '5px 0'
                       })
            ], style={
                'textAlign': 'center', 
                'padding': '20px', 
                'backgroundColor': '#ecf0f1', 
                'borderRadius': '10px', 
                'margin': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '30%',
                'display': 'inline-block'
            }),
            
            # Percentual de atrasos
            html.Div([
                html.H3(f"{big_numbers['delay_percentage']:.1f}%", 
                        style={
                            'fontSize': '2.5em', 
                            'color': '#f39c12', 
                            'margin': '0',
                            'fontWeight': 'bold'
                        }),
                html.P("Voos com Atraso", 
                       style={
                           'fontSize': '1.2em', 
                           'color': '#7f8c8d',
                           'margin': '5px 0'
                       })
            ], style={
                'textAlign': 'center', 
                'padding': '20px', 
                'backgroundColor': '#ecf0f1', 
                'borderRadius': '10px', 
                'margin': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '30%',
                'display': 'inline-block'
            }),
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Segunda linha de métricas
        html.Div([
            # Percentual de cancelamentos
            html.Div([
                html.H3(f"{big_numbers['cancelled_percentage']:.1f}%", 
                        style={
                            'fontSize': '2.5em', 
                            'color': '#e67e22', 
                            'margin': '0',
                            'fontWeight': 'bold'
                        }),
                html.P("Voos Cancelados", 
                       style={
                           'fontSize': '1.2em', 
                           'color': '#7f8c8d',
                           'margin': '5px 0'
                       })
            ], style={
                'textAlign': 'center', 
                'padding': '20px', 
                'backgroundColor': '#ecf0f1', 
                'borderRadius': '10px', 
                'margin': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '45%',
                'display': 'inline-block'
            }),
            
            # Percentual de desvios
            html.Div([
                html.H3(f"{big_numbers['diverted_percentage']:.1f}%", 
                        style={
                            'fontSize': '2.5em', 
                            'color': '#9b59b6', 
                            'margin': '0',
                            'fontWeight': 'bold'
                        }),
                html.P("Voos Desviados", 
                       style={
                           'fontSize': '1.2em', 
                           'color': '#7f8c8d',
                           'margin': '5px 0'
                       })
            ], style={
                'textAlign': 'center', 
                'padding': '20px', 
                'backgroundColor': '#ecf0f1', 
                'borderRadius': '10px', 
                'margin': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '45%',
                'display': 'inline-block'
            }),
        ], style={'textAlign': 'center', 'marginBottom': '40px'}),
    ], style={'marginBottom': '40px'}),
    
    # PARTE 2 - DISTRIBUIÇÕES BÁSICAS
    html.Div([
        html.H2("📈 Análise de Distribuições", 
                style={
                    'color': '#34495e', 
                    'marginBottom': '20px',
                    'fontFamily': 'Arial, sans-serif'
                }),
        
        # Seletor de variável
        html.Div([
            html.Label("Selecione a métrica para análise:", 
                      style={
                          'fontSize': '1.1em', 
                          'marginBottom': '10px',
                          'fontWeight': 'bold',
                          'color': '#2c3e50'
                      }),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': '⏱️ Média de Atraso', 'value': 'avg_delay'},
                    {'label': '🔢 Quantidade de Atrasos', 'value': 'delay_count'},
                    {'label': '❌ Quantidade de Cancelamentos', 'value': 'cancelled_count'},
                    {'label': '🔄 Quantidade de Desvios', 'value': 'diverted_count'}
                ],
                value='avg_delay',
                style={'marginBottom': '20px'}
            )
        ], style={'marginBottom': '30px'}),
        
        # Gráficos de distribuição em grid
        html.Div([
            html.Div([
                dcc.Graph(id='top-airlines-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                dcc.Graph(id='top-cities-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        
        html.Div([
            html.Div([
                dcc.Graph(id='top-states-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                dcc.Graph(id='distance-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        
        html.Div([
            html.Div([
                dcc.Graph(id='day-of-month-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                dcc.Graph(id='day-of-week-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        
        html.Div([
            html.Div([
                dcc.Graph(id='hour-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                dcc.Graph(id='time-period-chart')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
    ], style={'marginBottom': '40px'}),
    
    # PARTE 3 - VISUALIZAÇÃO DO MAPA
    html.Div([
        html.H2("🗺️ Visualização Geográfica", 
                style={
                    'color': '#34495e', 
                    'marginBottom': '20px',
                    'fontFamily': 'Arial, sans-serif'
                }),
        html.Div([
            dcc.Graph(id='map-chart')
        ], style={'padding': '10px'})
    ], style={'marginTop': '40px'}),
    
], style={
    'padding': '20px', 
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa'
})

# Callbacks para atualizar os gráficos baseados na métrica selecionada
@app.callback(
    [Output('top-airlines-chart', 'figure'),
     Output('top-cities-chart', 'figure'),
     Output('top-states-chart', 'figure'),
     Output('distance-chart', 'figure'),
     Output('day-of-month-chart', 'figure'),
     Output('day-of-week-chart', 'figure'),
     Output('hour-chart', 'figure'),
     Output('time-period-chart', 'figure'),
     Output('map-chart', 'figure')],
    [Input('metric-dropdown', 'value')]
)
def update_charts(selected_metric):
    
    def create_metric_data(df, group_col, metric):
        if metric == 'avg_delay':
            data = df.groupby(group_col)['DELAY_OVERALL'].mean().sort_values(ascending=False)
            title_suffix = "Atraso Médio (min)"
        elif metric == 'delay_count':
            data = df.groupby(group_col)['DELAY'].sum().sort_values(ascending=False)
            title_suffix = "Quantidade de Atrasos"
        elif metric == 'cancelled_count':
            data = df.groupby(group_col)['CANCELLED'].sum().sort_values(ascending=False)
            title_suffix = "Quantidade de Cancelamentos"
        elif metric == 'diverted_count':
            data = df.groupby(group_col)['DIVERTED'].sum().sort_values(ascending=False)
            title_suffix = "Quantidade de Desvios"
        
        return data, title_suffix
    
    # Top 10 Companhias
    airlines_data, title_suffix = create_metric_data(df, 'AIRLINE_Description', selected_metric)
    airlines_fig = px.bar(
        x=airlines_data.head(10).values,
        y=airlines_data.head(10).index,
        orientation='h',
        title=f'🏢 Top 10 Companhias - {title_suffix}',
        labels={'x': title_suffix, 'y': 'Companhia'},
        color=airlines_data.head(10).values,
        color_continuous_scale='RdYlGn_r'
    )
    airlines_fig.update_layout(
        height=400, 
        yaxis={'categoryorder': 'total ascending'},
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Top 10 Cidades de Origem
    cities_data, _ = create_metric_data(df, 'ORIGIN_CITY', selected_metric)
    cities_fig = px.bar(
        x=cities_data.head(10).values,
        y=cities_data.head(10).index,
        orientation='h',
        title=f'🏙️ Top 10 Cidades de Origem - {title_suffix}',
        labels={'x': title_suffix, 'y': 'Cidade'},
        color=cities_data.head(10).values,
        color_continuous_scale='RdYlGn_r'
    )
    cities_fig.update_layout(
        height=400, 
        yaxis={'categoryorder': 'total ascending'},
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Top 10 Estados de Origem
    states_data, _ = create_metric_data(df, 'ORIGIN_STATE', selected_metric)
    states_fig = px.bar(
        x=states_data.head(10).values,
        y=states_data.head(10).index,
        orientation='h',
        title=f'🗺️ Top 10 Estados de Origem - {title_suffix}',
        labels={'x': title_suffix, 'y': 'Estado'},
        color=states_data.head(10).values,
        color_continuous_scale='RdYlGn_r'
    )
    states_fig.update_layout(
        height=400, 
        yaxis={'categoryorder': 'total ascending'},
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Distância
    df_temp = df.copy()
    df_temp['DISTANCE_BIN'] = pd.cut(df_temp['DISTANCE'], bins=10, precision=0)
    distance_data, _ = create_metric_data(df_temp, 'DISTANCE_BIN', selected_metric)
    distance_fig = px.bar(
        x=[str(x) for x in distance_data.index],
        y=distance_data.values,
        title=f'✈️ Distância vs {title_suffix}',
        labels={'x': 'Faixa de Distância (milhas)', 'y': title_suffix},
        color=distance_data.values,
        color_continuous_scale='RdYlGn_r'
    )
    distance_fig.update_layout(
        height=400, 
        xaxis_tickangle=-45,
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Dia do Mês
    day_data, _ = create_metric_data(df, 'FL_DAY', selected_metric)
    day_fig = px.line(
        x=day_data.index,
        y=day_data.values,
        title=f'📅 Dia do Mês vs {title_suffix}',
        labels={'x': 'Dia do Mês', 'y': title_suffix}
    )
    day_fig.update_traces(line_color='#e74c3c', line_width=3)
    day_fig.update_layout(
        height=400,
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Dia da Semana
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_data, _ = create_metric_data(df, 'DAY_OF_WEEK', selected_metric)
    weekday_data = weekday_data.reindex(weekday_order, fill_value=0)
    weekday_fig = px.bar(
        x=weekday_data.index,
        y=weekday_data.values,
        title=f'📆 Dia da Semana vs {title_suffix}',
        labels={'x': 'Dia da Semana', 'y': title_suffix},
        color=weekday_data.values,
        color_continuous_scale='RdYlGn_r'
    )
    weekday_fig.update_layout(
        height=400,
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Hora do Dia
    hour_data, _ = create_metric_data(df, 'TIME_HOUR', selected_metric)
    hour_fig = px.line(
        x=hour_data.index,
        y=hour_data.values,
        title=f'🕐 Hora do Dia vs {title_suffix}',
        labels={'x': 'Hora', 'y': title_suffix}
    )
    hour_fig.update_traces(line_color='#3498db', line_width=3)
    hour_fig.update_layout(
        height=400,
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Período do Dia
    period_order = ['Early Morning', 'Morning', 'Afternoon', 'Evening']
    period_data, _ = create_metric_data(df, 'TIME_PERIOD', selected_metric)
    period_data = period_data.reindex(period_order, fill_value=0)
    period_fig = px.bar(
        x=period_data.index,
        y=period_data.values,
        title=f'🌅 Período do Dia vs {title_suffix}',
        labels={'x': 'Período', 'y': title_suffix},
        color=period_data.values,
        color_continuous_scale='RdYlGn_r'
    )
    period_fig.update_layout(
        height=400,
        title_font_size=16,
        font=dict(size=12)
    )
    
    # Mapa
    map_fig = create_map(df, selected_metric)
    
    return (airlines_fig, cities_fig, states_fig, distance_fig, 
            day_fig, weekday_fig, hour_fig, period_fig, map_fig)

if __name__ == '__main__':
    print("Iniciando dashboard...")
    app.run(debug=True, host='0.0.0.0', port=8050)

