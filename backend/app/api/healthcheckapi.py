from fastapi import FastAPI,APIRouter
from app.db.connection import get_db2_connection
from app.services.healthcheck import get_healthcheck
import ibm_db

router = APIRouter(
    prefix="/api/v1/databases",
    tags=["HealthCheck"]
)

@router.get("/{db_name}/healthcheck")
def database_healthcheck(db_name: str):
    conn = get_db2_connection(db_name)
    try:
        health_status = get_healthcheck(conn)
        return health_status
    finally:
        
        ibm_db.close(conn)