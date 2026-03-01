import ibm_db

def get_utilities(conn):
    result = {}
     #Backup utilities
    stmt = ibm_db.exec_immediate(conn, """
        SELECT 
            ROUND(DECIMAL(SUM(TOTAL_BACKUP_TIME_SEC)/60.0, 12, 2)) AS TOTAL_BACKUP_TIME_MIN,
            ROUND(DECIMAL(AVG(BACKUP_THROUGHPUT_KB_PER_SEC), 12, 2)) AS AVG_BACKUP_THROUGHPUT_KB_PER_SEC,
            ROUND(DECIMAL(SUM(TOTAL_RESTORE_TIME_SEC)/60.0, 12, 2)) AS TOTAL_RE STORE_TIME_MIN,
            ROUND(DECIMAL(AVG(RESTORE_THROUGHPUT_KB_PER_SEC), 12, 2)) AS AVG_RESTORE_THROUGHPUT_KB_PER_SEC
        FROM SYSIBMADM.BACKUP_RESTORE_HISTORY
    """)
    row = ibm_db.fetch_assoc(stmt)
    result["total_backup_time_min"] = row["TOTAL_BACKUP_TIME_MIN"]
    result["avg_backup_throughput_kb_per_sec"] = row["AVG_BACKUP_THROUGHPUT_KB_PER_SEC"]
    result["total_restore_time_min"] = row["TOTAL_RE STORE_TIME_MIN"]       

    #runs statistics
    try:        
        stmt = ibm_db.exec_immediate(conn, """
            SELECT TABSCHEMA, TABNAME
            FROM SYSCAT.TABLES
            WHERE TYPE='T' AND (STATS_TIME IS NULL OR DAYS(SYSDATE) - DAYS(STATS_TIME) > 30)
        """)
        stats_issues = []
        row = ibm_db.fetch_assoc(stmt)
        while row:
            stats_issues.append({
                "table_schema": row["TABSCHEMA"],
                "table_name": row["TABNAME"]
            })
            row = ibm_db.fetch_assoc(stmt)
        if stats_issues:
            result["tables_to_run_stats"] = stats_issues
        else:
            result["tables_to_run_stats"] = "none"  
    except Exception as e:

        result["statistics_error"] = str(e)
    #load utilities
    stmt = ibm_db.exec_immediate(conn, """
        SELECT 
            ROUND(DECIMAL(SUM(TOTAL_LOAD_TIME_SEC)/60.0, 12, 2)) AS TOTAL_LOAD_TIME_MIN,
            ROUND(DECIMAL(AVG(LOAD_TH               
ROUGHPUT_KB_PER_SEC), 12, 2)) AS AVG_LOAD_THROUGHPUT_KB_PER_SEC
        FROM SYSIBMADM.LOAD_HISTORY         
    """)                    

    row = ibm_db.fetch_assoc(stmt)
    result["total_load_time_min"] = row["TOTAL_LOAD_TIME_MIN"]          
    result["avg_load_throughput_kb_per_sec"] = row["AVG_LOAD_THROUGHPUT_KB_PER_SEC"]        

            
    return result