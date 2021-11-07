import dash_bootstrap_components as dbc
from dash import dcc
from dash import html, callback_context
from dash.dependencies import Input, Output, State, ClientsideFunction

import json
import requests
import os
from ..webapp import is_logged_in
from .bucket import write_file_blob



good_button = dbc.Button(
    id='good-button',
    children='good',
    className='btn btn-success',
    style={'margin-top': '1%', 'width': '40%', 'height': '2%', 'line-height': '100%', 'font-size': '200%'}
)

bad_button = dbc.Button(
    id='bad-button',
    children='bad',
    className="btn btn-danger",
    style={'margin-top': '1%', 'width': '40%', 'height': '2%', 'line-height': '100%', 'font-size': '200%'}
)

back_button = dbc.Button(
    id='back-button',
    children='back',
    className="btn btn-warning",
    style={'margin-top': '1%', 'width': '40%', 'height': '2%', 'line-height': '100%', 'font-size': '200%'}
)



# The app layout
tune_layout = html.Div([
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
                              good_button,
                              bad_button,
                              #back_button
                          ]),

             ], style={'text-align': 'center', 'margin-bottom': '10%'}),

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
                110: {'label': 'Length', 'style': {'font-size': 'smaller'}},
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


def tune_register_callbacks(dashapp):
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
                      Output('main-textarea', 'style'),
                      [Input('div-mobile', 'children')],
                      State('slider-div', 'style'),
                      State('main-textarea', 'style'))
    def style_mobile(is_mobile, slider_style, text_style):
        print("IS MOBILE:", is_mobile)
        # if mobile overwrite style
        if is_mobile:
            slider_style['transform'] = 'scale(2.5)'
            slider_style['width'] = '40%'

            text_style['font-size'] = '150%'

        return slider_style, text_style

    @dashapp.callback(
        [Output('dynamic-button-container', 'children'),
         Output("main-textarea", "value"),
         Output("main-textarea", "rows"),
         Output("loading-output", "children"),
         Output('session', 'data')],
        Input('good-button', 'n_clicks'),
        Input('bad-button', 'n_clicks'),
        [State('dynamic-button-container', 'children'),
         State("main-textarea", 'value'),
         State('temp-slider', 'value'),
         State('length-slider', 'value'),
         State('session', 'data')])
    def display_newbutton(n_clicks_good, n_clicks_bad, children, textarea, temperature, max_tokens, store_data):
        # on page load


        if n_clicks_good is None and n_clicks_bad is None:
            # initial load in text?
            if textarea == '':
                textarea = '[Verse 1:'

            out = generate_out(textarea, temperature, max_tokens)

            # children = [good_button, bad_button]
            # print('Generating a new button')
            rows = out.count('\n')
            rows = rows + 1

            return children, out, rows, '', {'clicks': 0}
        else:
            # will use to keep count of swipes

            store_data['clicks'] += 1
            changed_id = [p['prop_id'] for p in callback_context.triggered][0]
            if 'good' in changed_id:
                which_button = 'good'
                # TODO save textarea to Bucket as file
                user = is_logged_in()

                textarea = textarea.replace('\n', '\\n')
                textarea += '\n'
                write_file_blob('central-bucket-george', user, textarea)
            # elif 'bad' in changed_id:
            #     which_button = 'bad'
            #     # TODO re-roll /reject bad

            textarea = '[Verse 1:'

            out = generate_out(textarea, temperature, max_tokens)

            children = [good_button, bad_button]
            # print('Generating a new button')
            rows = out.count('\n')
            rows = rows + 1
            return children, out, str(rows), '', store_data

    # Disable the button while it loads
    @dashapp.callback(
        Output('good-button', 'disabled'),
        Output('bad-button', 'disabled'),
        [Input('good-button', 'n_clicks'),
         Input('bad-button', 'n_clicks')]
    )
    def hide_newbutton(n_clicks, n_clicks_2):
        # i think this is on load none != 0 so no need to add n_clicks_2
        if n_clicks is None:
            return False, False
        else:
            return True, True

    def generate_out(prompt, temperature, length):
        RAPPER_API = os.getenv('API_URL')

        if RAPPER_API:
            data = {'text': prompt, 'max_tokens': length, 'temp': temperature}
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
