import io

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, MATCH, ALL, ClientsideFunction

import json
import requests
import os
import base64
import re

# DIS IS ME HAHA
import uberduckapi as ud

# Generate more button
# more More More! More!! MORE MORE! MORE!!! MMOORREE!!! MOOOORRREEE!
gen_button = dbc.Button(
    id='gen-button',
    children='more',
    style={'margin-top': '1%', 'width': '80%', 'height': '2%', 'line-height': '200%', 'font-size': '300%'}
)

voice_button = dbc.Button(
    id='voice-button',
    children='TO VOICE',
    style={'margin-top': '1%', 'width': '80%', 'height': '2%', 'line-height': '200%',
           'font-size': '300%'}
)

# The app layout
voice_layout = html.Div([
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
                children=[
                    html.Div([
                        html.Div(id="loading-output", children=''),
                        html.Div(id="loading-output-voice", children=''),
                    ])
                ],
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
                html.Div(id='voice-button-container', children=[voice_button]),

             ], style={'text-align': 'center'}),


    html.Div(id='audio-holder', children=[], style={'text-align': 'center'}),

    # Sliders get styled based on isMobile
    html.Div(id='sliders-div', children=[
        dcc.Slider(
            id='length-slider',
            min=10,
            max=210,
            value=50,
            step=10,
            # tooltip={"placement": "bottom"},
            marks={
                10: {'label': '10', 'style': {'color': '#77b0b1', 'font-size': 'smaller'}},
                110: {'label': 'Output Length', 'style': {'font-size': 'smaller'}},
                210: {'label': '210', 'style': {'color': '#f50', 'font-size': 'smaller', 'white-space': 'nowrap'}}
            },
            included=False,

        ),

        dcc.Slider(
            id='temp-slider',
            min=0.5,
            max=1.5,
            value=0.8,
            step=0.1,
            # tooltip={"placement": "bottom"},
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


def voice_register_callbacks(dashapp):
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

    @dashapp.callback(Output("main-textarea", "rows"), Input("main-textarea", "value"))
    def change_rows(text):
        return text.count('\n') + 1

    @dashapp.callback(
        [Output('dynamic-button-container', 'children'),
         Output("main-textarea", "value"),
         Output("loading-output", "children"),
         Output('session', 'data')],
        Input('gen-button', 'n_clicks'),
        [State('dynamic-button-container', 'children'),
         State("main-textarea", 'value'),
         State('temp-slider', 'value'),
         State('length-slider', 'value'),
         State('session', 'data'),
         State('url', 'pathname')])
    def more_clicked(n_clicks, children, textarea, temp, max_tokens, store_data, pathname):
        # on page load
        if n_clicks is None:
            return children, textarea, '', {'clicks': 0}
        else:
            store_data['clicks'] += 1

            # TODO generate a bunch of fake songs for raw_outputs.txt
            if textarea == '':
                # out = random.choice(raw_outputs)
                textarea = 'Rick:'

            out = generate_out(textarea, temp, max_tokens, pathname)

            children.pop()
            more = ['More', 'More!', 'More!!', 'MORE!!!', 'MMOORREE!!!', 'MOOOORRREEE!!!!!!!']

            gen_button.children = more[store_data['clicks'] % len(more)]
            children.append(gen_button)
            # print('Generating a new button')

            # rows = out.count('\n')
            # rows = rows + 1
            return children, out, '', store_data

    @dashapp.callback(
        Output('gen-button', 'disabled'),
        Input('gen-button', 'n_clicks'),
    )
    def hide_more(n_clicks):
        if n_clicks is None:
            return False
        else:
            print('Disabling the button')
            return True

    def generate_out(prompt, temp, length, who):

        RAPPER_API = os.getenv('API_URL')
        # if who == '/rapper':
        #     RAPPER_API = RAPPER_API + who
        #
        # elif who == '/Cowboy':
        #     RAPPER_API = RAPPER_API + '/cowboy'
        #
        # elif who == '/RickMorty':
        #     RAPPER_API = RAPPER_API + '/rick'
        #
        # else:
        #     RAPPER_API = RAPPER_API + '/rapper'
        RAPPER_API = RAPPER_API + '/rick'

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

    # I want to output a list of buttons that you can pick which to save.
    @dashapp.callback(
        Output('voice-button-container', 'children'),
        Output('audio-holder', "children"),
        Output("loading-output-voice", "children"),
        Input('voice-button', 'n_clicks'),
        State("main-textarea", 'value'),
        State('voice-button-container', 'children'),
    )
    def voice_turn_to_voice(n_clicks, text, children):
        print("HEY!!")
        if n_clicks is None:
            print("No click VOICE")
            return [voice_button], [], ''

        print("GETTING VOICE")
        # install uberduckapi HAHA
        my_duck = ud.UberDuck(os.environ['UBERDUCK_Key'], os.environ['UBERDUCK_Secret'])
        # rick = my_duck.get_voice('rick-sanchez', "Hey everyone I'm alive")
        lines = text.split('\n')
        rick_lines = []
        for line in lines:
            if 'Rick:' in line:
                print(line)
                last_line = line
                last_line = last_line.replace('Rick: ', '')
                rick_lines.append([last_line, 'rick'])
                # ud.download_result(rick, 'temp.wav')
                # ud.play_voice(rick)
            elif 'Morty: ' in line:
                print(line)
                last_line = line
                last_line = last_line.replace('Morty: ', '')
                rick_lines.append([last_line, 'morty'])
            else:
                pass

        rick_clips = []
        out = []
        for line in rick_lines:
            if line[1] == 'rick':
                rick = my_duck.get_voice('rick-sanchez', line[0])
                if rick:
                    out.append(html.Audio(src=rick.uuid, controls=True))
                    rick_clips.append(rick)
            else:
                morty = my_duck.get_voice('morty', line[0])
                if morty:
                    out.append(html.Audio(src=morty.uuid, controls=True))
                    rick_clips.append(morty)

        children.pop()
        children.append(voice_button)

        return children, out, ''


    @dashapp.callback(
        Output('voice-button', 'disabled'),
        Input('voice-button', 'n_clicks')
    )
    def hide_voice(n_clicks):
        if n_clicks is None:
            return False
        else:
            print('Disabling the button')
            return True

    def line_cleaner(line):
        re.sub(r'\([^)]*\)', line)  # remove all (text in parentheses)
        re.sub(r'\*[^)]*\*', line)  # remove all *text in stars*
        re.sub(r'\([^)]*\)', line)  # remove all [text in brackets]

        char, text = line.split(':')[0]  # get string before the :
