from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.content_store import CONTENT_DB
from llm.insight_engine import generate_insight
from pydantic import BaseModel
from fastapi import Body
from typing import Dict, Any

app = FastAPI()

# allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/links")
def get_links():
    return {
        "links": list(CONTENT_DB.keys())
    }

class LinkRequest(BaseModel):
    link: str

@app.post("/content/link")
def get_content_by_link(req: LinkRequest):
    if req.link not in CONTENT_DB:
        return {"error": "Link not found"}

    return CONTENT_DB[req.link]

@app.post("/analyze/link")
def analyze_by_link(req: LinkRequest):
    if req.link not in CONTENT_DB:
        return {"error": "Link not found"}

    base_output = CONTENT_DB[req.link]
    return generate_insight(base_output)

@app.post("/analyze/raw")
def analyze_raw(signals: Dict[str, Any]):
    return generate_insight(signals)