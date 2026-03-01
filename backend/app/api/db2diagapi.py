from fastapi import FastAPI, APIRouter
from app.db.connection import get_db2_connection
from app.services.diaglog import get_db2diag_crit,get_db2diag_err,get_db2diag_info,get_db2diag_warn
import ibm_db

router = APIRouter(
    prefix="/api/v1/databases",
    tags=["HealthCheck"]
)

# @router.get("/{db_name}/db2diag/{level}")
# def db2diag_level(db_name: str, level: str):
#     conn = get_db2_connection(db_name)
#     try:
#         if level == "crit":
#             return get_db2diag_crit(conn)
#         elif level == "err":
#             return get_db2diag_err(conn)
#         elif level == "warn":
#             return get_db2diag_warn(conn)
#         elif level == "info":
#             return get_db2diag_info(conn)
#         else:
#             return {"error": "Invalid level"}
#     finally:
#         ibm_db.close(conn)



@router.get("/{db_name}/db2diag/crit")

def db2diag_crit(db_name: str):
    conn = get_db2_connection(db_name)
    try:
        db2diag_crit_data = get_db2diag_crit(conn)
        return db2diag_crit_data
    finally:
        
        ibm_db.close(conn)

@router.get("/{db_name}/db2diag/err")
def db2diag_err(db_name: str):
    conn = get_db2_connection(db_name)
    try:
        db2diag_err_data = get_db2diag_err(conn)
        return db2diag_err_data
    finally:
        
        ibm_db.close(conn)

@router.get("/{db_name}/db2diag/warn")
def db2diag_warn(db_name: str):
    conn = get_db2_connection(db_name)
    try:
        db2diag_warn_data = get_db2diag_warn(conn)
        return db2diag_warn_data
    finally:
        
        ibm_db.close(conn)

@router.get("/{db_name}/db2diag/info")
def db2diag_info(db_name: str):
    conn = get_db2_connection(db_name)
    try:
        db2diag_info_data = get_db2diag_info(conn)
        return db2diag_info_data
    finally:
        
        ibm_db.close(conn)
