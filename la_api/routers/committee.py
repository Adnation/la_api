import os
import json

from fastapi import UploadFile
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi import APIRouter, Form, File


from la_api.db_utils import DBClient


db_client = DBClient()

router = APIRouter(
    prefix="/committee",
    tags=["committee"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_members():
    return json.loads(dumps(db_client.db.committee.find()))


@router.get("/{id}")
async def get_member(id: str):
    return json.loads(dumps(db_client.db.committee.find({"_id": ObjectId(id)})))


@router.post("/")
async def add_member(name: str = Form(...), role: str = Form(...), profile_pic: UploadFile = File(...)):
    member = {
        "picture_bin": profile_pic.file.read(),
        "name": name,
        "role": role
    }
    new_member = db_client.db.committee.insert_one(member).inserted_id
    return json.loads(dumps(new_member))
