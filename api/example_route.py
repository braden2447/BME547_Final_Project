from __main__ import app


@app.route('/example_route', methods=['GET'])
def example_route():
    """A simple example route to see how to implement
    routes within this git repository.

    Routes can be added to the server by importing them
    within start server method of ecg_server.py

    Returns:
        str, int: Example route!, 200
    """
    return "Example route!", 200
