from django.db import models
import cx_Oracle as ora
import string
import random
# Create your models here.
database = 'drlink/drlink00@192.168.0.14/orcl'
#database = 'test/test00@192.168.0.52/orcl'
# Create your models here.

def LoginCheck(id, pwd):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from dl_admin where id='{}' and pwd='{}'".format(id, pwd)
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

#인증번호 생성 : 김다유
def auth_num():
    LENGTH = 8
    string_pool = string.ascii_letters + string.digits
    auth_num = ""
    for i in range(LENGTH):
        auth_num += random.choice(string_pool)
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into doctor_verify values(auth_num_seq.nextval,:auth_num, 0)"
    cursor.execute(sql, auth_num=auth_num)
    cursor.close()
    conn.commit()
    conn.close()
    return auth_num

#환자 번호 출력 : 김다유
def getPatient_num():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select distinct patient_num from appointment order by patient_num"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#환자 구분 : 김다유
def getPatientType(p_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "SELECT DECODE(count(patient_num),1,'','기존') AS TYPE FROM prescription where patient_num={} group by patient_num".format(p_num)
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

#환자 결제 금액 : 김다유
def getPatientSumPrice(p_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select nvl(sum(price),'0') from payment_record where patient_num ={}".format(p_num)
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

#의사 리뷰 평점 : 김다유
def getReviewAVG(d_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select round(avg(review_rating),0) as rating from doc_review where doctor_num={} group by doctor_num".format(d_num)
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re


def getAPLatest(p_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.appointment_date from(select * from appointment where patient_num = {} order by appointment_num desc) a where rownum = 1".format(p_num)
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

#총 수익 : 김다유
def getSumPrice() :
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select sum(price) from payment_record order by paydate"
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    print(sql)
    print(re)
    return re

#분기별 수익 : 김다유
def getSeasonPrice():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select  to_char(extract(year from sysdate))," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+1),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+2),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+3),0) from dual "
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#주간 수익 : 김다유
def getPriceChart():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "SELECT TO_CHAR (SYSDATE + 1, 'fmiw')"\
   " ,nvl((select sum(price) from payment_record where TO_CHAR(paydate,'yy-mm-dd') = TO_CHAR(A.S_DATA    , 'yy-mm-dd')), 0) "\
   " ,nvl((select sum(price) from payment_record where TO_CHAR(paydate,'yy-mm-dd') = TO_CHAR(A.S_DATA +1 , 'yy-mm-dd') ), 0) "\
   " ,nvl((select sum(price) from payment_record where TO_CHAR(paydate,'yy-mm-dd') = TO_CHAR(A.S_DATA +2 , 'yy-mm-dd') ), 0) "\
   " ,nvl((select sum(price) from payment_record where TO_CHAR(paydate,'yy-mm-dd') = TO_CHAR(A.S_DATA +3 , 'yy-mm-dd') ), 0) "\
   " ,nvl((select sum(price) from payment_record where TO_CHAR(paydate,'yy-mm-dd') = TO_CHAR(A.S_DATA +4 , 'yy-mm-dd') ), 0) "\
   " FROM (SELECT SYSDATE - (TO_NUMBER(TO_CHAR(SYSDATE, 'd')) - 2) S_DATA FROM DUAL) A"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#성별 차트 : 김다유
def getGender():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select DECODE(p_gender, '1', '남자', '2', '여자') , count(case when p_gender = '1'then 1 when p_gender='2' then 0 end) as cnt from dl_user group by DECODE(p_gender, '1', '남자', '2', '여자')"
    #sql="select p_gender from dl_user"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#환자 연령통계 : 김다유
def getPatientCount() :
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "SELECT substr( to_char ( to_number(to_char(sysdate,'yyyy')) - to_number"\
       " (CASE substr (p_jumin_num,7,1) WHEN'1'THEN '19' WHEN '2' THEN '19' ELSE '20'END || substr (p_jumin_num,1,2))+1 ) ,1 ,1 )||'0대' as birth_ymd,count(*) FROM DL_USER"\
       " group by substr( to_char ( to_number(to_char(sysdate,'yyyy')) - to_number"\
       " (CASE substr (p_jumin_num,7,1) WHEN'1'THEN '19' WHEN '2' THEN '19' ELSE '20'END || substr (p_jumin_num,1,2))+1 ) ,1 ,1 ) order by birth_ymd"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#신규데이터 통계 : 김다유
def getNewChart():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select nvl((select count(*) from dl_doctor d where d.d_regdate >= sysdate-1 ),0),"\
        " nvl((select count(*) from dl_user u where u.p_regdate >= sysdate-1 ),0), "\
        " nvl((select count(*) from appointment a where a.reg_date >= sysdate-1 ),0) from dual"
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

#AI 통계 - 연령별 인기 순 : 김다유
def ai_gender_fav():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select * from (select nnn.* from (" \
        "select ai_model, count(*) f_cnt from ai_record a join dl_user b on a.patient_num = b.patient_num where p_gender = '2' group by ai_model order by f_cnt) nnn " \
        "where rownum = 1 ) female_model, ( select aaa.* from (" \
        "select ai_model, count(*) m_cnt from ai_record a join dl_user b on a.patient_num = b.patient_num where p_gender = '1' group by ai_model order by m_cnt" \
        ") aaa where rownum = 1 ) male_model  "
    cursor.execute(sql)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

#AI 통계 - 남성별 인기 순 : 김다유
def ai_male_fav():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select ai_model, count(*) from ai_record a join dl_user b on a.patient_num = b.patient_num where p_gender = '1' group by ai_model  "
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

#AI 통계 - 여성별 인기 순 : 김다유
def ai_female_fav():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select ai_model, count(*) from ai_record a join dl_user b on a.patient_num = b.patient_num where p_gender = '2' group by ai_model "
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re
#작년 수익 : 김다유
def lastyear():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select  to_char(extract(year from sysdate)-1)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-1) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-1) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+1),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-1) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+2),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-1) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+3),0) from dual "
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re
#재작년 수익 : 김다유
def twoyear():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select  to_char(extract(year from sysdate)-2)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-2) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-2) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+1),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-2) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+2),0)," \
        "nvl((select sum(price) from payment_record where to_char(extract(year from sysdate)-2) = to_char(paydate,'yyyy') and to_char(paydate,'q')=to_char(sysdate,'q')+3),0) from dual  "
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re


