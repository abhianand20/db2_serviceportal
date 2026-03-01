# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import databases, healthcheckapi,performanceapi,db2diagapi
from app.core import config

app = FastAPI(
    title="DB2 Read-Only Service Portal",
    version="1.0.0"
)
# Allow your React frontend origin
origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:5173",  # sometimes browsers use 127.0.0.1
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,      # <- important
#     allow_credentials=True,
#     allow_methods=["*"],         # allow GET, POST, etc.
#     allow_headers=["*"],         # allow all headers
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(databases.router)
app.include_router(healthcheckapi.router)
app.include_router(performanceapi.router)
app.include_router(db2diagapi.router)


@app.get("/health")
def health():
    return {"status": "ok"}



