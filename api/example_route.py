from __main__ import app

@app.route('/example_route', methods=['GET'])
def example_route():
    return "Example route!", 200