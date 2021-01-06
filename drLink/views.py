from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from drLink.models import *
from django.views.decorators.csrf import csrf_protect

from django.http import HttpResponse, JsonResponse
import json
import math

def home(request):
    if 'id' in request.session: #이미 로그인상태
        number_page = 10
        appointment_result = getAppointmentList(1,number_page) # [[doctor_num, d_name, d_photo, dep_name, patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, reg_date], ...]
        doctorList_result = getDoctorList(1,5)  # [[doctor_num, d_name, d_photo, b.dep_name, d_phone_num, d_email, d_regdate, retire_date,count] ...]
        patientListresult = getPatientList(1,5)
        newChart = getNewChart()
        sum_price = getSumPrice()
        patient_count = getPatientCount()
        gender = getGender()
        priceChart=getPriceChart()
        seosonPrice=getSeasonPrice()
        return render(request, "drLink/index.html",{'seosonPrice':seosonPrice,'priceChart':priceChart,'gender':gender,'newChart':newChart,'appointmentList':appointment_result,'doctorList':doctorList_result,'patientList':patientListresult,'sum_price':sum_price,'patient_count':patient_count})

    return render(request, "drLink/login.html")

def goLogin(request):
    if 'id' in request.session: #이미 로그인상태
        return render(request, "drLink/index.html")
    elif 'id' not in request.session:
        return render(request, "drLink/login.html")

