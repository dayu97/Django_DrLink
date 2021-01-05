from django.db import models
import cx_Oracle as ora
# Create your models here.
#database = 'final_dr/test00@192.168.0.44:1522/orcl1'
# database = 'drLink/123@123.214.63.87:1521/orcl'
database = 'drlink/drlink00@192.168.0.52/orcl'
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

def getSumPrice() :
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select to_char(paydate,'yy/mm/dd'), sum(price) from payment_record group by paydate order by paydate"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    print(re)
    return re

def getGender():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select DECODE(p_gender, '1', '남자', '2', '여자') , count(case when p_gender = '1'then 1 when p_gender='2' then 0 end) as cnt from dl_user group by DECODE(p_gender, '1', '남자', '2', '여자')"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    print(re)
    return re

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

def getNewChart():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql="select (select count(*) from dl_doctor d where d.d_regdate >= sysdate-1 ),(select count(*) from dl_user u where u.p_regdate >= sysdate-1 ), (select count(*) from appointment a where a.reg_date >= sysdate-1 ) from dual"
    cursor.execute(sql)
    re = cursor.fetchone()
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
    sql = "insert into department values(dep_num_seq.nextval, :dep_name)"
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
            " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt" \
            " from appointment a, dl_doctor b, dl_user c, department d " \
            " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd')"\
            " order by appointment_date ) nnn ) nn where r_num between 1 and 10 "
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from ("\
            " select a.doctor_num, d_name, d_photo, d.dep_name, a.patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, " \
            " to_char(reg_date,'YYYY-MM-DD') ,(select count(*) from appointment where appointment_date > to_char(sysdate, 'yyyy-mm-dd')) as cnt"\
            " from appointment a, dl_doctor b, dl_user c, department d "\
            " where a.doctor_num=b.doctor_num and a.patient_num=c.patient_num and b.dep_num=d.dep_num and appointment_date > to_char(sysdate, 'yyyy-mm-dd')"\
            " order by appointment_date ) nnn ) nn where r_num between {} and {} ".format(start, end)
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



def getDoctorList(p_num, number_page):
    conn = ora.connect(database)
    cursor = conn.cursor()
    p_num = int(p_num)
    if p_num == 1:
     sql = "select nn.* from ( select nnn.*, rownum r_num from (SELECT a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.d_phone_num, a.d_email, to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD'),count(c.doctor_num) as cnt, (select count(*) from dl_doctor) " \
          " FROM dl_doctor a LEFT JOIN appointment c ON a.doctor_num = c.doctor_num join department b on a.dep_num = b.dep_num " \
          " GROUP BY a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.d_phone_num, a.d_email,to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD') order by cnt desc) nnn ) nn "\
          " where r_num between 1 and {} ".format(number_page)
    else:
        start, end = p_num * number_page-9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from (SELECT a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.d_phone_num, a.d_email, to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD'),count(c.doctor_num) as cnt, (select count(*) from dl_doctor) "\
          " FROM dl_doctor a LEFT JOIN appointment c ON a.doctor_num = c.doctor_num join department b on a.dep_num = b.dep_num "\
          " GROUP BY a.doctor_num, a.d_name, a.d_photo, b.dep_name, a.d_phone_num, a.d_email,to_char(d_regdate,'YYYY-MM-DD'), to_char(d_retire_date,'YYYY-MM-DD') order by cnt desc) nnn ) nn "\
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
            " P_ADDRESS1, P_ADDRESS2, P_PHONE_NUM, p_retire_date, (select count(*) from dl_user), patient_num from dl_user order by p_regdate desc) nnn ) nn "\
            " where r_num between 1 and {} ".format(number_page)
    else:
        start, end = p_num * number_page - 9, p_num * number_page
        sql = "select nn.* from ( select nnn.*, rownum r_num from "\
            " (select P_ID, P_EMAIL, P_NAME, P_PHOTO,EXTRACT(YEAR FROM SYSDATE)-(DECODE(SUBSTR(P_JUMIN_NUM,7,1),'1', '19','2','19','20') || SUBSTR(P_JUMIN_NUM,1,2)) +1, "\
            " P_ADDRESS1, P_ADDRESS2, P_PHONE_NUM, p_retire_date, (select count(*) from dl_user), patient_num from dl_user order by p_regdate desc) nnn ) nn "\
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

def getReviewList():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select * from doc_review a, dl_user b, dl_doctor c where a.doctor_num=c.doctor_num and a.patient_num=b.patient_num"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

def deleteReviewSave(review_num):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "delete from doc_review where review_num=:review_num"
    cursor.execute(sql, review_num=review_num)
    cursor.close()
    conn.commit()
    conn.close()

def getTransactionsList():
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql = "select a.*, b.*, c.*, d.*, e.*, to_char(prescription_date,'YYYY-MM-DD'), to_char(paydate,'YYYY-MM-DD') from prescription a, payment_record b, dl_user c, dl_doctor d, department e where b.prescription_num(+)=a.prescription_num and a.patient_num=c.patient_num and a.doctor_num=d.doctor_num and d.dep_num=e.dep_num"
    cursor.execute(sql)
    re = cursor.fetchall()
    cursor.close()
    conn.close()
    return re

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
        sql_select = "select hh.*, (select count(*) from hospital_board) cnt from ( select h.*, rownum r_num from (select * from hospital_board order by hospital_board_num) h ) hh where r_num between 1 and 6"
    else:
        start, end = p_num * number_page - 5, p_num * number_page
        sql_select = "select hh.*, (select count(*) from hospital_board) cnt from ( select h.*, rownum r_num from (select * from hospital_board order by hospital_board_num) h ) " \
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
    sql = "select * from hospital_board where hospital_board_num=:b_num"
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
        sql_select = "select nn.*, (select count(*) from news_board) cnt from ( select n.*, rownum r_num from (select * from news_board order by news_board_num) n ) nn where r_num between 1 and 6"
    else:
        start, end = p_num*number_page-5, p_num * number_page
        sql_select = "select nn.*, (select count(*) from news_board) cnt from ( select n.*, rownum r_num from (select * from news_board order by news_board_num) n ) " \
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
    sql = "select ( select count(*) from news_repl where news_board_num=:n_num ) cnt, n.* \
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