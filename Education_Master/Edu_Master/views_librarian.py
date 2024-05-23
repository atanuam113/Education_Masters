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



# ------------------------------------------------Librarian section------------------------------------------------
@login_required(login_url='/loginpage/')
def librarian_dashboard(request):
    book = Books.objects.all().count()
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'book':book,'userprofile':userprofile,'Total_books':Total_books}
    return render(request,'Librarian/librarian_dashboard.html',context)

@login_required(login_url='/loginpage/')
def Librarian_Login_History(request):
    cuser = request.user
    obj_login = login_Log.objects.filter(LLog_User_PK=cuser)  
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]  
    context = {'obj_login':obj_login,'userprofile':userprofile}
    return render(request,'Librarian/Login_History.html',context)


def librarian_search(request):    
    if request.method == "POST":
        cuser = request.user    
        userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
        book_keyword = request.POST['search_keyword']
        book_objs = Books.objects.filter(Book_Title__contains = book_keyword)
        Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
        context = {'book_objs':book_objs,'userprofile':userprofile,'Total_books':Total_books}
    return render(request,'Librarian/librarian_search.html',context)

# def library_register(request):
#     all_register = Student_Library_Profile.objects.filter(Student_Status='Inactive')
#     context = {'all_register':all_register
#     return render(request,'Librarian/library_register.html',context)

class library_register(LoginRequiredMixin,ListView):
	model = Student_Library_Profile
	template_name = 'Librarian/library_register.html'
	# context_object_name = 'books'    
	paginate_by = 3

	def get_queryset(self):
		return Student_Library_Profile.objects.filter(Student_Status='Inactive')

@login_required(login_url='/loginpage/')
def library_register_details(request,pk):
    now = datetime.now()
    requested_user_obj = Student_Library_Profile.objects.get(pk=pk)
    requester_user = Student_Library_Profile.objects.filter(pk=pk).values('Library_User_Profile')[0]['Library_User_Profile']
    user_email = Student_Profile.objects.filter(pk=requester_user).values('Student_Email')[0]['Student_Email']
    user_name = Student_Profile.objects.filter(pk=requester_user).values('Student_Name')[0]['Student_Name']
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    u_id = user_name.split()[0]
    form = Library_registration_Request(instance=requested_user_obj)
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    user_id = "Education_Master_" + str(u_id)    
    user_pass = "Education_Master@123"

    if request.method == 'POST':
        form = Library_registration_Request(request.POST,instance = requested_user_obj)
        if form.is_valid():
            form.save()            
        # Send an Email to User For successfully Registration
        subject = "Education_Master Library Credentials"
        message = "Hello " + user_name + "!! \n" + "Your UserId: "+ user_id + "!! \n" + "Your Password: "+ user_pass +"\nPlease change your password as it is default system generated password.  \n\nThanking You\nTeam Education_Master"
        to_email = [user_email]
        obj_email = Email_Detail(Email_Sender = Email_sender,Email_Receiver = to_email
                                        ,Email_Receiver_Name = user_name,Email_subject = subject
                                        ,Email_Message = message,Email_Delivery_Status = "Not Delivered"
                                        ,Email_Submission_Type = "Login Credential",Email_Created_By = cuser,Email_DateTime = now
                                        ,Email_Last_Updated_By = cuser,Email_Last_Update_Date = now)
        obj_email.save()
        messages.success(request," Library registration request of "+ str(user_name) +" is accepted successfully !")
        return redirect('librarian_dashboard')

    context = {'form':form,'userprofile':userprofile,'Total_books':Total_books}
    return render(request,'Librarian/library_register_details.html',context)

@login_required(login_url='/loginpage/')
def book_request(request):
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    All_active_Book = Book_Request.objects.filter(Book_Request_Status='Active')
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'userprofile':userprofile,'All_active_Book':All_active_Book,'Total_books':Total_books,'Total_books':Total_books}
    return render(request,'Librarian/book_request.html',context)

