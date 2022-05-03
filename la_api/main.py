import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from db_utils import DBClient
from routers import committee
from routers import subscribers
from routers import events
from routers import rsvp

app = FastAPI()

origins = [
    "http://lohanadfw.org",
    "https://lohanadfw.org",
    "http://www.lohanadfw.org",
    "https://www.lohanadfw.org"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_client = DBClient()
app.include_router(committee.router)
app.include_router(subscribers.router)
app.include_router(events.router)
app.include_router(rsvp.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
