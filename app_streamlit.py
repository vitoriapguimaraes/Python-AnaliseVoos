
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from math import atan2, degrees
import warnings
warnings.filterwarnings("ignore")

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="Dashboard de Análise de Voos")

# --- Carregamento e Pré-processamento de Dados ---
@st.cache_data
def load_data():
    df = pd.read_csv("project_development/dataset/created/df_view.csv")
    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

    weekday_order = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    period_order = ["Madrugada", "Manhã", "Tarde", "Noite"]

    df["DAY_OF_WEEK"] = pd.Categorical(df["DAY_OF_WEEK"], categories=weekday_order, ordered=True)
    df["TIME_PERIOD"] = pd.Categorical(df["TIME_PERIOD"], categories=period_order, ordered=True)
    
    # Adicionar colunas para o mapa de rotas, se não existirem
    if "ORIGIN_LAT" not in df.columns:
        # Placeholder: Em um cenário real, você carregaria essas coordenadas de outro lugar
        # ou as calcularia. Para este exemplo, vamos simular.
        st.warning("Colunas de coordenadas (ORIGIN_LAT, ORIGIN_LON, DEST_LAT, DEST_LON) não encontradas. O mapa pode não funcionar corretamente.")
        df["ORIGIN_LAT"] = np.random.uniform(25, 50, len(df))
        df["ORIGIN_LON"] = np.random.uniform(-125, -70, len(df))
        df["DEST_LAT"] = np.random.uniform(25, 50, len(df))
        df["DEST_LON"] = np.random.uniform(-125, -70, len(df))

    return df

df = load_data()

# --- Funções de Cálculo e Processamento ---
def calculate_big_numbers(df):
    total_flights = len(df)
    avg_delay = df["DELAY_OVERALL"].mean() if "DELAY_OVERALL" in df.columns else 0
    delay_percentage = (df["DELAY"].sum() / total_flights) * 100 if total_flights > 0 else 0
    cancelled_percentage = (df["CANCELLED"].sum() / total_flights) * 100 if total_flights > 0 else 0
    diverted_percentage = (df["DIVERTED"].sum() / total_flights) * 100 if total_flights > 0 else 0
    
    return {
        "total_flights": total_flights,
        "avg_delay": avg_delay,
        "delay_percentage": delay_percentage,
        "cancelled_percentage": cancelled_percentage,
        "diverted_percentage": diverted_percentage
    }

def create_metric_data(df, group_col, metric, observed=True):
    if metric == "avg_delay":
        data = df.groupby(group_col, observed=observed)["DELAY_OVERALL"].mean().sort_values(ascending=False)
        title_suffix = "Atraso Médio (min)"
    elif metric == "delay_count":
        data = df.groupby(group_col, observed=observed)["DELAY"].sum().sort_values(ascending=False)
        title_suffix = "Quantidade de Atrasos"
    elif metric == "cancelled_count":
        data = df.groupby(group_col, observed=observed)["CANCELLED"].sum().sort_values(ascending=False)
        title_suffix = "Quantidade de Cancelamentos"
    elif metric == "diverted_count":
        data = df.groupby(group_col, observed=observed)["DIVERTED"].sum().sort_values(ascending=False)
        title_suffix = "Quantidade de Desvios"
    else:
        data = df.groupby(group_col, observed=observed)["DELAY_OVERALL"].mean().sort_values(ascending=False)
        title_suffix = "Atraso Médio (min)"
    
    return data, title_suffix

# --- Estilos de Gráficos (Adaptados de creating_fig.ipynb) ---
palette = ["#0077C8", "#005EA8", "#003F72", "#0094D8", "#66C5E3"]
palette_red = ["#DC1C13", "#EA4C46", "#F07470"]

def get_plotly_template():
    # Baseado no estilo do creating_fig.ipynb e adaptado para Plotly
    return go.layout.Template(
        layout=go.Layout(
            font=dict(family="Arial, sans-serif", size=12, color="#333"),
            title_font_size=18,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=50, r=20, t=60, b=40),
            xaxis=dict(
                showgrid=True, gridwidth=1, gridcolor="lightgray",
                linecolor="lightgray", linewidth=1,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                showgrid=True, gridwidth=1, gridcolor="lightgray",
                linecolor="lightgray", linewidth=1,
                tickfont=dict(size=10)
            ),
            colorway=palette, # Aplicar paleta de cores
            hoverlabel=dict(
                bgcolor="white",
                font=dict(family="Arial", size=12)
            )
        )
    )

