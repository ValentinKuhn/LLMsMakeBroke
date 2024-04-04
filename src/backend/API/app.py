from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/costs', methods=['GET'])
def get_costs():
    users = request.args.get('users', default=1, type=int)
    cost = users * 10
    return jsonify({"cost": cost})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
