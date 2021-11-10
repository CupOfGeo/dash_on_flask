import dash_bootstrap_components as dbc
from dash import html, callback_context
from dash.dependencies import Input, Output, State, MATCH, ALL
import json
import re

from app.models import get_models

from app.dashapp1.spotify_genius import get_playlist_name
from app.webapp import get_user

table_header = [
    html.Thead(html.Tr([html.Th("Model"), html.Th("Dataset"), html.Th("Use"), html.Th("Tune"), html.Th("Delete")]))
]

profile_layout = html.Div([

    html.H1(id='title'),

    html.Div(
        [
            dbc.Table(children=table_header,
                      id="table-model",
                      color="primary",
                      className="table table-hover",
                      ),
        ]
    ),
    dbc.Button(id='test', children='TEST'),
    dbc.Button(id='build', children='build'),
    html.Div(id='b')
])


def model_name_valid(model_name):
    pattern = re.compile('^\w+$')
    result = pattern.match(model_name)
    print(result)
    if result is None:
        return "Model must contain only letters numbers or underscore"

    # now to check if the user already has a model with this name
    models = get_models()
    for model in models:
        if model.name.lower() == model_name.lower():
            return f"You already have a model named {model_name}"

    return ''


def dataset_url_valid(dataset_url):
    # TODO assert no newlines
    pattern = re.compile('https:\/\/open\.spotify\.com\/playlist\/[0-9a-zA-Z]+$')
    result = pattern.match(dataset_url)
    print(result)
    if result is None:
        return "Not a spotify playlist link"

    return ''


def profile_register_callbacks(dashapp):
    # TODO change title n_clicks
    @dashapp.callback(Output('title', 'children'),
                      Input('title', 'n_clicks'))
    def make_title(n_clicks):
        user = get_user()
        return f'Hi, {user.username}! you have {user.models_in_use} in use of {user.models_allowed} models available'

    # Disable the button while it loads
    # TODO don't make the model query twice put it in a store or something maybe
    @dashapp.callback(
        Output('table-model', 'children'),
        Input('test', 'n_clicks'),
        Input({'type': 'delete', 'index': ALL}, 'n_clicks'),
        Input({'type': 'build_button', 'index': ALL}, 'n_clicks'),
        # going to have to make inputs for the text fields with the ALL MATCH
        State({'type': 'model_name_input', 'index': ALL}, 'value'),
        State({'type': 'dataset_url_input', 'index': ALL}, 'value'),
    )
    def make_table(test, delete_click, build_click, model_name, dataset_url):
        if len(model_name) == 1:
            model_name = model_name[0]
        if len(dataset_url) == 1:
            dataset_url = dataset_url[0]
        user = get_user()
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]

        if 'build_button' in changed_id:
            # Check that fields are valid
            name_error = model_name_valid(model_name)
            dataset_error = dataset_url_valid(dataset_url)
            if name_error == '' and dataset_error == '':
                # no errors create model and send alert

                # get the playlist name from id
                # https://open.spotify.com/playlist/1bsirFMYamoch1A5GyqDkA
                playlist_id = dataset_url.split('/')[-1]
                playlist_name = get_playlist_name(playlist_id)
                print(playlist_name)

                # make new model
                user.make_model(model_name, playlist_id)
            else:
                # TODO show error
                '''
                <div class="form-group has-success">
                  <label class="form-label mt-4" for="inputValid">Valid input</label>
                  <input type="text" value="correct value" class="form-control is-valid" id="inputValid">
                  <div class="valid-feedback">Success! You've done it.</div>
                </div>

                <div class="form-group has-danger">
                  <label class="form-label mt-4" for="inputInvalid">Invalid input</label>
                  <input type="text" value="wrong value" class="form-control is-invalid" id="inputInvalid">
                  <div class="invalid-feedback">Sorry, that username's taken. Try another?</div>
                </div>

                '''
                print(f'name_error:{name_error}')
                print(f'dataset_error:{dataset_error}')


        # Delete buttons
        if delete_click == [] or delete_click.count(None) == len(delete_click):
            pass
        else:
            res = json.loads(changed_id.split('.')[0])
            print(res['index'])
            user.delete_model(res['index'])

        # make table of models they already have
        models = get_models()

        row_list = []
        for model in models:
            delete_button = dbc.Button('Delete', id={
                'type': 'delete',
                'index': model.id
            }, n_clicks=None)

            row = html.Tr([
                html.Td(model.name),
                html.Td(get_playlist_name(model.dataset_id)),
                html.Td("Use"),
                html.Td("Tune"),
                html.Td(delete_button)])
            row_list.append(row)

        if user.models_in_use < user.models_allowed:
            # only if you are allowed to make more models
            new_model_row = html.Tr([
                html.Td(
                    dbc.Input(id={'type': 'model_name_input', 'index': 0}, placeholder='My_Model_Name', debounce=True)),
                html.Td(dbc.Input(id={'type': 'dataset_url_input', 'index': 0}, placeholder='Spotify Playlist URL',
                                  debounce=True)),
                html.Td(),
                html.Td(),
                html.Td(dbc.Button('Build', id={'type': 'build_button', 'index': 0}, n_clicks=None))])

            row_list.append(new_model_row)
            pass

        else:
            # else tell them to buy more
            pass

        table_body = [html.Tbody(row_list)]
        return table_header + table_body