@login_required(login_url='/loginpage/')
def book_request_details(request,pk):
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'userprofile':userprofile,'Total_books':Total_books}
    if request.method == 'POST':
        title = request.POST['title']
        year = request.POST['year']
        Audio_book_page = request.POST['Audio_Start_Page']
        year = request.POST['year']
        author = request.POST['author']
        Audio_book_page = request.POST['Audio_Start_Page']
        username = request.user.username
        current_user = request.user
        user_id = current_user.id
        Book_Genre = request.POST['Book_Genre']
        Book_Category = request.POST['Book_Genre']
        Book_Length = request.POST['Book_Length']
        Book_Edition = request.POST['Book_Edition']
        pdf = request.FILES['pdf']
        cover = request.FILES['cover']
        desc = request.POST['desc']
        Book_ISBN = request.POST['Book_ISBN']
        publisher = request.POST['publisher']
        a = Books(Book_Title=title, Book_Author=author, Book_Publish_Year=year, Book_Publisher=publisher, Book_Desc=desc, Book_Cover=cover, Book_Pdf=pdf,Book_ISBN = Book_ISBN,Book_Edition = Book_Edition,Book_Length=Book_Length,Book_Genre=Book_Genre,Book_Category = Book_Category, Book_Uploaded_By=username,Book_User_Id = user_id,Audio_Start_Page = Audio_book_page) 
        a.save()
        Book_Request.objects.filter(Book_Request_ID=pk).update(Book_Request_Status='Inactive')
        messages.success(request, ' Book was uploaded successfully')
        return redirect('recent_book')
    return render(request,'Librarian/book_request_details.html',context)

@login_required(login_url='/loginpage/')
def add_book(request):
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'userprofile':userprofile,'Total_books':Total_books}
    if request.method == 'POST':
        title = request.POST['title']
        year = request.POST['year']
        Audio_book_page = request.POST['Audio_Start_Page']
        year = request.POST['year']
        author = request.POST['author']
        Audio_book_page = request.POST['Audio_Start_Page']
        username = request.user.username
        current_user = request.user
        user_id = current_user.id
        Book_Genre = request.POST['Book_Genre']
        Book_Category = request.POST['Book_Genre']
        Book_Length = request.POST['Book_Length']
        Book_Edition = request.POST['Book_Edition']
        pdf = request.FILES['pdf']
        cover = request.FILES['cover']
        desc = request.POST['desc']
        Book_ISBN = request.POST['Book_ISBN']
        publisher = request.POST['publisher']
        a = Books(Book_Title=title, Book_Author=author, Book_Publish_Year=year, Book_Publisher=publisher, Book_Desc=desc, Book_Cover=cover, Book_Pdf=pdf,Book_ISBN = Book_ISBN,Book_Edition = Book_Edition,Book_Length=Book_Length,Book_Genre=Book_Genre,Book_Category = Book_Category, Book_Uploaded_By=username,Book_User_Id = user_id,Audio_Start_Page = Audio_book_page) 
        a.save()
        messages.success(request, ' Book was uploaded successfully')
        return redirect('recent_book')	
    return render(request,'Librarian/add_book.html',context)	  

class manage_book(LoginRequiredMixin,ListView):
	model = Books
	template_name = 'Librarian/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Books.objects.order_by('-Book_Id')

class view_book(LoginRequiredMixin,DetailView):
	model = Books
	template_name = 'Librarian/view_book.html'

class edit_book(LoginRequiredMixin,UpdateView):
	model = Books
	form_class = BookForm
	template_name = 'Librarian/edit_book.html'
	success_url = reverse_lazy('manage_book')
	success_message = 'Data was updated successfully'


class delete_book(LoginRequiredMixin,DeleteView):
	model = Books
	template_name = 'Librarian/delete_book.html'
	success_url = reverse_lazy('lmbook')
	success_message = 'Data was deleted successfully'


class recent_book(LoginRequiredMixin,ListView):
	model = Books
	template_name = 'Librarian/recent_book.html'
	paginate_by = 3

	def get_queryset(self):
		return Books.objects.all().order_by('-Book_Id')
