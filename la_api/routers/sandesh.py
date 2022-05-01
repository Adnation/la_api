import os
import re
import json

from fastapi import UploadFile
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi import APIRouter, Form, File, Request, HTTPException

from la_api.db_utils import DBClient


db_client = DBClient()

router = APIRouter(
    prefix="/sandesh",
    tags=["sandesh"],
    responses={404: {"description": "Not found"}}
)


collection = db_client.db.sandesh


@router.get("/")
async def get_all():
    return json.loads(dumps(collection.find()))


@router.get("/{id}")
async def get_by_(id: str):
    return json.loads(dumps(collection.find({"_id": ObjectId(id)})))


@router.post("/")
async def add_sandesh(month_year: str = Form(...), date_published: str = Form(...), pdf: UploadFile = File(...),
                      description: str = Form(...)):
    add_sandesh = {
        "month_year": month_year,
        "date_published": date_published,
        "pdf": pdf.file.read(),
        "description": description
    }
    new_member = collection.insert_one(add_sandesh).inserted_id
    return json.loads(dumps(new_member))
