from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from search import search_api

app = FastAPI(title="SkillWeave API")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search")

def search_endpoint(req: SearchRequest):

    results = search_api(req.query, req.top_k)

    return {
        "query": req.query,
        "results": results
    }