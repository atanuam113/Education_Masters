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
from .Add_admin_course import *


# --------------------------------Admin Section S T A R T -------------------------------------


@login_required(login_url='/loginpage/')
def admin_dashboard1(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    # --------================ Paging for Student ================--------
    allstudent_list = Student_Profile.objects.all()
    paginator1 = Paginator(allstudent_list, 1)  # 3 Student in each page
    page = request.GET.get('page1')
    try:
        allstudent_obj = paginator1.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allstudent_obj = paginator1.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allstudent_obj = paginator1.page(paginator1.num_pages)

    # --------================ Paging for Teacher ================--------
    allteacher_list = Teacher_Profile.objects.all()
    paginator2 = Paginator(allteacher_list, 1)  # 3 Student in each page
    page = request.GET.get('page2')
    try:
        allteacher_obj = paginator2.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allteacher_obj = paginator2.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allteacher_obj = paginator2.page(paginator2.num_pages)

    # --------================ Paging for Librarian ================--------
    all_librarian_list = Librarian_Profile.objects.all()
    paginator3 = Paginator(all_librarian_list, 1)  # 3 Student in each page
    page = request.GET.get('page3')
    try:
        all_librarian_obj = paginator3.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        all_librarian_obj = paginator3.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        all_librarian_obj = paginator3.page(paginator3.num_pages)

    # --------================ Paging for Course ================--------
    allcourse_list = Course_Detail.objects.all()
    paginator4 = Paginator(allcourse_list, 3)  # 3 Course in each page
    page = request.GET.get('page4')
    try:
        allcourse_obj = paginator4.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allcourse_obj = paginator4.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allcourse_obj = paginator4.page(paginator4.num_pages)

    # --------================ Paging for Events ================--------
    allevents_list = Events.objects.all()
    paginator5 = Paginator(allevents_list, 3)  # 6 Course in each page
    page5 = request.GET.get('page5')
    try:
        allevents_obj = paginator5.page(page5)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allevents_obj = paginator5.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allevents_obj = paginator5.page(paginator5.num_pages)
    
    NoOfCourses = Course_Detail.objects.count()
    NoOfStudents = Student_Profile.objects.count()
    NoOfEvents = Event_Register.objects.count()
    NoOfTeachers = Teacher_Profile.objects.count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'allstudent_obj':allstudent_obj,'allcourse_obj':allcourse_obj,'NoOfPendingBlog':NoOfPendingBlog,
    'allteacher_obj':allteacher_obj,'all_librarian_obj':all_librarian_obj,'allevents_obj':allevents_obj,
    'NoOfCourses':NoOfCourses,'NoOfStudents':NoOfStudents,'NoOfEvents':NoOfEvents,'NoOfTeachers':NoOfTeachers,
    'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    
    return render(request,'Admin_pannel/admindashboard.html',context)

@login_required(login_url='/loginpage/')
def admin_account_setting(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_account_setting.html',context)

@login_required(login_url='/loginpage/')
def Admin_Login_History(request):
    cuser = request.user
    obj_login = login_Log.objects.filter(LLog_User_PK=cuser).order_by('-LLog_Last_Login_Time')
    paginator = Paginator(obj_login, 10)  # 10 rows in each page
    page = request.GET.get('page')
    try:
        allLogin_obj = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allLogin_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allLogin_obj = paginator.page(paginator.num_pages)

    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]  
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count() 
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'obj_login':allLogin_obj,'TotalContactCount':TotalContactCount,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/Login_History.html',context)

@login_required(login_url='/loginpage/')
def admin_search(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    if request.method == "POST":
        text_str = request.POST['search_keyword']
        searched_course = Course_Detail.objects.filter(Course_Name__contains = text_str)
        searched_teacher = Teacher_Profile.objects.filter(Teacher_Name__contains = text_str)
        search_student = Student_Profile.objects.filter(Student_Name__contains = text_str)
        searched_event = Events.objects.filter(Event_Name__contains = text_str)
        searched_librarian = Librarian_Profile.objects.filter(Librarian_Name__contains = text_str)

        if searched_course:            
            context = {'searched_course':searched_course,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
           
        elif searched_teacher:            
            context = {'searched_teacher':searched_teacher,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
       
        elif search_student:                        
            context = {'search_student':search_student,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
           
        elif searched_event:            
            context = {'searched_event':searched_event,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
            
        elif searched_librarian:            
            context = {'searched_librarian':searched_librarian,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
        
        else:            
            context = {'text_str':text_str,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
        
    return render(request,'Admin_pannel/admin_search.html',context)



@login_required(login_url='/loginpage/')
def Admin_personal_details_edit(request,pk):    
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]  
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()           
    requested_userID = Admin_Profile.objects.get(pk=pk)
    form = Admin_Personal_Details(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Personal_Details(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
            Log_Admin = Admin_Profile.objects.get(pk=pk)
            Log_Name = Admin_Profile.objects.filter(pk=pk).values('Admin_Name')[0]['Admin_Name']
            Log_Email = Admin_Profile.objects.filter(pk=pk).values('Admin_Email')[0]['Admin_Email']
            Log_Phone  = Admin_Profile.objects.filter(pk=pk).values('Admin_Phone')[0]['Admin_Phone']
            Log_DOB  = Admin_Profile.objects.filter(pk=pk).values('Admin_DOB')[0]['Admin_DOB']
            Log_Address  = Admin_Profile.objects.filter(pk=pk).values('Admin_Address')[0]['Admin_Address']
            Log_Status  = Admin_Profile.objects.filter(pk=pk).values('Admin_Status')[0]['Admin_Status']
            Log_Bio  = Admin_Profile.objects.filter(pk=pk).values('Admin_Bio')[0]['Admin_Bio']
            Log_Git  = Admin_Profile.objects.filter(pk=pk).values('Admin_Github')[0]['Admin_Github']
            Log_LinkedIN  = Admin_Profile.objects.filter(pk=pk).values('Admin_Linkedin')[0]['Admin_Linkedin']
            Log_Twitter  = Admin_Profile.objects.filter(pk=pk).values('Admin_Twitter')[0]['Admin_Twitter']
            Log_Pic  = Admin_Profile.objects.filter(pk=pk).values('Admin_Profile_Pic')[0]['Admin_Profile_Pic']
            now = datetime.now()
            obj_Admin_Profile_Log = Admin_Profile_Log(APLog_Admin_PK=Log_Admin,APLog_Name=Log_Name
                                        ,APLog_Email = Log_Email,APLog_Phone = Log_Phone,APLog_DOB = Log_DOB
                                        ,APLog_Address = Log_Address,APLog_Status = Log_Status
                                        ,APLog_Bio =  Log_Bio
                                        ,APLog_Github = Log_Git
                                        ,APLog_Linkedin = Log_LinkedIN
                                        ,APLog_Twitter = Log_Twitter
                                        ,APLog_Profile_Pic = Log_Pic
                                        ,APLog_Updated_By = cuser
                                        ,APLog_Updated_Date = now)
            obj_Admin_Profile_Log.save()
            Email_subject = "Profile Details Change"
            Email_message = "Your profile is updated successfully."
            To_Email = [Log_Email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = To_Email
                                        ,Email_Receiver_Name = Log_Name,Email_subject = Email_subject
                                        ,Email_Message = Email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Profile Change",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()
            messages.success(request,' Your Personal Details is updated successfully !')
        return redirect('admin_account_setting')                    
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'form':form,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}

    return render(request,'Admin_pannel/Admin_personal_details_edit.html',context)

class admin_notification(LoginRequiredMixin,ListView):
	model = User
	template_name = 'Admin_pannel/admin_notification.html'
	# context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return User.objects.filter(is_active=False,Registered_As='None') 

@login_required(login_url='/loginpage/')
def admin_Pending_Blog(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objAllBlog = Blog.objects.filter(Blog_Active_Status = False)
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'objAllBlog':objAllBlog,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_Pending_Blog.html',context)

@login_required(login_url='/loginpage/')   
def admin_all_contact(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objAllContact = Contact_us.objects.all()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'objAllContact':objAllContact,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_contact.html',context)

@login_required(login_url='/loginpage/')
def admin_contact_response(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_contact_ID = Contact_us.objects.get(pk=pk)
    form = admin_contact_Reply(instance=requested_contact_ID)

    if request.method == 'POST':
        form = admin_contact_Reply(request.POST,instance=requested_contact_ID)
        if form.is_valid():
            form.save()
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S %Z")
            updated_by = Admin_Profile.objects.get(Admin_User_PK= cuser)
            contact_name = form.cleaned_data.get('Contact_Name')
            obj_Contact = Contact_us.objects.get(pk=pk)
            obj_Contact.Contact_Last_Updated_Date = dt_string
            obj_Contact.Contact_Last_Updated_By = updated_by
            obj_Contact.Contact_Effective_End_Date = None
            obj_Contact.Contact_Status = "Solved"
            obj_Contact.save()
            # ------=========================== Email Sending Information =============================-------------------
            to_email = Contact_us.objects.filter(pk=pk).values('Contact_Email')[0]['Contact_Email']
            to_email = [to_email]
            Contact_Name = Contact_us.objects.filter(pk=pk).values('Contact_Name')[0]['Contact_Name']
            email_Subject = "Contact Reply"
            email_message = "We have reply to your query. Please login to see our reply."
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = Contact_Name,Email_subject = email_Subject
                                        ,Email_Message = email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()
            messages.success(request," Your reply to "+ contact_name +" is sent successfully !")
            return redirect('admin_all_contact')
        else:
            messages.error(request,"Your reply is not sent successfully ! Please try again later !")
            return redirect('admin_all_contact')
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'form':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_contact_response.html',context)   

def admin_contact_view(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objContact = Contact_us.objects.filter(pk=pk)[0]
    form = admin_contact_Reply(instance=objContact)
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'objContact':objContact,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_contact_view.html',context)

@login_required(login_url='/loginpage/')
def admin_notification_details(request,pk):
    cuser = request.user
    now = datetime.now()
    obj_admin = Admin_Profile.objects.get(Admin_User_PK= cuser)
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()   
    requested_userID = User.objects.get(pk=pk)
    form = User_Registration_Request(instance=requested_userID)
    if request.method == 'POST':
        form = User_Registration_Request(request.POST,instance = requested_userID)
        user_type = form['Registered_As'].value()
        print(user_type)
        if(user_type == "None"):
            messages.error(request," Please select a user type !")
            return redirect('admin_notification')
        else:
            if form.is_valid():
                form.save()  
                first_name = form.cleaned_data.get('first_name') 
                last_name = form.cleaned_data.get('last_name')

                full_name = str(first_name)+' '+str(last_name)
                email = form.cleaned_data.get('email')
                user_DOB = form.cleaned_data.get('user_DOB')
                user_phone = form.cleaned_data.get('user_phone')
                user_status = "Active"
                UserAccount =  User.objects.get(pk=pk) 

                user_type = User.objects.filter(pk=pk).values('Registered_As')[0]['Registered_As']
                if(user_type == 'Student'):
                    student_obj = Student_Profile(Student_User_PK = UserAccount,Student_Name = full_name,Student_Email = email,Student_Phone = user_phone,Student_DOB = user_DOB,Student_Status = user_status)
                    student_obj.save()
                    userpk = student_obj.pk
                    Student_ID = 'STD' + str(userpk)
                    obj = Student_Profile.objects.get(pk = userpk)
                    obj.Student_ID = Student_ID
                    obj.save()
                elif(user_type == 'Teacher'):
                    Teacher_obj = Teacher_Profile(Teacher_User_PK=UserAccount,Teacher_Name = full_name,Teacher_Email = email,Teacher_Phone=user_phone,Teacher_DOB=user_DOB,Teacher_Status = user_status,Teacher_Address='None')
                    Teacher_obj.save()
                    teach_pk = Teacher_obj.pk
                    Teacher_ID = 'TECH'+ str(teach_pk)
                    obj = Teacher_Profile.objects.get(pk = teach_pk)
                    obj.Teacher_ID = Teacher_ID
                    obj.save()
            # Account Activation Email Link
            
            current_site = get_current_site(request)
            email_subject = "Verification Link for account activation"
            to_email = [email]

            email_messege = render_to_string('Admin_pannel/email_confirm.html',
            {
        
                'name' : full_name,
                'domain': current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(pk)),
                'token' : generate_token.make_token(requested_userID)
            })

            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                            ,Email_Receiver_Name = full_name,Email_subject = email_subject
                                            ,Email_Message = email_messege,Email_Delivery_Status = "Not Delivered"
                                            ,Email_Submission_Type = "Account Activation",Email_Created_By = cuser,Email_DateTime = now
                                            ,Email_Last_Updated_By = obj_admin,Email_Last_Update_Date = now)
            obj_email.save()
            
            # account_activation_link(email_subject,full_name,pk,to_email,requested_userID,request)
            messages.success(request,"Account activation link is sended !")
            return redirect('admin_notification')

    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'form':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_notification_details.html',context)


@login_required(login_url='/loginpage/')
def activate(request, uidb64, token):    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        UserAccount = User.objects.get(pk = uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        UserAccount = None

    if UserAccount is not None and generate_token.check_token(UserAccount,token):
        UserAccount.is_active = True
        UserAccount.save()
        auth.login(request,UserAccount)
        messages.success(request,"Your account is activated successfully !")
        return redirect('loginpage')
    else:
        return render(request,'Admin_pannel/activation_failed.html')


#-----------------------------Admin Course S T A R T ------------------------------
@login_required(login_url='/loginpage/')
def admin_add_course(request):
    cuser = request.user
    now = datetime.now()
    obj_admin = Admin_Profile.objects.get(Admin_User_PK= cuser)
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    allteacher_list = Teacher_Profile.objects.all()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,
               'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog
               ,'allteacher_list':allteacher_list}
    if request.method =="POST":
        # --------================ Data Insert Into Course Basic Information ================--------
        Course_Name = request.POST.get('Course_Name','')
        Course_Trainer_id = request.POST.get('Course_Trainer','')

        Start_Date = request.POST.get('Start_Date','')
        End_Date = request.POST.get('End_Date','')
        Course_Desc = request.POST.get('Course_Desc','')
        Course_Status = request.POST.get('Course_Status','')
        Course_Level = request.POST.get('Course_Level','')
        CourseBanner= request.FILES['CourseBanner']
        Course_Trainer = Teacher_Profile.objects.get(Teacher_ID = Course_Trainer_id)
        # -------==============Email Information For Teacher S T A R T ============------------------------
        Teacher_Email = Teacher_Profile.objects.filter(Teacher_ID = Course_Trainer_id).values('Teacher_Email')[0]['Teacher_Email']
        Teacher_name = Teacher_Profile.objects.filter(Teacher_ID = Course_Trainer_id).values('Teacher_Name')[0]['Teacher_Name']
        subject = "New course Teacher"
        message = "You are selected as a teacher for the new course "+ Course_Name +" . Please login to get more information about the course."
        to_email = [Teacher_Email]
        # -------==============Email Information For Teacher E N D ============------------------------
        
        if (Course_Detail.objects.filter(Course_Name = Course_Name)):
            messages.error(request," This Couse Name is aleady exist")            
        else:
            obj_course_basic_details = Course_Detail(Course_Name = Course_Name,Course_Instructor = Course_Trainer
                                                     ,Start_Date = Start_Date,End_Date = End_Date,Course_Desc = Course_Desc
                                                     ,Course_Status = Course_Status,CourseBanner = CourseBanner
                                                     ,Course_level = Course_Level)
            obj_course_basic_details.save()
            # --------================ Data Insert Into Course Syllabus ================--------
            menu_entries = request.POST.getlist('menu_syllabus')
            print("menu_module>>>",menu_entries)
            Admin_add_course_Syllabus(obj_course_basic_details,request)
            
            # for menu_entry in menu_entries:
            #     entry = menu_entry.split(",")
            #     lengths = len(entry)-1

            #     if(lengths == 0):
            #         messages.error(request," Please add course syllabus !")
            #     elif(lengths < 4):
            #         messages.error(request," Please fill the all columns")
            #     else:
            #         for i in range(0,lengths,4):
            #             NewArr = entry[i:i+4]
            #             if NewArr[0]:
            #                 module_name1 = str(NewArr[0])
            #             if NewArr[1]:
            #                 module_week = str(NewArr[1])
            #             if NewArr[2]:
            #                 module_topic = str(NewArr[2])
            #             if NewArr[3]:
            #                 module_desc = str(NewArr[3])
            #             obj_Course_Syllabus = Course_Syllabus(Course_Name = obj_course_basic_details,Module_Name = module_name1,Module_Week = module_week,Module_Topic = module_topic,Module_Description = module_desc,Module_Last_Updated_By = cuser,Module_Last_Update_Date = now)
            #             obj_Course_Syllabus.save()
            # --------================ Data Insert Into Course Module ================--------
            # course_modules = request.POST.getlist('menu_module')
            # for course_module in course_modules:
            #     entry1 = course_module.split(",")
            #     length1 = len(entry1) - 1
            #     if(length1 == 0):
            #         messages.error(request," Please add course Module !")
            #     elif(length1 < 2):
            #         messages.error(request," Please fill the all columns")
            #     else:
            #         for j in range(0,length1,2):
            #             NewArr1 = entry1[j:j+2]
            #             if NewArr1[0]:
            #                 module_topic = str(NewArr1[0])
            #             if NewArr1[1]:
            #                 Module_content = request.file[NewArr1[1]]
            
            # --------================ Data Insert Into Course Time Table ================--------
            # course_time_table = request.POST.getlist('menu_syllabus')
            # for course_time in course_time_table:
            #     entry1 = course_time.split(",")
            #     length2 = len(entry1)- 1
            #     if(length2 == 0):
            #         messages.error(request," Please add course Time table !")
            #     elif(length2 < 6):
            #         messages.error(request," Please fill the all columns")
            #     else:
            #         for k in range(0,length2,6):
            #             NewArr2 = entry1[k:k+6]                    
            #             if NewArr2[0]:
            #                 strDay = str(NewArr2[0])
            #             if NewArr2[1]:
            #                 strDate = str(NewArr2[1])
            #             if NewArr2[2]:
            #                 strStartTime = str(NewArr2[2])
            #             if NewArr2[3]:
            #                 strEndTime = str(NewArr2[3])
            #             if NewArr2[4]:
            #                 strTopic = str(NewArr2[4])
            #             if NewArr2[5]:
            #                 strClassLink = str(NewArr2[5])
            #             obj_course_time_table = Course_Time_Table(Course_Name = obj_course_basic_details,Class_Day = strDay
            #                                     ,Class_Date = strDate,Class_Start_Time = strStartTime
            #                                     ,Class_End_Time = strEndTime , Class_Topic= strTopic,Class_Link = strClassLink
            #                                     ,Class_Last_Updated_By = cuser,Class_Last_Update_Time = now)
            #             obj_course_time_table.save()
            # --------================ Data Insert Into Course Exam Table ================--------
            # course_Exam_table = request.POST.getlist('menu_exam')
            # for course_exam in course_Exam_table:
            #     entry = course_exam.split(",")
            #     length3 = len(entry) - 1
            #     if(length3 == 0):
            #         messages.error(request," Please add course Exam table !")
            #     elif(length3 < 5):
            #         messages.error(request," Please fill the all columns")
            #     else:
            #         for x in range(0,length3,5):
            #             NewArr3 = entry[x:x+5]
            #             if NewArr3[0]:
            #                 strExamName = str(NewArr3[0])
            #             if NewArr3[1]:
            #                 strExamDate = str(NewArr3[1])
                        
            #             if NewArr3[2]:
            #                 strExamStartTime = str(NewArr3[2])
            #             if NewArr3[3]:
            #                 strExamEndTime = str(NewArr3[3])
            #             if NewArr3[4]:
            #                 strExamLink = str(NewArr3[4])
            #             obj_Course_Exam_Table = Course_Exam_Table(Course_Name = obj_course_basic_details,Exam_Name = strExamName
            #                                     ,Exam_Date = strExamDate,Exam_Start_Time = strExamStartTime
            #                                     ,Exam_End_Time = strExamEndTime,Exam_Link = strExamLink
            #                                     ,Exam_Last_Updated_By = cuser,Exam_Last_Update_Time = now)
            #             obj_Course_Exam_Table.save()
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = Teacher_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Welcome Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = obj_admin,Email_Last_Update_Date = now)
            obj_email.save()
            # --------------------==================== Email send to all student S T A R T ==================----------
            objaddressbook_for_student = Student_Profile.objects.all()
            for ind_student in objaddressbook_for_student:
                subject = "New course "+Course_Name +" added !"
                message = "Please check out the newly added course "+Course_Name+" at Education Master."
                to_emailStd = [ind_student.Student_Email]
                to_name = ind_student.Student_Name
                obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = to_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = obj_admin,Email_Last_Update_Date = now)
                obj_email.save()
            # --------------------==================== Email send to all student E N D ==================----------
        messages.success(request," New Course is added successfully !")
        return redirect('admin_all_course')
    return render(request,'Admin_pannel/Admin_add_course.html',context)


# def admin_get_course_topic_dropdown(request):
#     cuser = request.user
#     now = datetime.now()
#     obj_admin = Admin_Profile.objects.get(Admin_User_PK= cuser)
#     TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
#     userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
#     NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
#     NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
#     allcourse_list = Course_Detail.objects.all()
#     Course_Name = request.GET.get('Course_Name')
#     objCourseTopic = Course_Syllabus.objects.filter(Course_Name=Course_Name)
#     context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,
#                'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog
#                ,'allcourse_list':allcourse_list,'objCourseTopic': objCourseTopic}
    
#     return render(request, 'Admin_pannel/admin_add_courrse_module.html', context)

def admin_add_course_module(request):
    cuser = request.user
    now = datetime.now()    
    obj_admin = Admin_Profile.objects.get(Admin_User_PK= cuser)
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    allcourse_list = Course_Detail.objects.all()
    objCourseTopic = Course_Syllabus.objects.none()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,
               'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog
               ,'allcourse_list':allcourse_list,'objCourseTopic': objCourseTopic}
    if request.method =="POST":
        Course_Name = request.POST.get('Course_Name','')
        print("Course_Name>>",Course_Name)
        Course_Topic = request.POST.get('Course_Topic','')
        CourseContent = request.FILES['CourseContent']
        obj_course_details = Course_Detail.objects.get(Course_Name = Course_Name)
        print(obj_course_details)
        objCourse_Module = Course_Module(Course_Name = obj_course_details,Module_Topic = Course_Topic,
                                    module_Content = CourseContent)
        objCourse_Module.save()
        return redirect('admin_all_course')
    return render(request,'Admin_pannel/admin_add_courrse_module.html',context)

@login_required(login_url='/loginpage/')
def admin_all_course(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    allcourse_obj = Course_Detail.objects.all()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'allcourse_obj':allcourse_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_course.html',context)

@login_required(login_url='/loginpage/')
def admin_course_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_course_details.html',context)


@login_required(login_url='/loginpage/')
def admin_course_module_list(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()

    requested_CourseID = Course_Detail.objects.get(pk=pk)
    requested_CourseName = Course_Detail.objects.filter(pk=pk)[0]
    ObjCourse_Module = Course_Module.objects.filter(Course_Name = requested_CourseID)

    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,
               'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog
               ,'ObjCourse_Module':ObjCourse_Module,'requested_CourseName':requested_CourseName}
    return render(request,'Admin_pannel/admin_course_module_list.html',context)

@login_required(login_url='/loginpage/')
def admin_course_module_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()

    requested_ModuleID = Course_Module.objects.get(pk=pk)
    requested_ModuleName = Course_Module.objects.filter(pk=pk)[0]
    form = Admin_Course_Module_edit(instance=requested_ModuleID)
    if request.method == 'POST':        
        form = Admin_Course_Module_edit(request.POST, request.FILES,instance = requested_ModuleID)
        if form.is_valid():
            form.save() 
        messages.success(request,"Course module is updated successfully !")
        return redirect('admin_all_course')

    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,
               'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog
               ,'ObjCourse_Module':form,'requested_ModuleID':requested_ModuleID}
    return render(request,'Admin_pannel/admin_course_module_details.html',context)
#-----------------------------Admin Course E N D ------------------------------


#----------------------------- Admin student S T A R T -----------------------------
@login_required(login_url='/loginpage/')
def admin_all_student(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    allstudent_obj = Student_Profile.objects.all()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'allstudent_obj':allstudent_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}    
    return render(request,'Admin_pannel/admin_all_student.html',context)

@login_required(login_url='/loginpage/')
def admin_add_student(request):
    cuser = request.user
    now = datetime.now()
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    if request.method =="POST":        
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        phoneNo= request.POST.get('phoneNo','')
        DateOfBirth= request.POST.get('dob','')
        address= request.POST.get('address','')
        profile_pic= request.FILES['profile_pic']
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        strCountry= request.POST.get('strCountry','')
        strState= request.POST.get('strState','')
        strcity= request.POST.get('strcity','')
        strZip= request.POST.get('strZip','')
        student_name = firstname +" "+ lastname

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.Registered_As = 'Student'
            UserAccount.save()
            userprofile = Student_Profile(Student_User_PK = UserAccount,Student_Name = student_name,Student_Email = email,Student_Phone = phoneNo,Student_DOB = DateOfBirth,Student_Address = address,Student_Status = 'Active',Student_Profile_Pic = profile_pic)
            userprofile.save()
            objaddressBook = Address_Book(AB_Party_Id = UserAccount,AB_Party_Type = 'Student'
                                        ,AB_Party_Address = address,AB_Party_City = strcity
                                        ,AB_Party_Name = student_name,AB_Party_Email = email
                                        ,AB_Party_State = strState,AB_Party_Country = strCountry
                                        ,AB_Party_Zip = strZip,AB_Party_phone = phoneNo
                                        ,AB_Last_Updated_By = cuser,AB_Last_Update_Date = now)
            objaddressBook.save()
            userpk = userprofile.pk
            Student_ID = 'STD' + str(userpk)
            obj = Student_Profile.objects.get(pk = userpk)
            obj.Student_ID = Student_ID
            obj.save()
            messages.success(request," You have successfully added the student !")
            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"            
            to_email = [UserAccount.email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = student_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Welcome Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()

            return redirect('admin_all_student')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_student.html',context)

@login_required(login_url='/loginpage/')
def admin_student_details(request,pk): 
    cuser = request.user
    request.session['pageIndicator'] = 'student'
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()           
    requested_userID = Student_Profile.objects.get(pk=pk)
    editeduser = Student_Profile.objects.filter(pk=pk).values('Student_Name')[0]['Student_Name']
    form = Admin_User_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_User_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
        Log_Student = Student_Profile.objects.get(pk=pk)
        Log_Name = Student_Profile.objects.filter(pk=pk).values('Student_Name')[0]['Student_Name']
        Log_Email = Student_Profile.objects.filter(pk=pk).values('Student_Email')[0]['Student_Email']
        Log_Phone  = Student_Profile.objects.filter(pk=pk).values('Student_Phone')[0]['Student_Phone']
        Log_DOB  = Student_Profile.objects.filter(pk=pk).values('Student_DOB')[0]['Student_DOB']
        Log_Address  = Student_Profile.objects.filter(pk=pk).values('Student_Address')[0]['Student_Address']
        Log_Status  = Student_Profile.objects.filter(pk=pk).values('Student_Status')[0]['Student_Status']
        Log_Bio  = Student_Profile.objects.filter(pk=pk).values('Student_Bio')[0]['Student_Bio']
        Log_Git  = Student_Profile.objects.filter(pk=pk).values('Student_Github')[0]['Student_Github']
        Log_LinkedIN  = Student_Profile.objects.filter(pk=pk).values('Student_Linkedin')[0]['Student_Linkedin']
        Log_Twitter  = Student_Profile.objects.filter(pk=pk).values('Student_Twitter')[0]['Student_Twitter']
        Log_Pic  = Student_Profile.objects.filter(pk=pk).values('Student_Profile_Pic')[0]['Student_Profile_Pic']
        now = datetime.now()
        obj_Student_Profile_Log = Student_Profile_Log(SPLOG_Student_PK=Log_Student,SPLOG_Name=Log_Name
                                    ,SPLOG_Email = Log_Email,SPLOG_Phone = Log_Phone,SPLOG_DOB = Log_DOB
                                    ,SPLOG_Address = Log_Address,SPLOG_Status = Log_Status
                                    ,SPLOG_Bio =  Log_Bio
                                    ,SPLOG_Github = Log_Git
                                    ,SPLOG_Linkedin = Log_LinkedIN
                                    ,SPLOG_Twitter = Log_Twitter
                                    ,SPLOG_Profile_Pic = Log_Pic
                                    ,SPLog_Updated_By = cuser
                                    ,SPLOG_Updated_Date = now)
        obj_Student_Profile_Log.save()
        Email_subject = "Profile Details Change"
        Email_message = "Your profile is updated successfully."
        To_Email = [Log_Email]
        obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = To_Email
                                        ,Email_Receiver_Name = Log_Name,Email_subject = Email_subject
                                        ,Email_Message = Email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Profile Change",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
        obj_email.save()
        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_student')               
     
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'objectid':pk,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_student_details.html',context)

@login_required(login_url='/loginpage/')
def admin_student_feedback(request,pk):
    cuser = request.user
    request.session['StudentId'] = pk
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objstudent = Student_Profile.objects.filter(Student_PK = pk)[0]
    obj_course_review = Course_review.objects.filter(Reviewer_Name = objstudent).exclude(Review_Status = 'Inactive').order_by('-Review_Date')
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'obj_course_review':obj_course_review,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_student_feedback.html',context)  

@login_required(login_url='/loginpage/')
def admin_student_feedback_details(request,pk):
    cuser = request.user
    studentId = request.session['StudentId']
    # request.session.pop('StudentId',None)
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_review = Course_review.objects.filter(Review_Id = pk)[0]
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'obj_review':obj_review,'studentId':studentId,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_student_feedback_details.html',context)

@login_required(login_url='/loginpage/')
def admin_student_feedback_delete(request,pk):
        now = datetime.now()
        Course_review.objects.filter(Review_Id=pk).update(Review_Effective_End_Date=now,Review_Status = 'Inactive')
        messages.success(request, ' The review is deleted successfully !')
        return redirect('admin_all_student')     

@login_required(login_url='/loginpage/')
def admin_student_course(request,pk):
    cuser = request.user
    request.session['StudentId'] = pk
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objstudent = Student_Profile.objects.filter(Student_PK = pk)[0]
    obj_student_course = course_registration.objects.filter(CR_Student = objstudent).order_by('-CR_DateTime')
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'NoOfPendingBlog':NoOfPendingBlog
            ,'TotalContactCount':TotalContactCount,'obj_student_course':obj_student_course
            ,'objstudent':objstudent}
    return render(request,'Admin_pannel/admin_student_course.html',context)  

@login_required(login_url='/loginpage/')
def admin_student_course_details(request,pk):
    cuser = request.user
    studentId = request.session['StudentId']
    objstudent = Student_Profile.objects.filter(Student_PK = studentId)[0]
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_student_course = course_registration.objects.filter(CR_ID = pk)[0]
    form = Admin_course_registration_edit(instance=obj_student_course)
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'NoOfPendingBlog':NoOfPendingBlog
            ,'TotalContactCount':TotalContactCount,'obj_student_course':obj_student_course
            ,'studentId':studentId,'objstudent':objstudent,'AllContext':form}
    
    if request.method == 'POST':        
        pk = request.POST.get('courseId','')
        obj_student_course = course_registration.objects.filter(CR_ID = pk)[0]
        course_name = obj_student_course.CR_Course
        form = Admin_course_registration_edit(request.POST,instance = obj_student_course)
        if form.is_valid():
            form.save() 
        messages.success(request,"The course "+ str(course_name) +"  is updated !")   
        return redirect('admin_all_student')
    
    return render(request,'Admin_pannel/admin_student_course_details.html',context)

@login_required(login_url='/loginpage/')
def admin_student_course_details_update(request):

    if request.method == 'POST':        
        pk = request.POST.get('courseId','')
        obj_student_course = course_registration.objects.filter(CR_ID = pk)[0]
        course_name = obj_student_course.CR_Course
        print(course_name)
        form = Admin_course_registration_edit(request.POST,instance = obj_student_course)
        if form.is_valid():
            form.save() 

        # messages.success(request," "+ str(edit_Blog) +" blog details is updated !")   
    return redirect('admin_all_student')

@login_required(login_url='/loginpage/')
def admin_student_blog(request,pk):
    cuser = request.user
    request.session['StudentId'] = pk
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objstudent = Student_Profile.objects.filter(Student_PK = pk)[0]
    obj_user = objstudent.Student_User_PK
    obj_student_blog = Blog.objects.filter(Blog_writer = obj_user).exclude(Blog_Status = 'Pending').order_by('-Blog_DateTime')
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'NoOfPendingBlog':NoOfPendingBlog
            ,'TotalContactCount':TotalContactCount,'obj_student_blog':obj_student_blog
            ,'objstudent':objstudent}
    return render(request,'Admin_pannel/admin_student_blog.html',context)

@login_required(login_url='/loginpage/')
def admin_student_blog_details(request,pk):
    cuser = request.user
    studentId = request.session['StudentId']
    objstudent = Student_Profile.objects.filter(Student_PK = studentId)[0]
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_student_Blog = Blog.objects.filter(Blog_Id = pk)[0]
    requested_BlogID = Blog.objects.get(pk=pk)
    blog_name = obj_student_Blog.Blog_Title
    form = Admin_Blog_edit(instance=obj_student_Blog)
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'NoOfPendingBlog':NoOfPendingBlog
            ,'TotalContactCount':TotalContactCount,'obj_student_Blog':obj_student_Blog
            ,'studentId':studentId,'objstudent':objstudent,'blog_name':blog_name,'AllContext':form}
    
    if request.method == 'POST':        
        pk = request.POST.get('courseId','')
        form = Admin_Blog_edit(request.POST, request.FILES,instance = requested_BlogID)
        if form.is_valid():
            form.save() 
        messages.success(request,"The Blog "+ str(blog_name) +" of "+str(objstudent.Student_Name) +" is updated !")   
        return redirect('admin_all_student')
    
    return render(request,'Admin_pannel/admin_student_blog_details.html',context)

@login_required(login_url='/loginpage/')
def user_email_send(request,pk):
    cuser = request.user
    pageindicator = request.session['pageIndicator']
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()  
    now = datetime.now()  
    Email_sender = settings.EMAIL_HOST_USER
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    if request.method == 'POST':
        if(pageindicator == 'student'):
            objstudent = Student_Profile.objects.filter(Student_PK = pk)
            to_email = objstudent.values('Student_Email')[0]['Student_Email']  
            name = objstudent.values('Student_Name')[0]['Student_Name']    
        elif(pageindicator == 'teacher'):
            objTeacher = Teacher_Profile.objects.filter(Teacher_PK = pk)
            to_email = objTeacher.values('Teacher_Email')[0]['Teacher_Email']  
            name = objTeacher.values('Teacher_Name')[0]['Teacher_Name']
        elif(pageindicator == 'librarian'):
            objLibrarian =  Librarian_Profile.objects.filter(Librarian_PK = pk)
            to_email = objLibrarian.values('Librarian_Email')[0]['Librarian_Email']  
            name = objLibrarian.values('Librarian_Name')[0]['Librarian_Name']
        elif(pageindicator == 'user'):
            objUser = Admin_Profile.objects.filter(Admin_PK = pk)
            to_email = objUser.values('Admin_Email')[0]['Admin_Email']  
            name = objUser.values('Admin_Name')[0]['Admin_Name']
            
        email_subject = request.POST.get('email_subject','')
        email_message = request.POST.get('email_body','')        
        filepath = request.FILES.get('email_file', False)
        if(filepath):
            email_file = request.FILES['email_file']
            to_email = [to_email]
            send_email_with_attachment(email_subject,email_message,to_email,name,email_file)
            objEmailTbl = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email,Email_Receiver_Name = name
                                        ,Email_Attachment = email_file
                                        ,Email_subject= email_subject,Email_Message = email_message,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            objEmailTbl.save()
            messages.success(request,"Email is send successfully to "+name)
            
        else:
            to_email = [to_email]
            objEmailTbl = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email,Email_Receiver_Name = name
                                        ,Email_subject= email_subject,Email_Message = email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Manual Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            objEmailTbl.save()
            messages.success(request,"Email is send successfully to "+name)        
        
        if(pageindicator == 'student'):
            return redirect('admin_all_student')
        elif(pageindicator == 'teacher'):
            return redirect('admin_all_teacher')
        elif(pageindicator == 'librarian'):
            return redirect('admin_all_librarian')
        elif(pageindicator == 'user'):
            return redirect('admin_all_user')
    request.session.pop('pageIndicator',None)

    return render(request,'Admin_pannel/user_email_send.html',context)
 
#----------------------------- Admin student E N D -----------------------------


#----------------------------- Admin Teacher S T A R T -----------------------------
@login_required(login_url='/loginpage/')
def admin_all_teacher(request):
    allteacher_obj = Teacher_Profile.objects.all()
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'allteacher_obj':allteacher_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}            
    return render(request,'Admin_pannel/admin_all_teacher.html',context)

@login_required(login_url='/loginpage/')
def admin_add_teacher(request):
    cuser = request.user
    now = datetime.now()
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    if request.method =="POST":            
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        phoneNo= request.POST.get('phoneNo','')
        DateOfBirth= request.POST.get('dob','')
        address= request.POST.get('address','')
        profile_pic= request.FILES['profile_pic']
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        strCountry= request.POST.get('strCountry','')
        strState= request.POST.get('strState','')
        strcity= request.POST.get('strcity','')
        strZip= request.POST.get('strZip','')
        Teacher_name = firstname +" "+ lastname

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:
            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.Registered_As = 'Teacher'
            UserAccount.save()            
            
            userprofile = Teacher_Profile(Teacher_User_PK = UserAccount,Teacher_Name = Teacher_name,Teacher_Email = email,Teacher_Phone = phoneNo,Teacher_DOB = DateOfBirth,Teacher_Address = address,Teacher_Status = 'Active',Teacher_Profile_Pic = profile_pic)
            userprofile.save()
            objaddressBook = Address_Book(AB_Party_Id = UserAccount,AB_Party_Type = 'Teacher'
                                        ,AB_Party_Address = address,AB_Party_City = strcity
                                        ,AB_Party_Name = Teacher_name,AB_Party_Email = email
                                        ,AB_Party_State = strState,AB_Party_Country = strCountry
                                        ,AB_Party_Zip = strZip,AB_Party_phone = phoneNo
                                        ,AB_Last_Updated_By = cuser,AB_Last_Update_Date = now)
            objaddressBook.save()
            userpk = userprofile.pk
            Teacher_ID = 'TECH' + str(userpk)
            obj = Teacher_Profile.objects.get(pk = userpk)
            obj.Teacher_ID = Teacher_ID
            obj.save()
            messages.success(request," You have successfully added the Teacher !")

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
            
            to_email = [UserAccount.email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = Teacher_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Welcome Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()
            return redirect('admin_all_teacher')
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_teacher.html',context)

@login_required(login_url='/loginpage/')
def admin_teacher_details(request,pk):
    cuser = request.user
    request.session['pageIndicator'] = 'teacher'
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_userID = Teacher_Profile.objects.get(pk=pk)
    editeduser = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Name')[0]['Teacher_Name']
    form = Admin_Teacher_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Teacher_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 

        Log_Teacher = Teacher_Profile.objects.get(pk=pk)
        Log_Name = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Name')[0]['Teacher_Name']
        Log_Email = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Email')[0]['Teacher_Email']
        Log_Phone  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Phone')[0]['Teacher_Phone']
        Log_DOB  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_DOB')[0]['Teacher_DOB']
        Log_Address  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Address')[0]['Teacher_Address']
        Log_Status  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Status')[0]['Teacher_Status']
        Log_Bio  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Bio')[0]['Teacher_Bio']
        Log_Git  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Github')[0]['Teacher_Github']
        Log_LinkedIN  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Linkedin')[0]['Teacher_Linkedin']
        Log_Twitter  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Twitter')[0]['Teacher_Twitter']
        Log_Pic  = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Profile_Pic')[0]['Teacher_Profile_Pic']
        now = datetime.now()
        obj_Teacher_Profile_Log = Teacher_Profile_Log(TPLog_Teacher_PK=Log_Teacher,TPLog_Name=Log_Name
                                    ,TPLog_Email = Log_Email,TPLog_Phone = Log_Phone,TPLog_DOB = Log_DOB
                                    ,TPLog_Address = Log_Address,TPLog_Status = Log_Status
                                    ,TPLog_Bio =  Log_Bio
                                    ,TPLog_Github = Log_Git
                                    ,TPLog_Linkedin = Log_LinkedIN
                                    ,TPLog_Twitter = Log_Twitter
                                    ,TPLog_Profile_Pic = Log_Pic
                                    ,TPLog_Updated_By = cuser
                                    ,TPLog_Updated_Date = now)
        obj_Teacher_Profile_Log.save()
        Email_subject = "Profile Details Change"
        Email_message = "Your profile is updated successfully."
        To_Email = [Log_Email]
        obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = To_Email
                                        ,Email_Receiver_Name = Log_Name,Email_subject = Email_subject
                                        ,Email_Message = Email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Profile Change",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
        obj_email.save()
        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_teacher')  
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'objectid':pk,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_teacher_details.html',context)

#----------------------------- Admin Teacher E N D -----------------------------


#----------------------------- Admin Librarian S T A R T -----------------------------

@login_required(login_url='/loginpage/')
def admin_all_librarian(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    all_librarian_obj = Librarian_Profile.objects.all()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'all_librarian_obj':all_librarian_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_librarian.html',context)

@login_required(login_url='/loginpage/')
def admin_add_librarian(request):
    cuser = request.user
    now = datetime.now()
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    if request.method =="POST":        
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        phoneNo= request.POST.get('phoneNo','')
        DateOfBirth= request.POST.get('dob','')
        address= request.POST.get('address','')
        profile_pic= request.FILES['profile_pic']
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        strCountry= request.POST.get('strCountry','')
        strState= request.POST.get('strState','')
        strcity= request.POST.get('strcity','')
        strZip= request.POST.get('strZip','')
        librarian_name = firstname +" "+ lastname

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.Registered_As = 'LibraryAdmin'
            UserAccount.save()
            messages.success(request," You have successfully added the librarian !")
            
            userprofile = Librarian_Profile(Librarian_User_PK = UserAccount,Librarian_Name = librarian_name,Librarian_Email = email,Librarian_Phone = phoneNo,Librarian_DOB = DateOfBirth,Librarian_Address = address,Librarian_Status = 'Active',Librarian_Profile_Pic = profile_pic)
            userprofile.save()
            objaddressBook = Address_Book(AB_Party_Id = UserAccount,AB_Party_Type = 'Librarian'
                                        ,AB_Party_Address = address,AB_Party_City = strcity
                                        ,AB_Party_Name = librarian_name,AB_Party_Email = email
                                        ,AB_Party_State = strState,AB_Party_Country = strCountry
                                        ,AB_Party_Zip = strZip,AB_Party_phone = phoneNo
                                        ,AB_Last_Updated_By = cuser,AB_Last_Update_Date = now)
            objaddressBook.save()
            userpk = userprofile.pk
            Librarian_ID = 'STD' + str(userpk)
            obj = Librarian_Profile.objects.get(pk = userpk)
            obj.Librarian_ID = Librarian_ID
            obj.save()

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
          
            to_email = [UserAccount.email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = librarian_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Welcome Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = UserAccount,Email_Last_Update_Date = now)
            obj_email.save()

            return redirect('admin_all_librarian')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")
            
    return render(request,'Admin_pannel/admin_add_librarian.html',context)

@login_required(login_url='/loginpage/')
def admin_librarian_details(request,pk):
    cuser = request.user
    request.session['pageIndicator'] = 'librarian'
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()

    requested_userID = Librarian_Profile.objects.get(pk=pk)
    editeduser = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Name')[0]['Librarian_Name']
    form = Admin_Librarian_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Librarian_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save()
            Log_Librarian = Librarian_Profile.objects.get(pk=pk)
            Log_Name = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Name')[0]['Librarian_Name']
            Log_Email = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Email')[0]['Librarian_Email']
            Log_Phone  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Phone')[0]['Librarian_Phone']
            Log_DOB  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_DOB')[0]['Librarian_DOB']
            Log_Address  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Address')[0]['Librarian_Address']
            Log_Status  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Status')[0]['Librarian_Status']
            Log_Bio  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Bio')[0]['Librarian_Bio']
            Log_Git  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Github')[0]['Librarian_Github']
            Log_LinkedIN  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Linkedin')[0]['Librarian_Linkedin']
            Log_Twitter  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Twitter')[0]['Librarian_Twitter']
            Log_Pic  = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Profile_Pic')[0]['Librarian_Profile_Pic']
            now = datetime.now()
            obj_Librarian_Profile_Log = Librarian_Profile_Log(LPLog_Librarian_PK=Log_Librarian,LPLog_Name=Log_Name
                                        ,LPLog_Email = Log_Email,LPLog_Phone = Log_Phone,LPLog_DOB = Log_DOB
                                        ,LPLog_Address = Log_Address,LPLog_Status = Log_Status
                                        ,LPLog_Bio =  Log_Bio
                                        ,LPLog_Github = Log_Git
                                        ,LPLog_Linkedin = Log_LinkedIN
                                        ,LPLog_Twitter = Log_Twitter
                                        ,LPLog_Profile_Pic = Log_Pic
                                        ,LPLog_Updated_By = cuser
                                        ,LPLog_Updated_Date = now)
            obj_Librarian_Profile_Log.save()
            Email_subject = "Profile Details Change"
            Email_message = "Your profile is updated successfully."
            To_Email = [Log_Email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = To_Email
                                        ,Email_Receiver_Name = Log_Name,Email_subject = Email_subject
                                        ,Email_Message = Email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Profile Change",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()
        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_librarian')               
     
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'form':form,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'objectid':pk,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_librarian_details.html',context)

#----------------------------- Admin Librarian E N D -----------------------------


#----------------------------- Admin User S T A R T -----------------------------
@login_required(login_url='/loginpage/')
def admin_all_user(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_All_User = Admin_Profile.objects.all()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'obj_All_User':obj_All_User,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_user.html',context)

@login_required(login_url='/loginpage/')
def admin_user_details(request,pk):
    cuser = request.user
    request.session['pageIndicator'] = 'user'
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_userID = Admin_Profile.objects.get(pk = pk)
    editeduser = Admin_Profile.objects.filter(pk=pk).values('Admin_Name')[0]['Admin_Name']
    form = Admin_Personal_Details(instance=requested_userID)
    if request.method == 'POST':
        form = Admin_Personal_Details(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save()
            Log_Admin = Admin_Profile.objects.get(pk=pk)
            Log_Name = Admin_Profile.objects.filter(pk=pk).values('Admin_Name')[0]['Admin_Name']
            Log_Email = Admin_Profile.objects.filter(pk=pk).values('Admin_Email')[0]['Admin_Email']
            Log_Phone  = Admin_Profile.objects.filter(pk=pk).values('Admin_Phone')[0]['Admin_Phone']
            Log_DOB  = Admin_Profile.objects.filter(pk=pk).values('Admin_DOB')[0]['Admin_DOB']
            Log_Address  = Admin_Profile.objects.filter(pk=pk).values('Admin_Address')[0]['Admin_Address']
            Log_Status  = Admin_Profile.objects.filter(pk=pk).values('Admin_Status')[0]['Admin_Status']
            Log_Bio  = Admin_Profile.objects.filter(pk=pk).values('Admin_Bio')[0]['Admin_Bio']
            Log_Git  = Admin_Profile.objects.filter(pk=pk).values('Admin_Github')[0]['Admin_Github']
            Log_LinkedIN  = Admin_Profile.objects.filter(pk=pk).values('Admin_Linkedin')[0]['Admin_Linkedin']
            Log_Twitter  = Admin_Profile.objects.filter(pk=pk).values('Admin_Twitter')[0]['Admin_Twitter']
            Log_Pic  = Admin_Profile.objects.filter(pk=pk).values('Admin_Profile_Pic')[0]['Admin_Profile_Pic']
            now = datetime.now()
            obj_Admin_Profile_Log = Admin_Profile_Log(APLog_Admin_PK=Log_Admin,APLog_Name=Log_Name
                                        ,APLog_Email = Log_Email,APLog_Phone = Log_Phone,APLog_DOB = Log_DOB
                                        ,APLog_Address = Log_Address,APLog_Status = Log_Status
                                        ,APLog_Bio =  Log_Bio
                                        ,APLog_Github = Log_Git
                                        ,APLog_Linkedin = Log_LinkedIN
                                        ,APLog_Twitter = Log_Twitter
                                        ,APLog_Profile_Pic = Log_Pic
                                        ,APLog_Updated_By = cuser
                                        ,APLog_Updated_Date = now)
            obj_Admin_Profile_Log.save()
            Email_subject = "Profile Details Change"
            Email_message = "Your profile is updated successfully."
            To_Email = [Log_Email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = To_Email
                                        ,Email_Receiver_Name = Log_Name,Email_subject = Email_subject
                                        ,Email_Message = Email_message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Profile Change",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()
            messages.success(request," "+ str(editeduser) + "'s personal details is updated !")
            return redirect('admin_all_user')
        else:
            messages.error(request," "+ str(editeduser) + "'s personal details is not updated !")
            return redirect('admin_all_user')
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'form':form,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'objectid':pk,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_user_details.html',context)

#----------------------------- Admin User E N D -----------------------------

#----------------------------- Admin Mails S T A R T ----------------------------

@login_required(login_url='/loginpage/')
def admin_all_mails(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_All_Mail = Email_Detail.objects.all()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'obj_All_Mail':obj_All_Mail,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_mails.html',context)


@login_required(login_url='/loginpage/')
def admin_add_mail(request):
    Email_sender =  os.environ.get('EMAIL_HOST_USER')
    cuser = request.user
    now = datetime.now()

    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()

    objUserList = User.objects.all()
    choiceList = []
    submission_type = [choice[1] for choice in Email_Detail._meta.get_field('Email_Submission_Type').choices]
   
    for object in objUserList:
        username = object.username
        choiceList.append(username)

    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg
               ,'objUserList':objUserList,'TotalContactCount':TotalContactCount
               ,'NoOfPendingBlog':NoOfPendingBlog,'choiceList':choiceList
               ,'submission_type':submission_type}

    # Save into Database
    if request.method == 'POST':
        mailReceiverName = request.POST.get('mailReceiverName','')
        MailSub = request.POST.get('MailSub','')
        mailBody = request.POST.get('mailBody','')
        MailType = request.POST.get('MailType','')
        MailStatus = request.POST.get('MailStatus','')
        if 'file_field_name' in request.FILES:
            MailAttachment = request.FILES['MailAttachment']

        if MailSub == '':
            messages.error(request," Please provide the Mail Subject !")
        else:
            UserObj = User.objects.get(username = mailReceiverName)
            receiverMail = UserObj.email
            print("receiverMail>>",receiverMail)
            receiverFirstName = UserObj.first_name
            receiverLastName = UserObj.last_name
            receiverFullName = receiverFirstName+" "+receiverLastName
            print("receiverFullName>>"+receiverFullName)

            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = receiverMail
                                        ,Email_Receiver_Name = receiverFullName,Email_subject = MailSub
                                        ,Email_Message = mailBody,Email_Delivery_Status = MailStatus
                                        ,Email_Submission_Type = MailType,Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Update_Date = now)
            if MailAttachment:
                obj_email.Email_Attachment = MailAttachment
            obj_email.save()
            messages.success(request," Mail is stored successfully !")
            return redirect('admin_all_mails')

    
    return render(request,'Admin_pannel/admin_add_mail.html',context)
    

@login_required(login_url='/loginpage/')
def admin_mail_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()

    requested_EmailID = Email_Detail.objects.get(pk=pk)
    edit_mail_receiver = Email_Detail.objects.filter(pk=pk).values('Email_Receiver_Name')[0]['Email_Receiver_Name']    
    form = Email_Detail_edit(instance=requested_EmailID)
    if request.method == 'POST':        
        form = Email_Detail_edit(request.POST, request.FILES,instance = requested_EmailID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(edit_mail_receiver) +" Email details is updated !")   
        return redirect('admin_all_mails')   
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_mail_details.html',context)



#----------------------------- Admin Mails E N D ----------------------------

#----------------------------- Admin Blogs S T A R T ----------------------------- 
@login_required(login_url='/loginpage/')
def admin_add_blog(request):
    cuser = request.user
    now = datetime.now()
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    if request.method =="POST":        
        BlogName= request.POST.get('BlogName','')
        BlogDesc= request.POST.get('BlogDesc','')
        BlogBanner= request.FILES['BlogBanner']
        obj_blog = Blog(Blog_Title = BlogName,Blog_writer = cuser,Blog_DateTime = now
                        ,Blog_Description = BlogDesc,Blog_Banner = BlogBanner
                        , Blog_Status = 'Active',Blog_Last_Update_Date = now)
        obj_blog.save()
        messages.success(request," Your Blog is uploaded successfully !")   
        return redirect('admin_all_blog')

    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_add_blog.html',context)

@login_required(login_url='/loginpage/')
def admin_all_blog(request):
    cuser = request.user
    now = datetime.now()
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_all_blog = Blog.objects.all().exclude(Blog_Status = 'Pending').order_by('-Blog_DateTime')
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'obj_all_blog':obj_all_blog,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_blog.html',context)

@login_required(login_url='/loginpage/')
def admin_blog_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_BlogID = Blog.objects.get(pk=pk)
    edit_Blog = Blog.objects.filter(pk=pk).values('Blog_Title')[0]['Blog_Title']    
    form = Admin_Blog_edit(instance=requested_BlogID)
    if request.method == 'POST':        
        form = Admin_Blog_edit(request.POST, request.FILES,instance = requested_BlogID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(edit_Blog) +" blog details is updated !")   
        return redirect('admin_all_blog')   
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_blog_details.html',context)

#----------------------------- Admin Blogs E N D ----------------------------- 

#----------------------------- Admin events S T A R T ----------------------------- 
@login_required(login_url='/loginpage/')
def admin_all_events(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    allevents_list = Events.objects.all().order_by('Event_ID')
    paginator = Paginator(allevents_list, 3)  # 6 Course in each page
    page = request.GET.get('page')
    try:
        allevents_obj = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allevents_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allevents_obj = paginator.page(paginator.num_pages)
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'allevents_obj':allevents_obj,'page':page,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_events.html',context)

@login_required(login_url='/loginpage/')
def admin_event_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_eventID = Events.objects.get(pk=pk)
    edit_event = Events.objects.filter(pk=pk).values('Event_Name')[0]['Event_Name']    
    form = Admin_Event_edit(instance=requested_eventID)
    if request.method == 'POST':        
        form = Admin_Event_edit(request.POST, request.FILES,instance = requested_eventID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(edit_event) +" event details is updated !")   
        return redirect('admin_all_events')               
    # AllContext.append([form])  
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'objectid':pk,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_event_details.html',context)

def admin_event_registered_user(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_eventID = Events.objects.get(pk=pk)
    event_reg_users = Event_Register.objects.filter(Event_ID = requested_eventID)
    print(event_reg_users)
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg
               ,'objectid':pk,'TotalContactCount':TotalContactCount
               ,'NoOfPendingBlog':NoOfPendingBlog,'event_reg_users':event_reg_users}
    return render(request,'Admin_pannel/admin_event_registered_user.html',context)

@login_required(login_url='/loginpage/')
def admin_add_event(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()  
    now = datetime.now()  
    Email_sender = settings.EMAIL_HOST_USER
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    if request.method =='POST':
        EventName=request.POST.get('EventName','')
        EventDesc = request.POST.get('EventDesc','')
        EventTopic = request.POST.get('EventTopic','')
        EventSDesc = request.POST.get('EventSDesc','')
        EventDept = request.POST.get('EventDept','')
        EventDate = request.POST.get('EventDate','')
        EventTime = request.POST.get('EventTime','')
        Eventlevel = request.POST.get('Eventlevel','')
        EventEndTime = request.POST.get('EventEndTime','')
        EventLink = request.POST.get('EventLink','')
        EventBanner = request.FILES['EventBanner']

        obj_event = Events(Event_Name = EventName,Event_Topic = EventTopic,Event_Short_Desc = EventSDesc,Event_Date = EventDate,Event_Time = EventTime,Event_Long_desc = EventDesc,Event_Dept = EventDept,Event_End_Time =EventEndTime,Event_Level = Eventlevel,Event_Link=EventLink,Event_Banner = EventBanner,Event_Status = "Active")
        obj_event.save()        
        # --------------------==================== Email send to all student S T A R T ==================----------
        if(Eventlevel == "Student"):
            objaddressbook_for_student = Student_Profile.objects.filter(Student_Status = "Active")
            for ind_student in objaddressbook_for_student:
                subject = "Education Master presents an event "+EventName +" ."
                message = "We are pleased to invite you to the event: "+EventName+". The event details are mentained below.\n You can register for the event by clicking the register now button.\n Event Date: "+ EventDate+" .\n Event Time: "+EventTime + " .\n Event location: "+ EventLink+" . \n Event Description: "+EventDesc+" ."
                            
                to_emailStd = [ind_student.Student_Email]
                to_name = ind_student.Student_Name
                obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = ind_student.Student_Email
                                        ,Email_Receiver_Name = to_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
                obj_email.save()
        # --------------------==================== Email send to all student E N D ==================----------

        # --------------------==================== Email send to all Teacher S T A R T ==================----------
        elif(Eventlevel == "Teacher"):
            objaddressbook_for_Teacher = Teacher_Profile.objects.all()
            for ind_Teacher in objaddressbook_for_Teacher:
                subject = "Education Master presents an event "+EventName +" ."
                message = "We are pleased to invite you to the event: "+EventName+". The event details are mentained below.\n You can register for the event by clicking the register now button.\n Event Date: "+ EventDate+" .\n Event Time: "+EventTime + " .\n Event location: "+ EventLink+" . \n Event Description: "+EventDesc+" ."
                            
                to_emailStd = [ind_Teacher.Teacher_Email]
                to_name = ind_Teacher.Teacher_Name
                obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = ind_Teacher.Teacher_Email
                                        ,Email_Receiver_Name = to_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
                obj_email.save()
        # --------------------==================== Email send to all Teacher E N D ==================----------
        
        # --------------------==================== Email send to all Librarian S T A R T ==================----------
        elif(Eventlevel == "Librarian"):
            objaddressbook_for_Librarian = Librarian_Profile.objects.all()
            for ind_Librarian in objaddressbook_for_Librarian:
                subject = "Education Master presents an event "+EventName +" ."
                message = "We are pleased to invite you to the event: "+EventName+". The event details are mentained below.\n You can register for the event by clicking the register now button.\n Event Date: "+ EventDate+" .\n Event Time: "+EventTime + " .\n Event location: "+ EventLink+" . \n Event Description: "+EventDesc+" ."
                            
                to_emailStd = [ind_Librarian.Librarian_Email]
                to_name = ind_Librarian.Librarian_Name
                obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = ind_Librarian.Librarian_Email
                                        ,Email_Receiver_Name = to_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
                obj_email.save()
        # --------------------==================== Email send to all Librarian E N D ==================----------
        
        # --------------------==================== Email send to all Admin S T A R T ==================----------
        elif(Eventlevel == "Admin"):
            objaddressbook_for_Admin = Admin_Profile.objects.all()
            for ind_Admin in objaddressbook_for_Admin:
                subject = "Education Master presents an event "+EventName +" ."
                message = "We are pleased to invite you to the event: "+EventName+". The event details are mentained below.\n You can register for the event by clicking the register now button.\n Event Date: "+ EventDate+" .\n Event Time: "+EventTime + " .\n Event location: "+ EventLink+" . \n Event Description: "+EventDesc+" ."
                            
                to_emailStd = [ind_Admin.Admin_Email]
                to_name = ind_Admin.Admin_Name
                obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = ind_Admin.Admin_Email
                                        ,Email_Receiver_Name = to_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
                obj_email.save()
        # --------------------==================== Email send to all Admin E N D ==================----------

        # --------------------==================== Email send to all General S T A R T ==================----------
        elif(Eventlevel == "General"):
            objaddressbook_for_General = Address_Book.objects.all()
            for ind_General in objaddressbook_for_General:
                subject = "Education Master presents an event "+EventName +" ."
                message = "We are pleased to invite you to the event: "+EventName+". The event details are mentained below.\n You can register for the event by clicking the register now button.\n Event Date: "+ EventDate+" .\n Event Time: "+EventTime + " .\n Event location: "+ EventLink+" . \n Event Description: "+EventDesc+" ."                            
                to_emailStd = [ind_General.AB_Party_Email]
                to_name = ind_General.AB_Party_Name
                obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = ind_General.AB_Party_Email
                                        ,Email_Receiver_Name = to_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
                obj_email.save()
            
        # --------------------==================== Email send to all General E N D ==================----------

        messages.success(request," Event is added successfully !")
        return redirect('admin_all_events')

    return render(request,'Admin_pannel/admin_add_event.html',context)

#----------------------------- Admin events S T A R T ----------------------------- 


#----------------------------- Admin Exam S T A R T ----------------------------- 
@login_required(login_url='/loginpage/')
def admin_all_exam(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_exam.html',context)

@login_required(login_url='/loginpage/')
def admin_add_exam(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_add_exam.html',context)

@login_required(login_url='/loginpage/')
def admin_exam_details(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_exam_details.html',context)

#----------------------------- Admin Exam E N D ----------------------------- 

#----------------------------- Admin ADD GROUP S T A R T ----------------------------- 
@login_required(login_url='/loginpage/')
def admin_all_groups(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_groups.html',context)

@login_required(login_url='/loginpage/')
def admin_add_group(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_add_group.html',context)

#----------------------------- Admin ADD GROUP E N D ----------------------------- 


#----------------------------- Admin Enquiry S T A R T ----------------------------- 
@login_required(login_url='/loginpage/')
def admin_all_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_all_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_course_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_course_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_admission_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_admission_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_seminar_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_seminar_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_event_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_event_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_common_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_common_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_view_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    NoOfPendingBlog = Blog.objects.filter(Blog_Active_Status = False).count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount,'NoOfPendingBlog':NoOfPendingBlog}
    return render(request,'Admin_pannel/admin_view_enquiry.html',context)
#----------------------------- Admin Enquiry S T A R T ----------------------------- 