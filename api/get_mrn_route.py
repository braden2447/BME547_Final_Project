from __main__ import app
from database_init import Patient
from flask import Flask, request, jsonify


@app.route('/api/get_mrn', methods=['GET'])
def get_mrn_route():
    MRN_list = get_mrns_from_database()
    MRN_list.sort()
    return jsonify(MRN_list), 200


def get_mrns_from_database():
    MRN_list = []
    results = Patient.objects.raw({})

    for item in results:
        MRN_list.append(item.MRN)

    return MRN_list
