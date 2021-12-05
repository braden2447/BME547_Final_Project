from __main__ import app
from flask import Flask, request, jsonify
from pymodm import errors as pymodm_errors
from api.shared_methods import validate_dict_input
from api.shared_methods import str_to_int


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

    return "Patient info added to database", 200


def update_patient_fields(input_MRN, in_data):
    from api.shared_methods import get_patient_from_db
    from database_init import Patient    

    patient = get_patient_from_db(input_MRN)
    if(patient is False):       # No patient exists in db yet; create new one
        patient = Patient(MRN=input_MRN).save()
    keys = list(in_data.keys())

    if 'patient_name' in keys:
        patient.patient_name = in_data['patient_name']
    if 'ECG_Trace' in keys:
        patient.ECG_trace.append(in_data['ECG_Trace'])
    if 'heart_rate' in keys:
        patient.heart_rate.append(in_data['heart_rate'])
    if 'medical_image' in keys:
        patient.medical_image.append(in_data['medical_image'])
    if 'receipt_timestamps' in keys:
        patient.receipt_timestamps.append(in_data['receipt_timestamps'])
    

# The upload may also include a name, medical image, and/or heart
# rate & ECG image
# If the upload contains a medical record number not already found
# in the database,
# a new entry should be made for that patient, and the information
# sent with the
# request stored in this new record
