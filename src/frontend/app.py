# Importing required libraries
import dash
from dash import html, dcc, Input, Output, State, dash_table
import requests
from time import sleep

# Initialize the Dash app
app = dash.Dash(__name__)

try:
    models = requests.get('http://llm_api:5000/models').json()
except:
    sleep(3)
    models = requests.get('http://llm_api:5000/models').json()
model_names = [model["model"] for model in models['models']]

# Define the layout of the app
app.layout = html.Div([
    html.H1(f"LLMs make me broke"),
    html.H3("Choose your model:"),
    dcc.Dropdown(model_names, model_names[0], id='input-model'),
    html.H3("How many tokens will be prompted?"),
    dcc.Input(id='input-input_token', type='number', placeholder='Token in million per month'),
    html.H3("How muany tokens will the model return?"),
    dcc.Input(id='input-output_token', type='number', placeholder='Token in million per month'),
    html.H3(""),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container')
])



# Define the callback to update the cost
@app.callback(
    Output('container', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('input-model', 'value'), 
     State('input-input_token', 'value'), 
     State('input-output_token', 'value'), 
    ])
def update_output(n_clicks, model_name,input_token,output_token):
    if n_clicks > 0:
        # Call your API with the input parameters
        response = requests.get('http://llm_api:5000/costs', params={'model': model_name, 'input_token': input_token, "output_token": output_token})
        cost = response.json()  # Assuming the API returns a JSON with the cost
        return f'The monthly cost is: {cost["cost"]}'
    return 'Enter values to get the cost'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
