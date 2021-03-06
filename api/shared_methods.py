from database_init import Patient, PatientTest
from pymodm import errors as pymodm_errors
from datetime import datetime as dt


def validate_dict_input(in_data, expected_keys):
    """Validate the presence of expected keys, value types of
    in_data

    Format expected_keys as follows:

    expected_keys = {
        "key1": [allowed_type1, allowed_type2,...],
        "key2": [allowed_type1, allowed_type2,...],
        ...
    }

    This method will return true only if all expected keys
    exist within in in_data and all in_data value types
    are allowed

    Note that user may need to include functionality
    for allowed types to verify certain cases

    Args:
        in_data (dict(string:obj)): dictionary input data
        expected_keys (dict(string:list)):

    Returns:
        str, bool: error string or boolean truth value
        int: status code
    """
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    for key in expected_keys:
        # Ensure all expected keys exist within in_data
        if key not in in_data:
            return "The key {} is missing from input".format(key), 400

        # Ensure all types are valid
        if type(in_data[key]) not in expected_keys[key]:
            return "The key {} has invalid data type".format(key), 400

        # Verify str are able to cleanly cast to int
        if set(expected_keys[key]) == set([str, int]):
            check = str_to_int(in_data[key])
            if not check[1]:
                m1 = "The value \"{}\"".format(in_data[key])
                m2 = " in key {} cannot be cast to int".format(key)
                return m1+m2, 400

    return True, 200


def str_to_int(value):
    """Converts an input string
    into int value, or returns input
    if input is already int

    Method curated by Anuj Som

    Args:
        value (int, str): Accepts an int or string to convert to int

    Returns:
        tuple (int, bool): returns (integer value, True) if conversion success
                           returns (-1,False)            if conversion failed
    """
    if(type(value) == int):
        return (value, True)
    try:
        int_val = int(value)
    except ValueError:
        return (-1, False)
    return (int_val, True)


# For api/get_mrn route
def get_mrns_from_database(results):
    """Accepts json request and posts new patient heart rate
    to server database.

    Method curated by Braden Garrison

    json request should contain a dict formatted as follows:
    {
        "patient_id": int, # Should be patient MRN
        "heart_rate_average_since": str # Should be formatted in form:
                                        # "2018-03-09 11:00:36"
    }
    This method will be used to calculate and return the heart
    rate interval average of a specified patient since the given
    date/time.

    Args:
        QuerySet: all patients within database

    Returns:
        list [int]: list of MRNs within database
    """
    MRN_list = []

    for item in results:
        MRN_list.append(item.MRN)

    return MRN_list


def get_patient_from_db(MRN):
    """Accepts MRN and gets specified patient from database,
    else returns False if no patient with MRN in database.

    Args:
        int: MRN to lookup

    Returns:
        QuerySet, bool: patient object from db or False if not found
    """
    try:
        db_item = Patient.objects.raw({"_id": MRN}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return db_item


def get_patient_from_db_pt(MRN):
    """Same as get_patient_from_db method
    but for PatientTest mongodb collection

    Args:
        int: MRN to lookup

    Returns:
        QuerySet, bool: patient object from db or False if not found
    """
    try:
        db_item = PatientTest.objects.raw({"_id": MRN}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return db_item


# For api/post_new_patient_info route
def update_patient_fields(input_MRN, in_data):
    """Updates mongodb database fields according
    to information found in in_data for patient
    found by input_MRN

    in_data should contain a dict formatted as follows:
    {
        "MRN": [int, str]         # can be an int or string
        "patient_name": str,      # Should be patient MRN
        "ECG_trace": b64_str      # Image info as b64_string
        "heart_rate": int         # heart rate of above image
        "medical_images": b64_str # Image info as b64_string
    }
    The only required field is "MRN". If an ECG trace is
    uploaded, it must be accompanied by a heart_rate and
    vice-versa. Will save this information to the database
    by either creating new entries or appending to existing
    lists.

    Args:
        int: Input MRN to add data to
        dict: input data with information to assign
    """
    patient = get_patient_from_db(input_MRN)
    if(patient is False):       # No patient exists in db yet; create new one
        patient = Patient(MRN=input_MRN).save()
    keys = list(in_data.keys())

    if 'patient_name' in keys:
        patient.patient_name = in_data['patient_name']
    if 'ECG_trace' in keys:
        patient.ECG_trace.append(in_data['ECG_trace'])
        now_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        patient.receipt_timestamps.append(now_time)
    if 'heart_rate' in keys:
        patient.heart_rate.append(str_to_int(in_data['heart_rate'])[0])
    if 'medical_image' in keys:
        patient.medical_image.append(in_data['medical_image'])
    patient.save()


# Exact same function as above but for PatientTest class
def update_patient_fields_pt(input_MRN, in_data):
    """Same as update_patient_fields but for PatientTest
    class

    in_data should contain a dict formatted as follows:
    {
        "MRN": [int, str]         # can be an int or string
        "patient_name": str,      # Should be patient MRN
        "ECG_trace": b64_str      # Image info as b64_string
        "heart_rate": int         # heart rate of above image
        "medical_images": b64_str # Image info as b64_string
    }
    The only required field is "MRN". If an ECG trace is
    uploaded, it must be accompanied by a heart_rate and
    vice-versa. Will save this information to the database
    by either creating new entries or appending to existing
    lists.

    Args:
        int: Input MRN to add data to
        dict: input data with information to assign
    """
    patient = get_patient_from_db_pt(input_MRN)
    if(patient is False):       # No patient exists in db yet; create new one
        patient = PatientTest(MRN=input_MRN).save()
    keys = list(in_data.keys())

    if 'patient_name' in keys:
        patient.patient_name = in_data['patient_name']
    if 'ECG_trace' in keys:
        patient.ECG_trace.append(in_data['ECG_trace'])
        now_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        patient.receipt_timestamps.append(now_time)
    if 'heart_rate' in keys:
        patient.heart_rate.append(str_to_int(in_data['heart_rate'])[0])
    if 'medical_image' in keys:
        patient.medical_image.append(in_data['medical_image'])
    patient.save()


# For api/get_patient_from_database route
def field_from_patient(field, valid_fields, db_item):
    """Gets specific field from a patient object,
    making sure field requested is within valid_fields

    Valid fields are: ['MRN', 'patient_name', 'ECG_trace',
                      'heart_rate', 'receipt_timestamps',
                      'medical_image']

    Args:
        str: field, a string of the valid fields
        valid_fields: the above list
        QuerySet: patient object from database

    Returns:
        int/list/str: requested field from patient
    """
    db_fields = [db_item.MRN, db_item.patient_name, db_item.ECG_trace,
                 db_item.heart_rate, db_item.receipt_timestamps,
                 db_item.medical_image]

    for iterator, fields in enumerate(valid_fields):
        if(field == fields):
            try:
                item = db_fields[iterator]
                return item, 200
            except pymodm_errors.DoesNotExist:
                return "{} field does not exist".format(field), 400
    return "Passed iterator without returning", 400
