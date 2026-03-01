from fastapi import FastAPI,APIRouter
from app.db.connection import get_db2_connection
from app.services.performance import get_performance_metrics
import ibm_db


router = APIRouter(    prefix="/api/v1/databases",
    tags=["DbPerformance"])

@router.get("/{db_name}/performance")

def get_db_performance(db_name:str):
   conn = get_db2_connection(db_name)
   try:
      performance_data = get_performance_metrics(conn)
      return performance_data
   finally:
        
        ibm_db.close(conn)
   


      
