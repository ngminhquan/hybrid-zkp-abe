from flask import make_response, abort
from config import db
from models import MData, mdata_schema, alldata_schema

def read_all():
    data = MData.query.all()
    return alldata_schema.dump(data)

def read_one(user_id):
    data = MData.query.filter(MData.user_id == user_id).one_or_none()

    if data is not None:
        return mdata_schema.dump(data)
    else:
        abort(404, f"Data with id {user_id} not found")

def add_data(mdata):
    #add zkp condition check
    user_id = mdata.get("user_id")
    user_id = mdata.get("user_id")
    existing_data = MData.query.filter(MData.user_id == user_id).one_or_none()

    if existing_data is None:
        new_data = mdata_schema.load(mdata, session=db.session)
        db.session.add(new_data)
        db.session.commit()
        return mdata_schema.dump(new_data), 201
    else:
        abort(406, f"Data with id {user_id} already exists")


def delete(user_id):
    existing_data = MData.query.filter(MData.user_id == user_id).one_or_none()

    if existing_data:
        db.session.delete(existing_data)
        db.session.commit()
        return make_response(f"{user_id} successfully deleted", 200)
    else:
        abort(404, f"Data with id {user_id} not found")