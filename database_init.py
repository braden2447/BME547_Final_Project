from pymodm import connect, MongoModel, fields
import pymongo

connect("mongodb+srv://AtlasUser:8dNHh2kXNijBjNuQ@cluster0.a532e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# client = pymongo.MongoClient("mongodb+srv://AtlasUser:<password>@cluster0.a532e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test

class User(MongoModel):
    name=fields.CharField()

x = User(name="Braden")
x.save()