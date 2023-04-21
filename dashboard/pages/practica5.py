from dash import Input, Output, dcc, html, register_page, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

register_page(__name__)

gapminder = pd.read_csv("dashboard/datasets/gapminderData2.csv")

scatter_figure = px.scatter(
    gapminder[gapminder.year == 2007],
    x="bornPerwom",
    y="gdpPercap",
    hover_name="country",
)


def serie_tiempo(pais: str, eje_y: str):
    df_pais = gapminder[gapminder.country == pais]
    return px.line(df_pais, x="year", y=eje_y).update_layout(title_text=pais)


layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("titulo"),
                        dcc.Graph(id="id_scatter", figure=scatter_figure),
                    ],
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [dcc.Graph(id="serie_a", figure=serie_tiempo("Chile", "lifeExp"))]
                ),
                dbc.Col(
                    [dcc.Graph(id="serie_b", figure=serie_tiempo("Chile", "gdpPercap"))]
                ),
            ],
        ),
        dbc.Row([dbc.Col([html.H1(id="text", children="hola")])]),
    ],
    fluid=True,
)


# @callback(
#     Output("serie_a", "figure"),
#     Output("serie_b", "figure"),
#     Input("id_scatter", "hoverData"),
# )
# def update_serie(hover_data):
#     a_series = "lifeExp"
#     b_series = "gdpPercap"
#     if not hover_data:
#         return (
#             serie_tiempo("Chile", a_series),
#             serie_tiempo("Chile", b_series),
#         )
#     country = hover_data["points"][0]["hovertext"]
#     return (
#         serie_tiempo(country, a_series),
#         serie_tiempo(country, b_series),
#     )


@callback(
    Output("serie_a", "figure"),
    Input("id_scatter", "selectedData"),
)
def update_text(selection):
    paises = [point["hovertext"] for point in selection["points"]]
    datos = gapminder[gapminder.country.isin(paises)]
    return px.line(datos, x="year", y="gdpPercap", color="country")
