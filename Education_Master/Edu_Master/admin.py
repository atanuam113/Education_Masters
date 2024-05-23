from django.contrib import admin
from .models import *



class Event_Slug(admin.ModelAdmin):
    list_display = ("Event_Name", "Event_Date", "Event_Dept",)
    prepopulated_fields = {"slug": ("Event_Name", )}

class Student_Profile_Slug(admin.ModelAdmin):
    list_display = ("Student_PK", "Student_Name", "Student_Email","Student_DOB")
    prepopulated_fields = {"slug": ("Student_Name", )}

class Student_Profile_Log_Slug(admin.ModelAdmin):
    list_display = ("SPLog_PK", "SPLOG_Name", "SPLOG_Email","SPLOG_DOB")
    prepopulated_fields = {"slug": ("SPLOG_Name", )}

class Student_Library_Profile_Slug(admin.ModelAdmin):
    list_display = ("Library_PK", "Library_user_ID", )
    prepopulated_fields = {"slug": ("Library_user_ID", "Library_PK")}

class Teacher_Profile_Slug(admin.ModelAdmin):
    list_display = ("Teacher_ID", "Teacher_Name", )
    prepopulated_fields = {"slug": ("Teacher_Name", "Teacher_ID")}

class Teacher_Profile_Log_Slug(admin.ModelAdmin):
    list_display = ("TPLog_PK", "TPLog_Name", )
    prepopulated_fields = {"slug": ("TPLog_Name", "TPLog_PK")}

class Admin_Profile_Slug(admin.ModelAdmin):
    list_display = ("Admin_PK", "Admin_Name", )
    prepopulated_fields = {"slug": ("Admin_Name", "Admin_PK")}

class Admin_Profile_Log_Slug(admin.ModelAdmin):
    list_display = ("APLog_PK", "APLog_Name", )
    prepopulated_fields = {"slug": ("APLog_Name", "APLog_PK")}

class Librarian_Profile_Slug(admin.ModelAdmin):
    list_display = ("Librarian_PK", "Librarian_Name", )
    prepopulated_fields = {"slug": ("Librarian_Name", "Librarian_PK")}

class Librarian_Profile_Log_Slug(admin.ModelAdmin):
    list_display = ("LPLog_PK", "LPLog_Name", )
    prepopulated_fields = {"slug": ("LPLog_Name", "LPLog_PK")}

class Books_Slug(admin.ModelAdmin):
    list_display = ("Book_Id", "Book_Title", )
    prepopulated_fields = {"slug": ("Book_Title", "Book_Id")}

class Book_Request_Slug(admin.ModelAdmin):
    list_display = ("Book_Request_ID", "Book_Request_Name", )
    prepopulated_fields = {"slug": ("Book_Request_Name", "Book_Request_ID")}

class Course_Detail_Slug(admin.ModelAdmin):
    list_display = ("Course_ID", "Course_Name", )
    prepopulated_fields = {"slug": ("Course_Name", )}

class Course_Syllabus_Slug(admin.ModelAdmin):
    list_display = ("Course_Syllabus_ID", "Module_Name", )
    prepopulated_fields = {"slug": ("Module_Name", "Course_Syllabus_ID")}

class Course_Module_Slug(admin.ModelAdmin):
    list_display = ("Course_Module_ID", "Module_Topic", )
    prepopulated_fields = {"slug": ("Module_Topic", "Course_Module_ID")}

class Course_Time_Table_Slug(admin.ModelAdmin):
    list_display = ("Course_Time_Table_ID", "Class_Topic", )
    prepopulated_fields = {"slug": ("Class_Topic", "Course_Time_Table_ID")}

class Course_Exam_Table_Slug(admin.ModelAdmin):
    list_display = ("Exam_ID", "Exam_Name", )
    prepopulated_fields = {"slug": ("Exam_Name", "Exam_ID")}

class Address_Book_Slug(admin.ModelAdmin):
    list_display = ("AB_ID", "AB_Party_Name", )
    prepopulated_fields = {"slug": ("AB_Party_Name", "AB_ID")}

class Contact_us_Slug(admin.ModelAdmin):
    list_display = ("Contact_ID", "Contact_Name", )
    prepopulated_fields = {"slug": ("Contact_Name", "Contact_ID")}

class Email_Detail_Slug(admin.ModelAdmin):
    list_display = ("Email_Id", "Email_Sender", )
    prepopulated_fields = {"slug": ("Email_Sender", )}

class Blog_Slug(admin.ModelAdmin):
    list_display = ("Blog_Id", "Blog_Title", )
    prepopulated_fields = {"slug": ("Blog_Title", )}

# Register your models here.
admin.site.register(User)
admin.site.register(Contact_us,Contact_us_Slug)
admin.site.register(Student_Profile,Student_Profile_Slug)
admin.site.register(Events, Event_Slug)
admin.site.register(Event_Register)
admin.site.register(Course_Detail,Course_Detail_Slug)
admin.site.register(Teacher_Profile,Teacher_Profile_Slug)
admin.site.register(Admin_Profile,Admin_Profile_Slug)
admin.site.register(Course_Syllabus,Course_Syllabus_Slug)
admin.site.register(Course_Module,Course_Module_Slug)
admin.site.register(Course_Time_Table,Course_Time_Table_Slug)
admin.site.register(Course_Exam_Table,Course_Exam_Table_Slug)
admin.site.register(Books)
admin.site.register(Student_Library_Profile,Student_Library_Profile_Slug)
admin.site.register(Librarian_Profile)
admin.site.register(Book_Request,Book_Request_Slug)
admin.site.register(Address_Book,Address_Book_Slug)
admin.site.register(Student_Profile_Log,Student_Profile_Log_Slug)
admin.site.register(Teacher_Profile_Log,Teacher_Profile_Log_Slug)
admin.site.register(Librarian_Profile_Log,Librarian_Profile_Log_Slug)
admin.site.register(Admin_Profile_Log,Admin_Profile_Log_Slug)
admin.site.register(login_Log)
admin.site.register(Email_Detail,Email_Detail_Slug)
admin.site.register(Course_review)
admin.site.register(course_registration)
admin.site.register(Blog,Blog_Slug)
admin.site.register(Blog_Review)
admin.site.register(User_Feedback)


