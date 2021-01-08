from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from drLink.models import *
from django.views.decorators.csrf import csrf_protect

from django.http import HttpResponse, JsonResponse
import json
import math
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import pandas as pd
import numpy as np
import joblib
import pickle
from tensorflow.keras.models import load_model
import requests
from bs4 import BeautifulSoup
from PIL import Image
import os, glob, numpy as np
from tensorflow.python.keras.models import load_model
import tensorflow as tf
from sklearn import utils
from sklearn.preprocessing import StandardScaler
# Create your views here.
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from tensorflow.compat.v2.keras.models import model_from_json
from wordcloud import wordcloud, WordCloud
from collections import Counter
import matplotlib.pyplot as plt


def jsonAIT(request):   # spring 연동
    jsonCall = request.GET.get("callback")
    jsonData = request.GET.get("img")
    # model.json 파일 열기
    json_file = open("/home/kosmo1/notedir/work1127/eyes_model.json", "r")
    origindir = "/home/kosmo1/notedir/work1127/Modeltrain/eyeTest"
    categories = os.listdir(origindir)
    loaded_model_json = json_file.read()
    json_file.close()
    # json파일로부터 model 로드하기
    loaded_model = model_from_json(loaded_model_json)
    # 로드한 model에 weight 로드하기
    loaded_model.load_weights("/home/kosmo1/notedir/work1127/eyes_model.h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    seed = 5
    tf.compat.v1.set_random_seed(seed)
    np.random.seed(seed)
    img_w = 64
    img_h = 64
    img_file = "/home/kosmo1/share/aiTest/{}".format(jsonData)
    #x_test = []
    img = Image.open(img_file)
    img = img.convert("RGB")
    img = img.resize((img_w, img_h))
    data = np.asarray(img)
    data = [data]
    #x_test.append(data)
    X = np.array(data)
    X = X.astype(float) / 255
    prediction = loaded_model.predict(X)
    print("prediction :",prediction)
    predict = int(prediction[0][np.argmax(prediction)] * 100)
    j_file = {'predict': predict, 'disease': categories[np.argmax(prediction)]}
    if jsonCall:
        response = HttpResponse("%s(%s);" % (jsonCall, json.dumps(j_file,ensure_ascii=False)))
        response["Content-type"] = "text/javascript; charset=utf-8"
    else:
        response = HttpResponse(json.dumps(j_file,ensure_ascii=False))
        response["Content-type"] = "application/json; charset=utf-8"
    # callback + "(" + result + ")"    callback + "("+ result +")"
    # return HttpResponse(json.dumps(aa), content_type='application/json', safe=False)
    return response

def home(request):
    if 'id' in request.session: #이미 로그인상태
        number_page = 10
        appointment_result = getAppointmentList(1,number_page) # [[doctor_num, d_name, d_photo, dep_name, patient_num, p_name, p_photo, appointment_num, appointment_date, appointment_time, reg_date], ...]
        doctorList_result = getDoctorList(1,5)  # [[doctor_num, d_name, d_photo, b.dep_name, d_phone_num, d_email, d_regdate, retire_date,count] ...]
        patientListresult = getPatientList(1,5)

        #차트
        newChart = getNewChart()
        sum_price = getSumPrice()
        patient_count = getPatientCount()
        ##########################
        # data = getGender()
        # data = pd.DataFrame(data, columns=['gender'])
        # female = data[data['gender'] == '2'].count()
        # male = data[data['gender'] == '1'].count()
        # gender = pd.concat([female, male], axis=1)
        # print(gender.iloc[0])
        ##########################
        gender=getGender()
        priceChart=getPriceChart()
        seosonPrice=getSeasonPrice()
        aiGenderFav = ai_gender_fav()
        aiFemaleFav = ai_female_fav()
        aiMaleFav = ai_male_fav()
        last_year = lastyear()
        two_year = twoyear()
        lastAppointment = []
        patient_type=[]
        ap_p_num =[]
        patient_num=[]
        p_num = getPatient_num()
        patient_sumprice=[]
        d_num=[]
        reviewAvg=[]
        for a in appointment_result:
            ap_p_num.append(a[4])
        for i,a in enumerate(ap_p_num):
            patient_type.append(getPatientType(a)[0])

        for a in patientListresult:
            patient_num.append(a[10])
        for i,a in enumerate(patient_num):
            patient_sumprice.append(getPatientSumPrice(a)[0])

        for a in doctorList_result:
            d_num.append(a[0])
        for i,a in enumerate(d_num):
            if getReviewAVG(a)== None:
                reviewAvg.append(0)
            else:
                reviewAvg.append(getReviewAVG(a)[0])
        for i in p_num:
            lastAppointment.append(getAPLatest(i[0])[0])
        return render(request, "drLink/index.html",{'twoyear':two_year,'lastyear':last_year,'aiMaleFav':aiMaleFav,'aiFemaleFav':aiFemaleFav,
                                                    'aiGenderFav':aiGenderFav,'gender':gender,'reviewAvg':reviewAvg,'patient_sumprice':patient_sumprice,
                                                    'patient_type':patient_type,'lastAppointment':lastAppointment,'seosonPrice':seosonPrice,'priceChart':priceChart,
                                                    'newChart':newChart,'appointmentList':appointment_result,'doctorList':doctorList_result,'patientList':patientListresult,
                                                    'sum_price':sum_price,'patient_count':patient_count})

    return render(request, "drLink/login.html")


@csrf_exempt
def insertAuthNumber(request):
    auth_number = auth_num()
    print('발급 된 인증번호 입니다. : ',auth_number)
    result = {'success' : auth_number}
    return JsonResponse(result)

def search_appointment_list(request):
    search_keyword = request.GET.get('search_keyword', '')
    search_type = self.request.GET.get('type', '')
    if search_keyword:
        if len(search_keyword) > 1:
            if search_type == 'all':
                search_notice_list = notice_list.filter(
                    Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword) | Q(
                        writer__user_id__icontains=search_keyword))
            elif search_type == 'title_content':
                search_notice_list = notice_list.filter(
                    Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
            elif search_type == 'title':
                search_notice_list = notice_list.filter(title__icontains=search_keyword)
            elif search_type == 'content':
                search_notice_list = notice_list.filter(content__icontains=search_keyword)
            elif search_type == 'writer':
                search_notice_list = notice_list.filter(writer__user_id__icontains=search_keyword)

            return search_notice_list
        else:
            messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
    return

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
    return render(request, "drLink/reviews.html", {'reviewList':result,'p_num':page_num})

#2020-12-29 송은
def specialities(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")

    result = getSpecialitiesList() # [[dep_num, dep_name], ...]
    doctorList_result = getDoctorList(1, 100)
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
    result = getDoctorInfo(request.GET['doctor_num'])
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
    n_detail = getN_board_details(n_num)
    n_r = getN_replList(n_num)
    return render(request, "drLink/health_blog_details.html" , {'n_detail': n_detail, 'n_repl':n_r})

def delete_health_board(request):
    if 'id' not in request.session: #로그인 필터
        return redirect("/drLink")
    n_num = request.GET['n_num']
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
    chk = pwd_chk()
    if pw == chk[0]:
        pwdC = "등록한 비밀번호와 일치"
    else:
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
