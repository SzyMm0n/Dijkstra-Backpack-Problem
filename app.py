# This is a simple Flask application that visualise Dijkstra backpack problem.
import logging

from flask import Flask, request, jsonify, render_template
from algorithm.dijkstra import dijkstra, get_path, get_items


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    if request.method == 'POST':
        try:
            weights = request.form['weights']
            values = request.form['values']
            capacity = request.form['capacity']
            weights = list(map(float, weights.split(',')))
            values = list(map(float, values.split(',')))
            capacity = float(capacity)
            if len(weights) != len(values):
                logging.error('weights and values must have same length')
                return render_template('error-template.html', error_code=400, 
                                      error_message='Weights and values must have same length!')
            if capacity <= 0:
                logging.error('capacity must be a positive number')
                return render_template('error-template.html', error_code=400, 
                                      error_message='Capacity must be a positive number!')
            if any(w <= 0 for w in weights):
                logging.error('weights must be positive numbers')
                return render_template('error-template.html', error_code=400, 
                                      error_message='Weights must be positive numbers!')
            if any(v <= 0 for v in values):
                logging.error('values must be positive numbers')
                return render_template('error-template.html', error_code=400, 
                                      error_message='Values must be positive numbers!')
        except ValueError:
            logging.error('Invalid input format. Please provide comma-separated number values.')
            return render_template('error-template.html', error_code=400, 
                                  error_message='Invalid input format! Please provide comma-separated number values!')
    return jsonify({'message': 'Input is valid.'}), 200

# Obsługa błędów 404 (nie znaleziono)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-template.html', error_code=404, 
                          error_message='Strona, której szukasz, nie istnieje.'), 404

# Obsługa błędów 500 (błąd serwera)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error-template.html', error_code=500, 
                          error_message='Wystąpił wewnętrzny błąd serwera.'), 500

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
