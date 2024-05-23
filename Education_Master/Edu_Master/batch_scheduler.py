#from models import *
from apscheduler.schedulers.background import BackgroundScheduler
from Edu_Master.mailserver import *
from . import Schedule_time

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_Schedule_mail, 'interval', minutes=1)
    scheduler.start()

