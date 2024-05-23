from asyncio.windows_events import NULL
from email.errors import MessageError
import tempfile
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import *
from django.contrib import auth, messages
from Education_Master import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from . token import generate_token
from datetime import datetime
from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .mailserver import *
from Education_Master.settings import EMAIL_HOST_USER as Email_sender



@login_required(login_url='/loginpage/')
def teacher_dashboard(request):
    cuser = request.user    
    userprofile = Teacher_Profile.objects.filter(Teacher_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,"Teacher/teacher_dashboard.html",context)


@login_required(login_url='/loginpage/')
def Teacher_Login_History(request):
    cuser = request.user
    obj_login = login_Log.objects.filter(LLog_User_PK=cuser)   
    userprofile = Teacher_Profile.objects.filter(Teacher_User_PK=cuser)[0]   
    context = {'obj_login':obj_login,'userprofile':userprofile}
    return render(request,'Teacher/Login_History.html',context)