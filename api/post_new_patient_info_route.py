from __main__ import app
from flask import Flask, request, jsonify
from pymodm import errors as pymodm_errors
from api.shared_methods import validate_dict_input
from api.shared_methods import str_to_int
from api.shared_methods import update_patient_fields


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