import os
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from . token import generate_token
from datetime import datetime
from . models import *

# Email details
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER =  os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =  os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT =  os.environ.get('EMAIL_PORT')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


def send_mail_to_user(email_subject,email_messege,to_email):
    form_email = EMAIL_HOST_USER
    send_mail(email_subject,email_messege,form_email,[to_email],fail_silently=True)

def account_activation_link(email_subject,email_messege,to_email):
    form_email = EMAIL_HOST_USER
    email = EmailMessage(
            email_subject,
            email_messege,
            form_email,
            to_email
        )
    email.fail_silently = True
    email.send()

def send_email_with_attachment(subject,message,to_email,name,attached_file):
    form_email = EMAIL_HOST_USER
    Email_message = render_to_string('Admin_pannel/admin_email.html',
        {
       
            'name' : name,
            'message': message
        })
    mail = EmailMessage(subject,Email_message,form_email,[to_email])
    mail.attach(attached_file.name,attached_file.read(),mimetype='text/plain')
    mail.fail_silently = True
    mail.send()


def send_Schedule_mail():
    print("Mail Server Called !")
    now = datetime.now()
    form_email = EMAIL_HOST_USER
    obj_Email = Email_Detail.objects.filter(Email_Delivery_Status = 'Not Delivered')
    for object in obj_Email:
        email_subject = object.Email_subject
        to_email = object.Email_Receiver
        receiver_name = object.Email_Receiver_Name
        email_messege = object.Email_Message
        email_submission_type = object.Email_Submission_Type
        email_file_obj = object.Email_Attachment
        email_file_name = email_file_obj.name
        email_file_content = email_file_obj.read()
        if(email_submission_type == 'Account Activation'):
            send_mail_to_user(email_subject,email_messege,to_email)
            object.Email_Delivery_Status = 'Delivered'
            object.Email_Last_Update_Date = now
            object.save()

        elif(email_file_name != '' and email_submission_type != 'Account Activation'):
            send_email_with_attachment(email_subject,email_messege,to_email,receiver_name,email_file_obj)
            object.Email_Delivery_Status = 'Delivered'
            object.Email_Last_Update_Date = now
            object.save()


