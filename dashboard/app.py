from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="5000")
