from django.urls import path

from drLink import views

urlpatterns=[
    # path('appointment_list', views.appointment_list),
    # path('doctor_list', views.doctor_list),
    # path('patient_list', views.patient_list),
    # path('profile', views.profile),
    # path('reviews', views.reviews),
    # path('specialities', views.specialities),
    # path('transactions_list', views.transactions_list),
    # path('insertSpeciality', views.insertSpeciality),
    # path('updateSpeciality', views.updateSpeciality),
    # path('deleteSpeciality', views.deleteSpeciality),
    # path('deleteDoctor', views.deleteDoctor),
    # path('doctor_profile', views.doctor_profile),
    # path('patient_profile', views.patient_profile),
    # path('deleteReview', views.deleteReview),
    # path('deleteTransaction', views.deleteTransaction),

    path('', views.home),
    path('index', views.home),
    path('adminLogin', views.adminLogin),
    path('adminLogout', views.adminLogout),
    path('appointment_list', views.appointment_list),
    path('doctor_list', views.doctor_list),
    path('patient_list', views.patient_list),
    path('doctor_profile', views.doctor_profile),
    path('patient_profile', views.patient_profile),
    path('reviews', views.reviews),
    path('deleteReview', views.deleteReview),
    path('specialities', views.specialities),
    path('insertSpeciality', views.insertSpeciality),
    path('deleteSpeciality', views.deleteSpeciality),
    path('updateSpeciality', views.updateSpeciality),
    path('transactions_list', views.transactions_list),
    path('notice', views.notice),
    path('notice_details', views.notice_details),
    path('update_notice_board', views.update_notice_board),
    path('delete_notice_board', views.delete_notice_board),
    path('insert_notice_board', views.insert_notice_board),
    path('edit_notice_board', views.edit_notice_board),
    path('health_info', views.health_info),
    path('health_blog_details', views.health_blog_details),
    path('update_health_board', views.update_health_board),
    path('delete_health_board', views.delete_health_board),
    path('insert_health_board', views.insert_health_board),
    path('edit_health_board', views.health_board_edit),
    path('question', views.question),
    path('faq_details', views.faq_details),
    path('add_blog', views.add_blog),
    path('insert_faq_board', views.insert_faq_board),
    path('edit_faq_board', views.edit_notice_board),
    path('delete_repl', views.delete_repl),
    path('pw_chk', views.pw_chk),
    path('jsonAIT', views.jsonAIT),
    path('insertAuthNumber',views.insertAuthNumber),
];