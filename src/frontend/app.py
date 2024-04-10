# Importing required libraries
import dash
from dash import html, dcc, Input, Output, State, dash_table
import requests
from time import sleep
import os
import dash_bootstrap_components as dbc
from utils.cards import user_prompts, output_prompts, input_prompts

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

api_host = f'http://{os.environ["api_host"]}:{os.environ["api_port"]}/'


try:
    models = requests.get(f'{api_host}/models').json()
except:
    sleep(3)
    models = requests.get(f'{api_host}/models').json()
model_names = [model["model"] for model in models]

money = dash_table.FormatTemplate.money(2)

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("What does my LLM cost?",
            style={'textAlign': 'center'}))),
    html.H3(""),
    input_prompts,
    html.H3(""),
    user_prompts,
    html.H3(""),
    output_prompts,
    html.H3(""),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.H3(""),
    html.Div(id='number_tokens'),
    html.H3(""),
    dash_table.DataTable(id='output_table',
                         columns=[{'name': 'Model',
                                   'id': 'model'},
                                  {'name': 'Vendor',
                                   'id': 'vendor'},
                                  {'name': 'Modelsize',
                                   'id': 'model_size'},
                                  {'name': 'Cost per month in $',
                                   'id': 'cost',
                                   "type": 'numeric',
                                   "format": money},
                                  {'name': 'Cost per month per user $',
                                   'id': 'cost_user',
                                   "type": 'numeric',
                                   "format": money}],
                         sort_action="native",
                         filter_action="native",
                         style_as_list_view=True)],
    fluid=True, style={'padding': '20px'}
)


# Define the callback to update the cost
@app.callback(
    Output('number_tokens', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('input-input_user', 'value'),
     State('input-input_amount', 'value'),
     State('input-input_tokens', 'value'),
     State('input-input_rag', 'value'),
     State('input-output_token', 'value'),
     ])
def update_output(n_clicks, input_user, input_amount, input_tokens, input_rag, output_token):
    if input_user is None or input_amount is None or input_tokens is None:
        return ""
    else:
        n_request = input_user * input_amount * 30
        n_tokens = n_request * input_tokens
        n_tokens_rag = n_request * input_rag
        return f'With {n_request} requests the users generate {round(n_tokens,0)} input tokens and uses additonally {n_tokens_rag} from an external source.'


# Define the callback to update the cost
@app.callback(
    Output('output_table', 'data'),
    [Input('submit-val', 'n_clicks')],
    [State('input-input_user', 'value'),
     State('input-input_amount', 'value'),
     State('input-input_tokens', 'value'),
     State('input-input_rag', 'value'),
     State('input-output_token', 'value'),
     ])
def update_output(n_clicks, input_user, input_amount, input_tokens, input_rag, output_token):
    if input_user is None or input_amount is None or input_tokens is None:
        return [{"model": '', "vendor": '', "model_size": '', "cost": ''}]
    else:
        n_request = input_user * input_amount * 30
        n_tokens_in = n_request * (input_tokens+input_rag) / 10**6
        n_tokens_out = n_request * output_token / 10**6
        for model in models:
            response = requests.get(f'{api_host}/costs', params={
                                    'model': model['model'], 'input_token': n_tokens_in, "output_token": n_tokens_out})
            cost = response.json()["cost"]
            # Assuming the API returns a JSON with the cost
            model['cost'] = cost
            model['cost_user'] = cost / input_user
        return models


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