plotly_template = get_plotly_template()

# --- Funções de Visualização (Adaptadas para Streamlit e estilos) ---
def create_simple_bar_chart(data, title, x_label, y_label):
    if data.empty:
        fig = px.bar(title=f"{title} (Sem dados)")
        fig.update_layout(height=400, title_x=0.5, template=plotly_template)
        return fig
         
    y_values = [str(x) for x in data.index]
    
    fig = px.bar(
        x=data.values,
        y=y_values,
        orientation="h",
        title=f"<b>{title}</b>",
        labels={"x": x_label, "y": y_label},
        color=data.values,
        color_continuous_scale=palette # Usar a paleta definida
    )
    
    fig.update_layout(
        height=400,
        yaxis={"categoryorder": "total ascending"},
        title_x=0.5,
        title_font_size=14,
        font=dict(size=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=20, t=60, b=40),
        showlegend=False,
        coloraxis_showscale=False,
        template=plotly_template # Aplicar template
    )
    return fig

def create_line_chart_continuous(data, title, x_label, y_label, group_col):
    if data.empty:
        fig = px.line(title=f"{title} (Sem dados)")
        fig.update_layout(height=400, title_x=0.5, template=plotly_template)
        return fig
    
    if group_col in ["FL_DAY", "TIME_HOUR"]:
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
        line_color=palette[0], # Usar a primeira cor da paleta
        line_width=3, 
        marker=dict(size=6),
        mode="lines+markers"
    )
    
    fig.update_layout(
        height=400,
        title_x=0.5,
        title_font_size=14,
        font=dict(size=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=20, t=60, b=40),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor="lightgray"),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor="lightgray"),
        template=plotly_template # Aplicar template
    )
    return fig

