from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Content Aggregator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Content Aggregator API"}

# Example endpoint for aggregated content
@app.get("/api/content")
async def get_content():
    # This will be expanded to fetch from different sources
    return {
        "content": [
            {"type": "social", "source": "twitter", "content": "Example tweet"},
            {"type": "rss", "source": "blog", "content": "Example article"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    