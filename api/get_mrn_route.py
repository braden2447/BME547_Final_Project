from __main__ import app
from database_init import Patient
from flask import Flask, request, jsonify
from api.shared_methods import get_mrns_from_database


@app.route('/api/get_mrn', methods=['GET'])
def get_mrn_route():
    """Accepts get request and returns list of existing
    MRNs within database.

    Calling this method will return a jsonified list of
    MRN integers within the database. If there are no patients
    in the database, the list will return empty.

    Returns:
        json: list of MRN integers
    """
    MRN_list = get_mrns_from_database(Patient.objects.raw({}))
    MRN_list.sort()
    return jsonify(MRN_list), 200
