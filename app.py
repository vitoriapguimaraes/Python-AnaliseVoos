import dash
from dash import dcc, html
import pandas as pd
from components.layout import create_layout
from utils.data_processing import load_and_process_data_from_db

print("Carregando dados do banco de dados...")
df = load_and_process_data_from_db()
print(f"Dados carregados: {len(df)} registros")

app = dash.Dash(__name__, assets_folder='assets')

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard de Voos</title>
        {%css%}
        <link rel="icon" type="image/x-icon" href="https://img.icons8.com/color/48/000000/airplane-take-off.png">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = create_layout(df)

# Importar callbacks DEPOIS de criar o app e layout
from callbacks.chart_callbacks import register_chart_callbacks
register_chart_callbacks(app, df)

if __name__ == '__main__':
    print("Iniciando dashboard...")
    app.run(debug=True, host='0.0.0.0', port=8050)