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



# ------------------------------------------------Digital Library------------------------------------------------
@login_required(login_url='/loginpage/')
def Library_Login_History(request):
    cuser = request.user
    obj_login = login_Log.objects.filter(LLog_User_PK=cuser)
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]  
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count() 
    context = {'obj_login':obj_login,'TotalContactCount':TotalContactCount,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg}
    return render(request,'Library/Login_History.html',context)

@login_required(login_url='/loginpage/')
def Library_Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = Student_Library_Profile.objects.filter(Library_user_ID=username,Library_Password=password)       
        if user_obj.exists():
            user_status = Student_Library_Profile.objects.filter(Library_user_ID=username).values('Student_Status')[0]['Student_Status']
            if user_status == 'Active': 
                if str(password) == 'Education_Master@123':
                    return redirect('Library_ChangePassword')
                else:
                    return redirect('Library_Index')
            else:
                messages.error(request," Your account is not activated yet !")
                
        # elif user_name.exists != True:
        #     messages.error(request,"No such account found. Register to access library !")
        #     return redirect('Library_Signup')
        else:
            messages.error(request," Your userid or password is wrong !")

    return render(request,'Edu_Master/Library_Login.html')

@login_required(login_url='/loginpage/')
def Library_Signup(request):
    cuser = request.user 
    now = datetime.now()         
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        user_name = Student_Profile.objects.filter(Student_User_PK=cuser).values('Student_Name')[0]['Student_Name']      
        u_name = user_name.split()[0]
        if Student_Library_Profile.objects.filter(Library_User_Profile = Student_pk).exists():
            messages.error(request," You have already registered for the library !")
        else:            
            user_status = 'Inactive'
            user_id = "Education_Master_" + str(u_name)
            user_pass = "Education_Master@123"
            result = Student_Library_Profile(Library_User_Profile=Student_pk,Student_Status=user_status,Library_user_ID=user_id,Library_Password=user_pass)
            result.save()

            # Send an Email to User For successfully Registration
            subject = "Education_Master Library Registration"
            message = "Hello " + Student_pk.Student_Name + "!! \n" + "Welcome to Education_Master Library!! You will get your login credentials very soon ! \nThank you for visiting our website\n.  \n\nThanking You\nTeam Education_Master"
            
            to_email = [Student_pk.Student_Email]
            obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = user_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Welcome Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
            obj_email.save()
            messages.success(request," You have registered successfully for library. You will get all details in your registered email shortly !")
            return redirect('Library_Login')        
    return render(request,'Edu_Master/Library_Signup.html',context)

@login_required(login_url='/loginpage/')
def Library_ForgotPassword(request):
    return render(request,'Edu_Master/Library_ForgotPassword.html')

@login_required(login_url='/loginpage/')
def Library_ChangePassword(request):
    cuser = request.user
    Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
    # user_name = Student_Library_Profile.objects.filter(Library_User_Profile=Student_pk).values('Library_user_ID')[0]['Library_user_ID']
    if request.method == "POST":
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            user_obj = Student_Library_Profile.objects.filter(Library_User_Profile=Student_pk).update(Library_Password = password)
            messages.success(request," Your library password is changed successfully !")
            return redirect('Library_Index')
        else:
            messages.error(request," Password and confirm password dosn't matched !")
    return render(request,'Edu_Master/Library_ChangePassword.html')

@login_required(login_url='/loginpage/')
def search_book(request):
    if request.method == "POST":
        book_keyword = request.POST['book_keyword']
        book_objs = Books.objects.filter(Book_Title__contains = book_keyword)
        context = {'book_objs':book_objs}
    return render(request,'Library/search_book.html',context)

class Library_Index(LoginRequiredMixin,ListView):
    model = Books
    template_name = 'Library/index2.html'
    extra_context={'range': range(1,5)}

class Library_Book_Media(LoginRequiredMixin,ListView):
	model = Books
	template_name = 'Library/books-media.html'
	paginate_by = 3

	def get_queryset(self):
		return Books.objects.all().order_by('Book_Id')

@login_required(login_url='/loginpage/')  
def Library_News_Event(request):
    return render(request,'Library/news-event.html')

@login_required(login_url='/loginpage/')  
def Library_Blog(request):
    return render(request,'Library/blog.html')

@login_required(login_url='/loginpage/')  
def Library_Blog_Detail(request):
    return render(request,'Library/news-event.html')

@login_required(login_url='/loginpage/')
def Library_Services(request):
    return render(request,'Library/services.html')

@login_required(login_url='/loginpage/')
def Library_Book_Request(request):
    cuser = request.user
    now = datetime.now()
    if request.method =="POST":
        Book_Request_Name = request.POST['Book_Name'] 
        Book_Request_Author = request.POST['Book_author'] 
        Book_Request_ISBN = request.POST['Book_ISBN']
        Book_Request_Date = datetime.now().strftime("YYYY-MM-DD")
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        Student_name = Student_pk.Student_Name
        result = Book_Request(Book_Request_Name=Book_Request_Name,Book_Request_Author=Book_Request_Author,Book_Request_ISBN=Book_Request_ISBN,Book_Request_Date=Book_Request_Date,Book_Request_By=Student_pk)
        result.save()                
        subject = "Education_Master Library Book Request"
        message = "Your book request is sending successfully ! We will upload that book soon !"
        email_messege = render_to_string('Library/email_format.html',
        {
       
            'message':message,
            'name':Student_pk.Student_Name
        })
      
        
        to_email = [Student_pk.Student_Email]
        obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = Student_name,Email_subject = subject
                                        ,Email_Message = email_messege,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "General Email",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
        obj_email.save()
        messages.success(request," Your book request is sended successfully !")
        return redirect('Library_Index')

    return render(request,'Library/Library_Book_Request.html')

class Library_Single_Book(LoginRequiredMixin,DetailView):
    model = Books
    template_name = 'Library/Library_Single_Book.html'


# def Library_Audio_Book(request,pk):
#     Total_Page = Books.objects.filter(Book_Id = pk).values('Book_Length')[0]['Book_Length']
#     Start_Page = Books.objects.filter(Book_Id = pk).values('Audio_Start_Page')[0]['Audio_Start_Page']
#     Book_Pdf = Books.objects.filter(Book_Id = pk).values('Book_Pdf')[0]['Book_Pdf']
    
#     First_path = ('E:\\python project\\Edustation\\Edustation\\media\\')
#     Book_Pdf = Book_Pdf.replace('/','\\')
#     BookPath =  ("".join([First_path,Book_Pdf]))
#     #print(BookPath)
#     #print(Total_Page)
#     #print(type(Total_Page))
#     #print(Start_Page)
#     #print(type(Start_Page))
#     AudioBook = Audio_Book.audiobook(BookPath,Total_Page,Start_Page)
#     return render(request,'User/AudioBook.html',{'AudioBook':AudioBook})

