#!/usr/bin/python3

import pymysql
import time
import tarfile
# 打开数据库连接
db = pymysql.connect(host="10.8.8.3",port=3308,user="remote",passwd="y61FJa02",db='mysql',charset='utf8')
print(db)
cursor = db.cursor()
#锁表操作
for dt in range(1,31):
    if dt < 10:
        dt = '0' + str(dt)
    date = "mt_201806%s"% str(dt)
    sql_anhui_chenggong = "SELECT final_ext_src,COUNT(*) FROM eums_sms_log.%s WHERE channel_id = '41' AND province = '安徽'AND submit_status = 'success' and report_status = 'DELIVRD' GROUP BY final_ext_src INTO OUTFILE '/tmp/zhaoxueqing/%s_anhui_chenggong.csv';"%(date,date)
    sql_anhui_weizhi = "SELECT final_ext_src,COUNT(*) FROM eums_sms_log.%s WHERE channel_id = '41' AND province = '安徽'AND submit_status = 'success' AND (TRIM(report_status) = '' OR report_status IS NULL) GROUP BY final_ext_src INTO OUTFILE '/tmp/zhaoxueqing/%s_anhui_weizhi.csv';" % (date,date)
    sql_qita_chenggong = "SELECT final_ext_src,COUNT(*) FROM eums_sms_log.%s WHERE channel_id = '41' AND province != '安徽'AND submit_status = 'success' and report_status = 'DELIVRD' GROUP BY final_ext_src INTO OUTFILE '/tmp/zhaoxueqing/%s_qita_chenggong.csv';" % (date, date)
    sql_qita_weizhi = "SELECT final_ext_src,COUNT(*) FROM eums_sms_log.%s WHERE channel_id = '41' AND province != '安徽'AND submit_status = 'success' AND (TRIM(report_status) = '' OR report_status IS NULL) GROUP BY final_ext_src INTO OUTFILE '/tmp/zhaoxueqing/%s_qita_weizhi.csv';" % (date, date)
    sql_list=list()
    sql_list.append(sql_anhui_chenggong)
    sql_list.append(sql_anhui_weizhi)
    sql_list.append(sql_qita_chenggong)
    sql_list.append(sql_qita_weizhi)
    for sql in sql_list:
        print(sql)
        cursor.execute(sql)
        time.sleep(3)

db.close()