import requests


# Test api/get_mrn route
r = requests.get("http://127.0.0.1:5000/api/get_mrn")
print("{}: {}".format(r.status_code, r.json()))
print(type(r.json()))
