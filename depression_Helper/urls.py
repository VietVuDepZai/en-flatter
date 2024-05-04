"""
URL configuration for depression_Helper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from Main_App import views
from django.views.static import serve
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
        path('', views.index, name="home"),
    path("accounts/", include("allauth.urls")), #most important
            path('choosing', views.choosing, name="choosing"),
                path("acc", views.acc, name="acc"), #most important
    path('chatgpt/', views.gemini),


            path('doctor-signup', views.doctor_signup_view, name="doctor-signup"),
            path('patient-signup', views.patient_signup_view, name="patient-signup"),

    path('feeling', views.login_face, name="feeling"),
    path('login/',views.login,name="login"),
    path('doctormain',views.doctormain,name="doctormain"),
        path('doctorpatient',views.doctorpatient,name="doctorpatient"),

    path('patientmain',views.patientmain,name="patientmain"),
    
path('patientchat',views.patientchat,name="patientchat"),
        path('signup',views.signup,name="signup"),
path('chat', views.chat, name="chat"),
path('data', views.data, name="data"),
   path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('comingsoon', views.comingsoon,name='comingsoon'),

    path('start-exam/', views.start_exam_view,name='start-exam'),
        # Đang làm path('sendlogin/', views.recieve_login_face),
         path('calendar/', views.CalendarView.as_view(), name='calendar'),
                  path('patient-calendar/', views.PatientCalendarView.as_view(), name='calendar'),
                  path('paunaccept-calendar/', views.PaUnAccept.as_view(), name='paunaccept-calendar'),
                                    path('unaccept-calendar/', views.UnCalendarView.as_view(), name='unaccept-calendar'),


    path('paevent/new/', views.paevent, name='paevent_new'),
    path('paevent/edit/<event_id>/', views.paevent, name='paevent_edit'),

    path('patient-doctor/<int:pk>',views.patient_view_doctor,name="patient-doctor"),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<event_id>/', views.event, name='event_edit'),

            path('thankyou/', views.marks,name='thankyou'),
   path('room/<str:room>/', views.room, name='room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)