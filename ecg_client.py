import requests
from PIL import Image
from database_init import Patient, PatientTest, clean_server
from datetime import datetime as dt
import image_toolbox as itb

host_route = "http://127.0.0.1:5000/"


# Test api/get_mrn route
# Will return sorted list of existing MRN in database
# r = requests.get(host_route + "api/get_mrn")
# print("{}: {}".format(r.status_code, r.json()))
# print(type(r.json()))

# # Testing Patient class & Database Connection
# x = Patient()
# x.MRN = 1
# x.patient_name = "Anuj Som"
# x.ECG_Trace = Image.open("images/acl1.jpg")
# x.reciept_timestamps.append(dt.now())
# x.save()

clean_server()

# Testing post_new_patient_info route
pat1_info = {
    'MRN': 1
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat1_info)
print("{}: {}".format(r.status_code, r.text))

pat2_info = {
    'MRN': 2,
    'patient_name': "Ali Baba"
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat2_info)
print("{}: {}".format(r.status_code, r.text))

b64_image = itb.file_to_b64("images/test_image.png")
pat3_info = {
    'MRN': 3,
    'patient_name': "Duke Duncan",
    'ECG_trace': b64_image
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat3_info)
print("{}: {}".format(r.status_code, r.text))
# We expect an error since no heart_rate posted along with ECG_trace

b64_image = itb.file_to_b64("images/test_image.png")
pat4_info = {
    'MRN': 4,
    'patient_name': "Duke Duncan",
    'ECG_trace': b64_image,
    'heart_rate': 60
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat4_info)
print("{}: {}".format(r.status_code, r.text))
# We now expect this to go through since heart_rate is posted

b64_image = itb.file_to_b64("images/test_image.png")
b64_medical_image = itb.file_to_b64("images/esophagus2.jpg")
pat5_info = {
    'MRN': 5,
    'patient_name': "Bob Boyles",
    'ECG_trace': b64_image,
    'heart_rate': 60,
    'medical_image': b64_medical_image
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat5_info)
print("{}: {}".format(r.status_code, r.text))

# Post more data to patient 5
b64_image = itb.file_to_b64("images/upj1.jpg")
b64_medical_image = itb.file_to_b64("images/esophagus 1.jpg")
pat5_info = {
    'MRN': 5,
    'ECG_trace': b64_image,
    'heart_rate': 64,
    'medical_image': b64_medical_image
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat5_info)
print("{}: {}".format(r.status_code, r.text))

b64_image = itb.file_to_b64("images/upj2.jpg")
b64_medical_image = itb.file_to_b64("images/acl1.jpg")
pat5_info = {
    'MRN': 5,
    'ECG_trace': b64_image,
    'heart_rate': 75,
    'medical_image': b64_medical_image
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat5_info)
print("{}: {}".format(r.status_code, r.text))

# Post with no ECG_trace but heart rate data
pat6_info = {
    'MRN': 5,
    'heart_rate': 75
}
r = requests.post(host_route + "api/post_new_patient_info", json=pat6_info)
print("{}: {}".format(r.status_code, r.text))

# Posts with incorrect types/weird clauses
b64_image = itb.file_to_b64("images/test_image.png")
patTest_info = {
    'MRN': "five"
}
r = requests.post(host_route + "api/post_new_patient_info", json=patTest_info)
print("{}: {}".format(r.status_code, r.text))

patTest_info = {
    'MRN': "9"
}
r = requests.post(host_route + "api/post_new_patient_info", json=patTest_info)
print("{}: {}".format(r.status_code, r.text))

patTest_info = {
    'MRN': 9,
    'ECG_trace': b64_image,
    'heart_rate': "75",
}
r = requests.post(host_route + "api/post_new_patient_info", json=patTest_info)
print("{}: {}".format(r.status_code, r.text))

# 'receipt_timestamps': dt.now().strftime("%Y-%m-%d %H:%M:%S")
