
import pymysql
db = pymysql.connect(host='10.8.8.7', port=3306, user='remote', passwd='y61FJa02', db='mysql', charset='utf8')
print(db)
cursor = db.cursor()
def sqlsql(day):

    sql_1="select '运营商','总提交号码','提交成功号码数','成功号码数','失败号码数','未知号码数','计费条数','总计费条数','提交成功','发送成功','发送失败','未知' \
UNION \
SELECT provider ,count(dest_number), \
SUM(case when submit_status = 'success' then 1 else 0 end), \
SUM(case when (submit_status = 'success' AND report_status = 'DELIVRD') then 1 else 0 end), \
SUM(case when (submit_status = 'success' AND report_status <> 'DELIVRD' AND trim(report_status) <> '' AND report_status is not NULL) then 1 else 0 end), \
SUM(case when (submit_status = 'success' AND (report_status is NULL OR trim(report_status) = '')) then 1 else 0 end) , \
lm_total, \
SUM(lm_total) as total,SUM(case when submit_status = 'success' then lm_total else 0 end), \
SUM(case when (submit_status = 'success' AND report_status = 'DELIVRD') then lm_total else 0 end), \
SUM(case when (submit_status = 'success' AND report_status <> 'DELIVRD' AND trim(report_status) <> '' AND report_status is not NULL) then lm_total else 0 end), \
SUM(case when (submit_status = 'success' AND (report_status is NULL OR trim(report_status) = '')) then lm_total else 0 end)  \
FROM eums_sms_log.mt_201807{_table} WHERE app_id='4708' GROUP BY provider,lm_total into outfile '/tmp/zhaoxueqing/{_dir}/mmmaimai_201807{_file}.xls';".format(_table=day,_dir=day, _file=day)

    sql_2 = """select 
'账号','运营商','首条成功下发时间','最后一条成功下发时间','提交号码数','黑名单数','成功数','失败数','未知数','提交短信条数','成功提交条数','未知条数','回退订','回复其他','停机'
union 
select 
 'mmyx',
 a.provider,min,max,submit,black1,delivr,fail,nulll,lm_total,delivr_lm_total,null_lm_total,black2,el,fail
from ( 
select app_id,
case when provider='cmcc' then '移动' when provider='unicom' then '联通'
		when provider='telecom' then '电信' else '未知' end provider,MIN(submit_time) min,MAX(submit_time) max ,
count(*) as submit
,sum(case when report_status='black' then 1 else 0 end) as black1
,sum(case when report_status='DELIVRD' then 1 else 0 end) as delivr
,sum(case when report_status<>'DELIVRD' and report_status<>'black' then 1 else 0 end) as fail
,sum(case when report_status is null then 1 else 0 end) as nulll
,SUM(lm_total) lm_total
,sum(case when report_status='DELIVRD' then lm_total else 0 end) as delivr_lm_total
,sum(case when report_status is null then lm_total else 0 end) as null_lm_total
from eums_sms_log.mt_201807{_table}
where app_id=3187 
group by provider,app_id ) as a 
left join
(select provider 
,sum(case when black_flag='yes' then 1 else 0 end ) as black2
,sum(case when black_flag='no' then 1 else 0 end ) as el
 from eums_sms_log.mo_201807
 a join statistics.phone_number b on left(src_number,3)=b.segment or left(src_number,4)=b.segment 
where  app_id =3187 
and left(unique_id,4) =DATE_FORMAT(DATE_ADD(CURDATE() ,INTERVAL -1 day),'%m%d')
group by provider) as b 
on a.provider=b.provider into outfile '/tmp/zhaoxueqing/{_day}/mmhy_201807{_file}.xls'""".format(_table=day, _file=day,_day=day)

    sql_3 = """select '运营商','总提交号码','提交成功号码数','成功号码数','失败号码数','未知号码数','计费条数','总计费条数','提交成功','发送成功','发送失败','未知'
UNION
SELECT provider ,count(dest_number),
SUM(case when submit_status = 'success' then 1 else 0 end),
SUM(case when (submit_status = 'success' AND report_status = 'DELIVRD') then 1 else 0 end),
SUM(case when (submit_status = 'success' AND report_status <> 'DELIVRD' AND trim(report_status) <> '' AND report_status is not NULL) then 1 else 0 end),
SUM(case when (submit_status = 'success' AND (report_status is NULL OR trim(report_status) = '')) then 1 else 0 end) ,
lm_total,
SUM(lm_total) as total,SUM(case when submit_status = 'success' then lm_total else 0 end),
SUM(case when (submit_status = 'success' AND report_status = 'DELIVRD') then lm_total else 0 end),
SUM(case when (submit_status = 'success' AND report_status <> 'DELIVRD' AND trim(report_status) <> '' AND report_status is not NULL) then lm_total else 0 end),
SUM(case when (submit_status = 'success' AND (report_status is NULL OR trim(report_status) = '')) then lm_total else 0 end) 
FROM eums_sms_log.mt_201807{_day} WHERE app_id='4546' GROUP BY provider,lm_total into outfile '/tmp/zhaoxueqing/{dir}/mmyx_201807{_file}.xls';""".format(_day=day,_file=day,dir=day)

    cursor.execute(sql_1)
    cursor.execute(sql_2)
    cursor.execute(sql_3)
    

for day in range(10,24):
    sqlsql(day)
db.close()

