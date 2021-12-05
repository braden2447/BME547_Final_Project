import requests
from PIL import Image
from database_init import Patient, PatientTest
from datetime import datetime as dt
import image_toolbox as itb

host_route = "http://127.0.0.1:5000/"


# Test api/get_mrn route
# r = requests.get(host_route + "api/get_mrn")
# print("{}: {}".format(r.status_code, r.json()))
# print(type(r.json()))


# Testing post_new_patient_info route
b64_image = itb.file_to_b64("images/test_image.png")
b64_medical_image = itb.file_to_b64("images/esophagus2.jpg")
pat1_info = {
    'MRN': 1,
    'patient_name': "John Smith",
    'ECG_Trace': b64_image,
    'heart_rate': 65,
    'medical_image': b64_medical_image
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat1_info)
print("{}: {}".format(r.status_code, r.text))