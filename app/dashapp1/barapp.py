import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, MATCH, ALL, ClientsideFunction

import json
import requests
import os
import base64

# Generate more button
# more More More! More!! MORE MORE! MORE!!! MMOORREE!!! MOOOORRREEE!
gen_button = dbc.Button(
    id='gen-button',
    children='more',
    style={'margin-top': '1%', 'width': '80%', 'height': '2%', 'line-height': '200%', 'font-size': '300%'}
)

# The app layout
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # title
    # html.H1("Synthetic Bars", style={'text-align': 'center', }),
    html.Div(
        [
            # Main Text
            dcc.Textarea(id="main-textarea",
                         value='',
                         style={'resize': 'none', 'overflow': 'auto', 'width': '80%', 'height': '80%',
                                'display': 'block',
                                'margin-left': 'auto',
                                'margin-right': 'auto',
                                'margin-top': '2%',
                                'font-size': '250%',
                                'border': '1px solid black'}),

            # loading wheel
            dcc.Loading(
                id="loading-wheel",
                children=[html.Div([html.Div(id="loading-output", children='')])],
                type="circle",
            )
        ]),

    # Buttons
    html.Div(id='button_holder',
             children=[
                 # GEN MORE
                 html.Div(id='dynamic-button-container',
                          children=[
                              gen_button
                          ]),

             ], style={'text-align': 'center'}),

    # Sliders get styled based on isMobile
    html.Div(id='sliders-div', children=[
        dcc.Slider(
            id='length-slider',
            min=10,
            max=210,
            value=50,
            step=10,
            marks={
                10: {'label': '10', 'style': {'color': '#77b0b1', 'font-size': 'smaller'}},
                110: {'label': 'Output Length', 'style': {'font-size': 'smaller'}},
                210: {'label': '210', 'style': {'color': '#f50', 'font-size': 'smaller', 'white-space': 'nowrap'}}
            },
            included=False
        ),

        dcc.Slider(
            id='temp-slider',
            min=0.5,
            max=1.5,
            value=0.8,
            step=0.1,
            marks={
                0.5: {'label': 'Cold 0.5', 'style': {'color': '#77b0b1', 'font-size': 'smaller'}},
                1: {'label': 'Spice', 'style': {'font-size': 'smaller'}},
                1.5: {'label': 'Hot 1.5', 'style': {'color': '#f50', 'font-size': 'smaller', 'white-space': 'nowrap'}}
            },
            included=False
        ),
    ], style={'transform': 'scale(2)', 'display': 'block', 'margin-top': '5%', 'margin-left': 'auto',
              'margin-right': 'auto', 'width': '45%'}),

    html.P(id='placeholder'),
    html.Div(id='div-mobile', style={"display": "none"}),
    dcc.Store(id='session', storage_type='session', data={'clicks': 0}),

])


def register_callbacks(dashapp):
    dashapp.clientside_callback(
        """
            function(label) {          
                document.title = 'New page title : ' + label;
                shareon();            
            }
            """,
        Output('placeholder', 'children'),
        Input('placeholder', 'n_clicks'),
        prevent_initial_call=True
    )

    dashapp.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='isMobile'
        ),
        Output('div-mobile', 'children'),
        Input('div-mobile', 'n_clicks')
    )

    # IsMobile styling
    @dashapp.callback(Output('sliders-div', 'style'),
                      [Input('div-mobile', 'children')], )
    def style_mobile(is_mobile):
        print("IS MOBILE:", is_mobile)
        if is_mobile:
            rows = '20'
            style = {'transform': 'scale(2.5)', 'display': 'block', 'margin-top': '15%', 'margin-left': 'auto',
                     'margin-right': 'auto', 'width': '40%'}
        else:
            rows = '10'
            style = {'transform': 'scale(2)', 'display': 'block', 'margin-top': '5%', 'margin-left': 'auto',
                     'margin-right': 'auto', 'width': '45%'}
        # return rows, style
        return style

    @dashapp.callback(
        [Output('dynamic-button-container', 'children'),
         Output("main-textarea", "value"),
         Output("main-textarea", "rows"),
         Output("loading-output", "children"),
         Output('session', 'data')],
        Input('gen-button', 'n_clicks'),
        [State('dynamic-button-container', 'children'),
         State("main-textarea", 'value'),
         State('temp-slider', 'value'),
         State('length-slider', 'value'),
         State('session', 'data'),
         State('url', 'pathname')])
    def display_newbutton(n_clicks, children, textarea, temp, max_tokens, store_data, pathname):
        # on page load

        if n_clicks is None:
            return children, textarea, '2', '', {'clicks': 0}
        else:
            store_data['clicks'] += 1

            # TODO generate a bunch of fake songs for raw_outputs.txt
            if textarea == '':
                # out = random.choice(raw_outputs)
                textarea = '[Verse 1:'

            out = generate_out(textarea, temp, max_tokens, pathname)

            children.pop()
            more = ['More', 'More!', 'More!!', 'MORE!!!', 'MMOORREE!!!', 'MOOOORRREEE!!!!!!!']

            gen_button.children = more[store_data['clicks'] % len(more)]
            children.append(gen_button)
            # print('Generating a new button')
            rows = out.count('\n')
            rows = rows + 1
            return children, out, str(rows), '', store_data

    @dashapp.callback(
        Output('gen-button', 'disabled'),
        [Input('gen-button', 'n_clicks')]
    )
    def hide_newbutton(n_clicks):
        if n_clicks is None:
            return False
        else:
            print('Disabling the button')
            return True

    def generate_out(prompt, temp, length, who):

        RAPPER_API = os.getenv('API_URL')
        if who == '/rapper':
            RAPPER_API = RAPPER_API + who

        elif who == '/Cowboy':
            RAPPER_API = RAPPER_API + '/cowboy'

        else:
            RAPPER_API = RAPPER_API + '/rapper'

        if RAPPER_API:
            data = {'text': prompt, 'max_tokens': length, 'temp': temp}
            data_json = json.dumps(data)
            r = requests.post(RAPPER_API, data=data_json)
            if r.status_code == 200:
                out = r.json()['out']
                out = out.replace('\\n', '\n')
            else:
                out = 'API OFFLINE'
            return str(out)
        else:
            return 'MORE!'
