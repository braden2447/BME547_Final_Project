from typing import Type
from flask import Flask, request, jsonify
import requests
from datetime import datetime as dt
import logging


app = Flask(__name__)


@app.route("/", methods=["GET"])
def status():
    """States that server is on feedback message

    Returns:
        string: "Server is on"
    """
    return "Server is on"


def start_server():
    import database_init
    import api.get_mrn_route
    import api.get_patient_from_database_route
    import api.post_new_patient_info_route
    import api.shared_methods
    app.run()


if __name__ == "__main__":
    logging.basicConfig(filename='./logging/ECG_server_log.log',
                        filemode='w', level=logging.INFO)
    start_server()
