from django.urls import path, include
from . import views,views_teacher,views_admin,views_librarian,views_library
from django.contrib.auth import views as auth_views


urlpatterns = [

path('register/',views.register,name='register'),
path('',views.login,name='login'),
path('forgotpass/',views.forgotpass,name='forgotpass'),
path('LogOut/',views.LogOut,name='LogOut'),
path('Admin_Login_History/',views_admin.Admin_Login_History,name='Admin_Login_History'),
path('loginpage/',views.login,name='loginpage'),
path('LoginWithOTP/',views.LoginWithOTP,name='LoginWithOTP'),
path("activate/<uidb64>/<token>/",views_admin.activate,name="activate"),

#Student section
path('home/',views.home,name='home'),
path('about/',views.about,name='about'),
path('award/',views.award,name='award'),
path('research/',views.research,name='research'),
path('facilities/',views.facilities,name='facilities'),
path('student_search/',views.student_search,name='student_search'),
path('facilities_detail/',views.facilities_detail,name='facilities_detail'),
path('departments/',views.departments,name='departments'),
path('all_course/',views.all_course,name='all_course'),
path('course_review/',views.course_review,name='course_review'),
path('course_register/',views.course_register,name='course_register'),
path('seminar/',views.seminar,name='seminar'),
path('course_details/<slug:slug>',views.course_details,name='course_details'),
path('blog/',views.blog,name='blog'),
path('student_blog/',views.student_blog,name='student_blog'),
path('student_login_history/',views.student_login_history,name='student_login_history'),
path('student_add_blog/',views.student_add_blog,name='student_add_blog'),
path('blog_review/',views.blog_review,name='blog_review'),
path('blog_details/<slug:slug>',views.blog_details,name='blog_details'),
path('contact_us/',views.contact_us,name='contact_us'),
path('Feedback/',views.Feedback,name='Feedback'),
path('event/',views.event,name='event'),
path('event_register/<slug:slug>',views.event_register,name='event_register'),
path('event_details/<slug:slug>',views.event_details,name='event_details'),
path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
path('student_profile/',views.student_profile,name='student_profile'),
path('student_course/',views.student_course,name='student_course'),
path('student_exam/',views.student_exam,name='student_exam'),
path('student_class_time/',views.student_class_time,name='student_class_time'),
path('student_notification/',views.student_notification,name='student_notification'),
path('student_notification_detail/<int:pk>',views.student_notification_detail,name='student_notification_detail'),
path('Subcribed_course/<int:pk>',views.Subcribed_course,name='Subcribed_course'),
path('student_Profile_Edit/<slug:slug>',views.student_Profile_Edit,name='student_Profile_Edit'),
path('all_trainer/',views.all_trainer,name='all_trainer'),

# Library Section
# path('library_home/', views_library.library_home.as_view(), name='library_home'),
path('Library_Login/', views_library.Library_Login, name='Library_Login'),
path('Library_Login_History/',views_library.Library_Login_History,name='Library_Login_History'),
path('Library_Signup/', views_library.Library_Signup, name='Library_Signup'),
path('Library_ForgotPassword/', views_library.Library_ForgotPassword, name='Library_ForgotPassword'),
path('Library_ChangePassword/', views_library.Library_ChangePassword, name='Library_ChangePassword'),
path('search_book/', views_library.search_book, name='search_book'),
path('Library_Index/', views_library.Library_Index.as_view(), name='Library_Index'),
path('Library_Book_Media/', views_library.Library_Book_Media.as_view(), name='Library_Book_Media'),
path('Library_News_Event/', views_library.Library_News_Event, name='Library_News_Event'),
path('Library_Blog/', views_library.Library_Blog, name='Library_Blog'),
path('Library_Blog_Detail/', views_library.Library_Blog_Detail, name='Library_Blog_Detail'),
path('Library_Services/', views_library.Library_Services, name='Library_Services'),
path('Library_Single_Book/<int:pk>', views_library.Library_Single_Book.as_view(), name='Library_Single_Book'),
# path('Library_Audio_Book/<int:pk>',views_library.Library_Audio_Book,name='Library_Audio_Book'),
path('Library_Book_Request/', views_library.Library_Book_Request, name='Library_Book_Request'),


#Admin Section
path('admin_dashboard1/',views_admin.admin_dashboard1,name='admin_dashboard1'),
path('admin_notification/',views_admin.admin_notification.as_view(),name='admin_notification'),
path('admin_Pending_Blog/',views_admin.admin_Pending_Blog,name='admin_Pending_Blog'),
path('admin_account_setting/',views_admin.admin_account_setting,name='admin_account_setting'),
path('admin_search/',views_admin.admin_search,name='admin_search'),
path('admin_notification_details/<int:pk>',views_admin.admin_notification_details,name='admin_notification_details'),
path('Admin_personal_details_edit/<int:pk>',views_admin.Admin_personal_details_edit,name='Admin_personal_details_edit'),

path('admin_all_course/',views_admin.admin_all_course,name='admin_all_course'),
path('admin_add_course/',views_admin.admin_add_course,name='admin_add_course'),
path('admin_add_course_module/',views_admin.admin_add_course_module,name='admin_add_course_module'),
# path('admin_get_course_topic_dropdown/',views_admin.admin_get_course_topic_dropdown,name='admin_get_course_topic_dropdown'),
path('admin_course_details/<int:pk>',views_admin.admin_course_details,name='admin_course_details'),
path('admin_course_module_list/<int:pk>',views_admin.admin_course_module_list,name='admin_course_module_list'),
path('admin_course_module_details/<int:pk>',views_admin.admin_course_module_details,name='admin_course_module_details'),

path('admin_all_teacher/',views_admin.admin_all_teacher,name='admin_all_teacher'),
path('admin_add_teacher/',views_admin.admin_add_teacher,name='admin_add_teacher'),
path('admin_teacher_details/<int:pk>',views_admin.admin_teacher_details,name='admin_teacher_details'),

path('admin_all_student/',views_admin.admin_all_student,name='admin_all_student'),
path('admin_add_student/',views_admin.admin_add_student,name='admin_add_student'),
path('admin_student_details/<int:pk>',views_admin.admin_student_details,name='admin_student_details'),
path('admin_student_feedback/<int:pk>',views_admin.admin_student_feedback,name='admin_student_feedback'),
path('admin_student_feedback_details/<int:pk>',views_admin.admin_student_feedback_details,name='admin_student_feedback_details'),
path('admin_student_feedback_delete/<int:pk>',views_admin.admin_student_feedback_delete,name='admin_student_feedback_delete'),

path('admin_student_course/<int:pk>',views_admin.admin_student_course,name='admin_student_course'),
path('admin_student_course_details/<int:pk>',views_admin.admin_student_course_details,name='admin_student_course_details'),
path('admin_student_course_details_update/',views_admin.admin_student_course_details_update,name='admin_student_course_details_update'),

path('admin_student_blog/<int:pk>',views_admin.admin_student_blog,name='admin_student_blog'),
path('admin_student_blog_details/<int:pk>',views_admin.admin_student_blog_details,name='admin_student_blog_details'),


path('admin_all_librarian/',views_admin.admin_all_librarian,name='admin_all_librarian'),
path('admin_add_librarian/',views_admin.admin_add_librarian,name='admin_add_librarian'),
path('admin_librarian_details/<int:pk>',views_admin.admin_librarian_details,name='admin_librarian_details'),

path('admin_all_user/',views_admin.admin_all_user,name='admin_all_user'),
path('admin_add_librarian/',views_admin.admin_add_librarian,name='admin_add_librarian'),
path('admin_user_details/<int:pk>',views_admin.admin_user_details,name='admin_user_details'),

path('admin_all_mails/',views_admin.admin_all_mails,name='admin_all_mails'),
#path('admin_delivered_mails/',views_admin.admin_delivered_mails,name='admin_delivered_mails'),
#path('admin_not_delivered_mails/',views_admin.admin_not_delivered_mails,name='admin_not_delivered_mails'),
#path('admin_hold_mails/',views_admin.admin_hold_mails,name='admin_hold_mails'),
path('admin_add_mail/',views_admin.admin_add_mail,name='admin_add_mail'),
path('admin_mail_details/<int:pk>',views_admin.admin_mail_details,name='admin_mail_details'),

path('admin_add_blog/',views_admin.admin_add_blog,name='admin_add_blog'),
path('admin_all_blog/',views_admin.admin_all_blog,name='admin_all_blog'),
path('admin_blog_details/<int:pk>',views_admin.admin_blog_details,name='admin_blog_details'),

path('admin_all_contact/',views_admin.admin_all_contact,name='admin_all_contact'),
# path('admin_add_librarian/',views_admin.admin_add_librarian,name='admin_add_librarian'),
path('admin_contact_response/<int:pk>',views_admin.admin_contact_response,name='admin_contact_response'),
path('admin_contact_view/<int:pk>',views_admin.admin_contact_view,name='admin_contact_view'),

path('admin_all_events/',views_admin.admin_all_events,name='admin_all_events'),
path('admin_add_event/',views_admin.admin_add_event,name='admin_add_event'),
path('admin_event_details/<int:pk>',views_admin.admin_event_details,name='admin_event_details'),
path('admin_event_registered_user/<int:pk>',views_admin.admin_event_registered_user,name='admin_event_registered_user'),

path('admin_all_exam/',views_admin.admin_all_exam,name='admin_all_exam'),
path('admin_add_exam/',views_admin.admin_add_exam,name='admin_add_exam'),
path('admin_exam_details/',views_admin.admin_exam_details,name='admin_exam_details'),
path('admin_all_groups/',views_admin.admin_all_groups,name='admin_all_groups'),
path('admin_add_group/',views_admin.admin_add_group,name='admin_add_group'),

path('admin_all_enquiry/',views_admin.admin_all_enquiry,name='admin_all_enquiry'),
path('admin_course_enquiry/',views_admin.admin_course_enquiry,name='admin_course_enquiry'),
path('admin_admission_enquiry/',views_admin.admin_admission_enquiry,name='admin_admission_enquiry'),
path('admin_seminar_enquiry/',views_admin.admin_seminar_enquiry,name='admin_seminar_enquiry'),
path('admin_event_enquiry/',views_admin.admin_event_enquiry,name='admin_event_enquiry'),
path('admin_common_enquiry/',views_admin.admin_common_enquiry,name='admin_common_enquiry'),
path('admin_view_enquiry/',views_admin.admin_view_enquiry,name='admin_view_enquiry'),
path('user_email_send/<int:pk>',views_admin.user_email_send,name='user_email_send'),

# Teacher Section
path('teacher_dashboard/',views_teacher.teacher_dashboard,name='teacher_dashboard'),
path('Teacher_Login_History/',views_teacher.Teacher_Login_History,name='Teacher_Login_History'),


# Librarian Section 
path('librarian_dashboard/',views_librarian.librarian_dashboard,name='librarian_dashboard'),
path('Librarian_Login_History/',views_librarian.Librarian_Login_History,name='Librarian_Login_History'),
path('add_book/',views_librarian.add_book,name='add_book'),
path('librarian_search/',views_librarian.librarian_search,name='librarian_search'),
path('manage_book/', views_librarian.manage_book.as_view(), name='manage_book'),
path('recent_book/', views_librarian.recent_book.as_view(), name='recent_book'),
path('library_register/', views_librarian.library_register.as_view(), name='library_register'),
path('view_book/<int:pk>', views_librarian.view_book.as_view(), name='view_book'),
path('edit_book/<int:pk>', views_librarian.edit_book.as_view(), name='edit_book'),
path('delete_book/<int:pk>', views_librarian.delete_book.as_view(), name='delete_book'),
path('library_register_details/<int:pk>', views_librarian.library_register_details, name='library_register_details'),
path('book_request/', views_librarian.book_request, name='book_request'),
path('book_request_details/<int:pk>', views_librarian.book_request_details, name='book_request_details'),

]