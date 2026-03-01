from fastapi import FastAPI,APIRouter
from app.db.connection import get_db2_connection
from app.services.db_summary import get_db_summary
import ibm_db

router = APIRouter(
    prefix="/api/v1/databases",
    tags=["Databases"]
)

@router.get("/{db_name}/summary")
def database_summary(db_name: str):
  
    conn = get_db2_connection(db_name)

    try:
        summary = get_db_summary(conn)
        return summary
    finally:
      ibm_db.close(conn)


# # app/api/databases.py
# from fastapi import APIRouter

# router = APIRouter(
#     prefix="/api/v1/databases",
#     tags=["Databases"]
# )
