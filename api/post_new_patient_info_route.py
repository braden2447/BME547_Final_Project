from __main__ import app
from flask import Flask, request, jsonify
from pymodm import errors as pymodm_errors
from api.shared_methods import validate_dict_input
from api.shared_methods import str_to_int


@app.route('/api/post_new_patient_info', methods=['POST'])
def post_new_patient():
    in_data = request.get_json()
    # Validate input has MRN
    keys = list(in_data.keys())
    expected_keys = {"MRN": [str, int]}
    error_string, status_code = validate_dict_input(in_data, expected_keys)
    if error_string is not True:
        return error_string, status_code
    MRN = str_to_int(in_data["MRN"])[0]
    
    # Validate each acceptable field
    if 'patient_name' in keys:
        expected_keys = {"patient_name": [str]}
        error_string, status_code = validate_dict_input(in_data, expected_keys)
        if error_string is not True:
            return error_string, status_code
    if 'medical_image' in keys:
        expected_keys = {"medical_image": [str]}
        error_string, status_code = validate_dict_input(in_data, expected_keys)
        if error_string is not True:
            return error_string, status_code
    if ('ECG_trace' in keys) or ('heart_rate' in keys):
        expected_keys = {"ECG_trace": [str], "heart_rate": [int, str]}
        error_string, status_code = validate_dict_input(in_data, expected_keys)
        if error_string is not True:
            return error_string, status_code

    # Call function to update fields accordingly in database
    update_patient_fields(MRN, in_data)

    # Return that information has been added
    return "Patient information added to database", 200


def update_patient_fields(input_MRN, in_data):
    from api.shared_methods import get_patient_from_db
    from database_init import Patient
    from datetime import datetime as dt

    patient = get_patient_from_db(input_MRN)
    if(patient is False):       # No patient exists in db yet; create new one
        patient = Patient(MRN=input_MRN).save()
    keys = list(in_data.keys())

    if 'patient_name' in keys:
        patient.patient_name = in_data['patient_name']
    if 'ECG_trace' in keys:
        patient.ECG_trace.append(in_data['ECG_trace'])
        patient.receipt_timestamps.append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
    if 'heart_rate' in keys:
        patient.heart_rate.append(str_to_int(in_data['heart_rate'])[0])
    if 'medical_image' in keys:
        patient.medical_image.append(in_data['medical_image'])
    patient.save()


# The upload may also include a name, medical image, and/or heart
# rate & ECG image
# If the upload contains a medical record number not already found
# in the database,
# a new entry should be made for that patient, and the information
# sent with the
# request stored in this new record
