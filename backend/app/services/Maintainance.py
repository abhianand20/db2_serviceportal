import ibm_db       

def DB_Maintainance(conn,tabname):
    result = {}

    # Reorganize Tables
    try:
        stmt = ibm_db.exec_immediate(conn, """
           Select distinct cast(TABLE_SCHEMA as varchar(20)) as Schema, cast(TABLE_NAME as varchar(60)) as Table from SESSION.TB_STATS WHERE TABLE_SCHEMA NOT LIKE 'SYS%' AND TABLE_NAME NOT LIKE 'EXPLAIN%' AND REORG LIKE '%*%'
        """)
        table_issues = []
        row = ibm_db.fetch_assoc(stmt)
        while row:
            table_issues.append({
                "table_schema": row["TABSCHEMA"],
                "table_name": row["TABNAME"]
            })
            row = ibm_db.fetch_assoc(stmt)
        if table_issues:
            result["tables_to_reorganize"] = table_issues
        else:
            result["tables_to_reorganize"] = "none"
    except Exception as e:
        result["reorganization_error"] = str(e)

    #run statistics
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

    
    # Indexes to Rebuild
    try:    
        stmt = ibm_db.exec_immediate(conn, """
            SELECT INDSCHEMA, INDNAME
            FROM SYSCAT.INDEXES
            WHERE STATS_TIME IS NULL OR DAYS(SYSDATE) - DAYS(STATS_TIME) > 60
        """)
        index_issues = []
        row = ibm_db.fetch_assoc(stmt)
        while row:
            index_issues.append({
                "index_schema": row["INDSCHEMA"],
                "index_name": row["INDNAME"]
            })
            row = ibm_db.fetch_assoc(stmt)
        if index_issues:
            result["indexes_to_rebuild"] = index_issues
        else:
            result["indexes_to_rebuild"] = "none"
    except Exception as e:
        result["index_rebuild_error"] = str(e)


    return result