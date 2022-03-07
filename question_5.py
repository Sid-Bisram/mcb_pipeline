import db

from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import pandas as pd

### Data
data = {'Country': ['Afghanistan', 'China', 'France'], 'latitude': ['33.7680065', '35.000074', '46.603354'],
        'longitude': ['66.2385139', '104.999927', '1.8883335'],
        'map_image': ['https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Afghanistan.svg',
                      'https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg',
                      'https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg'],
        'desc': ['Description 1', 'Description 2', 'Description 3'],
        'year': ['2015', '2016', '2016']}

data = db.get_Q5_dataset()
df = pd.DataFrame(data,columns=['year','Country','map_image','latitude','longitude','happiness_score','happiness_status'])

### Figure
fig = go.Figure(data=[
    go.Scattergeo(
    lon=df['longitude'],
    lat=df['latitude'],
    text=df['Country'],
    mode='markers'
)])

# turn off native plotly.js hover effects - make sure to use
# hoverinfo="none" rather than "skip" which also halts events.
fig.update_traces(hoverinfo="none", hovertemplate=None)

fig.update_layout(geo_scope='world')

app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
options_array=db.get_year_list()
OptionList = [{'label': i, 'value': i} for i in options_array]

app.layout = html.Div([


    html.H1("Happiness Report Map Visualisation", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 # options=[
                 #     {"label": "2015", "value": 2015},
                 #     {"label": "2016", "value": 2016},
                 #     {"label": "2017", "value": 2017},
                 #     {"label": "2018", "value": 2018}],
                 options=OptionList,
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure=fig,clear_on_unhover=True,style={'width': "1500px",'height': "1500px"}),
    dcc.Tooltip(id="graph-tooltip")

])

# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure'),
     Output(component_id='graph-tooltip', component_property='show'),
    Output(component_id='graph-tooltip', component_property='bbox'),
    Output(component_id='graph-tooltip', component_property='children')],
    [Input(component_id='slct_year', component_property='value'),Input(component_id='my_bee_map', component_property='hoverData')],
)

def update_graph(option_slctd,hoverData):
    # print(option_slctd)
    # print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)



    dff = df.copy()
    dff = dff[dff["year"] == option_slctd]


    fig = go.Figure(data=[
        go.Scattergeo(
            lon=dff['longitude'],
            lat=dff['latitude'],
            text=dff['Country'],
            mode='markers'
        )])

    if hoverData is None:
        return container,fig,False, no_update, no_update


    # demo only shows the first point, but other points may also be available
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df.iloc[num]
    img_src = df_row['map_image']
    name = df_row['Country']
    form = df_row['happiness_score']
    desc = df_row['happiness_status']
    if len(desc) > 300:
        desc = desc[:100] + '...'

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{name}", style={"color": "darkblue"}),
            html.P("Happiness score : {0}".format(f"{form}")),
            html.P("Happiness Status: {0}".format(f"{desc}")),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]

    return container,fig,True, bbox, children

if __name__ == '__main__':
    app.run_server(debug=True)
