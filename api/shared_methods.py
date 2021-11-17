def validate_input(in_data, expected_keys):
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    for key in expected_keys:
        if key not in in_data:
            return "The key {} is missing from input".format(key), 400
        if type(in_data[key]) is not expected_keys[key]:
            return "The key {} has the wrong data type".format(key), 400
    return True, 200


# For api/get_mrn route
def get_mrns_from_database(results):
    MRN_list = []

    for item in results:
        MRN_list.append(item.MRN)

    return MRN_list
