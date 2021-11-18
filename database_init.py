from pymodm import connect, MongoModel, fields
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
    ECG_Trace = fields.ImageField()
    heart_rate = fields.IntegerField()
    reciept_timestamps = fields.DateTimeField()
    medical_image = fields.ImageField()


def get_server():
    return mongodb_server


# Testing Patient class & Database Connection
# x = Patient()
# x.MRN = 100
# x.reciept_timestamps = dt.now()
# x.save()
