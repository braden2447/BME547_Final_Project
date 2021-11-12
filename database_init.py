from pymodm import connect, MongoModel, fields
import pymongo

db_server = "mongodb+srv://AtlasUser:8dNHh2kXNijBjNuQ@cluster0.a532e"
db_server += ".mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

connect(db_server)


class User(MongoModel):
    name = fields.CharField()
