from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

def get_data(local: bool):
    if local:
        return pd.read_csv("data/prices.csv")
    else:
        return pd.DataFrame({}) # Implement remote database access
    

price_data = get_data(local=os.environ['local_data']=="TRUE")

@app.route('/costs', methods=['GET'])
def get_costs():
    model = request.args.get('model', type=str)
    input_token = request.args.get('input_token', default=1, type=float) 
    output_token = request.args.get('output_token', default=1, type=float)
    costs = price_data[price_data.model == model].to_dict('records')[0]
    cost = costs['price_1m_input'] * input_token + costs['price_1m_output'] * output_token
    return jsonify({"cost": cost})

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify(price_data[['model', 'vendor', 'model_size']].to_dict('records'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
