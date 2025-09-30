from dash import html

def create_header():
    return html.Div([
        html.H1("✈️ Dashboard de Análise de Voos", 
                className="header-title")
    ], className="header-container")