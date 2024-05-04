from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,  HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
import base64
from django.core.mail import send_mail
# from Main_App import  utility
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from fer import FER
# import cv2
from . import forms,models
# pass server cũ: ENup9tvWMi@2
from django.contrib.auth import login as auth_login
from datetime import datetime, timedelta, date
from django.views import generic
from .utility import Calendar
from .forms import EventForm
from django.utils.safestring import mark_safe
import calendar
# import google.generativeai as palm
from django.conf import settings

import google.generativeai as genai
import re
# Create your views here.
# add here to your generated API key
genai.configure(api_key="AIzaSyBLccnrIBeX4QpflJE1lKbSLleiv-MA6YA")

def room(request, room):
    username = request.GET.get('username')
    room_details = models.Room.objects.get(name=room)
    return render(request, 'patient/patientchatdirect.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(room, username):

    if models.Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = models.Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = models.Room.objects.get(name=room).id

    new_message = models.Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = models.Room.objects.get(name=room)

    messages = models.Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
def text_to_html_paragraphs(text):
    # First, replace multiple newlines with a single newline,
    # so you don't get empty paragraphs
    text = re.sub(r'\n\s*\n', '\n', text)

    # Split the text into lines
    lines = text.split('\n')

    # Wrap each line in a <p> tag and join them
    return ''.join(f'{line.strip()}\n<br>' for line in lines)


def gemini(request):
    text = request.GET.get('prompt')
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat()
    response = chat.send_message(text)
    user = request.user
    # Extract necessary data from response
    mess = text_to_html_paragraphs(response.text)
    return JsonResponse({"message":  mess})

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def comingsoon(request):
    if is_doctor(request.user):
        return render(request, 'commingsoon.html', {'event':models.Event.objects.all().count()}) 
    else:
        return render(request, 'soonpa.html', {'event':models.Event.objects.all().count()}) 

# Hiển thị giao diện lịch
class CalendarView(generic.ListView):
    model = models.Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, True)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event'] = models.Event.objects.all().count(),
        return context

class UnCalendarView(generic.ListView):
    model = models.Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, False)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event'] = models.Event.objects.all().count(),
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = models.Event()
    if event_id:
        instance = get_object_or_404(models.Event, pk=event_id)
    else:
        instance = models.Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        event = form.save()
        if is_doctor(request.user):
            event.status = True
            event.save()
            return redirect("/calendar")
        else:
            event.save()
            return redirect("/patient-calendar")
    if is_doctor(request.user):
        return render(request, 'event.html', {'form': form, 'event':models.Event.objects.all().count()})
    else:
        return render(request, 'paevent.html', {'form': form, 'event':models.Event.objects.all().count()})

# def recieve_login_face(request):
# Đang làm thêm
#     # photos = request.POST.getlist('photos[]')
#     # paths = []
#     # for i, photo in enumerate(photos):
#     #     ext, img = photo.split(';base64,')
        
#     #     ext = ext.split('/')[-1]
        
#     #     name = 'static/temp/rec' + str(i) + '.' + ext
#     #     fh = open(name, 'wb')
#     #     fh.write(base64.b64decode(img))
#     #     fh.close()
#     #     paths.append('static/temp/rec' + str(i) + '.' + ext)
#     #     emotion_detector = FER(mtcnn=True)
#     #     test_img = cv2.imread(name)
#     #     analysis = emotion_detector.detect_emotions(test_img)
#     #     dominant_emotion, emotion_score = emotion_detector.top_emotion(test_img)
#     #     print(dominant_emotion, emotion_score)
#     #     if emotion_score is not None:
#     #         score = emotion_score * 100
#     #     else: 
#     #         score = 0

#     # return JsonResponse({'id': 1, 'name': str(dominant_emotion), 'percentage': score})
#     return render(request,"login_face.html")

def login_face(request):
    return render(request,"login_face.html")


def data(request):
    return render(request,"data.html")

