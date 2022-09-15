from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dis_model import happy_df

# Specify HTML <head> elements
app = Dash(__name__,
           title="Summarising and illustrating data",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

# Specify app layout (HTML <body> elements) using dash.html, dash.dcc and dash_bootstrap_components
# All component IDs should relate to the Input or Output of callback functions in *_controller.py
app.layout = dbc.Container([
    # User Input
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label(children=["Variable"],
                          className="label",
                          html_for="cols-dropdown"),
                dbc.Select(id="cols-dropdown",
                           options=[{"label": x, "value": x}
                                    for x in happy_df.columns[1:]],
                           value="Sex")
            ], **{"aria-live": "polite"})
        ], xs=7, sm=6, md=4, lg=3)
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            dbc.Button(id="toggle",
                       n_clicks=0,
                       children=[],
                       class_name="button",
                       style={"margin": "0 auto"})
        ], xs=8, md=5, lg=4, className="d-flex justify-content-center")
    ], justify="center"),
    # Descriptive Statistics
    dbc.Row([
        dbc.Col([
            dbc.Collapse([
                html.Div([
                    dbc.Card([
                        dbc.CardBody(id="desc1",
                                     class_name="descriptive",
                                     children=[])
                    ])
                ], **{"aria-live": "polite"})
            ], id="collapse1", is_open=True)
        ], xs=12, md=6, xl=5),
        dbc.Col([
            dbc.Collapse([
                html.Div([
                    dbc.Card([
                        dbc.CardBody(id="desc2",
                                     class_name="descriptive",
                                     children=[])
                    ])
                ], **{"aria-live": "polite"})
            ], id="collapse2", is_open=True)
        ], xs=12, md=6, xl=5)
    ], justify="center"),
    # Histograms
    dbc.Row([
        dbc.Col([
            # Graph components are placed inside a Div with role="img" to manage the experience for screen reader users
            html.Div([
                dcc.Graph(id="graph-hist1",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False},
                          className="dis-graph")
            ], role="img", **{"aria-hidden": "true"}),
            # A second Div is used to associate alt text with the relevant Graph component to manage the experience for screen reader users, styled using CSS
            html.Div(id="sr-hist1",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6, xl=5),
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-hist2",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False},
                          className="dis-graph")
            ], role="img", **{"aria-hidden": "true"}),
            html.Div(id="sr-hist2",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6, xl=5)
    ], justify="center"),
    # Boxplots
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-box1",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False},
                          className="dis-graph")
            ], role="img", **{"aria-hidden": "true"}),
            html.Div(id="sr-box1",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6, xl=5),
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-box2",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False},
                          className="dis-graph")
            ], role="img", **{"aria-hidden": "true"}),
            html.Div(id="sr-box2",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6, xl=5)
    ], justify="center")
], fluid=True)
