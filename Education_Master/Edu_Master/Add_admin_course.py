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
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def Admin_add_course_Syllabus(obj_course_basic_details,request):
    cuser = request.user
    now = datetime.now()
    menu_entries = request.POST.getlist('menu_entries')
    #menu_entries = json.loads(request.body)
    for menu_entry in menu_entries:
                entry = menu_entry.split(",")
                lengths = len(entry)-1

                if(lengths == 0):
                    messages.error(request," Please add course syllabus !")
                elif(lengths < 4):
                    messages.error(request," Please fill the all columns")
                else:
                    for i in range(0,lengths,4):
                        NewArr = entry[i:i+4]
                        if NewArr[0]:
                            module_name1 = str(NewArr[0])
                        if NewArr[1]:
                            module_week = str(NewArr[1])
                        if NewArr[2]:
                            module_topic = str(NewArr[2])
                        if NewArr[3]:
                            module_desc = str(NewArr[3])
                    # module_name1 = menu_entry.get('moduleName')  
                    # module_week =  menu_entry.get('moduleWeek')
                    # module_topic = menu_entry.get('moduleTopic')
                    # module_desc = menu_entry.get('moduleDesc')
                        # print("module_name1>>>"+module_name1)
                        # print("module_week>>>"+module_week)
                        # print("module_topic>>>"+module_topic)
                        # print("module_desc>>>"+module_desc)
                        obj_Course_Syllabus = Course_Syllabus(Course_Name = obj_course_basic_details,Module_Name = module_name1,Module_Week = module_week,Module_Topic = module_topic,Module_Description = module_desc,Module_Last_Updated_By = cuser,Module_Last_Update_Date = now)
                        obj_Course_Syllabus.save()
    Admin_add_course_time_table(obj_course_basic_details,request)



def Admin_add_course_module(obj_course_basic_details,request):  
    print("Admin_add_course_module call")  
    cuser = request.user
    now = datetime.now()
    course_modules = request.POST.getlist('menu_module')
    print("course_modules>>>>>>>>>>>>>>>",course_modules)
    for course_module in course_modules:
        entry1 = course_module.split(",")
        length1 = len(entry1) - 1
        if(length1 == 0):
            messages.error(request," Please add course Module !")
        elif(length1 < 2):
            messages.error(request," Please fill the all columns")
        else:
            for j in range(0,length1,2):
                NewArr1 = entry1[j:j+2]
                if NewArr1[0]:
                    module_topic = str(NewArr1[0])
                if NewArr1[1]:
                    Module_content = request.file[NewArr1[1]]
                print("module_topic New>>>"+module_topic)
                objCourse_Module = Course_Module(Course_Name = obj_course_basic_details,Module_Topic = module_topic,
                                    module_Content = Module_content)
                objCourse_Module.save()


def Admin_add_course_time_table(obj_course_basic_details,request): 
    print("Admin_add_course_time_table call")  
    cuser = request.user
    now = datetime.now()
    course_time_table = request.POST.getlist('menu_syllabus')
   # print("course_time_table>>>"+course_time_table)
    for course_time in course_time_table:
        entry1 = course_time.split(",")
        length2 = len(entry1)- 1
        if(length2 == 0):
            messages.error(request," Please add course Time table !")
        elif(length2 < 6):
            messages.error(request," Please fill the all columns")
        else:
            for k in range(0,length2,6):
                NewArr2 = entry1[k:k+6]                    
                if NewArr2[0]:
                    strDay = str(NewArr2[0])
                if NewArr2[1]:
                    strDate = str(NewArr2[1])
                if NewArr2[2]:
                    strStartTime = str(NewArr2[2])
                if NewArr2[3]:
                    strEndTime = str(NewArr2[3])
                if NewArr2[4]:
                    strTopic = str(NewArr2[4])
                if NewArr2[5]:
                    strClassLink = str(NewArr2[5])
                obj_course_time_table = Course_Time_Table(Course_Name = obj_course_basic_details,Class_Day = strDay
                                        ,Class_Date = strDate,Class_Start_Time = strStartTime
                                        ,Class_End_Time = strEndTime , Class_Topic= strTopic,Class_Link = strClassLink
                                        ,Class_Last_Updated_By = cuser,Class_Last_Update_Time = now)
                obj_course_time_table.save()