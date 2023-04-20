from dash import Input, Output, dcc, html, register_page, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

register_page(__name__)

gapminder = pd.read_csv("dashboard/datasets/gapminderData2.csv")
scatter_figure = px.scatter(
    gapminder[gapminder.year == 2007], x="bornPerwom", y="gdpPercap"
)

migrantes = pd.read_excel("dashboard/datasets/MigrantesChile.xlsx")


def plot_heatmap(data: pd.DataFrame, continent):
    data.loc[:, "total"] = data.loc[:, range(2005, 2016)].sum(axis=1)
    data2 = data.sort_values("total", ascending=False, inplace=False)
    data2 = data2[data2.Continent == continent]
    top5 = data2.iloc[:5]
    top5.set_index("Country", inplace=True)
    heatmap = px.imshow(
        top5[range(2005, 2016)],
        labels={"x": "Year", "y": "Country", "color": "Migrantes"},
        x=list(range(2005, 2016)),
        y=top5.index.values,
    )
    return heatmap


def continent_options(data):
    return [
        {"label": continent, "value": continent}
        for continent in data.Continent.unique()
    ]


layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("titulo"),
                        dcc.Graph(id="id_scatter", figure=scatter_figure),
                    ],
                    width=7,
                ),
                dbc.Col(
                    [
                        html.H1("Heatmap"),
                        dbc.Select(
                            id="select",
                            options=continent_options(migrantes),
                            value="América",
                        ),
                        dcc.Graph(
                            id="id_heatmap", figure=plot_heatmap(migrantes, "América")
                        ),
                    ]
                ),
            ]
        ),
    ],
    fluid=True,
)


@callback(
    Output(component_id="id_heatmap", component_property="figure"),
    Input(component_id="select", component_property="value"),
)
def update_heatmap(continent):
    return plot_heatmap(migrantes, continent)