#2020-12-29 송은
#진료과목(department)
def getSpecialitiesList():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from department order by dep_num"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

def insertSpecialitysave(dep_name):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into department values((select max(dep_num)+10 from department), :dep_name)"
    cursor.execute(sql, dep_name=dep_name)
    cursor.close()
    conn.commit()
    conn.close()


def updateSpecialitysave(dep_num, dep_name):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "update department set dep_name=:dep_name where dep_num=:dep_num"
    cursor.execute(sql,dep_num=dep_num, dep_name=dep_name)
    cursor.close()
    conn.commit()
    conn.close()

def deleteSpecialitysave(dep_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete from department where dep_num=:dep_num"
    cursor.execute(sql,dep_num=dep_num)
    cursor.close()
    conn.commit()
    conn.close()
#/진료과목(department)

#2020-12-29 송은
def getAppointmentList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql = "select nn.* from ( select nnn.*, rownum r_num from (" \
            " select a.doctor_num, d_name, d_photo, d.dep_name, a.patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, " \
            " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt,(select count(*) from appointment) as allcnt" \
            " from appointment a, dl_doctor b, dl_user c, department d " \
            " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd')"\
            " order by appointment_date ) nnn ) nn where r_num between 1 and 10 order by appointment_num  "
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from ("\
            " select a.doctor_num, d_name, d_photo, d.dep_name, a.patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, " \
            " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt,(select count(*) from appointment) as allcnt"\
            " from appointment a, dl_doctor b, dl_user c, department d "\
            " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd')"\
            " order by appointment_date ) nnn ) nn where r_num between {} and {} order by appointment_num ".format(start, end)
    try:
        cursor.execute(sql)
        n_boardList = cursor.fetchall()
        cursor.close()
        return n_boardList
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def getAppointmentList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql = " select nn.* from ( select nnn.*, rownum r_num from (" \
            " select a.doctor_num, d_name, d_photo, d.dep_name, a.patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, " \
            " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt,(select count(*) from appointment) as allcnt" \
            " from appointment a, dl_doctor b, dl_user c, department d " \
            " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd')"\
            " order by appointment_num desc, appointment_date  ) nnn ) nn where r_num between 1 and 10 order by appointment_num desc "
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from ("\
            " select a.doctor_num, d_name, d_photo, d.dep_name, a.patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, " \
            " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt,(select count(*) from appointment) as allcnt"\
            " from appointment a, dl_doctor b, dl_user c, department d "\
            " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd')"\
            " order by appointment_num desc, appointment_date ) nnn ) nn where r_num between {} and {} order by appointment_num desc ".format(start, end)
    try:
        cursor.execute(sql)
        n_boardList = cursor.fetchall()
        cursor.close()
        return n_boardList
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def getAppointmentSearchList(p_num, number_page,search_keyword,type):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num != 1:
        start,end = p_num,number_page
    start, end = p_num * number_page - 9, p_num * number_page
    sql = "select nn.* from ( select nnn.*, rownum r_num from ("\
        " select a.doctor_num, d_name, d_photo, d.dep_name, a.patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, " \
        " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt,(select count(*) from appointment) as allcnt"\
        " from appointment a, dl_doctor b, dl_user c, department d "\
        " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd') and {} like '%{}%' "\
        " order by appointment_date ) nnn ) nn where r_num between {} and {} order by appointment_num ".format(type,search_keyword,start, end)
    try:
        cursor.execute(sql)
        n_boardList = cursor.fetchall()
        cursor.close()
        print(n_boardList)
        return n_boardList
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()



def getDoctorList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
     sql = "select nn.* from ( select nnn.*, rownum r_num from (SELECT a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.dep_num, a.d_phone_num, a.d_email, " \
           "to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD'),count(c.doctor_num) as cnt, (select count(*) from dl_doctor) " \
           ",nvl(round(avg(review_rating),0),'0')" \
           " FROM dl_doctor a LEFT JOIN appointment c ON a.doctor_num = c.doctor_num join department b on a.dep_num = b.dep_num left join doc_review e on a.doctor_num = e.doctor_num" \
           " GROUP BY a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.dep_num, a.d_phone_num, a.d_email,to_char(d_regdate,'YYYY-MM-DD'), " \
           " to_char(d_retire_date,'YYYY-MM-DD') order by doctor_num ) nnn ) nn "\
          " where r_num between 1 and {} ".format(number_page)
    else:
        start, end = p_num * number_page-9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from (SELECT a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.dep_num, a.d_phone_num, a.d_email, " \
              "to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD'),count(c.doctor_num) as cnt, (select count(*) from dl_doctor) " \
              ",nvl(round(avg(review_rating),0),'0')" \
              " FROM dl_doctor a LEFT JOIN appointment c ON a.doctor_num = c.doctor_num join department b on a.dep_num = b.dep_num left join doc_review e on a.doctor_num = e.doctor_num" \
              " GROUP BY a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.dep_num, a.d_phone_num, a.d_email,to_char(d_regdate,'YYYY-MM-DD'), " \
              " to_char(d_retire_date,'YYYY-MM-DD') order by doctor_num ) nnn ) nn "\
              " where r_num between {} and {} ".format(start, end)
    try:
        cursor.execute(sql)
        doctor_List = cursor.fetchall()
        cursor.close()
        return doctor_List
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()


def getDoctorSearchList(p_num, number_page,search_keyword,type):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num != 1:
        start,end = p_num,number_page
    start, end = p_num * number_page-9, p_num * number_page
    sql = "select nn.* from ( select nnn.*, rownum r_num from (SELECT a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.dep_num, a.d_phone_num, a.d_email, " \
       "to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD'),count(c.doctor_num) as cnt, (select count(*) from dl_doctor) " \
       ",nvl(round(avg(review_rating),0),'0')" \
       " FROM dl_doctor a LEFT JOIN appointment c ON a.doctor_num = c.doctor_num join department b on a.dep_num = b.dep_num left join doc_review e on a.doctor_num = e.doctor_num" \
       " where {} like '%{}%' GROUP BY a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.dep_num, a.d_phone_num, a.d_email,to_char(d_regdate,'YYYY-MM-DD'), " \
       " to_char(d_retire_date,'YYYY-MM-DD') order by doctor_num ) nnn ) nn "\
      " where r_num between {} and {} ".format(type, search_keyword, start, end)
    try:
        cursor.execute(sql)
        doctor_List = cursor.fetchall()
        cursor.close()
        return doctor_List

    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def deleteDoctorSave(doctor_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "update dl_doctor set retire_date=sysdate where doctor_num=:doctor_num"
    cursor.execute(sql, doctor_num=doctor_num)
    cursor.close()
    conn.commit()
    conn.close()

def getPatientList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql = "select nn.* from ( select nnn.*, rownum r_num from "\
            " (select P_ID, P_EMAIL, P_NAME, P_PHOTO,EXTRACT(YEAR FROM SYSDATE)-(DECODE(SUBSTR(P_JUMIN_NUM,7,1),'1', '19','2','19','20') || SUBSTR(P_JUMIN_NUM,1,2)) +1, "\
            " P_ADDRESS1, P_ADDRESS2, P_PHONE_NUM, p_retire_date, (select count(*) from dl_user), patient_num from dl_user order by patient_num desc) nnn ) nn "\
            " where r_num between 1 and {} ".format(number_page)
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from "\
            " (select P_ID, P_EMAIL, P_NAME, P_PHOTO,EXTRACT(YEAR FROM SYSDATE)-(DECODE(SUBSTR(P_JUMIN_NUM,7,1),'1', '19','2','19','20') || SUBSTR(P_JUMIN_NUM,1,2)) +1, "\
            " P_ADDRESS1, P_ADDRESS2, P_PHONE_NUM, p_retire_date, (select count(*) from dl_user), patient_num from dl_user order by patient_num desc) nnn ) nn "\
            " where r_num between {} and {} ".format(start, end)
    try:
        cursor.execute(sql)
        patient_List = cursor.fetchall()
        cursor.close()
        return patient_List
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def getDoctorInfo(doctor_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.*, b.*, to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD'), (DECODE(SUBSTR(d_JUMIN_NUM,7,1),'1', '19','2','19','20') || SUBSTR(d_JUMIN_NUM,1,6))  from dl_doctor a, department b where a.DOCTOR_NUM=:doctor_num and a.DEP_NUM=b.DEP_NUM"
    cursor.execute(sql, doctor_num=doctor_num)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re


def getPatientInfo(patient_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.*, to_char(p_regdate,'YYYY-MM-DD'), to_char(p_retire_date,'YYYY-MM-DD'), (DECODE(SUBSTR(p_JUMIN_NUM,7,1),'1', '19','2','19','20') || SUBSTR(p_JUMIN_NUM,1,6)) from dl_user a where patient_num=:patient_num"
    cursor.execute(sql, patient_num=patient_num)
    re = cursor.fetchone()
    cursor.close()
    conn.close()
    return re

def getReviewList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql = "select nn.* from (select nnn.*, rownum r_num from ("\
               " select a.review_num, c.d_name, c.d_photo, c.doctor_num, b.p_name, b.patient_num, a.review_content, a.review_rating, a.review_date, (select count(*) from doc_review) as cnt from doc_review a, dl_user b, dl_doctor c "\
               " where a.doctor_num=c.doctor_num and a.patient_num=b.patient_num group by a.review_num, c.d_name, c.d_photo, c.doctor_num, b.p_name, b.patient_num, a.review_content, a.review_rating, a.review_date order by a.review_num desc) nnn"\
               " ) nn where r_num between 1 and {} ".format(number_page)
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from (select nnn.*, rownum r_num from (" \
              " select a.review_num, c.d_name, c.d_photo, c.doctor_num, b.p_name, b.patient_num,a.review_content, a.review_rating, a.review_date, (select count(*) from doc_review) as cnt from doc_review a, dl_user b, dl_doctor c " \
              " where a.doctor_num=c.doctor_num and a.patient_num=b.patient_num group by a.review_num, c.d_name, c.d_photo, c.doctor_num, b.p_name,b.patient_num, a.review_content, a.review_rating, a.review_date order by a.review_num desc) nnn" \
              " ) nn where r_num between {} and {} ".format(start, end)
    try:
        cursor.execute(sql)
        re = cursor.fetchall()
        cursor.close()
        return re
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()


def deleteReviewSave(review_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete from doc_review where review_num=:review_num"
    cursor.execute(sql, review_num=review_num)
    cursor.close()
    conn.commit()
    conn.close()

def getTransactionsList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql = "select nn.* from (select nnn.*, rownum r_num from (" \
              " select a.prescription_num,c.patient_num,c.p_name,d.d_photo,d.doctor_num,d.d_name,e.dep_name, a.prescription_date,a.price,to_char(b.paydate,'yyyy/mm/dd'),a.payment_check,(select count(*) from prescription) as cnt" \
              " from prescription a, payment_record b, dl_user c, dl_doctor d, department e where b.prescription_num(+)=a.prescription_num" \
              " and a.patient_num = c.patient_num and a.doctor_num = d.doctor_num and d.dep_num = e.dep_num order by a.prescription_num desc) nnn ) nn where r_num between 1 and {} ".format(number_page)
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from (select nnn.*, rownum r_num from (" \
              " select a.prescription_num,c.patient_num,c.p_name,d.d_photo,d.doctor_num,d.d_name,e.dep_name, a.prescription_date,a.price,to_char(b.paydate,'yyyy/mm/dd'),a.payment_check,(select count(*) from prescription) as cnt" \
              " from prescription a, payment_record b, dl_user c, dl_doctor d, department e where b.prescription_num(+)=a.prescription_num" \
              " and a.patient_num = c.patient_num and a.doctor_num = d.doctor_num and d.dep_num = e.dep_num order by a.prescription_num desc) nnn ) nn where r_num between {} and {} ".format(start, end)
    try:
        cursor.execute(sql)
        re = cursor.fetchall()
        cursor.close()
        print(re)
        return re
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def deleteTransactionSave(prescription_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete from prescription where prescription_num=:prescription_num"
    cursor.execute(sql, prescription_num=prescription_num)
    cursor.close()
    conn.commit()
    conn.close()














##############################################################################################################

def getH_boardList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql_select = "select hh.*, (select count(*) from hospital_board) cnt,to_char(hospital_regdate,'yyyy-mm-dd') from ( select h.*, rownum r_num from (select * from hospital_board order by hospital_board_num) h ) hh where r_num between 1 and 6"
    else:
        start, end = p_num * number_page - 5, p_num * number_page
        sql_select = "select hh.*, (select count(*) from hospital_board) cnt,to_char(hospital_regdate,'yyyy-mm-dd') from ( select h.*, rownum r_num from (select * from hospital_board order by hospital_board_num) h ) " \
                     "hh where r_num between {} and {}".format(start, end)
    try:
        cursor.execute(sql_select)
        h_boardList = cursor.fetchall()
        cursor.close()
        return h_boardList
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def getH_board_details(b_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select ( select count(*) from hospital_board where hospital_board_num=:b_num ) cnt, n.*, to_char(hospital_regdate,'yyyy-mm-dd') from hospital_board n where hospital_board_num=:b_num"
    try:
        cursor.execute(sql, b_num=b_num)
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(e)
    finally:
        conn.close()

def getN_boardList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
        sql_select = "select nn.*, (select count(*) from news_board) cnt,to_char(news_regdate,'yyyy-mm-dd') from ( select n.*, rownum r_num from (select * from news_board order by news_board_num) n ) nn where r_num between 1 and 6"
    else:
        start, end = p_num*number_page-5, p_num * number_page
        sql_select = "select nn.*, (select count(*) from news_board) cnt,to_char(news_regdate,'yyyy-mm-dd') from ( select n.*, rownum r_num from (select * from news_board order by news_board_num) n ) " \
                "nn where r_num between {} and {}".format(start, end)
    try:
        cursor.execute(sql_select)
        n_boardList = cursor.fetchall()
        cursor.close()
        return n_boardList
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()


def update_noticeBoard(h_num):
    print("들어온 보드넘버 : ", h_num['hospital_board_num'])
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "update hospital_board set hospital_photo=:hospital_photo, hospital_title=:hospital_title, hospital_content=:hospital_content where hospital_board_num=:hospital_board_num"
    cursor.execute(sql, hospital_photo=h_num['hospital_photo'], hospital_title=h_num['hospital_title'], hospital_content=h_num['hospital_content'], hospital_board_num=h_num['hospital_board_num'])
    cursor.close()
    conn.commit()
    conn.close()

def delete_noticeBoard(h_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete hospital_board where hospital_board_num=:hospital_board_num"
    cursor.execute(sql, hospital_board_num=h_num)
    cursor.close()
    conn.commit()
    conn.close()

def getN_board_details(n_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select ( select count(*) from news_repl where news_board_num=:n_num ) cnt, n.*, to_char(news_regdate,'yyyy-mm-dd') \
           from news_board n where news_board_num=:n_num"
    try:
        cursor.execute(sql, n_num=n_num)
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(e)
    finally:
        conn.close()

def getN_replList(news_board_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    news_board_num = int(news_board_num)
    sql_select = 'select nr.news_reply_num news_reply_num, nr.n_repl_date n_repl_date, p.p_name p_name, p.patient_num patient_num, d.d_name d_name, d.doctor_num doctor_num,' \
            'nr.news_repl_comment news_repl_comment, nr.n_comments_num n_comments_num from dl_user p, news_repl nr, dl_doctor d ' \
            'where p.patient_num(+) = nr.patient_num AND d.doctor_num(+) = nr.doctor_num AND nr.news_board_num =:news_board_num order by nr.news_reply_num'
    try:
        cursor.execute(sql_select, news_board_num=news_board_num)
        n_replList = cursor.fetchall()
        cursor.close()
        return n_replList
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()

def update_healthBoard(n_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "update news_board set news_url=:news_url, news_photo=:news_photo, news_title=:news_title, news_content=:news_content where news_board_num=:news_board_num"
    cursor.execute(sql, news_url=n_num['news_url'], news_photo=n_num['news_photo'], news_title=n_num['news_title'], news_content=n_num['news_content'], news_board_num=n_num['news_board_num'])
    cursor.close()
    conn.commit()
    conn.close()

def delete_healthBoard(n_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete news_board where news_board_num=:news_board_num"
    cursor.execute(sql, news_board_num=n_num)
    cursor.close()
    conn.commit()
    conn.close()

def del_repl(repl):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete news_repl where news_board_num=:news_board_num and news_reply_num=:news_reply_num"
    cursor.execute(sql, news_board_num=repl['news_board_num'], news_reply_num=repl['news_reply_num'])
    cursor.close()
    conn.commit()
    conn.close()

def insert_healthBoard(health_board):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into news_board values(news_board_num.nextVal, :1, :2, :3, :4, sysdate, 0)"
    cursor.execute(sql, health_board)
    cursor.close()
    conn.commit()
    conn.close()

def insert_noticeBoard(notice_board):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into hospital_board values(hospital_board_num.nextVal, :1, :2, :3, sysdate, 0)"
    cursor.execute(sql, notice_board)
    cursor.close()
    conn.commit()
    conn.close()

def insert_faqBoard(health_board):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "insert into news_board values(news_board_num.nextVal, :1, :2, :3, :4, sysdate, 0)"
    cursor.execute(sql, health_board)
    cursor.close()
    conn.commit()
    conn.close()

def pwd_chk():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql_select = 'select pwd from admin'
    try:
        cursor.execute(sql_select)
        pw = cursor.fetchone()
        cursor.close()
        return pw
    except Exception as e:
        print(e)
        print("실패")
    finally:
        conn.close()