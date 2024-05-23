from asyncio.windows_events import NULL
import logging
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
from django.utils import timezone
from Education_Master.settings import EMAIL_HOST_USER as Email_sender



# ------------------------------------------------Authentication Section------------------------------------------------
def Valid_User_check(user):
    sessionUserName = request.session['UserNameSession']
    if user.username == sessionUserName:
        return True
    else:
        return False

def register(request):
    if request.method =="POST":
        now = datetime.now()        
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        user_DOB= request.POST.get('user_DOB','')
        user_phone= request.POST.get('user_phone','')

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
            UserAccount.user_DOB = user_DOB
            UserAccount.user_phone = user_phone
            UserAccount.is_active = False
            UserAccount.Registered_As = 'None'
            UserAccount.save()
            
            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Welcome to Education_Master!! \nThank you for visiting our website.\n We will sent you account activation link once your details will be verified."
            # form_email = settings.EMAIL_HOST_USER
            user_name = UserAccount.first_name
            to_email = [UserAccount.email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = user_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Welcome Email",Email_Created_By = UserAccount,Email_DateTime = now
                                        ,Email_Last_Update_Date = now)
            obj_email.save()
            messages.success(request," Your Account has been created succesfully!! Please check your email to get all information !")
            return redirect('loginpage')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")


    return render(request,'Edu_Master/register.html')

