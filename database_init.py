from pymodm import connect, MongoModel, fields
from pymodm.base.fields import MongoBaseField
import pymongo
from datetime import datetime as dt

db_server = "mongodb+srv://AtlasUser:8dNHh2kXNijBjNuQ@cluster0.a532e"
db_server += ".mongodb.net/ECGServer?retryWrites=true&w=majority"

mongodb_server = connect(db_server)


class Patient(MongoModel):
    # Medical Record Number
    # Patient Name
    # ECG Images as b64 string
    # Heart Rate Data
    # Datetime timestamps as strftime strings
    # Medical Images as b64 string
    MRN = fields.IntegerField(primary_key=True)
    patient_name = fields.CharField()
    ECG_trace = fields.ListField(fields.CharField())
    heart_rate = fields.ListField(fields.IntegerField())
    receipt_timestamps = fields.ListField(fields.CharField())
    medical_image = fields.ListField(fields.CharField())


class PatientTest(MongoModel):
    MRN = fields.IntegerField(primary_key=True)
    patient_name = fields.CharField()
    ECG_trace = fields.ListField(fields.CharField())
    heart_rate = fields.ListField(fields.IntegerField())
    receipt_timestamps = fields.ListField(fields.CharField())
    medical_image = fields.ListField(fields.CharField())


def get_database():
    """Simply returns the mongodb_server object

    Returns:
        mongodb_server object
    """
    return mongodb_server


def clean_database():
    """Deletes all contents of the Patient database
    """
    Patient.objects.raw({}).delete()

# from PIL import Image
# # Testing Patient class & Database Connection
# import image_toolbox as tb
# x = PatientTest()
# x.MRN = 1
# x.patient_name = "Anuj Som"
# x.ECG_trace.append(tb.file_to_b64("images/test_image.png"))
# x.heart_rate.append(60)
# x.receipt_timestamps.append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
# x.save()
