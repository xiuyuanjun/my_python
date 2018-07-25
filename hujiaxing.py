
import pymysql
db = pymysql.connect(host='10.8.8.3', port=3308, user='remote', passwd='y61FJa02', db='mysql', charset='utf8')
print(db)
cursor = db.cursor()
def sqlsql(day):
    sql="SELECT provider AS '运营商',lm_total AS '计费条数',COUNT(dest_number) AS '提交号码数',\
    SUM(CASE WHEN submit_status = 'success' THEN 1 ELSE 0 END) AS '提交成功号码数',\
    SUM(CASE WHEN (submit_status = 'success' AND report_status = 'DELIVRD') THEN 1 ELSE 0 END) AS '状态成功号码数',\
    SUM(CASE WHEN (submit_status = 'success' AND report_status <> 'DELIVRD' AND TRIM(report_status) <> '' AND report_status IS NOT NULL) THEN 1 ELSE 0 END) AS '状态失败号码数',\
    SUM(CASE WHEN (submit_status = 'success' AND (report_status IS NULL OR TRIM(report_status) = '')) THEN 1 ELSE 0 END) AS '状态未知号码数'\
    FROM eums_sms_log.`mt_201807%s` WHERE app_id= (SELECT id FROM eums_sms_core.fors_application WHERE app_name = 'maimaihy') GROUP BY provider,lm_total INTO OUTFILE '/tmp/zhaoxueqing/mt_201807%s.csv'" %(str(day),str(day))
    cursor.execute(sql)
for day in range(10,24):
    sqlsql(day)
db.close()
