import ibm_db



def get_db2diag_info(conn):
    #db2diag-Info

    stmt = ibm_db.exec_immediate(conn,"""
         SELECT TIMESTAMP, DBPARTITIONNUM, substr(APPL_ID,1,15) as APPL_ID_TRUNC, MSGSEVERITY as SEV, MSGTYPE, MSGNUM, substr(MSG,1,50) as MSG_trunc  FROM TABLE ( PD_GET_LOG_MSGS( CURRENT_TIMESTAMP - 1 DAYS)) as T where UPPER(MSGSEVERITY) = 'I' ORDER BY TIMESTAMP DESC
    """)
    row = ibm_db.fetch_assoc(stmt)
    db2diag_data = []

    while row:
         db2diag_data.append(row)
         row = ibm_db.fetch_assoc(stmt)
    
    return {"db2diag_info": db2diag_data}

# #db2diag-warn
def get_db2diag_warn(conn):
    
    
    stmt = ibm_db.exec_immediate(conn,"""
        SELECT TIMESTAMP, DBPARTITIONNUM, substr(APPL_ID,1,15) as APPL_ID_TRUNC, MSGSEVERITY as SEV, MSGTYPE, MSGNUM, substr(MSG,1,50) as MSG_trunc  FROM TABLE ( PD_GET_LOG_MSGS( CURRENT_TIMESTAMP - 1 DAYS)) as T where MSGSEVERITY = 'W' ORDER BY TIMESTAMP DESC
""")
    row = ibm_db.fetch_assoc(stmt)
    db2diag_data = []

    while row:
         db2diag_data.append(row)
         row = ibm_db.fetch_assoc(stmt)
    
    return {"db2diag_warn": db2diag_data}
    
# #db2diag-err

def get_db2diag_err(conn):

    
    stmt = ibm_db.exec_immediate(conn,"""
     SELECT TIMESTAMP, DBPARTITIONNUM, substr(APPL_ID,1,15) as APPL_ID_TRUNC, MSGSEVERITY as SEV, MSGTYPE, MSGNUM, substr(MSG,1,50) as MSG_trunc  FROM TABLE ( PD_GET_LOG_MSGS( CURRENT_TIMESTAMP - 1 DAYS)) as T where MSGSEVERITY = 'E' ORDER BY TIMESTAMP DESC
""")
    row = ibm_db.fetch_assoc(stmt)
    db2diag_data = []

    while row:
         db2diag_data.append(row)
         row = ibm_db.fetch_assoc(stmt)
    
    return {"db2diag_err": db2diag_data}

#db2diag-crit
def get_db2diag_crit(conn):

   
    stmt = ibm_db.exec_immediate(conn,"""
        SELECT TIMESTAMP, DBPARTITIONNUM, substr(APPL_ID,1,15) as APPL_ID_TRUNC, MSGSEVERITY as SEV, MSGTYPE, MSGNUM, substr(MSG,1,50) as MSG_trunc  FROM TABLE ( PD_GET_LOG_MSGS( CURRENT_TIMESTAMP - 1 DAYS)) as T where MSGSEVERITY = 'C' ORDER BY TIMESTAMP DESC
""")
    row = ibm_db.fetch_assoc(stmt)
    db2diag_data = []

    while row:
         db2diag_data.append(row)
         row = ibm_db.fetch_assoc(stmt)
    
    return {"db2diag_crit": db2diag_data}


