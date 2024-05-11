from config import db, ma

class MData(db.Model):
    __tablename__ = "medicaldata"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    enc_key = db.Column(db.Text)
    cipher = db.Column(db.Text)

class DataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MData
        load_instance = True
        sqla_session = db.session

mdata_schema = DataSchema()
alldata_schema = DataSchema(many=True)