def login(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            logger.warning("Logging Successfully")
            user.user_live_status = True
            user.save()
            request.session['UserNameSession'] = username
            cuser = request.user
            now = datetime.now()
            obj_Login_Log = login_Log(LLog_User_PK = cuser,LLog_Last_Login_Time = now)
            obj_Login_Log.save()  
            print("Login:"+user.Registered_As);          
            if user.Registered_As=='Admin' or user.is_superuser:
                return redirect('admin_dashboard1')
            elif user.Registered_As =='Student':
                return redirect('home')		
            elif user.Registered_As =='LibraryAdmin':
                return redirect('librarian_dashboard')
            	
            elif user.Registered_As =='Teacher':
                return redirect('teacher_dashboard')
            	
            else:
                messages.error(request, " Invalid username or password !")
                return redirect('login')
        else:
            messages.error(request, " Invalid username or passwords !")

    return render(request,'Edu_Master/login.html')

def LoginWithOTP(request):
    return render(request,'Edu_Master/LoginWithOTP.html')

@login_required(login_url='/loginpage/')
def LogOut(request):
    cuser = request.user
    now = datetime.now()
    user_obj = login_Log.objects.filter(LLog_User_PK=cuser,LLog_Effective_End_Date__isnull = True).update(LLog_LogOut_Time = now,LLog_Effective_End_Date = now)
    cuser.user_live_status = False
    cuser.save()
    logout(request)
    return redirect("login")


def forgotpass(request):
    return render(request,'Edu_Master/forgotpass.html')
# ------------------------------------------------Student Section------------------------------------------------
@login_required(login_url='/loginpage/')
def home(request):
    cuser = request.user   
    print("cuser: "+str(cuser)) 
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    HighRatedCourse = Course_Detail.objects.filter(Course_Rating__gte=4.5)[:5]
    contextItem = {'userprofile':userprofile,'HighRatedCourse':HighRatedCourse}
    return render(request,'Edu_Master/Index.html',contextItem)

@login_required(login_url='/loginpage/')
def student_search(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    if request.method == "POST":
        text_str = request.POST['search_keyword']        
        searched_course = Course_Detail.objects.filter(Course_Name__contains = text_str)
        searched_event = Events.objects.filter(Event_Name__contains = text_str)

        if searched_course:
            context = {'userprofile':userprofile,'searched_course':searched_course}
        elif searched_event:
            context = {'userprofile':userprofile,'searched_event':searched_event}
        else:
            context = {'userprofile':userprofile,'text_str':text_str}
        
    return render(request,'Edu_Master/student_search.html',context)

@login_required(login_url='/loginpage/')
def student_dashboard(request):
    cuser = request.user    
    today = date.today()
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_course_register = course_registration.objects.filter(CR_Student = userprofile)
    obj_course_registerForList = course_registration.objects.filter(CR_Student = userprofile,CR_Status = 'Active')
    course_list = []
    for i in obj_course_registerForList:
        obj_course = i.CR_Course
        course_list.append(obj_course)
        
    obj_course_table = Course_Time_Table.objects.filter(Course_Name__in = course_list).order_by('Class_Date')   
    
    contextItem = {'userprofile':userprofile,'item':userprofile,'obj_course_register':obj_course_register,'obj_course_table':obj_course_table,'today':today}

    return render(request,'Edu_Master/student_dashboard.html',contextItem)

@login_required(login_url='/loginpage/')
def student_profile(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    return render(request,'Edu_Master/student_profile.html',contextItem)

@login_required(login_url='/loginpage/')
def student_course(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    # AllCourse = Course_Detail.objects.all()
    obj_course_register = course_registration.objects.filter(CR_Student = userprofile)
    contextItem = {'userprofile':userprofile,'item':userprofile,'obj_course_register':obj_course_register}
    return render(request,'Edu_Master/student_course.html',contextItem)

@login_required(login_url='/loginpage/')
def student_exam(request):
    cuser = request.user   
    today = date.today() 
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_course_register = course_registration.objects.filter(CR_Student = userprofile,CR_Status = 'Active')
    course_list = []
    for i in obj_course_register:
        obj_course = i.CR_Course
        course_list.append(obj_course)
    obj_Course_Exam_Table = Course_Exam_Table.objects.filter(Course_Name__in = course_list).order_by('Exam_Date')   
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile,'obj_Course_Exam_Table':obj_Course_Exam_Table,'today':today}
    return render(request,'Edu_Master/student_exam.html',contextItem)

@login_required(login_url='/loginpage/')
def student_class_time(request):
    cuser = request.user    
    today = date.today()
    now = datetime.now()
    One_Hour_Ago_Time = now + timezone.timedelta(minutes=15)
    print(One_Hour_Ago_Time)
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_course_register = course_registration.objects.filter(CR_Student = userprofile,CR_Status = 'Active')
    course_list = []
    for i in obj_course_register:
        obj_course = i.CR_Course
        course_list.append(obj_course)
        
    obj_course_table = Course_Time_Table.objects.filter(Course_Name__in = course_list).order_by('Class_Date')   
    contextItem = {'userprofile':userprofile,'item':userprofile,'obj_course_table':obj_course_table,'today':today,'One_Hour_Ago_Time':One_Hour_Ago_Time,'now':now}
    return render(request,'Edu_Master/student_class_time.html',contextItem)


@login_required(login_url='/loginpage/')
def student_notification(request):
    cuser = request.user    
    UserObj = User.objects.get(username = cuser)
    receiverMail = UserObj.email
    today = date.today()
    now = datetime.now()
    One_Hour_Ago_Time = now + timezone.timedelta(minutes=15)
    print(One_Hour_Ago_Time)
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_Student_Mail = Email_Detail.objects.filter(Email_Receiver = receiverMail,Email_Submission_Type = 'Manual Email')
    
    contextItem = {'userprofile':userprofile,'item':userprofile,'obj_Student_Mail':obj_Student_Mail,'today':today,'One_Hour_Ago_Time':One_Hour_Ago_Time,'now':now}
    return render(request,'Edu_Master/student_notification.html',contextItem)

@login_required(login_url='/loginpage/')
def Subcribed_course(request,pk):
    cuser = request.user    
    UserObj = User.objects.get(username = cuser)
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    objCourseDtls = Course_Detail.objects.filter(Course_ID = pk)[0]
    obj_course_register = course_registration.objects.filter(CR_Course = objCourseDtls,CR_Student = userprofile,CR_Status = 'Active')
    if(obj_course_register):
        objCourseModule = Course_Module.objects.filter(Course_Name = objCourseDtls)
        print(objCourseModule)
        receiverMail = UserObj.email
        today = date.today()
        now = datetime.now()
        One_Hour_Ago_Time = now + timezone.timedelta(minutes=15)
    else:
        messages.error(request," Your are not subscribed the course !")
        return redirect('student_dashboard')
    
    obj_Student_Mail = Email_Detail.objects.filter(Email_Receiver = receiverMail,Email_Submission_Type = 'Manual Email')
    
    contextItem = {'userprofile':userprofile,'item':userprofile,
                   'obj_Student_Mail':obj_Student_Mail,'today':today,
                   'One_Hour_Ago_Time':One_Hour_Ago_Time,'now':now
                   ,'objCourseModule':objCourseModule,'objCourseDtls':objCourseDtls}
    return render(request,'Edu_Master/Subcribed_course.html',contextItem)

@login_required(login_url='/loginpage/')
def student_notification_detail(request,pk):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_notification = Email_Detail.objects.filter(pk = pk)[0]
    #obj_notification = Email_Detail_view(instance=pk)
    context = {'userprofile':userprofile,'item':userprofile,'AllContext':obj_notification}
    return render(request,'Edu_Master/student_notification_detail.html',context)

@login_required(login_url='/loginpage/')
def student_Profile_Edit(request,slug):
    AllContext = []
    cuser = request.user    
    item = Student_Profile.objects.filter(Student_User_PK=cuser)[0]            
    requested_userID = Student_Profile.objects.get(slug=slug)
    form = User_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = User_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
            messages.success(request," Your personal details is updated successfully !")
        return redirect('student_dashboard')               
    AllContext.append([item,form])  
    context = {'AllContext':AllContext,'item':item}
    return render(request,'Edu_Master/student_Profile_Edit.html',context)

@login_required(login_url='/loginpage/')
def about(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/about.html',context)

@login_required(login_url='/loginpage/')
def award(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/award.html',context)

@login_required(login_url='/loginpage/')
def research(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/research.html',context)

@login_required(login_url='/loginpage/')
def facilities(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/facilities.html',context)
   
@login_required(login_url='/loginpage/')
def facilities_detail(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/facilities_detail.html',context)

@login_required(login_url='/loginpage/')
def departments(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/departments.html',context)

@login_required(login_url='/loginpage/')
def all_course(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    allcourse = Course_Detail.objects.all().order_by('Course_ID')
    paginator = Paginator(allcourse, 2)  # 6 Course in each page
    page = request.GET.get('page')
    try:
        course_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        course_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        course_list = paginator.page(paginator.num_pages)


    context = {'userprofile':userprofile,'course_list':course_list,'page':page}
    return render(request,'Edu_Master/all_course.html',context)

@login_required(login_url='/loginpage/')
def seminar(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/seminar.html',context)

@login_required(login_url='/loginpage/')
def course_details(request,slug):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    objcourse = Course_Detail.objects.filter(slug = slug)[0]
    obj_course_review = Course_review.objects.filter(Reviewed_Course = objcourse).exclude(Review_Status = 'Inactive').order_by('-Review_Date')
    obj_course_register = course_registration.objects.filter(CR_Course = objcourse)
    context = {'userprofile':userprofile,'objcourse':objcourse
                ,'obj_course_review':obj_course_review,'obj_course_register':obj_course_register}
    return render(request,'Edu_Master/course_details.html',context)

@login_required(login_url='/loginpage/')
def course_register(request):
    cuser = request.user    
    now = datetime.now()
    if request.method == 'POST':
        course_id = request.POST.get('courseId','')
        obj_course = Course_Detail.objects.filter(Course_ID = course_id)[0]
        obj_student = Student_Profile.objects.get(Student_User_PK = cuser)
        if course_registration.objects.filter(CR_Student = obj_student,CR_Course = obj_course).exists():
            messages.error(request," You have already registered in this course !")
            return redirect('all_course')
        else:
            obj_course_register = course_registration(CR_Student = obj_student,CR_Course = obj_course
                                                    ,CR_Status = 'De-active',CR_DateTime = now,CR_Last_Updated_Date = now
                                                    ,CR_Last_Updated_By = cuser)
            obj_course_register.save()
            messages.success(request," You are successfully applied to this course.")
            return redirect('all_course')
        

@login_required(login_url='/loginpage/')
def course_review(request):
    cuser = request.user    
    now = datetime.now()
    if request.method == 'POST':
        course_id = request.POST.get('courseId','')
        obj_course = Course_Detail.objects.filter(Course_ID = course_id)[0]
        obj_student = Student_Profile.objects.get(Student_User_PK = cuser)
        review_msg = request.POST.get('ReviewMsg','')
        objcourse_review = Course_review(Reviewer_Name = obj_student,Reviewed_Course = obj_course
                                        ,Review_Date = now,Review_message = review_msg
                                        ,Review_Status = "Active",Review_Last_Updated_Date = now)

        objcourse_review.save()
        messages.success(request," Your review is submitted successfully.")
        return redirect('all_course')

@login_required(login_url='/loginpage/')
def blog(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_all_blog = Blog.objects.all().exclude(Blog_Status = 'Pending').order_by('-Blog_DateTime')
    paginator = Paginator(obj_all_blog, 3)  # 3 blog in each page
    page = request.GET.get('page')
    try:
        blog_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        blog_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        blog_list = paginator.page(paginator.num_pages)
    context = {'userprofile':userprofile,'obj_all_blog':blog_list,'page':page}
    return render(request,'Edu_Master/blog.html',context)

@login_required(login_url='/loginpage/')
def blog_details(request,slug):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    obj_blog = Blog.objects.filter(slug = slug)[0]
    obj_Blog_Review = Blog_Review.objects.filter(Reviewed_Blog = obj_blog).exclude(Review_Status = 'Inactive').order_by('-Review_Date')    
    context = {'userprofile':userprofile,'obj_blog':obj_blog,'obj_Blog_Review':obj_Blog_Review}
    return render(request,'Edu_Master/blog_details.html',context)

@login_required(login_url='/loginpage/')
def blog_review(request):
    cuser = request.user    
    now = datetime.now()
    if request.method == 'POST':
        blogId = request.POST.get('blogId','')
        obj_blog = Blog.objects.filter(Blog_Id = blogId)[0]
        obj_student = Student_Profile.objects.get(Student_User_PK = cuser)
        review_msg = request.POST.get('ReviewMsg','')
        objBlog_Review = Blog_Review(Reviewer_Name = obj_student,Reviewed_Blog = obj_blog
                                        ,Review_Date = now,Review_message = review_msg
                                        ,Review_Status = "Active",Review_Last_Updated_Date = now)

        objBlog_Review.save()
        messages.success(request," Your review is submitted successfully.")
        return redirect('blog')

@login_required(login_url='/loginpage/')
def student_blog(request):
    cuser = request.user    
    now = datetime.now()
    obj_blog = Blog.objects.filter(Blog_writer = cuser).exclude(Blog_Status = 'Pending')   
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile,'obj_blog':obj_blog,'item':userprofile}
    return render(request,'Edu_Master/student_blog.html',context)    

@login_required(login_url='/loginpage/')
def student_add_blog(request):
    cuser = request.user    
    now = datetime.now()
    obj_blog = Blog.objects.filter(Blog_writer = cuser)    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    if request.method =="POST":        
        BlogName= request.POST.get('BlogName','')
        BlogDesc= request.POST.get('BlogDesc','')
        BlogBanner= request.FILES['BlogBanner']
        obj_blog = Blog(Blog_Title = BlogName,Blog_writer = cuser,Blog_DateTime = now
                        ,Blog_Description = BlogDesc,Blog_Banner = BlogBanner
                        , Blog_Status = 'Pending',Blog_Last_Update_Date = now)
        obj_blog.save()
        messages.success(request," Your Blog is uploaded successfully !")   
        return redirect('student_blog')

    context = {'userprofile':userprofile,'obj_blog':obj_blog,'item':userprofile}
    return render(request,'Edu_Master/student_add_blog.html',context) 

@login_required(login_url='/loginpage/')
def student_login_history(request):
    cuser = request.user    
    now = datetime.now()  
    student_login_log = login_Log.objects.filter(LLog_User_PK=cuser).order_by('-LLog_Last_Login_Time')
    paginator = Paginator(student_login_log, 10)  # 10 records in each page
    page = request.GET.get('page')
    try:
        login_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        login_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        login_list = paginator.page(paginator.num_pages)
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile,'item':userprofile,'student_login_log':login_list,'page':page}
    return render(request,'Edu_Master/student_login_history.html',context)

    
@login_required(login_url='/loginpage/')
def event(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    event_obj = Events.objects.all().order_by('Event_ID')
    paginator = Paginator(event_obj, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    context = {'userprofile':userprofile,'page':page,'post_list':post_list}
    return render(request,'Edu_Master/event.html',context)

@login_required(login_url='/loginpage/')
def event_details(request,slug):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = Events.objects.get(slug=slug)
    contextDict = {'item':context,'userprofile':userprofile}
    return render(request,'Edu_Master/event_details.html',contextDict)

@login_required(login_url='/loginpage/')
def event_register(request,slug):
    item = Events.objects.filter(slug = slug)[0]    
    AllContext = []
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    
    AllContext.append([item,userprofile])
    contextDict = {'AllContext':AllContext,'userprofile':userprofile}
    now = datetime.now()
    dt_string = now.strftime("YYYY-MM-DD HH:MM")

    if request.method =="POST":
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        Eventid = Events.objects.get(slug = slug)        
        if Event_Register.objects.filter(Student_PK = Student_pk,Event_ID = Eventid).exists():
            messages.error(request," You have already registered in this events !")
            return redirect('event')
        else:
            register_result = Event_Register()
            register_result.save()
            register_result.Event_ID.add(Eventid)
            register_result.Student_PK.add(Student_pk)
            userpk = register_result.pk
            
            obj = Event_Register.objects.get(pk = userpk)
            obj.Registration_Date = dt_string
            obj.save()
            messages.success(request," You have successfully registered for this events.")
            return redirect('event')
    
    return render(request,'Edu_Master/event_register.html',contextDict)

@login_required(login_url='/loginpage/')
def all_trainer(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    objAllTrainer = Teacher_Profile.objects.all()
    context = {'userprofile':userprofile,'objAllTrainer':objAllTrainer}
    return render(request,'Edu_Master/all_trainer.html',context)

@login_required(login_url='/loginpage/')
def contact_us(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        c_name= request.POST.get('Contact_Name','')
        c_email= request.POST.get('Contact_Email','')
        c_message= request.POST.get('Contact_Message','')
        contactus = Contact_us(Contact_Name=c_name,Contact_Email=c_email,Contact_Message=c_message)
        
        contactus.save()
        messages.success(request," Your message is send successfully !")

    return render(request,'Edu_Master/contact_us.html',context)

@login_required(login_url='/loginpage/')
def Feedback(request):
    cuser = request.user  
    now = datetime.now()  
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        c_message= request.POST.get('feedback_message','')
        F_File = request.FILES['feedback_attachment']
        contactus = User_Feedback(Feedback_Updated_By=cuser,Feedback_Text=c_message
        ,Feedback_attachment = F_File
        ,Feedback_Date = now,Feedback_staus = "Active",Feedback_Updated_Date = now)
        
        contactus.save()
        return redirect('home')
        messages.success(request," Your feedback is send successfully !")

    return render(request,'Edu_Master/Feedback.html',context)



@login_required(login_url='/loginpage/')
def error_404_view(request,exception):
    return render(request,'Edu_Master/error_404_view.html')