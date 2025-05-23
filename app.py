# This is a simple Flask application that visualise Dijkstra backpack problem.
import logging
from random import randint,uniform

from flask import Flask, request, jsonify, render_template
from algorithm.dijkstra import dijkstra, get_path, get_items,create_graph


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    """
    This function takes in the input data from the request and solves the backpack problem using Dijkstra algorithm.
    It returns the graph in a format that can be used by vis.js to visualize the graph.
    While doing so, it also validates the input data and handles errors.
    :return: JSON object with the graph in a format that can be used by vis.js
    """
    if request.is_json:
        # Get the input data from the json
        values = request.get_json().get('values')
        volumes = request.get_json().get('volumes')
        capacity = request.get_json().get('capacity')
        # Log the input data
        logging.info(f'Input data: values={values}, volumes={volumes}, capacity={capacity}')
        try:
            # Convert the input data to lists of floats
            values = list(map(float, values.split(',')))
            volumes = list(map(float, volumes.split(',')))
            capacity = float(capacity)
        except ValueError:
            logging.error('Invalid input format. Please provide number values.')
            return jsonify({'message': 'Invalid input format! Please provide comma-separated number values!'}),400
        else:
            # Validate the input data
            if not volumes or not values or not capacity:
                logging.error('Insufficient input data')
                return jsonify({'message': 'Insufficient input data! Please provide volumes, values and capacity!'}),400
            if len(volumes) != len(values):
                logging.error('Weights and values must have same length')
                return jsonify({'message': 'Weights and values lists must have same length!'}),400
            if capacity <= 0:
                logging.error('Capacity must be a positive number')
                return jsonify({'message': 'Capacity must be a positive number!'}),400
            if any(v <= 0 for v in volumes):
                logging.error('Weights must be positive numbers')
                return jsonify({'message': 'Weights must be positive numbers!'}),400
            if all(v > capacity for v in volumes):
                logging.error('No item can fit in the backpack')
                return jsonify({'message': 'No item can fit in the backpack!'}),400
            if any(v <= 0 for v in values):
                logging.error('Values must be positive numbers')
                return jsonify({'message': 'Values must be positive numbers!'}),400
            # Call the Dijkstra algorithm
            graph = create_graph(values=values,volumes=volumes, L=capacity)
            dist, prev = dijkstra(G=graph)
            # Get the path and items
            path = get_path(G=graph, prev=prev)
            items = get_items(path=path)

            def convert_to_vis_format(graph : dict, best_path=None, selected_items=None) -> dict:
                """
                Converts the graph to a format that can be used by vis.js to visualize the graph.
                :param graph: dictionary representing the graph.
                :param best_path: optimal path found by Dijkstra algorithm.
                :param selected_items: items selected in the backpack.
                :return: a dictionary containing nodes and edges in vis.js format.
                """
                nodes = set()
                edges = []

                # Create nodes set and format edges in vis.js format
                for from_node, neighbors in graph.items():
                    nodes.add(from_node)
                    for to_node, value in neighbors:
                        nodes.add(to_node)
                        edges.append({
                            "from": str(from_node),
                            "to": str(to_node),
                            "label": str(round(value, 2)),
                        })

                # Convert nodes to vis.js format with colors
                vis_nodes = []
                for node in nodes:
                    node_id = str(node)
                    # Node is described by capacity left and index
                    node_label = f"{round(float(node[0]),3)},{(node[1])}"
                    # Set color based on the node's properties
                    color = "lightgray" # default color
                    if best_path and node in best_path:
                        color = "lightgreen" # best path color
                    if selected_items:
                        idx = best_path.index(node) if node in best_path else -1
                        if idx > 0:
                            previous = best_path[idx - 1]
                            if node[0] < previous[0]:  # means the node is a parent
                                color = "orange" # picked item color
                    if node[1] == -1 or node[1] == len(best_path)-2: # means the node is a root or leaf
                        color = "#e74c3c" # root/leaf color

                    vis_nodes.append({
                        "id": node_id,
                        "label": node_label,
                        "color": color
                    })

                return {
                    "nodes": vis_nodes,
                    "edges": edges
                }
            # Convert the graph to vis.js format
            vis_graph = convert_to_vis_format(graph, best_path=path, selected_items=items)
            # Log the graph
            logging.info(f'Graph: {vis_graph}')
            return jsonify({"message": "Success", "data": vis_graph}),200
    else:
        logging.error('Invalid request method')
        return jsonify({'message': 'Invalid request method! Please use POST method!'}), 400

@app.route('/generate', methods=['GET'])
def generate():
    """
    This function generates random values, volumes and capacity for the backpack problem.
    Function generates random values and volumes for a number of vertices between 3 and 7.
    The values and volumes are generated as random floats between 1 and 100.
    The capacity is generated as a random float between 1 and 350.
    It returns the generated values, volumes and capacity in JSON format.
    :return: JSON object with generated values, volumes and capacity
    """
    number_of_vertices = randint(3,7)
    return jsonify(
        {
            "values": [round(uniform(1,100),2) for _ in range(number_of_vertices)],
            "volumes": [round(uniform(1,100),2) for _ in range(number_of_vertices)],
            "capacity": round(uniform(1,350),2),
        }
    )
@app.route('/results', methods=['POST'])
def result():
    """
    This function takes in the input data from the request and solves the backpack problem using Dijkstra algorithm.
    It returns summary of the items selected in the backpack, their total value and volume.
    :return: JSON object with selected items, their total value and volume
    """
    items_list = []
    value = 0
    volume = 0
    if request.is_json:
        data = request.get_json()
        # Log the input data
        logging.info(f'Input data: {data}')
        values = data.get('values')
        volumes = data.get('volumes')
        nodes = data.get('data').get('nodes')
        for node in nodes:
            if node.get('color') == 'orange':
                items_list.append(node.get('label').split(',')[1])
                value += values[int(items_list[-1])]
                volume += volumes[int(items_list[-1])]

        # Log the items
        logging.info(f'Items: {items_list}')
        # Log the value and volume
        logging.info(f'Value: {value}')
        logging.info(f'Volume: {volume}')

    return jsonify({"items": items_list, "value": value, "volume": volume}),200

# Error handler 404
@app.errorhandler(404)
def page_not_found(e):
    # Log the error
    logging.error(f'Page not found: {request.path}')
    # Return a custom error page
    return render_template('error-template.html', error_code=404, 
                          error_message='Page you are looking for does not exists!'), 404

# Error handler 500
@app.errorhandler(500)
def internal_server_error(e):
    # Log the error
    logging.error(f'Internal server error: {request.path}')
    # Return a custom error page
    return render_template('error-template.html', error_code=500, 
                          error_message='Server issue occurred!'), 500

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
