from __main__ import app
from database_init import Patient
from flask import Flask, request, jsonify
from api.shared_methods import get_mrns_from_database, str_to_int
from pymodm import errors as pymodm_errors


@app.route('/api/get_patient_from_database/<MRN>', methods=['GET'])
def get_patient_from_database_route(MRN):
    value, status = str_to_int(MRN)
    if(not status):
        return "Invalid MRN format", 400

    try:
        db_item = Patient.objects.raw({"_id": value}).first()
    except pymodm_errors.DoesNotExist:
        return "No patient with MRN in database", 400

    return jsonify(db_item.MRN), 200
