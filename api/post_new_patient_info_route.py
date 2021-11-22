from __main__ import app
from database_init import Patient
from flask import Flask, request, jsonify
from pymodm import errors as pymodm_errors
from api.shared_methods import get_mrns_from_database, validate_dict_input
from api.shared_methods import str_to_int


def get_patient_from_db(MRN):
    try:
        db_item = Patient.objects.raw({"_id": MRN}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return db_item


@app.route('/api/post_new_patient_info', methods=['POST'])
def post_new_patient():
    in_data = request.get_json()
    expected_keys = {"MRN": [str, int]}
    error_string, status_code = validate_dict_input(in_data, expected_keys)
    if error_string is not True:
        return error_string, status_code

    MRN = str_to_int(in_data["MRN"])[0]
    patient = get_patient_from_db(MRN)
    if(patient is False):       # No patient exists in db yet; create new one
        patient = Patient(MRN=MRN).save()

    if 'patient_name' in in_data.keys:
        patient.patient_name = in_data['patient_name']
    if 'ECG_Trace' in in_data.keys:
        patient.ECG_trace = in_data['ECG_Trace']

    return "Patient added to database", 200

# The upload may also include a name, medical image, and/or heart
# rate & ECG image
# If the upload contains a medical record number not already found
# in the database,
# a new entry should be made for that patient, and the information
# sent with the
# request stored in this new record