def criar_mapa_rotas_avancado(df, top_n=30, altura=600, selected_metric="avg_delay"):
    metric_config = {
        "avg_delay": {"col": "DELAY_OVERALL", "agg": "mean", "title": "Atraso Médio", "unit": "min"},
        "delay_count": {"col": "DELAY", "agg": "sum", "title": "Quantidade de Atrasos", "unit": "voos"},
        "cancelled_count": {"col": "CANCELLED", "agg": "sum", "title": "Quantidade de Cancelamentos", "unit": "voos"},
        "diverted_count": {"col": "DIVERTED", "agg": "sum", "title": "Quantidade de Desvios", "unit": "voos"}
    }
    
    config = metric_config[selected_metric]
    
    required_cols = ["ORIGIN_CITY", "DEST_CITY", "ORIGIN_LAT", "ORIGIN_LON", "DEST_LAT", "DEST_LON"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        fig = go.Figure()
        fig.update_layout(
            title=f"Dados de coordenadas não disponíveis: {", ".join(missing_cols)}",
            height=altura,
            template=plotly_template
        )
        return fig

    rotas_data = (
        df.groupby(["ORIGIN_CITY", "DEST_CITY", "ORIGIN_LAT", "ORIGIN_LON", "DEST_LAT", "DEST_LON"], 
                           as_index=False)
        .agg({
            config["col"]: config["agg"], 
            "FL_DATE": "count",
            "TIME_HOUR": "mean"  # Hora média para definir cor
        })
        .rename(columns={"FL_DATE": "TOTAL_VOOS"})
        .sort_values(by=config["col"], ascending=False)
        .head(top_n)
        .dropna(subset=["ORIGIN_LAT", "ORIGIN_LON", "DEST_LAT", "DEST_LON"])
    )
    
    if rotas_data.empty:
        fig = go.Figure()
        fig.update_layout(title="Nenhuma rota válida encontrada", height=altura, template=plotly_template)
        return fig
    
    fig = go.Figure()

    min_metric = rotas_data[config["col"]].min()
    max_metric = rotas_data[config["col"]].max()
    
    for _, rota in rotas_data.iterrows():
        hora_normalizada = rota["TIME_HOUR"] / 23
        
        hue = 200 + (hora_normalizada * 20)        
        saturation = 70 + (hora_normalizada * 30)  
        lightness = 70 - (hora_normalizada * 50)   
        
        cor_hsl = f"hsl({hue}, {saturation}%, {lightness}%)"
        
        if max_metric > min_metric:
            metric_normalizada = (rota[config["col"]] - min_metric) / (max_metric - min_metric)
            espessura = 1 + (metric_normalizada ** 0.7) * 9  
        else:
            espessura = 3
        
        espessura = max(1, min(espessura, 10))
        
        fig.add_trace(go.Scattergeo(
            lon=[rota["ORIGIN_LON"], rota["DEST_LON"]],
            lat=[rota["ORIGIN_LAT"], rota["DEST_LAT"]],
            mode="lines",
            line=dict(width=espessura, color=cor_hsl),
            name=f"{rota["ORIGIN_CITY"]} → {rota["DEST_CITY"]}",
            showlegend=False,
            hovertemplate=(
                f"<b>%{{text}}</b><br>"+
                f"{config["title"]}: {rota[config["col"]]:.1f} {config["unit"]}<br>"+
                f"Hora Média: {rota["TIME_HOUR"]:.1f}h<br>"+
                f"Total de Voos: {rota["TOTAL_VOOS"]}<br>"+
                f"Espessura: {espessura:.1f}<br>"+
                "<extra></extra>"
            ),
            text=f"{rota["ORIGIN_CITY"]} → {rota["DEST_CITY"]}"
        ))
    
    fig.add_trace(go.Scattergeo(
        lon=rotas_data["ORIGIN_LON"],
        lat=rotas_data["ORIGIN_LAT"],
        mode="markers",
        marker=dict(size=8, color="green", symbol="circle", line=dict(width=1, color="white")),
        text=rotas_data["ORIGIN_CITY"],
        name="Origem",
        hovertemplate="<b>%{text}</b><br><i>Aeroporto de Origem</i><extra></extra>"
    ))
    
    fig.add_trace(go.Scattergeo(
        lon=rotas_data["DEST_LON"],
        lat=rotas_data["DEST_LAT"],
        mode="markers",
        marker=dict(size=8, color="red", symbol="circle", line=dict(width=1, color="white")),
        text=rotas_data["DEST_CITY"],
        name="Destino",
        hovertemplate="<b>%{text}</b><br><i>Aeroporto de Destino</i><extra></extra>"
    ))
    
    subtitle_text = (
        f"🎨 Azul claro = madrugada ⭢ Azul escuro = noite | "+
        f"📏 Espessura: atraso médio | "+
        f"🟢 Origem | 🔴 Destino"
    )
    
    fig.update_layout(
        title=dict(
            text=f"<b>As {top_n} rotas com maior atraso</b><br>"+
                 f"<sub>{subtitle_text}</sub>",
            x=0.5,
            xanchor="center"
        ),
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,
            landcolor="rgb(245, 245, 240)",
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
            showsubunits=True,
            subunitcolor="rgb(217, 217, 217)",
        ),
        height=altura,
        margin=dict(l=0, r=0, t=80, b=0),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="rgba(0,0,0,0.5)",
            borderwidth=1
        ),
        template=plotly_template # Aplicar template
    )
    return fig

# --- Layout do Streamlit ---
st.title("✈️ Dashboard de Análise de Voos")

# Big Numbers
metrics = calculate_big_numbers(df)

st.markdown("### Métricas Gerais")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Voos", f"{metrics["total_flights"]:,}".replace(",", "."))
col2.metric("Atraso Médio (min)", f"{metrics["avg_delay"]:.2f}")
col3.metric("Voos Atrasados (%)", f"{metrics["delay_percentage"]:.2f}%")
col4.metric("Voos Cancelados (%)", f"{metrics["cancelled_percentage"]:.2f}%")
col5.metric("Voos Desviados (%)", f"{metrics["diverted_percentage"]:.2f}%")

st.markdown("--- ")
st.markdown("### Análise de Distribuições")

selected_metric = st.radio(
    "Selecione a métrica para análise:",
    options=["avg_delay", "delay_count", "cancelled_count", "diverted_count"],
    format_func=lambda x: {
        "avg_delay": "⏱️ Média de Atraso",
        "delay_count": "🔢 Quantidade de Atrasos",
        "cancelled_count": "❌ Quantidade de Cancelamentos",
        "diverted_count": "🔄 Quantidade de Desvios"
    }[x],
    horizontal=True
)

