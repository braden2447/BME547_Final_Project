from __main__ import app
from database_init import Patient
from flask import Flask, request, jsonify
from pymodm import errors as pymodm_errors
from api.shared_methods import validate_dict_input
from api.shared_methods import str_to_int
from api.shared_methods import get_patient_from_db




@app.route('/api/post_new_patient_info', methods=['POST'])
def post_new_patient():
    in_data = request.get_json()
    expected_keys = {"MRN": [str, int]}
    error_string, status_code = validate_dict_input(in_data, expected_keys)
    if error_string is not True:
        return error_string, status_code

    MRN, error = str_to_int(in_data["MRN"])
    if(error == False):
        return "MRN cannot be cast to int", 400

    update_patient_fields(MRN, in_data)

    return "Patient added to database", 200


def update_patient_fields(MRN, in_data):
    patient = get_patient_from_db(MRN)
    if(patient is False):       # No patient exists in db yet; create new one
        patient = Patient(MRN=MRN).save()

    if 'patient_name' in in_data.keys:
        patient.patient_name = in_data['patient_name']
    if 'ECG_Trace' in in_data.keys:
        patient.ECG_trace = in_data['ECG_Trace']





# The upload may also include a name, medical image, and/or heart
# rate & ECG image
# If the upload contains a medical record number not already found
# in the database,
# a new entry should be made for that patient, and the information
# sent with the
# request stored in this new record
