from db import db

class TempHumModel(db.Model):

    __tablename__ = "tbl_temp_humidity"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), unique=True, nullable=False)
    time = db.Column(db.String(20), nullable=False)
    temp = db.Column(db.Float, nullable=False) 
    hum = db.Column(db.Float, nullable=False)  

    def __init__(self, date, time, temp, hum):
        self.date = date
        self.time = time
        self.temp = temp
        self.hum = hum
