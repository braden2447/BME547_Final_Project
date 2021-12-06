from __main__ import app
from database_init import Patient
from flask import Flask, json, request, jsonify
from api.shared_methods import get_mrns_from_database, str_to_int
from api.shared_methods import field_from_patient, get_patient_from_db
from pymodm import errors as pymodm_errors


@app.route('/api/get_patient_from_database/<MRN>/<field>', methods=['GET'])
def get_patient_from_database_route(MRN, field):
    """Allows client to obtain select data from the
    database

    Allows user to input MRN and field from patient
    they are interested in, and returns the information
    pulled from the database as specified by field.
    Valid fields are: 'MRN', 'patient_name', 'ECG_trace',
                      'heart_rate', 'receipt_timestamps',
                      'medical_image'

    Returns:
        json: requested information
    """
    value, status = str_to_int(MRN)
    if(not status):
        return "Invalid MRN format", 400
    valid_fields = ['MRN', 'patient_name', 'ECG_trace',
                    'heart_rate', 'receipt_timestamps', 'medical_image']

    if(field not in valid_fields):
        return "Invalid field format: {} not in {}".format(field,
                                                           valid_fields), 400

    db_item = get_patient_from_db(value)
    if db_item == False:
        return "No patient with MRN in database", 400

    # Obtain the requested field from the patient
    result, status = field_from_patient(field, valid_fields, db_item)
    if status != 200:  # Will be error string if status != 200
        return result, status
    return jsonify(result), 200
