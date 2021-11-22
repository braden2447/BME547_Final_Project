from pymodm import connect, MongoModel, fields
from pymodm.base.fields import MongoBaseField
import pymongo
from datetime import datetime as dt

db_server = "mongodb+srv://AtlasUser:8dNHh2kXNijBjNuQ@cluster0.a532e"
db_server += ".mongodb.net/ECGServer?retryWrites=true&w=majority"

mongodb_server = connect(db_server)


class Patient(MongoModel):
    MRN = fields.IntegerField(primary_key=True)    # Medical Record Number
    patient_name = fields.CharField()              # Patient Name
    ECG_Trace = fields.ImageField()                # ECG Images
    heart_rate = fields.IntegerField()             # Heart Rate Data
    reciept_timestamps = fields.DateTimeField()    # Datetime timestamps
    medical_image = fields.ImageField()            # Medical Images


class PatientTest(MongoModel):
    MRN = fields.IntegerField(primary_key=True)
    patient_name = fields.CharField()
    ECG_Trace = fields.ListField(fields.ImageField())
    heart_rate = fields.ListField(fields.IntegerField())
    reciept_timestamps = fields.ListField(fields.DateTimeField())
    medical_image = fields.ListField(fields.ImageField())


def get_server():
    return mongodb_server

# from PIL import Image
# # Testing Patient class & Database Connection
# x = PatientTest()
# x.MRN = 1
# x.patient_name = "Anuj Som"
# x.ECG_Trace = Image.open("images/acl1.jpg")
# x.reciept_timestamps.append(dt.now())
# x.save()
