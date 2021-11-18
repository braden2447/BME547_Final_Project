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
        [type]: [description]
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
    MRN_list = []

    for item in results:
        MRN_list.append(item.MRN)

    return MRN_list


# For api/get_patient_from_database/MRN route
def get_patient_from_database(MRN):
    None
