from __main__ import app
from database_init import Patient
from flask import Flask, json, request, jsonify
from api.shared_methods import get_mrns_from_database, str_to_int
from pymodm import errors as pymodm_errors


@app.route('/api/get_patient_from_database/<MRN>/<field>', methods=['GET'])
def get_patient_from_database_route(MRN, field):
    value, status = str_to_int(MRN)
    if(not status):
        return "Invalid MRN format", 400
    valid_fields = ['MRN', 'patient_name', 'images', 'ECG_images']

    if(field not in valid_fields):
        return "Invalid field format: {} not in {}".format(field, valid_fields), 400

    try:
        db_item = Patient.objects.raw({"_id": value}).first()
    except pymodm_errors.DoesNotExist:
        return "No patient with MRN in database", 400
    
    if(field == "patient_name"):
        try:
            patient_name = db_item.patient_name
            return jsonify(patient_name), 200
        except pymodm_errors.DoesNotExist:
            return "Patient name field does not exist"
    
    return jsonify(db_item.MRN), 200
        
