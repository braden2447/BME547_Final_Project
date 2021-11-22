import requests
from PIL import Image
from database_init import Patient, PatientTest
from datetime import datetime as dt
import base64
import io

host_route = "http://127.0.0.1:5000/"


# Test api/get_mrn route
# r = requests.get(host_route + "api/get_mrn")
# print("{}: {}".format(r.status_code, r.json()))
# print(type(r.json()))


# Testing Patient class & Database Connection
x = PatientTest.objects.raw({"_id": 1}).first()
def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string
# x.MRN = 1
# x.patient_name = "Anuj Som"
# img_obj = Image.open("images/acl1.jpg").convert("P")
# # print(type(img_obj))
# img_obj2 = img_obj.convert('P')
# img_obj.show()
# print(type(img_obj2))
# img_obj2.show()
# x.ECG_Trace.append(img_obj)
# print(x)
# for i in x:
#     print(i)
# x.ECG_Trace = [img_obj]
# x.reciept_timestamps.append(dt.now())
# x.save()

# PatientTest.objects.raw({}).delete()
# Patient.objects.raw({}).delete()
