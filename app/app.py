import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

# exemplo: gráfico inicial
fig = px.histogram(df, x="DEP_DELAY", nbins=50, title="Distribution of Departure Delays")

app.layout = html.Div([
    html.H1("Flight Delays Dashboard"),
    dcc.Graph(figure=fig),
    dcc.Dropdown(
        id="airline_filter",
        options=[{"label": a, "value": a} for a in df["AIRLINE_Description"].unique()],
        placeholder="Select Airline"
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
