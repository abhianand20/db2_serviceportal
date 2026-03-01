# services/db2_summary.py
import ibm_db

def get_db_summary(conn):
    result = {}
   
    #instance name
    stmt = ibm_db.exec_immediate(conn, "SELECT INST_NAME,SERVICE_LEVEL FROM sysibmadm.ENV_INST_INFO")
    row = ibm_db.fetch_assoc(stmt)
    result["instance_name"] = row["INST_NAME"]
    result["service_level"] = row["SERVICE_LEVEL"]

    # Database name
    stmt = ibm_db.exec_immediate(conn, "SELECT CURRENT SERVER as DBNAME FROM SYSIBM.SYSDUMMY1")
    row = ibm_db.fetch_assoc(stmt)
    result["database_name"] = row["DBNAME"]
    # Database status and other info

    stmt = ibm_db.exec_immediate(conn, "select MEMBER,DB_STATUS,DB_ACTIVATION_STATE,DB_CONN_TIME,LAST_BACKUP,NUM_LOCKS_WAITING,DEADLOCKS,LOCK_ESCALS,LOCK_TIMEOUTS  from TABLE (MON_GET_DATABASE( -2)) AS D")
    row = ibm_db.fetch_assoc(stmt)
    result["member"] = row["MEMBER"]
    result["db_status"] = row["DB_STATUS"]
    result["activation_state"] = row["DB_ACTIVATION_STATE"]
    result["connection_time"] = row["DB_CONN_TIME"]
    result["num_locks_waiting"] = row["NUM_LOCKS_WAITING"]
    result["lock_escals"] = row["LOCK_ESCALS"]
    result["lock_timeouts"] = row["LOCK_TIMEOUTS"]  



    #start time
    stmt = ibm_db.exec_immediate(conn, """
     SELECT DB2START_TIME  FROM TABLE (MON_GET_INSTANCE(-2)); 
     """)
    row = ibm_db.fetch_assoc(stmt)
    result["db2_start_time"] = row["DB2START_TIME"]

    #LOG utilisatiom

    #logging utilization
    stmt = ibm_db.exec_immediate(conn, """
        SELECT member, TOTAL_LOG_AVAILABLE,TOTAL_LOG_USED,                                                     
            ROUND( (TOTAL_LOG_USED * 100.0 / TOTAL_LOG_AVAILABLE), 2) AS LOG_UTILIZATION_PERCENT
            FROM TABLE(MON_GET_TRANSACTION_LOG(-1)) AS T order by member asc;     
    """)

    row = ibm_db.fetch_assoc(stmt)
    log_utilisation = []

    while row:

      log_utilisation.append(
         
         {
           "MEMBER" : row ["MEMBER"],
           "TOTAL_LOG_AVAILABLE" : row ["TOTAL_LOG_AVAILABLE"],
           "LOG_UTILIZATION_PERCENT" : row ["LOG_UTILIZATION_PERCENT"]

         }
      )   
      row = ibm_db.fetch_assoc(stmt)
    
    if log_utilisation:
        result["log_utilisation_data"] = log_utilisation
    else:
        result["log_utilisation_data"] = "No Data"
         


    # Size
    stmt = ibm_db.exec_immediate(conn, """
     SELECT 
    DECIMAL(SUM(TBSP_USED_SIZE_KB)/1024.0, 12, 2) AS DATABASE_SIZE_MB,
    ROUND(DECIMAL(SUM(TBSP_USED_SIZE_KB)/1024.0/1024.0, 12, 3), 3) AS DATABASE_SIZE_GB
FROM SYSIBMADM.TBSP_UTILIZATION
    """)
    row = ibm_db.fetch_assoc(stmt)
    result["database_size_mb"] = row["DATABASE_SIZE_MB"]
    result["database_size_gb"] = row["DATABASE_SIZE_GB"]    

    

    #Last backup
    stmt = ibm_db.exec_immediate(conn, """
        select  date(timestamp(start_time)) as start_date , 
           time(timestamp(start_time)) as start_time ,
            timestampdiff ( 4, varchar(timestamp(end_time) - timestamp(start_time)) ) as duration,
        SUBSTR(LOCATION,1,80) as LOCATION , case when objecttype = 'D' then 'Database'
         else objecttype end as object , case operationtype when 'D' then 'Delta Offline' 
        when 'E' then 'Delta Online' when 'F' then 'Full Offline Backup' when 'I' then 
        'Incremental Offline'  when 'N' then 'Full Online Backup' when 'O' then 
        'Incremental Online' else operationtype end as Type from sysibmadm.db_history 
         where operation='B' and DATE(TIMESTAMP(start_time)) = (select date(timestamp(start_time)) as start_date from sysibmadm.db_history 
         where operation='B' and seqnum=1  order by start_date desc fetch first row only ) and operationtype='F' or operationtype='N' and seqnum=1  and SQLSTATE is null order by start_date desc , start_time  with ur 
    """)
    row = ibm_db.fetch_assoc(stmt)
    
    full_backup_data = []
    while row :
        full_backup_data.append({
            "start_date":row["START_DATE"],
            "start_time":row["START_TIME"],
            "duration":row["DURATION"],
            "location":row["LOCATION"],
            "objecttype":row["OBJECT"],
           "operationtype":row["TYPE"]
        
        })

        row = ibm_db.fetch_assoc(stmt)
    if full_backup_data:
        result["last_full_backup"] = full_backup_data
    else:
        result["last_full_backup"] = "No Data"
     #lastincremental
    stmt = ibm_db.exec_immediate(conn, """
        select  date(timestamp(start_time)) as start_date , 
           time(timestamp(start_time)) as start_time ,
            timestampdiff ( 4, varchar(timestamp(end_time) - timestamp(start_time)) ) as duration,
        SUBSTR(LOCATION,1,80) as LOCATION , case when objecttype = 'D' then 'Database'
         else objecttype end as object , case operationtype when 'D' then 'Delta Offline' 
        when 'E' then 'Delta Online' when 'F' then 'Full Offline Backup' when 'I' then 
        'Incremental Offline'  when 'N' then 'Full Online Backup' when 'O' then 
        'Incremental Online' else operationtype end as Type from sysibmadm.db_history 
         where operation='B' and DATE(TIMESTAMP(start_time)) = (select date(timestamp(start_time)) as start_date from sysibmadm.db_history 
         where operation='B' and seqnum=1  order by start_date desc fetch first row only ) and operationtype='I' or operationtype='O' and seqnum=1  and SQLSTATE is null order by start_date desc , start_time  with ur 
    """)
    row = ibm_db.fetch_assoc(stmt)
    
    inc_backup_data = []
    while row :
        inc_backup_data.append({
            "start_date":row["START_DATE"],
            "start_time":row["START_TIME"],
            "duration":row["DURATION"],
            "location":row["LOCATION"],
            "objecttype":row["OBJECT"],
           "operationtype":row["TYPE"]
        
        })

        row = ibm_db.fetch_assoc(stmt)

    if inc_backup_data:
        result["last_inc_backup"] = inc_backup_data
    else:
        result["last_inc_backup"] = "No Data"

    stmt = ibm_db.exec_immediate(conn, """
        select  date(timestamp(start_time)) as start_date , 
           time(timestamp(start_time)) as start_time ,
            timestampdiff ( 4, varchar(timestamp(end_time) - timestamp(start_time)) ) as duration,
        SUBSTR(LOCATION,1,80) as LOCATION , case when objecttype = 'D' then 'Database'
         else objecttype end as object , case operationtype when 'D' then 'Delta Offline' 
        when 'E' then 'Delta Online' when 'F' then 'Full Offline Backup' when 'I' then 
        'Incremental Offline'  when 'N' then 'Full Online Backup' when 'O' then 
        'Incremental Online' else operationtype end as Type from sysibmadm.db_history 
         where operation='B' and DATE(TIMESTAMP(start_time)) = (select date(timestamp(start_time)) as start_date from sysibmadm.db_history 
         where operation='B' and seqnum=1  order by start_date desc fetch first row only ) and operationtype='D' or operationtype='E' and seqnum=1  and SQLSTATE is null order by start_date desc , start_time  with ur 
    """)
    row = ibm_db.fetch_assoc(stmt)
    
    del_backup_data = []
    while row :
        del_backup_data.append({
            "start_date":row["START_DATE"],
            "start_time":row["START_TIME"],
            "duration":row["DURATION"],
            "location":row["LOCATION"],
            "objecttype":row["OBJECT"],
           "operationtype":row["TYPE"]
        
        })

        row = ibm_db.fetch_assoc(stmt)
    if del_backup_data:
        result["del_backup_data"] = del_backup_data
    else:
        result["del_backup_data"] = "No Data"

    #Replication

    stmt = ibm_db.exec_immediate(conn, """SELECT HADR_ROLE, STANDBY_ID, HADR_STATE,HADR_LOG_GAP, varchar(PRIMARY_MEMBER_HOST ,20)
   as PRIMARY_MEMBER_HOST, varchar(STANDBY_MEMBER_HOST ,20)
   as STANDBY_MEMBER_HOST from table(MON_GET_HADR(NULL))
    """)
    row = ibm_db.fetch_assoc(stmt)
    if row:
        result["hadr_role"] = row["HADR_ROLE"]
        result["standby_id"] = row["STANDBY_ID"]
        result["hadr_state"] = row["HADR_STATE"]
        result["hadr_log_gap"] = row["HADR_LOG_GAP"]
        result["primary_member_host"] = row["PRIMARY_MEMBER_HOST"]
        result["standby_member_host"] = row["STANDBY_MEMBER_HOST"]
    else:
        result["hadr_role"] = "No Data"
   


    #DPF
    stmt = ibm_db.exec_immediate(conn, """SELECT COUNT(*) FROM SYSCAT.DBPARTITIONGROUPS WHERE DBPGNAME = 'IBMCATGROUP'
    """)
    row = ibm_db.fetch_assoc(stmt)
    if row["1"] > 1:
        result["is_dpf"] = True
    else:
        result["is_dpf"] = False
        result["Num_of_partitions"] = row["1"]
   


    return result