def adminLogin(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    result = LoginCheck(id, pwd)
    if result:
        request.session['id']=result[0]
        request.session['name']=result[1]
        return redirect("/drLink")
    else:
        msg = '아이디나 비밀번호가 일치하지 않습니다.'
    return render(request, "drLink/login.html", {'msg':msg})

def adminLogout(request):
    if 'id' in request.session: #이미 로그인상태
        del (request.session['id'])
        del (request.session['name'])
    return redirect("/drLink")

def add_blog(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/add_blog.html")

#2020-12-29 송은
def appointment_list(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 10
    try:
        if request.GET['p_num'] != None:
            appointmentList = getAppointmentList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        appointmentList = getAppointmentList(1, number_page)
    page_num = math.ceil(appointmentList[0][11]/number_page)
    page_num = [i for i in range(1, page_num+1)]
    return render(request, "drLink/appointment_list.html", {'appointmentList':appointmentList, 'p_num':page_num})

def blog_details(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/blog_details.html")

#2020-12-29 송은
def doctor_list(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 10
    try:
        if request.GET['p_num'] != None:
            doctorList = getDoctorList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        doctorList = getDoctorList(1, number_page)
    page_num = math.ceil(doctorList[0][10] / number_page)
    page_num = [i for i in range(1, page_num + 1)]
    print(page_num)
    return render(request, "drLink/doctor_list.html", {'doctorList': doctorList, 'p_num': page_num})

def edit_blog(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/edit_blog.html")

def health_info(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/health_info.html")

def notice(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/notice.html")

#2020-12-29 송은
def patient_list(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 10
    try:
        if request.GET['p_num'] != None:
            patientList = getPatientList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        patientList = getPatientList(1, number_page)
    page_num = math.ceil(patientList[0][9] / number_page)
    page_num = [i for i in range(1, page_num + 1)]
    return render(request, "drLink/patient_list.html", {'patientList': patientList,'p_num':page_num})

def profile(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/profile.html")

def question(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    return render(request, "drLink/question.html")

def reviews(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 10
    try:
        if request.GET['p_num'] != None:
            result = getReviewList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        result = getReviewList(1, number_page)
    page_num = math.ceil(result[0][9] / number_page)
    page_num = [i for i in range(1, page_num+1)]
    print(result)
    return render(request, "drLink/reviews.html", {'reviewList':result,'p_num':page_num})

#2020-12-29 송은
def specialities(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    result = getSpecialitiesList() # [[dep_num, dep_name], ...]
    doctorList_result = getDoctorList(1, 100)
    print(doctorList_result[0][4])
    return render(request, "drLink/specialities.html",{'specialities':result,'doctorList':doctorList_result})

def transactions_list(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 10
    try:
        if request.GET['p_num'] != None:
            result = getTransactionsList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        result = getTransactionsList(1, number_page)
    page_num = math.ceil(result[0][11] / number_page)
    page_num = [i for i in range(1, page_num + 1)]
    return render(request, "drLink/transactions_list.html", {'transactionList': result, 'p_num': page_num})

#2020-12-29 송은
def insertSpeciality(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    insertSpecialitysave(request.POST['dep_name'])
    return redirect('/drLink/specialities')

def updateSpeciality(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    updateSpecialitysave(request.POST['dep_num'], request.POST['dep_name'])
    return redirect('/drLink/specialities')

def deleteSpeciality(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    deleteSpecialitysave(request.POST['dep_num'])
    return redirect('/drLink/specialities')
######################################

#2020-12-29 송은
def deleteDoctor(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    deleteDoctorSave(request.POST['doctor_num'])
    return redirect('/drLink/doctor_list')

def doctor_profile(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    print("request.GET['doctor_num']: ", request.GET['doctor_num'])
    result = getDoctorInfo(request.GET['doctor_num'])
    print("result ",result[12])
    graduation = result[12].split(',')
    career = result[13].split(',')
    gg = []
    gradu = []
    c_detail=[]
    c_detail2=[]
    cnt = 1
    for i in range(len(graduation)+1):
        if i < 3*cnt:
            gradu.append(graduation[i])
        elif i <= 3*cnt:
            cnt += 1
            gg.append(gradu)
            gradu = []
            if i >= len(graduation):
                break
            gradu.append(graduation[i])

    cnt = 1
    for i in range(len(career)+1):
        if i < 3*cnt:
            c_detail.append(career[i])
        elif i <= 3*cnt:
            cnt += 1
            c_detail2.append(c_detail)
            c_detail=[]
            if i >= len(career):
                break
            c_detail.append(career[i])
    return render(request, 'drLink/doctor_profile.html',{'doctor':result,'graduation':gg,'career':c_detail2})

def patient_profile(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    result = getPatientInfo(request.GET['patient_num'])
    return render(request, 'drLink/patient_profile.html',{'patient':result})

def deleteReview(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    deleteReviewSave(request.POST['review_num'])
    return redirect("/drLink/reviews")

def deleteTransaction(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    deleteTransactionSave(request.POST['prescription_num'])
    return redirect("/drLink/transactions_list")


##########################################################################################

def notice(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 6
    try:
        if request.GET['p_num'] != None:
            h_boardList = getH_boardList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        h_boardList = getH_boardList(1, number_page)
    page_num = math.ceil(h_boardList[0][7] / number_page)
    page_num = [i for i in range(1, page_num+1)]
    return render(request, "drLink/notice.html", {'h_List' : h_boardList, 'p_num': page_num})

def notice_details(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    h_num = request.GET['h_num']
    h_detail = getH_board_details(h_num)
    print(h_detail)
    return render(request, "drLink/notice_details.html", {'h_detail':h_detail})

def delete_notice_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    h_num = request.GET['h_num']
    delete_noticeBoard(h_num)
    return redirect('/drLink/notice')

def edit_notice_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    h_num = request.GET['h_num']
    h_edit = getH_board_details(h_num)
    return render(request, "drLink/edit_notice_board.html", {'h_edit':h_edit})

def health_info(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    number_page = 6
    try:
        if request.GET['p_num'] != None:
            n_boardList = getN_boardList(request.GET['p_num'], number_page)
    except Exception as ex:
        print(ex)
        n_boardList = getN_boardList(1, number_page)
    page_num = math.ceil(n_boardList[0][8]/number_page)
    page_num = [i for i in range(1, page_num+1)]
    return render(request, "drLink/health_info.html", {'n_boardList':n_boardList, 'p_num':page_num})

def health_blog_details(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    n_num = request.GET['n_num']
    print("건강정보 detail=", n_num)
    n_detail = getN_board_details(n_num)
    n_r = getN_replList(n_num)
    return render(request, "drLink/health_blog_details.html" , {'n_detail': n_detail, 'n_repl':n_r})

def delete_health_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    n_num = request.GET['n_num']
    print("delete_health_board 요청: ",n_num)
    delete_healthBoard(n_num)
    return redirect('/drLink/health_info')

def health_board_edit(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    n_num = request.GET['n_num']
    n_detail = getN_board_details(n_num)
    #return redirect('/drLink/health_info')
    return render(request, "drLink/edit_health_board.html", {'n_edit': n_detail})

UPLOAD_DIR = '/home/kosmo1/PycharmProjects/pythonProject/assets/img/blog/'
@csrf_protect
def insert_health_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    if 'board_img' in request.FILES:
        file = request.FILES['board_img']
        print(type(file))
        file_name = file.name
        print("========================>",file_name)
        fp = open("%s%s"%(UPLOAD_DIR,file_name),'wb')
            # 파일을 1바이트씩 조금씩 읽어서 저장
        for chunk in file.chunks():
               fp.write(chunk)
        fp.close() # 파일 닫기
    else:
        file_name = None
    print(request.POST['title'], request.POST['content'])
    if request.POST['url'] != None:
        boardList = (request.POST['url'], file_name, request.POST['title'], request.POST['content'])
        insert_healthBoard(boardList)
    else:
        boardList = (None, file_name, request.POST['title'], request.POST['content'])
        insert_healthBoard(boardList)
    return redirect("/drLink/health_info")

UPLOAD_DIR = '/home/kosmo1/PycharmProjects/pythonProject/assets/img/blog/'
@csrf_protect
def insert_notice_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    if 'board_img' in request.FILES:
        file = request.FILES['board_img']
        print(type(file))
        file_name = file.name
        print("========================>",file_name)
        fp = open("%s%s"%(UPLOAD_DIR,file_name),'wb')
            # 파일을 1바이트씩 조금씩 읽어서 저장
        for chunk in file.chunks():
               fp.write(chunk)
        fp.close() # 파일 닫기
    else:
        file_name = None
    boardList = (file_name, request.POST['title'], request.POST['content'])
    insert_noticeBoard(boardList)
    return redirect("/drLink/notice")

UPLOAD_DIR = '/home/kosmo1/PycharmProjects/pythonProject/assets/img/blog/'
@csrf_protect
def insert_faq_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    boardList = (request.POST['title'], request.POST['content'])
    insert_faqBoard(boardList)
    return redirect("/drLink/question")

def delete_repl(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    repl = {'news_reply_num':  request.GET['repl_num'], 'news_board_num':  request.GET['news_board_num'] }
    print(repl)
    del_repl(repl)
    return redirect("/drLink/health_blog_details?n_num="+repl['news_board_num'])

UPLOAD_DIR = '/home/kosmo1/PycharmProjects/pythonProject/assets/img/blog/'
@csrf_protect
def update_notice_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    if 'hospital_photo' in request.FILES:
        file = request.FILES['hospital_photo']
        print("사진 타입:",type(file))
        file_name = file.name
        print("========================>",file_name)
        fp = open("%s%s"%(UPLOAD_DIR,file_name),'wb')
            # 파일을 1바이트씩 조금씩 읽어서 저장
        for chunk in file.chunks():
               fp.write(chunk)
        fp.close() # 파일 닫기
    elif request.POST['hospital_photo'] != None or request.POST['hospital_photo'] != '':
        file_name = request.POST['hospital_photo']
    else:
        file_name = None
    up_H_board = list([request.POST['hospital_board_num'], request.POST['hospital_title'], request.POST['hospital_content']])
    h_list = {'hospital_board_num': up_H_board[0], 'hospital_photo': file_name, 'hospital_title':up_H_board[1], 'hospital_content': up_H_board[2]}
    update_noticeBoard(h_list)
    return redirect('/drLink/notice')

UPLOAD_DIR = '/home/kosmo1/PycharmProjects/pythonProject/assets/img/blog/'
@csrf_protect
def update_health_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    if 'news_photo' in request.FILES:
        file = request.FILES['news_photo']
        print(type(file))
        file_name = file.name
        print("========================>",file_name)
        fp = open("%s%s"%(UPLOAD_DIR,file_name),'wb')
            # 파일을 1바이트씩 조금씩 읽어서 저장
        for chunk in file.chunks():
               fp.write(chunk)
        fp.close() # 파일 닫기
    elif request.POST['news_photo'] != None or request.POST['news_photo'] != '':
        file_name = request.POST['news_photo']
    else:
        file_name = None
    up_Health_board = list([request.POST['n_num'], request.POST['news_url'], request.POST['news_title'], request.POST['news_content']])
    print(up_Health_board, "upup")
    n_list = {'news_board_num': up_Health_board[0], 'news_url':up_Health_board[1], 'news_photo':file_name, 'news_title': up_Health_board[2], 'news_content': up_Health_board[3]}
    print("nlist", n_list)
    update_healthBoard(n_list)
    return redirect('/drLink/health_info')

@csrf_protect
def pw_chk(request):
    pw = request.POST['chk_pwd']
    print("들어온:",pw)
    chk = pwd_chk()
    print("받아온",chk)
    if pw == chk[0]:
        print("if 일치")
        pwdC = "등록한 비밀번호와 일치"
    else:
        print("else 불일치")
        pwdC = None
    result = {
        'result': 'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data': "not exist" if pwdC is None else "exist"
    }
    return HttpResponse(json.dumps(result), "application/json")

def add_blog(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    category = request.GET['category']
    return render(request, "drLink/add_blog.html",{'category':category})

def question(request):
    return render(request, "drLink/question.html")

def faq_details(request):
    return render(request, "drLink/faq_details.html")

def edit_faq_board(request):
    return render(request, '/drLink/edit_faq_board.html')

