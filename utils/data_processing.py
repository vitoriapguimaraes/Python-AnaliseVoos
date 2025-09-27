import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from math import atan2, degrees
from sqlalchemy import create_engine
import os

def load_and_process_data_from_db():
    """Carrega dados do banco de dados PostgreSQL"""
    # Obter a URL do banco da variável de ambiente
    db_url = os.getenv('DB_URL')
    
    if not db_url:
        raise ValueError("DB_URL não encontrada nas variáveis de ambiente")
    
    # Criar conexão
    engine = create_engine(db_url)
    
    # Carregar dados da tabela 'flights'
    print("Conectando ao banco de dados...")
    query = "SELECT * FROM flights"
    df = pd.read_sql(query, engine)
    
    print(f"Dados carregados do banco: {len(df)} registros")

    if 'FL_DATE' in df.columns:
        df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    
    return df

def calculate_big_numbers(df):
    """Calcula as métricas principais"""
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

def create_metric_data(df, group_col, metric, observed=True):
    """Cria dados agrupados para métricas específicas"""
    if metric == 'avg_delay':
        data = df.groupby(group_col, observed=observed)['DELAY_OVERALL'].mean().sort_values(ascending=False)
        title_suffix = "Atraso Médio (min)"
    elif metric == 'delay_count':
        data = df.groupby(group_col, observed=observed)['DELAY'].sum().sort_values(ascending=False)
        title_suffix = "Quantidade de Atrasos"
    elif metric == 'cancelled_count':
        data = df.groupby(group_col, observed=observed)['CANCELLED'].sum().sort_values(ascending=False)
        title_suffix = "Quantidade de Cancelamentos"
    elif metric == 'diverted_count':
        data = df.groupby(group_col, observed=observed)['DIVERTED'].sum().sort_values(ascending=False)
        title_suffix = "Quantidade de Desvios"
    else:
        data = df.groupby(group_col, observed=observed)['DELAY_OVERALL'].mean().sort_values(ascending=False)
        title_suffix = "Atraso Médio (min)"
    
    return data, title_suffix

