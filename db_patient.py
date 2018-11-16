from pymodm import connect
from pymodm import MongoModel, fields

connect(
    "mongodb://heart-rate-db:GODUKE10@ds159263.mlab.com:59263/bme590heartdata")


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    h_r_times = fields.ListField(field=fields.DateTimeField())