def chat(request):           
    return render(request,"chat.html",{'doctor':models.Doctor.objects.all()})

def patientchat(request):           
    return render(request,"patient/patientchat.html",{'doctor':models.Doctor.objects.all()})

def index(request):
    if request.method == 'POST':
            email = request.POST.get('email')
            name=request.POST.get('username')
            message = request.POST.get('message')
            date = request.POST.get('date')
            send_mail('Họ tên: '+str(name)+' || '+'Email: '+str(email)+' || '+'Thời gian: '+str(date)+'',message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
    return render(request, 'index.html')

def signup(request):
    form = forms.RegistrationForm()
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/choosing')
    return render(request, 'signup.html', {'form': form})

def login(request):

    if request.user.is_authenticated:
        pass
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            print("HSuuu")
            if user is not None:
                print("HSuuu")
                auth_login(request, user)
                print(is_doctor(user))
                if is_doctor(user):
                    return redirect("/doctormain")
                if is_patient(user):
                    return redirect("/patientmain")
                else:
                    return redirect("/choosing")
            

    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def start_exam_view(request):
    questions=models.Question.objects.all()
    if request.method=='POST':
        total_marks=0
        questions=models.Question.objects.all()
        questions_num=models.Question.objects.all().count()
        ans = []
        for i in range(questions_num):
            selected_ans = request.COOKIES.get(str(i+1))
            print(selected_ans)
            ans.append
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        result = models.Result()
        result.marks=total_marks
        if total_marks <= 12 and total_marks >= 10:
            print("Seasonal Affective Disorder")
            result.save()
            return redirect('/chat')
        questionone = request.COOKIES.get(str(1))
        questionten = request.COOKIES.get(str(10))
        questionseven = request.COOKIES.get(str(7))
        questionsix = request.COOKIES.get(str(6))
        questiontwelve = request.COOKIES.get(str(12))
        questiontwelve = request.COOKIES.get(str(11))
        if questionone == "Yes" and questionsix == "Yes" and questionten == "Yes" and questionseven == "Yes":
            print("Manic Depression")
            result.typeof = "Manic Depression"
            result.save()
            return redirect('/chat')
        if questionone == "Yes" and questionsix == "Yes" and questiontwelve == "Yes" and questiontwelve == "Yes" and questionten == "No" and questionseven == "No":
            print("Psychotic Depression")
            result.typeof = "Psychotic Depression"
            result.save()
            return redirect('/chat')
        else:
            result.typeof = "You are OK"
            result.save()
            return redirect('/thankyou')

    return render(request,'start_exam.html',{'questions':questions})


def marks(request):
    questions=models.Question.objects.all()
    result=models.Result.objects.all().last()
    return render(request,'score.html',{'questions':questions,'result':result})
# Create your views here.

@csrf_exempt
def choosing(request):
    if is_doctor(request.user):
        return redirect("/doctormain")
    if is_patient(request.user):
        return redirect("/doctormain")
    else:
        username = request.COOKIES.get("username")
        password = request.COOKIES.get("password")
        email = request.COOKIES.get("email")

    return render(request,'choice.html',{'username':username, 'email':email, 'password':password})

# def doctor_signup_view(request):
#     doctorForm=forms.doctorForm()
#     mydict={'doctorForm':doctorForm}
#     if request.method == 'POST':
#         form = forms.doctorForm(request.POST,request.FILES,instance=request.user)
#         if form.is_valid():
#             form.save()
#             my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
#             my_doctor_group[0].user_set.add(request.user)
#             print(my_doctor_group[0])
#         return HttpResponseRedirect('logout')
#     return render(request,'doctor/doctorsignup.html',context=mydict)

def doctor_signup_view(request):
    doctorForm=forms.doctorForm()
    mydict={'doctorForm':doctorForm}
    if request.method == 'POST':
        form = forms.doctorForm(request.POST,request.FILES)
        print("Hii")
        if form.is_valid():
            print("Hii")
            doctor=doctorForm.save(commit=False)
            doctor.user=request.user
            doctor.desc=request.POST.get("desc")
            doctor.address=request.POST.get("address")
            doctor.mobile=request.POST.get("mobile")
            doctor.profile_pic=request.FILES.get("profile_pic")
            doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(request.user)
            print(my_doctor_group[0])
        return HttpResponseRedirect('logout')
    return render(request,'doctor/doctorsignup.html',context=mydict)

def patient_signup_view(request):
    patientForm=forms.patientForm()
    mydict={'patientForm':patientForm}
    if request.method == 'POST':
        form = forms.patientForm(request.POST,request.FILES)
        print("Hii")
        if form.is_valid():
            print("Hii")
            patient=patientForm.save(commit=False)
            patient.user=request.user
            patient.desc=request.POST.get("desc")
            patient.mobile=request.POST.get("mobile")
            patient.profile_pic=request.FILES.get("profile_pic")
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(request.user)
            print(my_patient_group[0])
        return HttpResponseRedirect('logout')
    return render(request,'patient/patientsignup.html',context=mydict)



def doctormain(request):
    dict={
        'numpatient':models.Patient.objects.all().count(),
        'patient':models.Patient.objects.all(),
        'event':models.Event.objects.all().count(),

    }
    if is_doctor(request.user):
        pass
    else:
        return redirect("/")
            

    return render(request,'doctor/doctorpanel.html',context=dict)


def doctorpatient(request):
    dict={
        'numpatient':models.Patient.objects.all().count(),
        'patient':models.Patient.objects.all(),
        'event':models.Event.objects.all().count(),

    }
    if is_doctor(request.user):
        pass
    else:
        return redirect("/")
            

    return render(request,'doctor/doctorpatient.html',context=dict)


def acc(request):
    doctor = models.Doctor.objects.get(user=request.user)
    form = forms.doctorForm(instance=doctor)   
    user = User.objects.get(id=request.user.id)
    dict={'form': form,'user':user,'numpatient':models.Patient.objects.all().count(),
        'patient':models.Patient.objects.all(),
        'event':models.Event.objects.all().count(),}
    if request.method == 'POST':
        form = forms.doctorForm(request.POST, instance=request.user)
        if form.is_valid():
            doctor = form.save()
            doctor.user=request.user
            doctor.save()
            return HttpResponseRedirect('/doctormain')
    return render(request,'doctor/doctoraccount.html',context=dict)


def patientmain(request):
    dict={
        'numpatient':models.Doctor.objects.all().count(),
        'patient':models.Doctor.objects.all(),
        'event':models.Event.objects.all().count(),

    }
    if is_patient(request.user):
        pass
    else:
        return redirect("/")
            

    return render(request,'patient/patientpanel.html',context=dict)


def paevent(request, event_id=None):
    instance = models.Event()
    if event_id:
        instance = get_object_or_404(models.Event, pk=event_id)
    else:
        instance = models.Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return redirect('/patient-calendar')
    return render(request, 'paevent.html', {'form': form, 'event':models.Event.objects.all().count()})


def patient_view_doctor(request,pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctorForm = forms.doctorForm(instance=doctor)
    if request.method == "POST":
        star = 0
        for i in range(6):
            checked = request.COOKIES.get(f"rating-{i}")
            if checked:
                doctor.timeclick += 1
                star = i
                print(star)
        doctor.star = star
        doctor.save()
        return HttpResponseRedirect(f'/patient-doctor/{pk}')
    return render(
        request=request,
        template_name='patient/doctor_contact.html',
        context={"doctor": doctor, "doctorForm":doctorForm}
        )


class PatientCalendarView(generic.ListView):
    model = models.Event
    template_name = 'patientcalendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, True)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event'] = models.Event.objects.all().count(),
        return context


class PaUnAccept(generic.ListView):
    model = models.Event
    template_name = 'patientcalendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, False)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event'] = models.Event.objects.all().count(),
        return context