def calcular_direcao(lat1, lon1, lat2, lon2):
    """Calcula a direção entre dois pontos em graus"""
    d_lon = lon2 - lon1
    x = np.cos(np.radians(lat2)) * np.sin(np.radians(d_lon))
    y = np.cos(np.radians(lat1)) * np.sin(np.radians(lat2)) - np.sin(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.cos(np.radians(d_lon))
    direcao = degrees(atan2(x, y))
    return (direcao + 360) % 360

def criar_mapa_rotas_avancado(df, top_n=30, altura=800, selected_metric='avg_delay'):
    """
    Cria um mapa interativo das rotas de voo com setas - VERSÃO MELHORADA
    """
    
    metric_config = {
        'avg_delay': {
            'col': 'DELAY_OVERALL', 
            'agg': 'mean', 
            'title': 'Atraso Médio',
            'unit': 'min',
            'line_title': 'Intensidade do Atraso'
        },
        'delay_count': {
            'col': 'DELAY', 
            'agg': 'sum', 
            'title': 'Quantidade de Atrasos',
            'unit': 'voos',
            'line_title': 'Quantidade de Atrasos'
        },
        'cancelled_count': {
            'col': 'CANCELLED', 
            'agg': 'sum', 
            'title': 'Quantidade de Cancelamentos',
            'unit': 'voos',
            'line_title': 'Quantidade de Cancelamentos'
        },
        'diverted_count': {
            'col': 'DIVERTED', 
            'agg': 'sum', 
            'title': 'Quantidade de Desvios',
            'unit': 'voos',
            'line_title': 'Quantidade de Desvios'
        }
    }
    
    config = metric_config[selected_metric]
    
    # Agrupar por rota
    rotas_data = (
        df.groupby(["ORIGIN_CITY", "DEST_CITY", 
                   "ORIGIN_LAT", "ORIGIN_LON", "DEST_LAT", "DEST_LON"], 
                  as_index=False)
        .agg({
            config['col']: config['agg'],
            'TIME_HOUR': 'mean',
            'FL_DATE': 'count'
        })
        .rename(columns={'FL_DATE': 'TOTAL_VOOS'})
        .sort_values(by=config['col'], ascending=False)
        .head(top_n)
        .dropna(subset=['ORIGIN_LAT', 'ORIGIN_LON', 'DEST_LAT', 'DEST_LON'])
    )
    
    if rotas_data.empty:
        print("⚠️ Nenhuma rota válida encontrada para o mapa")
        return go.Figure()
    
    # Calcular ponto médio e direção
    rotas_data['MID_LAT'] = (rotas_data['ORIGIN_LAT'] + rotas_data['DEST_LAT']) / 2
    rotas_data['MID_LON'] = (rotas_data['ORIGIN_LON'] + rotas_data['DEST_LON']) / 2
    rotas_data['DIRECAO'] = rotas_data.apply(
        lambda x: calcular_direcao(x['ORIGIN_LAT'], x['ORIGIN_LON'], x['DEST_LAT'], x['DEST_LON']), 
        axis=1
    )
    
    # Normalizar métricas
    min_metrica = rotas_data[config['col']].min()
    max_metrica = rotas_data[config['col']].max()
    
    fig = go.Figure()
    
    # Adicionar cada rota ao mapa
    for idx, rota in rotas_data.iterrows():
        # Espessura da linha baseada na métrica
        if max_metrica > min_metrica:
            intensidade_linha = 2 + ((rota[config['col']] - min_metrica) / (max_metrica - min_metrica)) * 10
        else:
            intensidade_linha = 6
            
        # Cor baseada na hora do dia
        hora_media = rota['TIME_HOUR']
        intensidade_cor = (hora_media % 24) / 24
        cor = px.colors.sample_colorscale("Blues", [intensidade_cor])[0]
        
        # Linha da rota
        fig.add_trace(go.Scattergeo(
            lon=[rota['ORIGIN_LON'], rota['DEST_LON']],
            lat=[rota['ORIGIN_LAT'], rota['DEST_LAT']],
            mode='lines',
            line=dict(width=intensidade_linha, color=cor),
            name=f"{rota['ORIGIN_CITY']} → {rota['DEST_CITY']}",
            text=f"{rota['ORIGIN_CITY']} → {rota['DEST_CITY']}",
            customdata=[[rota[config['col']], rota['TIME_HOUR'], rota['TOTAL_VOOS']]],
            hovertemplate=(
                "<b>%{text}</b><br><br>"
                f"<b>{config['title']}:</b> %{{customdata[0]:.1f}} {config['unit']}<br>"
                "<b>Hora Média:</b> %{customdata[1]:.1f}h<br>"
                "<b>Total de Voos:</b> %{customdata[2]}<br>"
                "<b>Direção:</b> %{customdata[3]:.0f}°<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))
        
        # Seta no ponto médio
        fig.add_trace(go.Scattergeo(
            lon=[rota['MID_LON']],
            lat=[rota['MID_LAT']],
            mode='markers',
            marker=dict(
                size=10,
                color=cor,
                symbol='arrow',
                angle=rota['DIRECAO'],
                line=dict(width=1, color='white')
            ),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Marcadores de origem
    fig.add_trace(go.Scattergeo(
        lon=rotas_data['ORIGIN_LON'],
        lat=rotas_data['ORIGIN_LAT'],
        mode='markers',
        marker=dict(size=6, color='green', symbol='circle', line=dict(width=1, color='white')),
        text=rotas_data['ORIGIN_CITY'],
        hovertemplate="<b>%{text}</b><br><i>Origem</i><extra></extra>",
        name="Aeroportos de Origem",
        showlegend=True
    ))
    
    # Marcadores de destino
    fig.add_trace(go.Scattergeo(
        lon=rotas_data['DEST_LON'],
        lat=rotas_data['DEST_LAT'],
        mode='markers',
        marker=dict(size=8, color='red', symbol='circle', line=dict(width=1, color='white')),
        text=rotas_data['DEST_CITY'],
        hovertemplate="<b>%{text}</b><br><i>Destino</i><extra></extra>",
        name="Aeroportos de Destino",
        showlegend=True
    ))
    
    # Layout do mapa - SIMPLIFICADO (sem barras de cor laterais)
    titulo_metricas = {
        'avg_delay': 'Atraso Médio',
        'delay_count': 'Quantidade de Atrasos', 
        'cancelled_count': 'Quantidade de Cancelamentos',
        'diverted_count': 'Quantidade de Desvios'
    }
    
    fig.update_layout(
        title=dict(
            text=f"<b>Top {top_n} Rotas - {titulo_metricas[selected_metric]}</b><br>"
                 f"<sup>🎯 Setas indicam direção | 📏 Espessura: {config['line_title'].lower()} | 🎨 Cor: Hora média do dia</sup>",
            x=0.5,
            xanchor='center',
            font=dict(size=16, color='#2c3e50')
        ),
        geo=dict(
            scope='north america',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(245, 245, 240)',
            countrycolor='rgb(180, 180, 180)',
            coastlinecolor='rgb(140, 140, 140)',
            lakecolor='rgb(100, 173, 240)',
            showsubunits=True,
            subunitcolor='rgb(200, 200, 200)',
            showlakes=True,
            showcountries=True,
            fitbounds="locations",
            lataxis=dict(range=[20, 55]),
            lonaxis=dict(range=[-130, -60])
        ),
        height=altura,
        margin=dict(l=0, r=0, t=80, b=0),  # Margens reduzidas
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='closest',
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='rgba(0, 0, 0, 0.2)',
            borderwidth=1,
            font=dict(size=10)
        )
    )
    
    print(f"🗺️ Mapa criado com {len(rotas_data)} rotas")
    return fig

def create_map(df, metric='avg_delay'):
    """Função wrapper para manter compatibilidade"""
    return criar_mapa_rotas_avancado(df, top_n=30, altura=600, selected_metric=metric)