import ibm_db


def get_performance_metrics(conn):
    result = {}

    # Buffer pool hit ratio
    stmt = ibm_db.exec_immediate(conn, """
        SELECT 
    BP_NAME,
    -- Overall Hit Ratio
    DEC(100 * (1 - (CAST(pool_data_p_reads + pool_index_p_reads AS DECIMAL(18,2)) / 
    NULLIF(pool_data_l_reads + pool_index_l_reads, 0))), 5, 2) AS OVERALL_HIT_RATIO,
    -- Data Hit Ratio
    DEC(100 * (1 - (CAST(pool_data_p_reads AS DECIMAL(18,2)) / 
    NULLIF(pool_data_l_reads, 0))), 5, 2) AS DATA_HIT_RATIO,
    -- Index Hit Ratio
    DEC(100 * (1 - (CAST(pool_index_p_reads AS DECIMAL(18,2)) / 
    NULLIF(pool_index_l_reads, 0))), 5, 2) AS INDEX_HIT_RATIO,MEMBER
FROM TABLE(MON_GET_BUFFERPOOL('', -2)) AS T
    """)
    row = ibm_db.fetch_assoc(stmt)
    bp_details = []
    
    while row:
        bp_details.append(
            {
                "bp_name" : row["BP_NAME"],
                "total_hit_ratio_percent": row ["OVERALL_HIT_RATIO"],
                "data_hit_ratio_percent": row ["DATA_HIT_RATIO"],
                "index_hit_ration_percent": row ["INDEX_HIT_RATIO"],
                "member": row["MEMBER"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)

    result["buffer_pool_data"] = bp_details


    # package cache  hit ratio
    stmt = ibm_db.exec_immediate(conn, """
        SELECT
    DECIMAL(
        CASE
            WHEN PKG_CACHE_LOOKUPS = 0 THEN 0
            ELSE (1 - (FLOAT(PKG_CACHE_INSERTS) / FLOAT(PKG_CACHE_LOOKUPS))) * 100
        END,
        5, 2
    ) AS PKG_CACHE_HIT_RATIO
FROM TABLE(MON_GET_DATABASE(-2)) AS T
WITH UR

    """)
    row = ibm_db.fetch_assoc(stmt)

    result["pkg_cache_hit_ratio"] = row["PKG_CACHE_HIT_RATIO"]

    #catalog_cache_hit_ratio

    stmt = ibm_db.exec_immediate(conn, """
        SELECT 
            DECIMAL(
                CASE
                    WHEN CAT_CACHE_LOOKUPS = 0 THEN 0
                    ELSE (1 - (FLOAT(CAT_CACHE_INSERTS) / FLOAT(CAT_CACHE_LOOKUPS))) * 100
                END,
                5, 2
            ) AS CAT_CACHE_HIT_RATIO
        FROM TABLE(MON_GET_DATABASE(-2)) AS T
        WITH UR

    """)
    row = ibm_db.fetch_assoc(stmt)

    result["cat_cache_hit_ratio"] = row["CAT_CACHE_HIT_RATIO"]






    # # I/O wait time percent
    # stmt = ibm_db.exec_immediate(conn, """
    #     SELECT 
    #         ROUND(DECIMAL(SUM(READ_IO_TIME + WRITE_IO_TIME) * 100.0 / NULLIF(SUM(UOW_TOTAL_TIME), 0), 5, 2          )) AS IO_WAIT_TIME_PERCENT
    #     FROM TABLE(MON_GET_DATABASE(-2))
    # """)
    # row = ibm_db.fetch_assoc(stmt)      
    # result["io_wait_time_percent"] = row["IO_WAIT_TIME_PERCENT"]    


    #  # Disk read/write ratio
    # stmt = ibm_db.exec_immediate(conn, """
    #     SELECT  
    #         ROUND(DECIMAL(SUM(READS) * 100.0 / NULLIF(SUM(WRITES), 0), 5, 2)) AS DISK_READ_WRITE_RATIO
    #     FROM TABLE(MON_GET_DATABASE(-2))
    # """)            
    # row = ibm_db.fetch_assoc(stmt)      
    # result["disk_read_write_ratio"] = row["DISK_READ_WRITE_RATIO"]          

        #deadlocks
    stmt = ibm_db.exec_immediate(conn, """
        SELECT DEADLOCKS           
        FROM TABLE(MON_GET_DATABASE(-2))                    
    """)                                                        
    row = ibm_db.fetch_assoc(stmt)          
    result["deadlocks"] = row["DEADLOCKS"]


    #lock-wait details
    stmt = ibm_db.exec_immediate(conn, """
        SELECT SUBSTR(TABSCHEMA,1,8) AS TABSCHEMA, SUBSTR(TABNAME,1,15) AS TABNAME, LOCK_OBJECT_TYPE, LOCK_MODE, LOCK_MODE_REQUESTED,AGENT_ID_HOLDING_LK FROM   SYSIBMADM.LOCKWAITS
    """)
    row = ibm_db.fetch_assoc(stmt)
    lock_details = []
    
    while row:
        lock_details.append(
            {
                "tabschema": row["TABSCHEMA"],
                "tabname": row ["TABNAME"],
                "lock_object_type": row ["LOCK_OBJECT_TYPE"],
                "lock_mode": row ["LOCK_MODE"],
                "lock_mode_requested": row["LOCK_MODE_REQUESTED"],
                "agent_holding_lock": row["AGENT_ID_HOLDING_LK"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if lock_details:
        result["locking_data"] = lock_details
    else: 
        result["locking_data"] = "No Data"


    #longrunningquery
    stmt = ibm_db.exec_immediate(conn, """
        SELECT SUBSTR(APPLICATION_NAME,1,20) as APPLICATION_NAME,  SUBSTR(SESSION_AUTH_ID,1,20) as SESSION_AUTH_ID, elapsed_time_sec, activity_state, rows_read, SUBSTR(stmt_text,1,100) as stmt_text FROM sysibmadm.mon_current_sql where elapsed_time_sec > 300 ORDER BY elapsed_time_sec DESC FETCH FIRST 3 ROWS ONLY
    """)
    row = ibm_db.fetch_assoc(stmt)
    longrunning_query = []
    
    while row:
        longrunning_query.append(
            {
                "app_name" : row["APPLICATION_NAME"],
                "session_authid": row ["SESSION_AUTH_ID"],
                "elapsed_time_sec": row ["ELAPSED_TIME_SEC"],
                "activity_state": row ["ACTIVITY_STATE"],
                "rows_read": row["ROWS_READ"],
                "stmt_text": row["STMT_TEXT"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if longrunning_query:
        result["longrunning_query_data"] = longrunning_query
    else: 
       result["longrunning_query_data"] = "No Data"  


    #tablescan
    stmt = ibm_db.exec_immediate(conn, """
        SELECT varchar(tabschema,10) as tabschema, varchar(tabname,40) as tabname,table_scans FROM TABLE(MON_GET_TABLE('','',-2)) AS t  GROUP BY tabschema, tabname,TABLE_SCANS ORDER BY TABLE_SCANS DESC FETCH FIRST 5 ROWS ONLY
    """)
    row = ibm_db.fetch_assoc(stmt)
    tablescan = []
    
    while row:
        tablescan.append(
            {
                "tabschema" : row["TABSCHEMA"],
                "tabname": row["TABNAME"],
                "table_scans": row ["TABLE_SCANS"]

            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if tablescan:
        result["tablescan"] = tablescan
    else: 
        result["tablescan"] = "No Data"

    #table_rows_read
    stmt = ibm_db.exec_immediate(conn, """
        SELECT varchar(tabschema,10) as tabschema, varchar(tabname,40) as tabname,        sum(rows_read) as total_rows_read,        sum(rows_inserted) as total_rows_inserted,        sum(rows_updated) as total_rows_updated,        sum(rows_deleted) as total_rows_deleted FROM TABLE(MON_GET_TABLE('','',-2)) AS t  GROUP BY tabschema, tabname,TABLE_SCANS ORDER BY total_rows_read DESC FETCH FIRST 5 ROWS ONLY
    """)
    row = ibm_db.fetch_assoc(stmt)
    table_rows_read = []
    
    while row:
        table_rows_read.append(
            {
                "tabschema" : row["TABSCHEMA"],
                "tabname": row ["TABNAME"],
                "total_rows_read": row ["TOTAL_ROWS_READ"],
                "total_rows_inserted": row ["TOTAL_ROWS_INSERTED"],
                "total_rows_updated": row ["TOTAL_ROWS_UPDATED"],
                "total_rows_deleted": row ["TOTAL_ROWS_DELETED"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if table_rows_read:
        result["table_rows_read"] = table_rows_read
    else: 
        result["table_rows_read"] = "Not Data"


    #table_read_efficiency
    stmt = ibm_db.exec_immediate(conn, """
       WITH SUM_TAB (SUM_RR) AS ( SELECT FLOAT(SUM(ROWS_READ)) FROM sysibmadm.snapdyn_sql AS T) SELECT SUBSTR(STMT_TEXT,1,220) AS STATEMENT, ROWS_READ, ROWS_WRITTEN, NUM_EXECUTIONS FROM sysibmadm.snapdyn_sql AS T, SUM_TAB ORDER BY ROWS_READ DESC FETCH FIRST 5 ROWS ONLY WITH UR
    """)
    row = ibm_db.fetch_assoc(stmt)
    table_read_efficiency = []
    
    while row:
        table_read_efficiency.append(
            {
                "statement" : row["STATEMENT"],
                "rows_read": row["ROWS_READ"],
                "rows_written": row["ROWS_WRITTEN"],
                "num_executions": row["NUM_EXECUTIONS"]

            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if table_read_efficiency:

        result["table_read_efficiency"] = table_read_efficiency
    else: 
        result["table_read_efficiency"] = "No Data"


    #high_cpu_query
    stmt = ibm_db.exec_immediate(conn, """
    SELECT MEMBER,APPLICATION_HANDLE,APPLICATION_ID,UOW_START_TIME,
                                 DEADLOCKS,LOCK_WAITS,SORT_OVERFLOWS,
    DYNAMIC_SQL_STMTS,STATIC_SQL_STMTS FROM TABLE(MON_GET_UNIT_OF_WORK(NULL,-1))
                                  ORDER BY total_cpu_time DESC FETCH FIRST 5 Rows only
        """)
    row = ibm_db.fetch_assoc(stmt)
    high_cpu_query = []
        
    while row:
        high_cpu_query.append(
            {
                "member" : row["MEMBER"],
                "app_handle": row["APPLICATION_HANDLE"],
                "app_id": row["APPLICATION_ID"],
                "uow_start_time": row["UOW_START_TIME"],
                "deadlocks": row["DEADLOCKS"], 
                "lock_waits": row["LOCK_WAITS"],
                "sort_overflows": row["SORT_OVERFLOWS"],
                "dyn_sql_stmt": row["DYNAMIC_SQL_STMTS"],
                "statics_sql_stmt": row["STATIC_SQL_STMTS"]

            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if high_cpu_query:

        result["high_cpu_query"] = high_cpu_query
    else:
        result["high_cpu_query"] = "No Data"


    #frequent_queries
    stmt = ibm_db.exec_immediate(conn, """
        SELECT SNAPSHOT_TIMESTAMP,MEMBER,SUBSTR(STMT_TEXT,1,60) AS STMT_TEXT, NUM_EXECUTIONS,DBPARTITIONNUM FROM SYSIBMADM.TOP_DYNAMIC_SQL ORDER BY NUM_EXECUTIONS DESC FETCH FIRST 5 ROWS ONLY
    """)
    row = ibm_db.fetch_assoc(stmt)
    frequent_queries = []
    
    while row:
        frequent_queries.append(
            {
                "snapshot_timestampt": row["SNAPSHOT_TIMESTAMP"],
                "member": row["MEMBER"],
                "stmt_text": row["STMT_TEXT"],
                "num_exec": row["NUM_EXECUTIONS"],
                "dbpartitionnum": row["DBPARTITIONNUM"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if frequent_queries :

        result["frequent_queries"] = frequent_queries
    else: 
           result["frequent_queries"] = "No Data"

    #top_sort_queries
    stmt = ibm_db.exec_immediate(conn, """
    SELECT MEMBER, SUBSTR(STMT_TEXT, 1, 260) AS STMT_TEXT,TOTAL_SORT_TIME,TOTAL_EXEC_TIME,DBPARTITIONNUM FROM SYSIBMADM.SNAPDYN_SQL ORDER BY TOTAL_SORT_TIME DESC FETCH FIRST 5 ROWS ONLY
    """)
    row = ibm_db.fetch_assoc(stmt)
    top_sort_queries = []
    
    while row:
        top_sort_queries.append(
            {

                "member": row["MEMBER"],
                "stmt_text": row["STMT_TEXT"],
                "total_sort_time": row["TOTAL_SORT_TIME"],
                "total_exec_time": row["TOTAL_EXEC_TIME"],
                "dbpartitionnum": row["DBPARTITIONNUM"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if top_sort_queries:
        result["top_sort_queries"] = top_sort_queries
    else:
        result["top_sort_queries"] = "No Data"

    #problematic_query
    stmt = ibm_db.exec_immediate(conn, """
    WITH SUM_TAB AS (
    SELECT
        FLOAT(SUM(ROWS_READ))        AS SUM_RR,
        FLOAT(SUM(TOTAL_EXEC_TIME))  AS SUM_EXEC,
        FLOAT(SUM(TOTAL_SORT_TIME))  AS SUM_SORT,
        FLOAT(SUM(NUM_EXECUTIONS))   AS SUM_NUM_EXEC
    FROM sysibmadm.snapdyn_sql
),
SQL_STATS AS (
    SELECT
        SUBSTR(STMT_TEXT, 1, 120) AS STATEMENT,
        ROWS_READ,
        TOTAL_EXEC_TIME,
        TOTAL_SORT_TIME,
        NUM_EXECUTIONS,
        CASE WHEN SUM_TAB.SUM_RR = 0 THEN 0
             ELSE DECIMAL(100 * FLOAT(ROWS_READ) / SUM_TAB.SUM_RR, 5, 2)
        END AS PCT_TOT_RR,
        CASE WHEN SUM_TAB.SUM_EXEC = 0 THEN 0
             ELSE DECIMAL(100 * FLOAT(TOTAL_EXEC_TIME) / SUM_TAB.SUM_EXEC, 5, 2)
        END AS PCT_TOT_EXEC,
        CASE WHEN SUM_TAB.SUM_SORT = 0 THEN 0
             ELSE DECIMAL(100 * FLOAT(TOTAL_SORT_TIME) / SUM_TAB.SUM_SORT, 5, 2)
        END AS PCT_TOT_SORT,
        CASE WHEN SUM_TAB.SUM_NUM_EXEC = 0 THEN 0
             ELSE DECIMAL(100 * FLOAT(NUM_EXECUTIONS) / SUM_TAB.SUM_NUM_EXEC, 5, 2)
        END AS PCT_TOT_NUM_EXEC
    FROM sysibmadm.snapdyn_sql T
    CROSS JOIN SUM_TAB
)
SELECT *
FROM SQL_STATS
WHERE
      PCT_TOT_RR       > 10
   OR PCT_TOT_EXEC     > 10
   OR PCT_TOT_SORT     > 10
   OR PCT_TOT_NUM_EXEC > 10
ORDER BY ROWS_READ DESC
FETCH FIRST 20 ROWS ONLY
WITH UR;

    """)
    row = ibm_db.fetch_assoc(stmt)
    problematic_queries = []
    
    while row:
        problematic_queries.append(
            {

                "statement": row["STATEMENT"],
                "total_exe_time": row["TOTAL_EXEC_TIME"],
                "total_sort_time": row["TOTAL_SORT_TIME"],
                "num_execution": row["NUM_EXECUTIONS"],
                "pct_tot_rr": row["PCT_TOT_RR"],
                "pct_tot_exec": row["PCT_TOT_EXEC"],
                "pct_tot_sort": row["PCT_TOT_SORT"],
                "pct_tot_num_exec": row["PCT_TOT_NUM_EXEC"]
            }
        )
        row = ibm_db.fetch_assoc(stmt)
    if problematic_queries:
        result["problematic_queries"] = problematic_queries
    else:
         result["problematic_queries"] = "No Data"


        



    #logging utilization
    stmt = ibm_db.exec_immediate(conn, """
        SELECT member, TOTAL_LOG_AVAILABLE,TOTAL_LOG_USED,                            
            SEC_LOGS_ALLOCATED,APPLID_HOLDING_OLDEST_XACT,NUM_INDOUBT_TRANS,                         
            ROUND( (TOTAL_LOG_USED * 100.0 / TOTAL_LOG_AVAILABLE), 2) AS LOG_UTILIZATION_PERCENT
            FROM TABLE(MON_GET_TRANSACTION_LOG(-1)) AS T order by member asc;     
    """)

    row = ibm_db.fetch_assoc(stmt)
    log_utilisation = []

    while row:

        log_utilisation.append(
            
            {
            "MEMBER": row["MEMBER"],
            "TOTAL_LOG_AVAILABLE" : row["TOTAL_LOG_AVAILABLE"],
            "SEC_LOGS_ALLOCATED": row["SEC_LOGS_ALLOCATED"],
            "APPLID_HOLDING_OLDEST_XACT" : row["APPLID_HOLDING_OLDEST_XACT"],
            "NUM_INDOUBT_TRANS" : row["NUM_INDOUBT_TRANS"],
            "LOG_UTILIZATION_PERCENT" : row["LOG_UTILIZATION_PERCENT"]

            }
        )   
        row = ibm_db.fetch_assoc(stmt)

    if log_utilisation:

        result["log_utilisation_data"] = log_utilisation
    else: 
         result["log_utilisation_data"] = "No Data"



    # temp table usage
    stmt = ibm_db.exec_immediate(conn, """
        SELECT 
            STMT_TEXT, 
            POOL_TEMP_DATA_L_READS + POOL_TEMP_INDEX_L_READS AS TEMP_READS,
            NUM_EXECUTIONS
        FROM TABLE(MON_GET_PKG_CACHE_STMT(NULL, NULL, NULL, -2))
        ORDER BY TEMP_READS DESC
        FETCH FIRST 5 ROWS ONLY;
                
    """)            
    row = ibm_db.fetch_assoc(stmt)  

    temp_table_queries = []

    while row:

            temp_table_queries.append(
                
                {
                "stmt_txt" : row["STMT_TEXT"],
                "temp_reads" : row["TEMP_READS"],
                "num_executions" : row["NUM_EXECUTIONS"]
        

                }
            )   
            row = ibm_db.fetch_assoc(stmt)
    if temp_table_queries:
        result["temp_table_queries"] = temp_table_queries
    else:
        result["temp_table_queries"] = "No Data"


    return result