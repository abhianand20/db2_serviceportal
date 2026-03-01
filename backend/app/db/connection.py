# app/db/connection.py
import ibm_db
import os

def get_db2_connection(db_name: str):
    conn_str = (
        f"DATABASE={db_name};"
        f"HOSTNAME={os.getenv('DB2_HOST')};"
        f"PORT={os.getenv('DB2_PORT')};"
        f"PROTOCOL=TCPIP;"
        f"UID={os.getenv('DB2_USER')};"
        f"PWD={os.getenv('DB2_PASSWORD')};"
    )



    return ibm_db.connect(conn_str, "", "")
