import requests

host_route = "http://127.0.0.1:5000/"


# Test api/get_mrn route
r = requests.get(host_route + "api/get_mrn")
print("{}: {}".format(r.status_code, r.json()))
print(type(r.json()))
