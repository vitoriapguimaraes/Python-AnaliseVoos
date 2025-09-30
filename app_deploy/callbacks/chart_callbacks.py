import dash
from dash import Input, Output, State, callback
import plotly.express as px
import pandas as pd
from utils.data_processing import create_metric_data, criar_mapa_rotas_avancado

def register_chart_callbacks(app, df):
    
    # Callback principal simplificado
    @app.callback(
        [Output("top-airlines-chart", "figure"),
         Output("top-cities-chart", "figure"),
         Output("top-states-chart", "figure"),
         Output("distance-chart", "figure"),
         Output("day-of-month-chart", "figure"),
         Output("day-of-week-chart", "figure"),
         Output("hour-chart", "figure"),
         Output("time-period-chart", "figure"),
         Output("map-chart", "figure")],
        [Input("metric-selector", "value")],
        prevent_initial_call=False
    )
    def update_charts(selected_metric):
        print(f"Atualizando gráficos com métrica: {selected_metric}")
        
        # Usar métrica padrão se não houver seleção
        if not selected_metric:
            selected_metric = 'avg_delay'
        
        def create_simple_bar_chart(data, title, x_label, y_label):
            """Cria um gráfico de barras simplificado"""
            if len(data) == 0:
                fig = px.bar(title=f"{title} (Sem dados)")
                fig.update_layout(height=400, title_x=0.5)
                return fig
                
            # Converter índices para string para evitar problemas
            y_values = [str(x) for x in data.index]
            
            fig = px.bar(
                x=data.values,
                y=y_values,
                orientation="h",
                title=f"<b>{title}</b>",
                labels={"x": x_label, "y": y_label},
                color=data.values,
                color_continuous_scale="RdYlGn_r"
            )
            
            fig.update_layout(
                height=400,
                yaxis={"categoryorder": "total ascending"},
                title_x=0.5,
                title_font_size=16,
                font=dict(size=12),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=50, r=20, t=60, b=40),
                showlegend=False
            )
            return fig

        def create_line_chart_continuous(data, title, x_label, y_label, group_col):
            """Cria um gráfico de linhas contínuo com agrupamento correto"""
            if len(data) == 0:
                fig = px.line(title=f"{title} (Sem dados)")
                fig.update_layout(height=400, title_x=0.5)
                return fig
            
            # Para gráficos temporais, garantir ordem correta
            if group_col == 'FL_DAY':
                # Ordenar por dia do mês
                data = data.sort_index()
                x_values = data.index
            elif group_col == 'TIME_HOUR':
                # Ordenar por hora
                data = data.sort_index()
                x_values = data.index
            else:
                x_values = data.index
            
            fig = px.line(
                x=x_values,
                y=data.values,
                title=f"<b>{title}</b>",
                labels={"x": x_label, "y": y_label}
            )
            
            fig.update_traces(
                line_color="#e74c3c", 
                line_width=3, 
                marker=dict(size=6),
                mode="lines+markers"
            )
            
            fig.update_layout(
                height=400,
                title_x=0.5,
                title_font_size=16,
                font=dict(size=12),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=50, r=20, t=60, b=40),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                )
            )
            return fig

        try:
            # Verificar se as colunas necessárias existem no DataFrame
            required_columns = ['AIRLINE_Description', 'ORIGIN_CITY', 'ORIGIN_STATE', 'DISTANCE', 
                              'FL_DAY', 'DAY_OF_WEEK', 'TIME_HOUR', 'TIME_PERIOD', 'DELAY_OVERALL',
                              'DELAY', 'CANCELLED', 'DIVERTED']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"⚠️ Colunas faltando: {missing_columns}")
                error_fig = px.bar(title=f"Colunas faltando: {', '.join(missing_columns)}")
                error_fig.update_layout(height=400, title_x=0.5)
                return [error_fig] * 9
            
            # Top 10 Companhias
            airlines_data, title_suffix = create_metric_data(df, "AIRLINE_Description", selected_metric)
            airlines_fig = create_simple_bar_chart(
                airlines_data.head(10),
                f"🏢 Top 10 Companhias - {title_suffix}", 
                title_suffix, 
                "Companhia"
            )
            
            # Top 10 Cidades
            cities_data, _ = create_metric_data(df, "ORIGIN_CITY", selected_metric)
            cities_fig = create_simple_bar_chart(
                cities_data.head(10),
                f"🏙️ Top 10 Cidades de Origem - {title_suffix}", 
                title_suffix, 
                "Cidade"
            )
            
            # Top 10 Estados
            states_data, _ = create_metric_data(df, "ORIGIN_STATE", selected_metric)
            states_fig = create_simple_bar_chart(
                states_data.head(10),
                f"🗺️ Top 10 Estados de Origem - {title_suffix}", 
                title_suffix, 
                "Estado"
            )
            
            # Distância
            df_temp = df.copy()
            df_temp["DISTANCE_BIN"] = pd.cut(df_temp["DISTANCE"], bins=10, precision=0)
            distance_data, _ = create_metric_data(df_temp, "DISTANCE_BIN", selected_metric, observed=True)
            distance_fig = create_simple_bar_chart(
                distance_data,
                f"✈️ Distância vs {title_suffix}", 
                title_suffix, 
                "Faixa de Distância"
            )
            
            # Dia do Mês - Agora com linha contínua
            day_data, _ = create_metric_data(df, "FL_DAY", selected_metric, observed=True)
            day_fig = create_line_chart_continuous(
                day_data,
                f"📅 Dia do Mês vs {title_suffix}", 
                "Dia do Mês", 
                title_suffix,
                "FL_DAY"
            )
            
            # Dia da Semana (mantém como barras)
            weekday_data, _ = create_metric_data(df, "DAY_OF_WEEK", selected_metric, observed=True)
            weekday_fig = create_simple_bar_chart(
                weekday_data,
                f"📆 Dia da Semana vs {title_suffix}", 
                title_suffix, 
                "Dia da Semana"
            )
            
            # Hora do Dia - Agora com linha contínua
            hour_data, _ = create_metric_data(df, "TIME_HOUR", selected_metric, observed=True)
            hour_fig = create_line_chart_continuous(
                hour_data,
                f"🕐 Hora do Dia vs {title_suffix}", 
                "Hora", 
                title_suffix,
                "TIME_HOUR"
            )
            
            # Período do Dia (mantém como barras)
            period_data, _ = create_metric_data(df, "TIME_PERIOD", selected_metric, observed=True)
            period_fig = create_simple_bar_chart(
                period_data,
                f"🌅 Período do Dia vs {title_suffix}", 
                title_suffix, 
                "Período"
            )
            
            # Mapa
            map_columns = ['ORIGIN_LAT', 'ORIGIN_LON', 'DEST_LAT', 'DEST_LON']
            if all(col in df.columns for col in map_columns):
                map_fig = criar_mapa_rotas_avancado(df, top_n=30, altura=600, selected_metric=selected_metric)
            else:
                map_fig = px.scatter(title="⚠️ Dados de coordenadas não disponíveis para o mapa")
                map_fig.update_layout(height=600, title_x=0.5)
            
            print("✅ Gráficos atualizados com sucesso!")
            return (airlines_fig, cities_fig, states_fig, distance_fig, 
                    day_fig, weekday_fig, hour_fig, period_fig, map_fig)
                    
        except Exception as e:
            print(f"❌ Erro ao criar gráficos: {e}")
            import traceback
            traceback.print_exc()
            
            error_fig = px.bar(title=f"Erro: {str(e)}")
            error_fig.update_layout(height=400, title_x=0.5)
            return (error_fig, error_fig, error_fig, error_fig, 
                    error_fig, error_fig, error_fig, error_fig, error_fig)