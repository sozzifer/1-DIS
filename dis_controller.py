from dash import html, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from dis_view import app
from dis_model import get_df, get_stats, stat_colours

# app.callback Outputs and Inputs are all associated with unique elements in *_view.py though the first argument (component_id) and control/are controlled by the second argument (component_property)

# Callback function to populate descriptive statistics cards based on dropdown user selection
@app.callback(
    Output("desc1", "children"),
    Output("desc2", "children"),
    Input("cols-dropdown", "value")
)
def update_statistics(value):
    categories, stats_df1, stats_df2 = get_df(value)
    group1 = categories[0]
    group2 = categories[1]
    n1, mean1, std1, q1_1, median1, q3_1, iqr1 = get_stats(stats_df1)
    n2, mean2, std2, q1_2, median2, q3_2, iqr2 = get_stats(stats_df2)
    return [html.Div([
                html.P(f"Descriptive statistics for {value} = {group1}")
            ], className="desc-header"),
            html.Div([
                html.Div([
                    html.P("Sample size:"),
                    html.P("Mean:"),
                    html.P("Median:"),
                    html.P("Standard deviation (SD):"),
                    html.P("First quartile (Q1):"),
                    html.P("Third quartile (Q3):"),
                    html.P("Interquartile range:")
                ], className="desc-body-r"), 
                html.Div([
                    html.P(f"{n1}"),
                    html.P(f"{mean1}"),
                    html.P(f"{median1}"),
                    html.P(f"\u00B1{std1}"),
                    html.P(f"{q1_1}"),
                    html.P(f" {q3_1}"),
                    html.P(f"{iqr1}")])
            ], className="desc-body")],\
            [html.Div([
                html.P(f"Descriptive statistics for {value} = {group2}")
            ], className="desc-header"),
            html.Div([
                html.Div([
                    html.P("Sample size:"),
                    html.P("Mean:"),
                    html.P("Median:"),
                    html.P("Standard deviation:"),
                    html.P("First quartile (Q1):"),
                    html.P("Third quartile (Q3):"),
                    html.P("Interquartile range:")
                ], className="desc-body-r"), 
                html.Div([
                    html.P(f"{n2}"),
                    html.P(f"{mean2}"),
                    html.P(f"{median2}"),
                    html.P(f"\u00B1{std2}"),
                    html.P(f"{q1_2}"),
                    html.P(f" {q3_2}"),
                    html.P(f"{iqr2}")])
            ], className="desc-body")]


# Add descriptive statistics line graphs to histograms (mean, median, Q1, Q3, +-1SD)
def format_histogram(df, fig):
    scatter_range = list(range(0, 93))
    _, mean, std, q1, median, q3, _ = get_stats(df)
    fig.update_layout(xaxis2=dict(matches='x',
                                  layer="above traces",
                                  overlaying="x"),
                      margin=dict(t=20, b=10, l=20, r=20),
                      height=300,
                      font_size=14,
                      dragmode=False)
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(title_text=None,
                     range=[0, 91])
    fig.update_traces(marker_line_width=1)
    fig.add_trace(
        go.Scatter(x=[mean] * 92,
                   y=scatter_range,
                   name="Mean",
                   marker_color=stat_colours["mean"],
                   line_width=3,
                   hovertemplate="Mean: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[median] * 92,
                   y=scatter_range,
                   name="Median",
                   marker_color=stat_colours["median"],
                   line_width=3,
                   hovertemplate="Median: %{x}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[mean + std] * 92,
                   y=scatter_range,
                   name=u"Mean \u00B1 SD",
                   marker_color=stat_colours["std"],
                   line_width=3,
                   hovertemplate="Mean + SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[mean - std] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["std"],
                   line_width=3,
                   hovertemplate="Mean - SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Scatter(x=[q1] * 92,
                   y=scatter_range,
                   name="Q1, Q3",
                   marker_color=stat_colours["quartile"],
                   line_width=3,
                   hovertemplate="Q1: %{x}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[q3] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["quartile"],
                   line_width=3,
                   hovertemplate="Q3: %{x}<extra></extra>",
                   showlegend=False))


