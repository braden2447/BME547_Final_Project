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
    valid_fields = ['MRN', 'patient_name', 'ECG_trace',
                    'heart_rate', 'receipt_timestamps', 'medical_image']

    if(field not in valid_fields):
        return "Invalid field format: {} not in {}".format(field, valid_fields), 400

    try:
        db_item = Patient.objects.raw({"_id": value}).first()
    except pymodm_errors.DoesNotExist:
        return "No patient with MRN in database", 400

    # Obtain the requested field from the patient
    result, status = field_from_patient(field, valid_fields, db_item)
    if status != 200: # Will be error string
        return result, status
    return jsonify(result), 200


def field_from_patient(field, valid_fields, db_item):
    db_fields = [db_item.MRN, db_item.patient_name, db_item.ECG_trace,
                 db_item.heart_rate, db_item.receipt_timestamps, db_item.medical_image]

    for iterator, fields in enumerate(valid_fields):
        if(field == fields):
            try:
                item = db_fields[iterator]
                return item, 200
            except pymodm_errors.DoesNotExist:
                return "{} field does not exist".format(field), 400
    return "Passed iterator without returning", 400
        
