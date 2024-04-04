from flask import Flask, request, jsonify
import pandas as pd


app = Flask(__name__)
price_data = pd.read_csv("data/prices.csv")
@app.route('/costs', methods=['GET'])
def get_costs():
    model = request.args.get('model', type=str)
    input_token = request.args.get('input_token', default=1, type=int) 
    output_token = request.args.get('output_token', default=1, type=int)
    costs = price_data[price_data.model == model].to_dict('records')[0]
    cost = costs['price_1m_input'] * input_token + costs['price_1m_output'] * output_token
    return jsonify({"cost": cost})

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify({"models": price_data[['model', 'vendor']].to_dict('records')})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