# Callback function to update histograms and associated screen reader text based on dropdown user selection
@app.callback(
    Output("graph-hist1", "figure"),
    Output("graph-hist2", "figure"),
    Output("sr-hist1", "children"),
    Output("sr-hist2", "children"),
    Input("cols-dropdown", "value")
)
def update_histogram(value):
    categories, hist_df1, hist_df2 = get_df(value)
    fig1 = go.Figure(
        go.Histogram(x=hist_df1,
                     xaxis="x2",
                     hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}<extra></extra>",
                     showlegend=False))
    fig2 = go.Figure(
        go.Histogram(x=hist_df2,
                     xaxis="x2",
                     hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}<extra></extra>",
                     showlegend=False))
    fig1.update_traces(marker_line_color="rgba(209,3,115,1)",
                       marker_color="rgba(209,3,115,0.5)")
    fig1.update_xaxes(
        title_text=f"Histogram of Total happiness for {categories[0]}")
    fig2.update_traces(marker_line_color="rgba(158,171,5,1)",
                       marker_color="rgba(158,171,5,0.5)")
    fig2.update_xaxes(
        title_text=f"Histogram of Total happiness for {categories[1]}")
    format_histogram(hist_df1, fig1)
    format_histogram(hist_df2, fig2)
    # Screen reader text
    sr_hist1 = f"Histogram of Total happiness for {value} = {categories[0]}"
    sr_hist2 = f"Histogram of Total happiness for {value} = {categories[1]}"
    return fig1, fig2, sr_hist1, sr_hist2


# Add descriptive statistics line graphs to boxplots (mean, median, Q1, Q3, +-1SD)
# In order to set the go.Box trace to appear above the line graphs, it is added after the go.Scatter traces here rather than in the update_boxplot callback function
def format_boxplot(df, fig, color):
    scatter_range = np.linspace(-0.5, 0.5, 100)
    _, mean, std, q1, median, q3, _ = get_stats(df)
    fig.add_trace(
        go.Scatter(x=[mean]*100,
                   y=scatter_range,
                   name="Mean",
                   marker_opacity=0,
                   marker_color=stat_colours["mean"],
                   line_width=3,
                   hovertemplate="Mean: %{x}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[median]*100,
                   y=scatter_range,
                   name="Median",
                   marker_opacity=0,
                   marker_color=stat_colours["median"],
                   line_width=3,
                   hovertemplate="Median: %{x}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[mean + std]*100,
                   y=scatter_range,
                   name=u"Mean \u00B1 SD",
                   marker_opacity=0,
                   marker_color=stat_colours["std"],
                   line_width=3,
                   hovertemplate="Mean + SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[mean - std]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["std"],
                   line_width=3,
                   hovertemplate="Mean - SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Scatter(x=[q1]*100,
                   y=scatter_range,
                   name="Q1, Q3",
                   marker_opacity=0,
                   marker_color=stat_colours["quartile"],
                   line_width=3,
                   hovertemplate="Q1: %{x}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[q3]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["quartile"],
                   line_width=3,
                   hovertemplate="Q3: %{x}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Box(x=df,
               xaxis="x2",
               hoverinfo="skip",
               hovertemplate=None,
               showlegend=False,
               marker_color=color))
    fig.update_layout(xaxis2=dict(matches='x',
                                  layer="above traces",
                                  overlaying="x"),
                      margin=dict(t=20, b=10, l=20, r=20),
                      height=300,
                      font_size=14,
                      dragmode=False)
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(visible=False,
                     showticklabels=False,
                     range=[-0.5, 0.5])
    return fig

# Callback function to update boxplots and associated screen reader text based on dropdown user selection
@app.callback(
    Output("graph-box1", "figure"),
    Output("graph-box2", "figure"),
    Output("sr-box1", "children"),
    Output("sr-box2", "children"),
    Input("cols-dropdown", "value")
)
def update_boxplot(value):
    categories, box_df1, box_df2 = get_df(value)
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig1.update_xaxes(
        title_text=f"Boxplot of Total happiness for {categories[0]}")
    fig2.update_xaxes(
        title_text=f"Boxplot of Total happiness for {categories[1]}")
    format_boxplot(box_df1, fig1, stat_colours["grp1"])
    format_boxplot(box_df2, fig2, stat_colours["grp2"])
    # Screen reader text
    sr_box1 = f"Boxplot of Total happiness for {value} = {categories[0]}"
    sr_box2 = f"Boxplot of Total happiness for {value} = {categories[1]}"
    return fig1, fig2, sr_box1, sr_box2

# Callback function to show/hide descriptive statistics section
@app.callback(
    Output("collapse1", "is_open"),
    Output("collapse2", "is_open"),
    Input("toggle", "n_clicks"),
    State("collapse1", "is_open"),
    State("collapse2", "is_open"),
)
def toggle_cards(n_clicks, is_open1, is_open2):
    if n_clicks:
        return not is_open1, not is_open2
    return is_open1, is_open2

# Callback function to set the correct text for the show/hide button
@app.callback(
    Output("toggle", "children"),
    Output("toggle", "title"),
    Input("toggle", "n_clicks")
)
def button_text(n_clicks):
    if n_clicks%2 == 1:
        return "Show Descriptive statistics", "Show Descriptive statistics"
    else:
        return "Hide Descriptive statistics", "Hide Descriptive statistics"


if __name__ == "__main__":
    # app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
