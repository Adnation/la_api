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
    prefix="/survey",
    tags=["survey"],
    responses={404: {"description": "Not found"}}
)


collection = db_client.db.survey


@router.get("/")
async def get_all():
    return json.loads(dumps(collection.find()))


@router.get("/{id}")
async def get_by_(id: str):
    return json.loads(dumps(collection.find({"_id": ObjectId(id)})))


@router.post("/")
async def add_survey(request: Request):
    payload = await request.json()
    for f in ['name', 'survey_link', 'expiry']:
        if f not in payload:
            raise HTTPException(status_code=400, detail=f"Missing {f} in payload")

    new_member = collection.insert_one(await request.json()).inserted_id
    return json.loads(dumps(new_member))
