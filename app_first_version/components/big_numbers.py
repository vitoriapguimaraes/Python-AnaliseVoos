from dash import html
from utils.data_processing import calculate_big_numbers

def create_big_numbers(df):
    big_numbers = calculate_big_numbers(df)
    
    return html.Div([
        html.H2("📊 Resumo Geral", className="section-title"),
        
        # Primeira linha - Total e Média de Atraso
        html.Div([
            create_number_card(
                "✈️", 
                f"{big_numbers['total_flights']:,}", 
                "Total de Voos", 
                "blue"
            ),
            create_number_card(
                "⏱️", 
                f"{big_numbers['avg_delay']:.1f} min", 
                "Atraso Médio", 
                "red"
            ),
        ], className="big-numbers-row first-row"),
        
        # Segunda linha - Três porcentagens
        html.Div([
            create_number_card(
                "⚠️", 
                f"{big_numbers['delay_percentage']:.1f}%", 
                "Voos com Atraso", 
                "orange"
            ),
            create_number_card(
                "❌", 
                f"{big_numbers['cancelled_percentage']:.1f}%", 
                "Voos Cancelados", 
                "cancelled"
            ),
            create_number_card(
                "🔄", 
                f"{big_numbers['diverted_percentage']:.1f}%", 
                "Voos Desviados", 
                "diverted"
            ),
        ], className="big-numbers-row second-row"),
    ], className="big-numbers-container")

def create_number_card(icon, value, label, color_type):
    color_classes = {
        "blue": "card-blue",
        "red": "card-red", 
        "orange": "card-orange",
        "cancelled": "card-cancelled",
        "diverted": "card-diverted"
    }
    
    card_class = f"big-number-card {color_classes[color_type]}"
    
    return html.Div([
        html.Div([
            html.H3(icon, className="card-icon"),
            html.H3(value, className="card-value"),
            html.P(label, className="card-label")
        ], className="card-content")
    ], className=card_class)