# Gráficos
st.subheader("Companhias e Distâncias")
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    airlines_data, title_suffix = create_metric_data(df, "AIRLINE_Description", selected_metric)
    airlines_fig = create_simple_bar_chart(
        airlines_data.head(10),
        f"🏢 Top 10 Companhias - {title_suffix}", 
        title_suffix, 
        "Companhia"
    )
    st.plotly_chart(airlines_fig, use_container_width=True)

with col_chart2:
    df_temp = df.copy()
    df_temp["DISTANCE_BIN"] = pd.cut(df_temp["DISTANCE"], bins=10, precision=0)
    distance_data, _ = create_metric_data(df_temp, "DISTANCE_BIN", selected_metric, observed=True)
    distance_fig = create_simple_bar_chart(
        distance_data,
        f"✈️ Distância vs {title_suffix}", 
        title_suffix, 
        "Faixa de Distância"
    )
    st.plotly_chart(distance_fig, use_container_width=True)

st.subheader("Cidades e Estados")
col_chart3, col_chart4 = st.columns(2)
with col_chart3:
    cities_data, _ = create_metric_data(df, "ORIGIN_CITY", selected_metric)
    cities_fig = create_simple_bar_chart(
        cities_data.head(10),
        f"🏙️ Top 10 Cidades de Origem - {title_suffix}", 
        title_suffix, 
        "Cidade"
    )
    st.plotly_chart(cities_fig, use_container_width=True)

with col_chart4:
    states_data, _ = create_metric_data(df, "ORIGIN_STATE", selected_metric)
    states_fig = create_simple_bar_chart(
        states_data.head(10),
        f"🗺️ Top 10 Estados de Origem - {title_suffix}", 
        title_suffix, 
        "Estado"
    )
    st.plotly_chart(states_fig, use_container_width=True)

st.subheader("Padrões Temporais")
col_chart5, col_chart6 = st.columns(2)
with col_chart5:
    day_data, _ = create_metric_data(df, "FL_DAY", selected_metric, observed=True)
    day_fig = create_line_chart_continuous(
        day_data,
        f"📅 Dia do Mês vs {title_suffix}", 
        "Dia do Mês", 
        title_suffix,
        "FL_DAY"
    )
    st.plotly_chart(day_fig, use_container_width=True)

with col_chart6:
    weekday_data, _ = create_metric_data(df, "DAY_OF_WEEK", selected_metric, observed=True)
    weekday_fig = create_simple_bar_chart(
        weekday_data,
        f"📆 Dia da Semana vs {title_suffix}", 
        title_suffix, 
        "Dia da Semana"
    )
    st.plotly_chart(weekday_fig, use_container_width=True)

col_chart7, col_chart8 = st.columns(2)
with col_chart7:
    hour_data, _ = create_metric_data(df, "TIME_HOUR", selected_metric, observed=True)
    hour_fig = create_line_chart_continuous(
        hour_data,
        f"🕐 Hora do Dia vs {title_suffix}", 
        "Hora", 
        title_suffix,
        "TIME_HOUR"
    )
    st.plotly_chart(hour_fig, use_container_width=True)

with col_chart8:
    period_data, _ = create_metric_data(df, "TIME_PERIOD", selected_metric, observed=True)
    period_fig = create_simple_bar_chart(
        period_data,
        f"🌅 Período do Dia vs {title_suffix}", 
        title_suffix, 
        "Período"
    )
    st.plotly_chart(period_fig, use_container_width=True)

st.markdown("--- ")
st.markdown("### Visualização Geográfica")

map_quantity = st.slider(
    "Quantidade de rotas a exibir no mapa:",
    min_value=5, max_value=100, value=30, step=5
)

map_fig = criar_mapa_rotas_avancado(df, top_n=map_quantity, altura=600, selected_metric=selected_metric)
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("--- ")
st.markdown(
    "<div style=\'text-align: center; color: #666; font-size: 0.9em;\'>"+
    "Desenvolvido por <strong>Ianna Castro e Vitória Pistori</strong> | Acesse o "+
    "<a href=\'https://github.com/vitoriapguimaraes/Python-AnaliseVoos\' target=\'_blank\' style=\'color: #3498db; text-decoration: none;\'>repositório original</a> no GitHub"+
    "</div>", 
    unsafe_allow_html=True
)