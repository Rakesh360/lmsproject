from django.conf import settings
from django.utils import timezone
import base64
import math
import sys
import pytz
import json
import string
import random
import datetime
import requests
import logging
import threading
import xlrd
import math
from random import randint
from django.core.mail import send_mail
from EasyHireApp.constants import *
from EasyHireApp.models import Problem, QuizResult, QuizSection, ProblemAttempted, QuizStatus
from accounts.models import Student as Applicant

logger = logging.getLogger(__name__)

def generate_random_string_of_length_N(N):
    import string
    import random
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
    return res

def get_quiz_result_problems_list(applicant_obj, quiz_obj):

    try:
        quiz_sections = QuizSection.objects.filter(quiz=quiz_obj)

        quiz_problem_attempted = {}

        sym = ','

        valid_problem_categories = ["1","2"]
        difficulty = {"1":"Easy","2":"Medium","3":"Hard"}
        header = {}
        header['no'] = "Sr. No"
        header['difficulty'] = "Difficulty"
        header['question'] = "Question"
        header['correct_options'] = "Correct"
        header['attempted_options'] = "Attempted"
        header['result'] = "Status"

        for quiz_section in quiz_sections:

            quiz_problem_attempted[quiz_section.topic.name] = []

            quiz_problem_attempted[quiz_section.topic.name].append(header)

            problems_in_section = ProblemAttempted.objects.filter(applicant=applicant_obj,quiz_section=quiz_section).order_by("problem__difficulty")

            i=1
            for pro in problems_in_section:
                try:

                    if pro.problem.category in valid_problem_categories:
                        # print(pro.problem)
                        temp = {}
                        temp['no'] = i
                        temp['difficulty'] = difficulty[pro.problem.difficulty]
                        temp['question'] = pro.problem.description
                        temp['correct_options'] = sym.join(sorted(pro.problem.get_correct_option_list()))
                        temp['attempted_options'] = sym.join(sorted(pro.get_attempted_option_list()))

                        if temp['correct_options'] == temp['attempted_options']:
                            temp['result'] = "Correct"
                        else:
                            temp['result'] = "Incorrect"

                        if len(temp['attempted_options'])==0:
                            temp['attempted_options'] = '-'
                            temp['result'] = 'Not Attempted'

                        quiz_problem_attempted[quiz_section.topic.name].append(temp)
                        i+=1

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("Error get quiz problems: %s at %s", str(e), str(exc_tb.tb_lineno))

        return quiz_problem_attempted
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error get quiz problems: %s at %s", str(e), str(exc_tb.tb_lineno))

def password_generator():
    #return ''.join(random.choice(chars) for _ in range(size))
    password = ""
    for i in range(6):
        password+=str(random.randint(1,9))
    return password

def is_user_authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def ascii_string(string):
    return str(string.encode("ascii", errors="ignore").decode("ascii"))

def get_list_of_rejected_applicants(Applicant):
    return Applicant.objects.filter(is_rejected=True)


def get_list_of_selected_applicants(Applicant):
    return Applicant.objects.filter(is_selected=True)


def get_list_of_registered_applicants(Applicant):
    return Applicant.objects.filter(is_registered=True)


def get_list_of_non_approved_applicants(Applicant):
    return Applicant.objects.filter(is_approved=False)

def get_list_of_campus_applicants(Applicant):
    return Applicant.objects.filter(category="1")

def get_list_of_walkin_applicants(Applicant):
    return Applicant.objects.filter(category="2")

def get_list_of_posting_applicants(Applicant):
    return Applicant.objects.filter(category="3")

def get_list_of_applicants_for_given_stream(Applicant, stream_objs):
    return Applicant.objects.filter(stream__in=stream_objs).distinct()

def get_list_of_applicants_for_given_institute(Applicant, institute_objs):
    return Applicant.objects.filter(college_name__in=institute_objs).distinct()


def get_applicant_objs_from_applicant_id_list(applicant_id_list, Applicant):
    applicant_objs = []
    for applicant_id in applicant_id_list:
        applicant_obj = ""
        try:
            applicant_obj = Applicant.objects.get(pk=int(applicant_id))
            applicant_obj.is_approved = True
            applicant_obj.save()
            applicant_objs.append(applicant_obj)
            #applicant_objs.append(Applicant.objects.get(pk=int(applicant_id)))
        except Exception as e:
            pass
    return applicant_objs


def get_quiz_obj(quiz_id, Quiz):
    quiz_obj = None
    try:
        quiz_obj = Quiz.objects.get(pk=int(quiz_id))
    except Exception as e:
        pass
    return quiz_obj


def get_quiz_obj_with_uuid(uuid, Quiz):
    quiz_obj = None
    try:
        quiz_obj = Quiz.objects.get(uuid=uuid)
    except Exception as e:
        pass
    return quiz_obj

def send_registration_msg_to_applicant(applicant_obj,password):
    try:
        phone_number = applicant_obj.phone_number
        message = f"Dear {applicant_obj.name}, Your registration is successful on assessment portal. Please log in at {settings.DOMAIN_NAME} with your username {applicant_obj.phone_number} and password {phone_number}"
        logger.info(message)
        #url = "http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+applicant_obj.phone_number+"&source=mcleod&message="+ message
        url = f"http://sms6.rmlconnect.net:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination={applicant_obj.phone_number}&source=macleo&message={message}"
        #r = requests.get("http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+str(applicant_obj.phone_number)+"&source=mcleod&message="+message)
        r = requests.get(url)
        if(r.text.split("|")[0] == "1701"):
            logger.info("Message Sent Successfully")
        else:
            logger.info("Message Failed")
    except Exception as e:
        logger.error("Message error %s", e)

def send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj):
    try:
        phone_number = applicant_obj.phone_number
        #message = str("Dear "+ applicant_obj.name + " Your registration is successful. Please login at "+ settings.DOMAIN_NAME +" with your username " + applicant_obj.phone_number+ " and password " + password)
        message = f"Dear {applicant_obj.name}, You have been assigned {quiz_obj.title} Quiz, which has {quiz_obj.get_section_with_question_count_for_sms()} questions and this shall be attempted within {quiz_obj.total_quiz_time()} minutes. Please log in at {settings.DOMAIN_NAME} with the credentials shared at the time of registration and attempt the quiz."
        logger.info(f"Message sent: {message}")
        #return
        #url = "http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+applicant_obj.phone_number+"&source=mcleod&message="+ message
        url = f"http://sms6.rmlconnect.net:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination={applicant_obj.phone_number}&source=macleo&message={message}"
        #r = requests.get("http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+str(applicant_obj.phone_number)+"&source=mcleod&message="+message)
        r = requests.get(url)
        if(r.text.split("|")[0] == "1701"):
            logger.info("Message Sent Successfully")
        else:
            logger.info("Message Failed")
    except Exception as e:
        logger.error("Message error %s", e)

def send_quiz_submission_msg_to_applicant(applicant_obj,quiz_assigned):
    try:
        phone_number = applicant_obj.phone_number
        #message = str("Dear "+ applicant_obj.name + " Your registration is successful. Please login at "+ settings.DOMAIN_NAME +" with your username " + applicant_obj.phone_number+ " and password " + password)
        message = f"Dear {applicant_obj.name}, Your quiz: {quiz_assigned} has submitted successfully, Please log in at https://hire.macleodspharma.com for further updates."
        logger.info(f"Message Sent: {message}")
        #return
        #url = "http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+applicant_obj.phone_number+"&source=mcleod&message="+ message
        url = f"http://sms6.rmlconnect.net:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination={applicant_obj.phone_number}&source=macleo&message={message}"
        #r = requests.get("http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+str(applicant_obj.phone_number)+"&source=mcleod&message="+message)
        r = requests.get(url)
        if(r.text.split("|")[0] == "1701"):
            logger.info("Message Sent Successfully")
        else:
            logger.info("Message Failed")
    except Exception as e:
        logger.error("Message error %s", e)                

def send_status_change_msg_to_applicant(applicant_obj,status):
    try:
        phone_number = applicant_obj.phone_number
        #message = str("Dear "+ applicant_obj.name + " Your registration is successful. Please login at "+ settings.DOMAIN_NAME +" with your username " + applicant_obj.phone_number+ " and password " + password)
        if status == "selected":
            message = f"Dear {applicant_obj.name}, Your profile has been shortlisted, Please log in at https://hire.macleodspharma.com for further updates."
        elif status == "rejected":
            message = f"Dear {applicant_obj.name}, Your profile has been rejected, Please log in at https://hire.macleodspharma.com for further updates."
        elif status == "reset":
            message = f"Dear {applicant_obj.name},\n Your account has been reset by the administrator. In case of any queries, please contact your HR Manager."
        else:
            raise Exception(f"Invalid choice of status passed --> {status}")
        logger.info(message)
        #url = "http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+applicant_obj.phone_number+"&source=mcleod&message="+ message
        url = f"http://sms6.rmlconnect.net:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination={applicant_obj.phone_number}&source=macleo&message={message}"
        #r = requests.get("http://sms6.routesms.com:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination="+str(applicant_obj.phone_number)+"&source=mcleod&message="+message)
        r = requests.get(url)
        if(r.text.split("|")[0] == "1701"):
            logger.info("Message Sent Successfully")
        else:
            logger.info("Message Failed")
    except Exception as e:
        logger.error("Message error %s", e) 


def send_reminder_msg_to_applicant(applicant_obj,quiz_obj,status):
    try:
        phone_number = applicant_obj.phone_number
        message =""
        if status == "not started":
            message = f"Dear {applicant_obj.name}, Gentle reminder to attempt Quiz - {quiz_obj.title} assigned to you. Please log in at {settings.DOMAIN_NAME} with the credentials shared at the time of registration and attempt the quiz."
        elif status == "not completed":
            message = f"Dear {applicant_obj.name}, Gentle reminder to compete Quiz - {quiz_obj.title} assigned to you. Please log in at {settings.DOMAIN_NAME} with the credentials shared at the time of registration and complete the quiz."
        logger.info(message)
        
        url = f"http://sms6.rmlconnect.net:8080/bulksms/bulksms?username=macleo&password=mac61leo&type=0&dlr=1&destination={applicant_obj.phone_number}&source=macleo&message={message}"
        
        r = requests.get(url)
        if(r.text.split("|")[0] == "1701"):
            logger.info("Message Sent Successfully")
        else:
            logger.info("Message Failed")
    except Exception as e:
        logger.error("Message error %s", e)

"""
def send_registration_email_to_applicant(applicant_obj, password):
    email=applicant_obj.email_id
    message =" Hi, Your registration is successfull. Please login at https://hire.macleodspharma.com/login/ with your mobile number as username and password is " + password
    try:
        send_mail('Macleods Registration Details', message, settings.RECRUITER_EMAIL,[email], settings.RECRUITER_EMAIL_PASSWORD)
    except Exception as e:
        logger.error("Send mail %s",e)
"""

def send_registration_email_to_applicant(applicant_obj, password):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    body = f"""<head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>Macleods| EasyHire Registration</title>
      <style type="text/css" media="screen">
      </style>
    </head>
    <body>
    <div style="padding:1em;border:0.1em black solid;" class="container">
        <p>
            Hello  {str(applicant_obj.name)},
        </p>
        <p>
             Your registration is successfull. Please login at https://hire.macleodspharma.com/login/
        </p>
        <p>Your mobile number is your username and your password is """ + str(password) + """</p>
    </div>
    </body>"""
    to_emai_id = applicant_obj.email_id
    from_email_id = settings.RECRUITER_EMAIL
    from_email_id_password = settings.RECRUITER_EMAIL_PASSWORD
    email_message = MIMEMultipart('alternative')
    email_message['subject'] = "Macleods EasyHire Registration"
    email_message['To'] = to_emai_id
    email_message['From'] = from_email_id
    email_message.preamble = ""
    email_html_body = MIMEText(body, 'html')
    email_message.attach(email_html_body)
    message_as_string = email_message.as_string()
    import smtplib, ssl
    smtp_server = 'smtp.macleodspharma.com'
    port = 465
    sender = 'hr@macleodspharma.com'
    password = 'NYTLDIa%14'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server,port, context=context) as server:
        server.login(sender,password)
        server.sendmail(from_email_id, to_emai_id, message_as_string)
        server.quit()

#def schedule_applicant_quiz(applicant_objs,
#                            start_date,
#                            start_time,
#                            end_date,
#                            end_time,
#                            quiz_obj,
#                            QuizStatus):
#    try:
#        start_datetime = None
#        end_datetime = None
#        try:
#            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
#            start_time_obj = datetime.datetime.strptime(
#                start_time, "%H:%M").time()
#            start_datetime = datetime.datetime.combine(
#                start_date_obj, start_time_obj)
#            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
#            end_time_obj = datetime.datetime.strptime(end_time, "%H:%M").time()
#            end_datetime = datetime.datetime.combine(
#                end_date_obj, end_time_obj)
#            ez = pytz.timezone(settings.TIME_ZONE)
#            start_datetime = ez.localize(start_datetime)
#            end_datetime = ez.localize(end_datetime)
#        except Exception as e:
#            pass
#        for applicant_obj in applicant_objs:
#            quiz_status_obj = None
#            if applicant_obj.is_rejected == True:
#                days_of_rejection = (timezone.now() - applicant_obj.attempted_datetime).days
#                print(days_of_rejection)
#                if(days_of_rejection <= 30):
#                    return False, False
#                else:
#                    try:
#                        quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
#                                                                 quiz=quiz_obj)
#                    except Exception as e:
#                        quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
#                                                                    quiz=quiz_obj)
#
#                    quiz_status_obj.quiz_start_time = start_datetime
#                    quiz_status_obj.quiz_end_time = end_datetime
#                    quiz_status_obj.time_remaining = -1
#                    quiz_status_obj.save()
#                    # content = "Dear {{applicant_name}}, you are assigned a quiz on Macleods EasyHire. Kindly complete the quiz at the earliest"
#                    # send_message_to_applicant(applicant_obj, content)
#                    send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
#                    applicant_obj.clear_attempted_quiz(quiz_obj)
#                    applicant_obj.status = APPLICANT_AT_QUIZ
#                    applicant_obj.attempted_datetime = timezone.now()
#                    applicant_obj.is_rejected = False
#                    applicant_obj.save()
#            else:
#                try:
#                    quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
#                                                             quiz=quiz_obj)
#                    return None,None
#                except Exception as e:
#                    quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
#                                                                quiz=quiz_obj)
#
#                quiz_status_obj.quiz_start_time = start_datetime
#                quiz_status_obj.quiz_end_time = end_datetime
#                quiz_status_obj.time_remaining = -1
#                quiz_status_obj.save()
#                # content = "Dear {{applicant_name}}, you are assigned a quiz on Macleods EasyHire. Kindly complete the quiz at the earliest"
#                # send_message_to_applicant(applicant_obj, content)
#                print(f"********Reached Here***************")
#                send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
#                print(f"********Completed Here***************")
#                applicant_obj.clear_attempted_quiz(quiz_obj)
#                applicant_obj.status = APPLICANT_AT_QUIZ
#                applicant_obj.attempted_datetime = timezone.now()
#                applicant_obj.save()
#        return True, True
#    except Exception as e:
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        logger.error("Error schedule_applicant_quiz: %s at %s",(e), str(exc_tb.tb_lineno))
#        return False, False


#def schedule_applicant_quiz(applicant_objs,
#                            start_date,
#                            start_time,
#                            end_date,
#                            end_time,
#                            quiz_obj,
#                            QuizStatus):
#    errors = []
#    try:
#        start_datetime = None
#        end_datetime = None
#
#        try:
#            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
#            start_time_obj = datetime.datetime.strptime(
#                start_time, "%H:%M").time()
#            start_datetime = datetime.datetime.combine(
#                start_date_obj, start_time_obj)
#            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
#            end_time_obj = datetime.datetime.strptime(end_time, "%H:%M").time()
#            end_datetime = datetime.datetime.combine(
#                end_date_obj, end_time_obj)
#            ez = pytz.timezone(settings.TIME_ZONE)
#            start_datetime = ez.localize(start_datetime)
#            end_datetime = ez.localize(end_datetime)
#        except Exception as e:
#            pass
#
#        for applicant_obj in applicant_objs:
#            quiz_status_obj = None
#            if applicant_obj.is_rejected == True:
#                days_of_rejection = (timezone.now() - applicant_obj.attempted_datetime).days
#                print(days_of_rejection)
#                if(days_of_rejection <= 30):
#                    errors.append(f'{applicant_obj.name} is rejected between 30 days.')
#                else:
#                    try:
#                        quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
#                                                                 quiz=quiz_obj)
#                    except Exception as e:
#                        quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
#                                                                    quiz=quiz_obj)
#
#                    quiz_status_obj.quiz_start_time = start_datetime
#                    quiz_status_obj.quiz_end_time = end_datetime
#                    quiz_status_obj.time_remaining = -1
#                    quiz_status_obj.save()
#                    # content = "Dear {{applicant_name}}, you are assigned a quiz on Macleods EasyHire. Kindly complete the quiz at the earliest"
#                    # send_message_to_applicant(applicant_obj, content)
#                    send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
#                    applicant_obj.clear_attempted_quiz(quiz_obj)
#                    applicant_obj.status = APPLICANT_AT_QUIZ
#                    applicant_obj.attempted_datetime = timezone.now()
#                    applicant_obj.is_rejected = False
#                    applicant_obj.save()
#                    errors.append(f'{applicant_obj.name} quiz assigned.')
#
#            else:
#                try:
#                    quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
#                                                             quiz=quiz_obj)
#                    # return None,None
#                    errors.append(f'{applicant_obj.name} unable to assign quiz because quiz already assigned')
#                except Exception as e:
#                    quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
#                                                                quiz=quiz_obj)
#
#                    errors.append(f'{applicant_obj.name} quiz assigned')
#
#                quiz_status_obj.quiz_start_time = start_datetime
#                quiz_status_obj.quiz_end_time = end_datetime
#                quiz_status_obj.time_remaining = -1
#                quiz_status_obj.save()
#                # content = "Dear {{applicant_name}}, you are assigned a quiz on Macleods EasyHire. Kindly complete the quiz at the earliest"
#                # send_message_to_applicant(applicant_obj, content)
#                print(f"********Reached Here***************")
#                send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
#                print(f"********Completed Here***************")
#                applicant_obj.clear_attempted_quiz(quiz_obj)
#                applicant_obj.status = APPLICANT_AT_QUIZ
#                applicant_obj.attempted_datetime = timezone.now()
#                applicant_obj.save()
#        return errors,True, True
#    except Exception as e:
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        logger.error("Error schedule_applicant_quiz: %s at %s",(e), str(exc_tb.tb_lineno))
#        errors.append(f'error schedule_applicant quiz')
#        return errors,False, False



##############

def schedule_applicant_quiz(applicant_objs,
                            start_date,
                            start_time,
                            end_date,
                            end_time,
                            quiz_obj,
                            QuizStatus):
    errors = []
    try:
        start_datetime = None
        end_datetime = None

        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            start_time_obj = datetime.datetime.strptime(
                start_time, "%H:%M").time()
            start_datetime = datetime.datetime.combine(
                start_date_obj, start_time_obj)
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_time_obj = datetime.datetime.strptime(end_time, "%H:%M").time()
            end_datetime = datetime.datetime.combine(
                end_date_obj, end_time_obj)
            ez = pytz.timezone(settings.TIME_ZONE)
            start_datetime = ez.localize(start_datetime)
            end_datetime = ez.localize(end_datetime)
        except Exception as e:
            pass

        for applicant_obj in applicant_objs:
            quiz_status_obj = None
            if applicant_obj.is_rejected == True:
                days_of_rejection = (timezone.now() - applicant_obj.attempted_datetime).days
                print(days_of_rejection)
                if(days_of_rejection <= 30):
                    errors.append(f'{applicant_obj.name} is rejected between 30 days.')
                else:
                    try:
                        quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
                                                                 quiz=quiz_obj)
                    except Exception as e:
                        quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
                                                                    quiz=quiz_obj)

                    quiz_status_obj.quiz_start_time = start_datetime
                    quiz_status_obj.quiz_end_time = end_datetime
                    quiz_status_obj.time_remaining = -1
                    quiz_status_obj.save()
                    # content = "Dear {{applicant_name}}, you are assigned a quiz on Macleods EasyHire. Kindly complete the quiz at the earliest"
                    # send_message_to_applicant(applicant_obj, content)
                    send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
                    applicant_obj.clear_attempted_quiz(quiz_obj)
                    applicant_obj.status = APPLICANT_AT_QUIZ
                    applicant_obj.attempted_datetime = timezone.now()
                    applicant_obj.is_rejected = False
                    applicant_obj.save()
                    errors.append(f'{applicant_obj.name} quiz assigned.')

            else:
                try:
                    quiz_status_objs = QuizStatus.objects.filter(applicant=applicant_obj,
                                                                    quiz=quiz_obj)
                    assigned_quiz_status_objs = []
                    for quiz_status_obj in quiz_status_objs:
                        if not quiz_status_obj.is_deleted:
                            assigned_quiz_status_objs.append(quiz_status_obj)

                    if len(assigned_quiz_status_objs) > 0:
                        errors.append(f"{applicant_obj.name} - Unable to assign as quiz already assigned")
                    else:
                        quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
                                                                 quiz=quiz_obj)
                        quiz_status_obj.quiz_start_time = start_datetime
                        quiz_status_obj.quiz_end_time = end_datetime
                        quiz_status_obj.time_remaining = -1
                        quiz_status_obj.save()
                        send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
                        applicant_obj.clear_attempted_quiz(quiz_obj)
                        applicant_obj.status = APPLICANT_AT_QUIZ
                        applicant_obj.attempted_datetime = timezone.now()
                        applicant_obj.save()
                except Exception as e:
                    logger.error(f"Error in assigning quiz to {applicant_obj.name} with error - {e}")

        return errors,True, True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error schedule_applicant_quiz: %s at %s",(e), str(exc_tb.tb_lineno))
        errors.append(f'error schedule_applicant quiz')
        return errors,False, False

##############




def schedule_applicant_interview(applicant_objs):
    try:
        for applicant_obj in applicant_objs:
            applicant_obj.status = APPLICANT_INTERVIEW
            applicant_obj.save()
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error schedule_applicant_interview: %s at %s",(e), str(exc_tb.tb_lineno))
        return False

def initiate_quiz_section(applicant_obj, quiz_config, quiz_section, QuizSectionResult, Problem):
    try:
        is_attempted = False
        quiz_section_result_objs = QuizSectionResult.objects.filter(quiz_section=quiz_section,
                                                                    applicant=applicant_obj)

        if len(quiz_section_result_objs) > 0:
            is_attempted = True
            logger.info("applicant has already attempted current section.")

            if quiz_section_result_objs[0].is_completed:
                return None, None

        topic = quiz_section.topic
        #problem_objs = Problem.objects.filter(topics__in=[topic], difficulty="1")

        if quiz_section.is_quiz_section_static:

            if is_attempted:
                no_question_attempted = quiz_section_result_objs[0].no_question_attempted
            else:
                no_question_attempted = 0

            if no_question_attempted < quiz_section.easy_questions:

                problem_objs = Problem.objects.filter(topics__in=[topic],
                                                          difficulty="1", is_active=True)
            elif no_question_attempted >= quiz_section.easy_questions and no_question_attempted < quiz_section.easy_questions + quiz_section.medium_questions:
                problem_objs = Problem.objects.filter(topics__in=[topic],
                                                          difficulty="2", is_active=True)
            else:
                problem_objs = Problem.objects.filter(topics__in=[topic],
                                                          difficulty="3", is_active=True)
        else:
            problem_objs = Problem.objects.filter(topics__in=[topic],
                                                      difficulty="1", is_active=True)

        problem_obj = None
        quiz_section_result_obj = None

        if is_attempted:
            quiz_section_result_obj = quiz_section_result_objs[0]
            attempted_problem_obj_list = quiz_section_result_obj.get_attempted_problem_list()
            problem_objs = list(set(problem_objs) -
                                set(attempted_problem_obj_list))
            problem_obj = random.choice(problem_objs)
        else:
            quiz_section_result_obj = QuizSectionResult.objects.create(quiz_section=quiz_section,
                                                                       applicant=applicant_obj)

            problem_obj = random.choice(list(problem_objs))
            quiz_section_result_obj.calibration = problem_obj.difficulty
            quiz_section_result_obj.right_answers = 0
            quiz_section_result_obj.no_question_attempted = 0
            quiz_section_result_obj.used_difficulties = 0
            quiz_section_result_obj.is_completed = False
            quiz_section_result_obj.observations = json.dumps({
                "calibration_list": [],
                "problem_pk_list": []
            })
            quiz_section_result_obj.save()

        try:
            quiz_status = QuizStatus.objects.get(applicant=applicant_obj, quiz=quiz_config)
            quiz_status.last_problem_time = datetime.datetime.now()
            quiz_status.save()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("initiate_quiz_section : %s at %s", e, str(exc_tb.tb_lineno))

        return problem_obj, quiz_section_result_obj
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("initiate_quiz_section: %s at %s",
                     e, str(exc_tb.tb_lineno))
        return None, None


def increment_problem_attempts(problem_obj):
    if problem_obj != None:
        total_attempts = problem_obj.total_attempts
        total_attempts += 1
        problem_obj.total_attempts = total_attempts
        problem_obj.save()


def increment_correct_attempts(problem_obj):
    if problem_obj != None:
        correct_attempts = problem_obj.correct_attempts
        correct_attempts += 1
        problem_obj.correct_attempts = correct_attempts
        problem_obj.save()


def save_problem_attempted(request_packet,
                           quiz_section,
                           applicant_obj,
                           quiz_status_obj,
                           Problem,
                           ProblemAttempted):
    problem_attempted_obj = None
    try:
        problem_id = int(request_packet["problem_id"])
        problem_obj = Problem.objects.get(pk=problem_id)
        current_problem_mode = request_packet["mode"]


        if quiz_status_obj is None:
            quiz_status_obj = QuizStatus.objects.get(applicant = applicant_obj , quiz = quiz_section.quiz , is_completed=False)
        else:
            quiz_status_obj = QuizStatus.objects.get(id = int(quiz_status_obj))

        logger.info(f"Entered Quiz Status obj is blank with value {quiz_status_obj}")
        try:
            problem_attempted_obj = ProblemAttempted.objects.get(quiz_section=quiz_section,
                                                                 applicant=applicant_obj,
                                                                 problem=problem_obj,quiz_status=quiz_status_obj)
        except Exception as e:
            problem_attempted_obj = ProblemAttempted.objects.create(quiz_section=quiz_section,
                                                                    applicant=applicant_obj,
                                                                    problem=problem_obj,quiz_status=quiz_status_obj)

        if problem_attempted_obj != None:
            # Single Choice Answer from User
            if current_problem_mode == "1":
                choice = request_packet["choice"]
                problem_attempted_obj.options = choice
            # Multiple Choice Answer from User
            elif current_problem_mode == "2":
                choice_list = request_packet["choice_list"]
                problem_attempted_obj.options = "|".join(choice_list)
            # Descriptive Answer
            elif current_problem_mode == "3":
                problem_attempted_obj.answer = ascii_string(
                    request_packet["text"])
            # Audio based answer
            elif current_problem_mode == "4":
                problem_attempted_obj.answer = "Audio"
            # Video based answer
            else:
                problem_attempted_obj.answer = ascii_string(
                    request_packet["text"])
                problem_attempted_obj.video_url = request_packet["video_url"]


            try:
                quiz_status = QuizStatus.objects.get(applicant=applicant_obj, quiz=quiz_section.quiz)
                problem_attempted_obj.start_time = quiz_status.last_problem_time
                problem_attempted_obj.end_time = datetime.datetime.now()
            except Exception as e:
                logger.error("save_problem_attempted: " + str(e))

            problem_attempted_obj.save()

            #compute_text_analysis = threading.Thread(target=problem_attempted_obj.generate_text_analysis,
            #                                         args=())
            #compute_text_analysis.daemon = True
            #compute_text_analysis.start()
            # if str(current_problem_mode) == "3" or str(current_problem_mode) == "5":
            #     if settings.ICICI_AWS_SECRET_ACCESS_KEY != "" and settings.ICICI_AWS_ACCESS_KEY != "":
            #         description_analysis_thread = threading.Thread(
            #             target=generate_descriptive_question_analysis, args=(problem_attempted_obj,))
            #         description_analysis_thread.daemon = True
            #         description_analysis_thread.start()
    except Exception as e:
        logger.error("save_problem_attempted: "+str(e))

    return problem_attempted_obj

def checkWhetherResponseIsCorrectOrNot(choice_list, current_problem_id):
    try:
        problem_obj = Problem.objects.get(pk=int(current_problem_id))
        #correct_choices = problem_obj.right_choices.all()
        correct_choices = problem_obj.correct_options
        # choice_list = [Choice.objects.get(pk=int(choice))
        #               for choice in choice_list]

        problem_attempted_obj = ProblemAttempt.objects.get(problem=problem_obj)

        choice_list = problem_attempted_obj.options

        for choice_obj in correct_choices:
            if choice_obj != "|":
                if choice_obj not in choice_list:
                    return False
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("checkWhetherResponseIsCorrectOrNot: %s at %s",
                     e, str(exc_tb.tb_lineno))
        return False


def min_calibration(n):
    calibration = 1 - 2*(math.log(n)+0.5772)
    return calibration


def max_calibration(n):
    calibration = 1 + 2*(math.log(n)+0.5772)
    return calibration


def get_difficulty_level_based_on_calibration(calibration, n):
    if n == 0:
        return DIFFICULTY_EASY

    min_cal = min_calibration(n)
    max_cal = max_calibration(n)

    calibration_step = (max_cal-min_cal)/float(3)

    if int(calibration) <= (min_cal+calibration_step):
        logger.info("Easy: Min calibration: %s, Max calibration: %s, calibration_step: %s, calibration: %s",
                    min_cal, max_cal, calibration_step, calibration)
        return DIFFICULTY_EASY
    elif int(calibration) > (min_cal+calibration_step) and int(calibration) <= (min_cal+(2*calibration_step)):
        logger.info("Medium: Min calibration: %s, Max calibration: %s, calibration_step: %s, calibration: %s",
                    min_cal, max_cal, calibration_step, calibration)
        return DIFFICULTY_MEDIUM
    else:
        logger.info("Hard: Min calibration: %s, Max calibration: %s, calibration_step: %s, calibration: %s",
                    min_cal, max_cal, calibration_step, calibration)
        return DIFFICULTY_HARD

def reset_counter(quiz_section_result_obj):
    quiz_section_result_obj.correct_answer_counter = 0
    quiz_section_result_obj.incorrect_answer_counter = 0
    quiz_section_result_obj.save()

def find_problem_based_on_threshold(quiz_section_result_obj, quiz_section, Problem, current_problem_mode):
    try:
        positive_threshold = quiz_section.positive_threshold
        negative_threshold = quiz_section.negative_threshold

        calibration = quiz_section_result_obj.calibration

        attempted_problem_obj_list = quiz_section_result_obj.get_attempted_problem_list()

        no_question_attempted = quiz_section_result_obj.no_question_attempted
        no_question_allowed_in_section = quiz_section.no_questions

        next_problem_section = quiz_section
        if no_question_attempted >= no_question_allowed_in_section:
            return None

        topic = quiz_section.topic
        problem_objs = Problem.objects.filter(topics__in=[topic], is_active=True)

        problem_objs = list(set(problem_objs)-set(attempted_problem_obj_list))

        correct_answer_counter = quiz_section_result_obj.correct_answer_counter
        incorrect_answer_counter = quiz_section_result_obj.incorrect_answer_counter

        next_problem_difficulty = int(current_problem_mode)
        if correct_answer_counter > positive_threshold:
            reset_counter(quiz_section_result_obj)
            if current_problem_mode == "1" or current_problem_mode == "2":
                next_problem_difficulty +=1
            else:
                next_problem_difficulty = 3
        elif incorrect_answer_counter > negative_threshold:
            reset_counter(quiz_section_result_obj)
            if current_problem_mode == "2" or current_problem_mode == "3":
                next_problem_difficulty -= 1
            else:
                next_problem_difficulty = 1
        else:
            next_problem_difficulty = current_problem_mode
        filtered_problem_objs = []
        for problem_obj in problem_objs:
            if str(problem_obj.difficulty) == str(next_problem_difficulty):
                filtered_problem_objs.append(problem_obj)

        if len(filtered_problem_objs) > 0:
            return random.choice(filtered_problem_objs)
        elif len(problem_objs) > 0:
            return random.choice(problem_objs)
        else:
            return None
    except Exception as e:
        logger.error("find_problem_based_on_threshold: "+str(e))
        return None

def find_next_static_problem(quiz_section_result_obj, quiz_section, Problem, current_problem_mode):
    try:
        logger.info("Static")
        attempted_problem_obj_list = quiz_section_result_obj.get_attempted_problem_list()

        no_question_attempted = quiz_section_result_obj.no_question_attempted
        no_question_allowed_in_section = quiz_section.no_questions

        next_problem_section = quiz_section
        if no_question_attempted >= no_question_allowed_in_section:
            return None
        topic = quiz_section.topic
        problem_objs = Problem.objects.filter(topics__in=[topic], is_active=True)

        problem_objs = list(set(problem_objs)-set(attempted_problem_obj_list))
        easy_questions = quiz_section.easy_questions
        medium_questions = quiz_section.medium_questions
        hard_questions = quiz_section.hard_questions

        next_problem_difficulty = int(current_problem_mode)

        logger.info("Current Level %s", next_problem_difficulty)

        attempted = 0
        if int(no_question_attempted) < int(easy_questions):
            next_problem_difficulty = 1
        else:
            attempted = int(no_question_attempted) - int(easy_questions)
            if int(attempted) < int(medium_questions):
                next_problem_difficulty = 2
            else:
                attempted = int(no_question_attempted) - \
                    (int(easy_questions) + int(medium_questions))
                if int(attempted) <= int(hard_questions):
                    next_problem_difficulty = 3
                else:
                    next_problem_difficulty = current_problem_mode
        logger.info("Problem difficulty %s", next_problem_difficulty)

        filtered_problem_objs = []
        for problem_obj in problem_objs:
            if str(problem_obj.difficulty) == str(next_problem_difficulty):
                filtered_problem_objs.append(problem_obj)

        if len(filtered_problem_objs) > 0:
            return random.choice(filtered_problem_objs)
        elif len(problem_objs) > 0:
            return random.choice(problem_objs)
        else:
            return None
    except Exception as e:
        logger.error("find_next_static_problem: "+str(e))
        return None

def find_problem_based_on_calibration(quiz_section_result_obj, quiz_section, Problem):
    try:
        calibration = quiz_section_result_obj.calibration

        attempted_problem_obj_list = quiz_section_result_obj.get_attempted_problem_list()

        no_question_attempted = quiz_section_result_obj.no_question_attempted
        no_question_allowed_in_section = quiz_section.no_questions

        next_problem_section = quiz_section
        if no_question_attempted >= no_question_allowed_in_section:
            return None

        topic = quiz_section.topic
        problem_objs = Problem.objects.filter(topics__in=[topic], is_active=True)

        problem_objs = list(set(problem_objs)-set(attempted_problem_obj_list))

        next_problem_difficulty = get_difficulty_level_based_on_calibration(
            calibration, no_question_allowed_in_section)

        filtered_problem_objs = []
        for problem_obj in problem_objs:
            if problem_obj.difficulty == next_problem_difficulty:
                filtered_problem_objs.append(problem_obj)

        if len(filtered_problem_objs) > 0:
            return random.choice(filtered_problem_objs)
        elif len(problem_objs) > 0:
            return random.choice(problem_objs)
        else:
            return None
    except Exception as e:
        logger.error("find_problem_based_on_calibration: "+str(e))
        return None


def get_next_problem(request_packet,
                     applicant_obj,
                     quiz_status_obj,
                     Quiz,
                     QuizSection,
                     QuizSectionResult,
                     Problem,
                     ProblemAttempted):
    try:
        # Fetch quiz conf
        quiz_config_uuid = request_packet["unique_quiz_config_id"]
        current_quiz_section_id = request_packet["quiz_section_id"]

        quiz_config = get_quiz_obj_with_uuid(quiz_config_uuid, Quiz)

        current_quiz_section = QuizSection.objects.get(pk=int(current_quiz_section_id),
                                                       quiz=quiz_config)

        current_problem_id = int(request_packet["problem_id"])
        current_problem_mode = request_packet["mode"]

        problem_obj = Problem.objects.get(pk=int(current_problem_id))
        problem_difficulty = problem_obj.difficulty
        # Increatement problem attempts
        increment_problem_attempts(problem_obj)

        quiz_section_result_obj = QuizSectionResult.objects.get(quiz_section=current_quiz_section,
                                                                applicant=applicant_obj)

        no_question_attempted = quiz_section_result_obj.no_question_attempted
        calibration = quiz_section_result_obj.calibration
        used_difficulties = quiz_section_result_obj.used_difficulties
        right_answers = quiz_section_result_obj.right_answers
        correct_answer_counter = quiz_section_result_obj.correct_answer_counter
        incorrect_answer_counter = quiz_section_result_obj.incorrect_answer_counter

        observations = json.loads(quiz_section_result_obj.observations)
        observations["calibration_list"].append(round(calibration, 3))
        observations["problem_pk_list"].append(problem_obj.pk)

        used_difficulties += int(problem_obj.difficulty)
        no_question_attempted += 1

        attempted_problem_obj = save_problem_attempted(request_packet,
                                                       current_quiz_section,
                                                       applicant_obj,
                                                       quiz_status_obj,
                                                       Problem,
                                                       ProblemAttempted)

        if current_problem_mode == "1" or current_problem_mode == "2" or current_problem_mode == "3":
            choice_list = []
            try:
                if current_problem_mode == "1":
                    choice_list = [request_packet["choice"]]
                else:
                    choice_list = request_packet["choice_list"]
            except Exception:
                choice_list = []
            if attempted_problem_obj.is_selected_option_correct():
                right_answers += 1
                correct_answer_counter +=1
                increment_correct_attempts(problem_obj)
                calibration = calibration + round(2.0/no_question_attempted, 3)
            else:
                incorrect_answer_counter += 1
                calibration = calibration - round(2.0/no_question_attempted, 3)
        else:
            increment_correct_attempts(problem_obj)
            right_answers += 1
            correct_answer_counter += 1
            logger.info("This is Descriptive answer or audio or video")

        quiz_section_result_obj.calibration = calibration
        quiz_section_result_obj.used_difficulties = used_difficulties
        quiz_section_result_obj.right_answers = right_answers
        quiz_section_result_obj.no_question_attempted = no_question_attempted
        quiz_section_result_obj.observations = json.dumps(observations)
        quiz_section_result_obj.incorrect_answer_counter = incorrect_answer_counter
        quiz_section_result_obj.correct_answer_counter = correct_answer_counter
        quiz_section_result_obj.save()

        quiz_type = current_quiz_section.is_quiz_section_static
        logger.info("Quiz Type %s", quiz_type)
        next_problem_obj = []
        if quiz_type:
            next_problem_obj = find_next_static_problem(
                quiz_section_result_obj, current_quiz_section, Problem, problem_difficulty)
        else:
            next_problem_obj = find_problem_based_on_threshold(
                quiz_section_result_obj, current_quiz_section, Problem, problem_difficulty)
        if next_problem_obj != None:
            try:
                quiz_status = QuizStatus.objects.get(applicant=applicant_obj, quiz=quiz_config)
                quiz_status.last_problem_time = datetime.datetime.now()
                quiz_status.save()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("get_next_problem : %s at %s",e, str(exc_tb.tb_lineno))
            return next_problem_obj, current_quiz_section
        return None, None
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_next_problem: %s at %s", e, str(exc_tb.tb_lineno))

    return None, None


def applicant_completed_quiz_section(applicant_obj, quiz_section, QuizSectionResult):
    try:
        quiz_section_result_obj = QuizSectionResult.objects.filter(applicant=applicant_obj, quiz_section=quiz_section)[0]
    except Exception as e:
        quiz_section_result_obj = QuizSectionResult.objects.create(applicant=applicant_obj, quiz_section=quiz_section)

    # if len(quiz_section_result_objs) > 0:
    # quiz_section_result_obj = quiz_section_result_objs[0]
    quiz_section_result_obj.is_completed = True
    quiz_section_result_obj.save()


def end_quiz(quiz, applicant, QuizSectionResult):
    try:
        quiz_sections = QuizSection.objects.filter(quiz=quiz)
        for quiz_section in quiz_sections:
            applicant_completed_quiz_section(applicant, quiz_section, QuizSectionResult)
        quiz_status = QuizStatus.objects.get(applicant=applicant, quiz=quiz)
        quiz_status.is_completed = True
        quiz_status.completion_date = datetime.datetime.now()
        quiz_status.save()
    except Exception as e:
        logger.error("Error end quiz %s", str(e))

def save_applicant_data_at_irecruit(applicant_obj):
    try:
        domain_name = settings.DOMAIN_NAME
        gender = ""
        if applicant_obj.gender == "1":
            gender = "M"
        elif applicant_obj.gender == "2":
            gender = "F"
        else:
            gender = "O"

        resume = ""
        with open("/home/ubuntu/macleods/EasyHire"+applicant_obj.resume.url, "rb") as r:
            f = r.read()
            b = bytearray(f)
        resume = base64.b64encode(b)
        #resume.decode("utf-8")
        logger.info(applicant_obj.image)
        image = ""
        with open("/home/ubuntu/macleods/EasyHire"+applicant_obj.image.url, "rb") as r:
            f = r.read()
            b = bytearray(f)
        image = base64.b64encode(b)
        #image.decode("utf-8")

        URL = "https://ats.macleodspharma.com/api/saveCandidateAPI/"
        Headers = {
            "apiKey":settings.IRECRUIT_SAVE_CANDIDATE_API_KEY,
            "updateDuplicate":"Y",
            "Content-Type": "application/json"
        }
        Data = {
                "tmp": "false",
                "downloadFileFlg": "false",
                "blockEmail": "false",
                "updatedByCndFlg": "false",
                "cndId": applicant_obj.pk,
                "cndName": applicant_obj.name,
                "email": applicant_obj.email_id,
                "mobile":applicant_obj.phone_number,
                "dob":applicant_obj.dob.strftime('%Y-%m-%d'),
                "gender":str(gender),
                "institution": applicant_obj.college_name,
                "currentLocation":applicant_obj.location,
                "custField32":applicant_obj.event.name,
                "custField3":applicant_obj.id_proof_adhaar_number,
                "custField1":applicant_obj.id_proof_pan_number,
                "currentEmployer":applicant_obj.current_company,
                "designation":applicant_obj.current_designation,
                "currentCtc":applicant_obj.current_ctc,
                "img":image.decode("utf-8"),
                "imgName": str(applicant_obj.image),
                "imagePath":"/home/ubuntu/macleods/EasyHire"+applicant_obj.image.url,
                "fileName": str(applicant_obj.resume),
                "resume": resume.decode("utf-8"),
                "totalExperience": 0.0,
                "projectedExperience": 0.0,
                "inactive": "false",
                "isAllocated": "false",
                "isBlock": "false",
                "cndStatusId": 0,
                "gdprFlg": "false",
                "cndJobRating": 0,
                #"createdBy":"vendor@macleodspharma.com",
                # "createdDate":applicant_obj.attempted_datetime.strftime('%Y-%m-%d'),
                "custField5": applicant_obj.attempted_datetime.strftime('%Y-%m-%d'),
                }
        #print(json.dumps(Data))
        r = requests.post(url=URL, headers=Headers, data=json.dumps(Data), timeout=10)
        logger.info(r)
        json_response = json.loads(r.text)
        logger.info(json_response)
        print(json_response)
        if(json_response["status"] == 200):
            logger.info("SUCCESS")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("save_applicant_data_at_irecruit: %s at %s",
                     e, str(exc_tb.tb_lineno))


def push_applicant_data_at_irecruit(applicant_obj, quiz_result_obj):
    try:
        domain_name = settings.DOMAIN_NAME
        # quiz_result_obj = QuizResult.objects.filter(applicant=applicant_obj)
        applicant_score = quiz_result_obj.get_applicant_quiz_score()
        descriptive_score = quiz_result_obj.description_score
        logger.info("Descriptive score %s", descriptive_score)
        gender = ""
        if applicant_obj.gender == "1":
            gender = "M"
        elif applicant_obj.gender == "2":
            gender = "F"
        else:
            gender = "O"

        resume = ""
        with open("/home/ubuntu/macleods/EasyHire"+applicant_obj.resume.url, "rb") as r:
            f = r.read()
            b = bytearray(f)
        resume = base64.b64encode(b)

        image = ""
        with open("/home/ubuntu/macleods/EasyHire"+applicant_obj.image.url, "rb") as r:
            f = r.read()
            b = bytearray(f)
        resume = base64.b64encode(b)

        image = ""
        with open("/home/ubuntu/macleods/EasyHire"+applicant_obj.image.url, "rb") as r:
            f = r.read()
            b = bytearray(f)
        image = base64.b64encode(b)

        URL = "https://ats.macleodspharma.com/api/saveCandidateAPI/"
        Headers = {
            "apiKey": settings.IRECRUIT_SAVE_CANDIDATE_API_KEY,
            "updateDuplicate": "Y",
            "Content-Type": "application/json"
        }
        logger.info("Applicant Score %s", applicant_score)
        if applicant_obj.event:
            event_name = applicant_obj.event.name
        else:
            event_name = "NA"
        if applicant_score != None:
            Data = {
                "tmp": "false",
                "downloadFileFlg": "false",
                "blockEmail": "false",
                "updatedByCndFlg": "false",
                "cndId": applicant_obj.pk,
                "cndName": applicant_obj.name,
                "email": applicant_obj.email_id,
                "mobile": applicant_obj.phone_number,
                "dob": applicant_obj.dob.strftime('%Y-%m-%d'),
                "gender": str(gender),
                "institution": applicant_obj.college_name,
                "currentLocation": applicant_obj.location,
                "custField32": event_name,
                "custField3": applicant_obj.id_proof_adhaar_number,
                "custField1": applicant_obj.id_proof_pan_number,
                "currentEmployer": applicant_obj.current_company,
                "designation": applicant_obj.current_designation,
                "currentCtc": applicant_obj.current_ctc,
                "img": image.decode("utf-8"),
                "imagePath": "/home/ubuntu/macleods/EasyHire"+applicant_obj.image.url,
                "resume": resume.decode("utf-8"),
                "fileName": str(applicant_obj.resume),
                "imgName": str(applicant_obj.image),
                "totalExperience": 0.0,
                "projectedExperience": 0.0,
                "inactive": "false",
                "isAllocated": "false",
                "isBlock": "false",
                "cndStatusId": 0,
                "gdprFlg": "false",
                "cndJobRating": 0,
                "custField30": applicant_score,
            }
        else:
            logger.info("Sending Descriptive Answer")
            Data = {
                "tmp": "false",
                "downloadFileFlg": "false",
                "blockEmail": "false",
                "updatedByCndFlg": "false",
                "cndId": applicant_obj.pk,
                "cndName": applicant_obj.name,
                "email": applicant_obj.email_id,
                "mobile": applicant_obj.phone_number,
                "dob": applicant_obj.dob.strftime('%Y-%m-%d'),
                "gender": str(gender),
                "institution": applicant_obj.college_name,
                "currentLocation": applicant_obj.location,
                "custField32": event_name,
                "custField3": applicant_obj.id_proof_adhaar_number,
                "custField1": applicant_obj.id_proof_pan_number,
                "currentEmployer": applicant_obj.current_company,
                "designation": applicant_obj.current_designation,
                "currentCtc": applicant_obj.current_ctc,
                "img": image.decode("utf-8"),
                "imagePath": "/home/ubuntu/macleods/EasyHire"+applicant_obj.image.url,
                "resume": resume.decode("utf-8"),
                "fileName": str(applicant_obj.resume),
                "imgName": str(applicant_obj.image),
                "totalExperience": 0.0,
                "projectedExperience": 0.0,
                "inactive": "false",
                "isAllocated": "false",
                "isBlock": "false",
                "cndStatusId": 0,
                "gdprFlg": "false",
                "cndJobRating": 0,
                "custField31": descriptive_score,
            }
        r = requests.post(url=URL, headers=Headers, data=json.dumps(Data))
        json_response = json.loads(r.text)
        logger.info(json_response)
        if(json_response["status"] == 200):
            applicant_obj.save_at_irecruit = True
            applicant_obj.save()
        else:
            applicant_obj.save_at_irecruit = False
            applicant_obj.save()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("push_applicant_data_at_irecruit: %s at %s",
                     e, str(exc_tb.tb_lineno))

#def generate_applicant_quiz_result(applicant_obj, quiz_obj, QuizResult):
#    try:
#        quiz_result_obj = None
#        try:
#            quiz_result_obj = QuizResult.objects.get(applicant=applicant_obj,
#                                                     quiz=quiz_obj)
#        except Exception as e:
#            quiz_result_obj = QuizResult.objects.create(applicant=applicant_obj,
#                                                        quiz=quiz_obj)
#
#        quiz_result_obj.generate_quiz_result()
#        logger.info("Quiz Result saved successfully.")
#        quiz_result_obj.generate_quiz_description_result()
#        #push_applicant_data_at_irecruit(applicant_obj, quiz_result_obj)
#        logger.info("Data pushed at iRecruit successfully.")
#    except Exception as e:
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        logger.error("generate_applicant_quiz_result: %s at %s",
#                     e, str(exc_tb.tb_lineno))

def generate_applicant_quiz_result(applicant_obj, quiz_obj, quiz_status_obj, QuizResult):
    try:
        quiz_result_obj = None
        try:
            quiz_result_obj = QuizResult.admin_objects.get(applicant=applicant_obj,
                                                     quiz=quiz_obj,
                                                     quiz_status=quiz_status_obj
                                                     )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"generate_applicant_quiz_result: {e} at { str(exc_tb.tb_lineno)} {applicant_obj} \n {quiz_obj} \n {quiz_status_obj} \n {QuizResult}")
            quiz_result_obj = QuizResult.admin_objects.create(applicant=applicant_obj,
                                                        quiz=quiz_obj,
                                                        quiz_status=quiz_status_obj
                                                        )


        quiz_result_obj.quiz_status = quiz_status_obj
        quiz_result_obj.save()
        quiz_result_obj.generate_quiz_result()
        logger.info("Quiz Result saved successfully.")
        quiz_result_obj.generate_quiz_description_result()
        #push_applicant_data_at_irecruit(applicant_obj, quiz_result_obj)
        #logger.info("Data pushed at iRecruit successfully.")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("generate_applicant_quiz_result: %s at %s",
                     e, str(exc_tb.tb_lineno))


def valid_url_check(path):
    try:
        r = requests.head(path)
        return r.status_code == requests.codes.ok
    except Exception as e:
        return False

def save_problem(json_data, request, Administrator, Problem, Topic):
    try:
        administrator_obj = Administrator

        problem_id = json_data["problem_id"]
        category_id = json_data["problem_category"]
        difficulty = json_data["problem_difficulty"]
        topic_id_list = json_data["problem_topics"]
        description = json_data["problem_description"]
        solution = json_data["problem_solution"]
        hint = json_data["problem_hint"]
        selected_choice = json_data["selected_choices"]
        correct_choice = json_data["correct_choices"]
        image_path = json_data["image_path"]
        video_url = json_data["video_url"]
        text_to_speech = json_data["text_to_speech"]
        selected_urls = json_data["selected_urls"]
        pdf_url = json_data["pdf_url"]
        if category_id == "1" or category_id == "2":

            if len(correct_choice.split('|')) > 1:
                category_id = "2"
            else:
                category_id = "1"

        selected_urls_list = None
        try:
            selected_urls_list = selected_urls.split(",")
            updated_urls_list = []
            for selected_url in selected_urls_list:
                if valid_url_check(selected_url):
                    updated_urls_list.append(ascii_string(selected_url))

            selected_urls_list = json.dumps({"items":updated_urls_list})
        except Exception as e:
            pass

        problem_video = None
        try:
            video_urls_list = video_url.split(",")
            updated_video_urls_list = []
            for video_url in video_urls_list:
                if valid_url_check(video_url):
                    updated_video_urls_list.append(video_url)

            problem_video = json.dumps({
                    "items":updated_video_urls_list
                })
        except Exception as e:
            pass

        problem_obj = None
        if problem_id == "None":
            problem_obj = Problem.objects.create(description=ascii_string(description),
                                                 solution=ascii_string(solution),
                                                 hint=ascii_string(hint),
                                                 category=ascii_string(category_id),
                                                 typed_by=administrator_obj.username,
                                                 difficulty=ascii_string(difficulty),
                                                 image=image_path,
                                                 video=problem_video,
                                                 options = selected_choice,
                                                 correct_options = correct_choice,
                                                 graph_url = selected_urls_list)
        else:
            problem_obj = Problem.objects.get(pk=int(problem_id))
            problem_obj.description = ascii_string(description)
            problem_obj.solution = ascii_string(solution)
            problem_obj.hint = ascii_string(hint)
            problem_obj.category = ascii_string(category_id)
            problem_obj.typed_by = administrator_obj.username
            problem_obj.difficulty = ascii_string(difficulty)

            if problem_obj.image == None or image_path != None:
                problem_obj.image = image_path

            problem_obj.video = problem_video
            problem_obj.graph_url = selected_urls_list

        if not valid_url_check(pdf_url):
            pdf_url = None

        problem_obj.text_to_speech = text_to_speech
        problem_obj.pdf = pdf_url
        problem_obj.save()

        problem_obj.options = selected_choice
        problem_obj.correct_options = correct_choice
        problem_obj.clear_problem_topics()
        for topic_id in topic_id_list:
            topic_obj = Topic.objects.get(pk=int(topic_id))
            problem_obj.topics.add(topic_obj)

        problem_obj.save()
        logger.info("New Problem created successfully.")
        return problem_obj.pk
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("saveProblem: %s at %s", e, str(exc_tb.tb_lineno))
        return -1

def import_mcq_from_excel(file_path, employee_obj, topic_obj):
    try:
        wb = xlrd.open_workbook("files/"+file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        print(e)
        return False, "Excel File Read Error"
    rows_error = "Error at following Rows (Sr. No):<br>"
    for i in range(1, sheet.nrows):
        try:
            category_id = "1"

            description = sheet.cell_value(i, 1)
            description = description.strip()

            if len(description) == 0:
                raise Exception('No description provided in question %s in file %s', str(i), str(file_path))

#            ans = str(sheet.cell_value(i, 7)).strip().lower()
#
#            if len(ans) == 0:
#                raise Exception('No answer provided in question %s in file %s', str(i), str(file_path))
#
#            answer = None
#
#            choice1 = None
#            choice1 = str(sheet.cell_value(i, 2)).strip()
#            choice2 = None
#            choice2 = str(sheet.cell_value(i, 3)).strip()
#            choice3 = None
#            choice3 = str(sheet.cell_value(i, 4)).strip()
#            choice4 = None
#            choice4 = str(sheet.cell_value(i, 5)).strip()
#
#            choice_list = []
#
#            if choice1 is not None and len(choice1):
#                choice_list.append(choice1)
#                if ans == "a":
#                    answer = choice1
#            elif ans == "a":
#                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))
#
#            if choice2 is not None and len(choice2):
#                choice_list.append(choice2)
#                if ans == "b":
#                    answer = choice2
#            elif ans == "b":
#                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))
#
#            if choice3 is not None and len(choice3):
#                choice_list.append(choice3)
#                if ans == "c":
#                    answer = choice3
#            elif ans == "c":
#                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))
#
#            if choice4 is not None and len(choice4):
#                choice_list.append(choice4)
#                if ans == "d":
#                    answer = choice4
#            elif ans == "d":
#                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))
#
#            if answer is None:
#                raise Exception('Invalid answer provided in question %s in file %s', str(i), str(file_path))
#
#            choices = '|'.join(choice_list)

            ans = str(sheet.cell_value(i, 7)).strip().lower()

            ans = set(ans.split(','))

            ans2 = set()

            for elem in ans:
                elem = elem.strip()
                if "a" <= elem <= "d":
                    ans2.add(elem)

            ans = ans2

            if len(ans) == 0:
                raise Exception('No answer provided in question %s in file %s', str(i), str(file_path))

            answer = []

            choice1 = None
            choice1 = str(sheet.cell_value(i, 2)).strip()
            choice2 = None
            choice2 = str(sheet.cell_value(i, 3)).strip()
            choice3 = None
            choice3 = str(sheet.cell_value(i, 4)).strip()
            choice4 = None
            choice4 = str(sheet.cell_value(i, 5)).strip()

            choice_list = []

            if choice1 is not None and len(choice1):
                choice_list.append(choice1)
                if "a" in ans:
                    answer.append(choice1)
            elif "a" in ans:
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if choice2 is not None and len(choice2):
                choice_list.append(choice2)
                if "b" in ans:
                    answer.append(choice2)
            elif "b" in ans:
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if choice3 is not None and len(choice3):
                choice_list.append(choice3)
                if "c" in ans:
                    answer.append(choice3)
            elif "c" in ans:
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if choice4 is not None and len(choice4):
                choice_list.append(choice4)
                if "d" in ans:
                    answer.append(choice4)
            elif "d" in ans:
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if len(answer) == 0:
                raise Exception('Invalid answer provided in question %s in file %s', str(i), str(file_path))
            elif len(answer) > 1:
                category_id = "2"

            if len(choice_list) == 0:
                raise Exception('No choices provided in question %s in file %s', str(i), str(file_path))

            choices = '|'.join(choice_list)
            answer = '|'.join(answer)

            difficulty = int(float(sheet.cell_value(i, 6)))

            if difficulty < 1 or difficulty > 3:
                raise Exception('Invalid difficulty provided in question %s in file %s', str(i), str(file_path))

#            description = str(description)
#
#            choice1 = None
#            choice1 = sheet.cell_value(i, 2)
#            choice2 = None
#            choice2 = sheet.cell_value(i, 3)
#            choice3 = None
#            choice3 = sheet.cell_value(i, 4)
#            choice4 = None
#            choice4 = sheet.cell_value(i, 5)
#
#            choices = ""
#            choices = str(str(choice1)+"|"+str(choice2)+"|"+str(choice3)+"|"+str(choice4))
#
#            difficulty = int(float(sheet.cell_value(i, 6)))
#
#            ans = sheet.cell_value(i, 7)
#
#            answer = None
#            if(ans == "A" or ans == "a"):
#                answer = choice1
#            elif(ans == "B" or ans == "b"):
#                answer = choice2
#            elif(ans == "C" or ans == "c"):
#                answer = choice3
#            elif(ans == "D" or ans == "d"):
#                answer = choice4
#            else:
#                answer = None

            sol = ""
            try:
                sol = sheet.cell_value(i, 8)
            except Exception as e:
                pass

            hint = ""
            image_path = ""
            video_url = None
            try:
                problem_obj = Problem.objects.create(description=str(description), solution=str(sol.encode("ascii", errors="ignore")), hint=hint.encode(
                    "ascii", errors="ignore"), category=category_id, typed_by=employee_obj, difficulty=str(difficulty), image=image_path, video=video_url,
                pdf="", options=choices,correct_options=answer)
            except Exception as e:
               logger.error(e)

            problem_obj.topics.add(topic_obj)
            problem_obj.save()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error importQuestionsFromExcel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Questions Are Uploaded.<br>Take note of above questions before refreshing the page."
        return False, rows_error


def import_descriptive_from_excel(file_path, employee_obj, topic_obj):
    try:
        wb = xlrd.open_workbook("files/"+file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        return False, "Excel File Read Error"

    rows_error = "Error at following Rows (Sr. No):<br>"

    for i in range(1, sheet.nrows):
        try:
            category_id = "3"   ## descriptive questions

#            description = sheet.cell_value(i, 1)

#            answer = sheet.cell_value(i, 2)

            description = str(sheet.cell_value(i, 1)).strip()

            if len(description) == 0:
                raise Exception('Invalid description provided in question %s in file %s', str(i), str(file_path))

            answer = str(sheet.cell_value(i, 2)).strip()
            try:
                difficulty = int(float(sheet.cell_value(i,3)))
            except ValueError as e:
                raise Exception("Provide Valid Difficulty level")
            except Exception as e:
                difficulty = 1

            if difficulty < 1 or difficulty >3:
                raise Exception("Provide Valid Difficulty Level")

            if len(answer) == 0:
                raise Exception('Invalid answer provided in question %s in file %s', str(i), str(file_path))

            problem_obj = Problem.objects.create(description=description,
                                                 solution=answer,
                                                 category=category_id,
                                                 typed_by=employee_obj,
                                                 difficulty=str(difficulty),
                                                 hint="",
                                                 image=None,
                                                 video=None,
                                                 pdf="")
            problem_obj.topics.add(topic_obj)
            problem_obj.save()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error importDescriptiveQuestionFromExcel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Questions Are Uploaded.<br>Take note of above questions before refreshing the page."
        return False, rows_error


"""
def import_mcq_from_excel(file_path, administrator_obj, topic_obj):
    logger.info("Entered in import_mcq_from_excel in utils.py")
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except:
        return False, "Excel File Read Error"
    rows_error = "Error at following Rows (Sr. No):<br>"
    for i in range(1, sheet.nrows):
        try:
            category_id = "1"

            description = sheet.cell_value(i, 1)
            description = description.strip()

            if len(description) == 0:
                raise Exception('No description provided in question %s in file %s', str(i), str(file_path))

            ans = str(sheet.cell_value(i, 7)).strip().lower()

            if len(ans) == 0:
                raise Exception('No answer provided in question %s in file %s', str(i), str(file_path))

            answer = None

            choice1 = None
            choice1 = str(sheet.cell_value(i, 2)).strip()
            choice2 = None
            choice2 = str(sheet.cell_value(i, 3)).strip()
            choice3 = None
            choice3 = str(sheet.cell_value(i, 4)).strip()
            choice4 = None
            choice4 = str(sheet.cell_value(i, 5)).strip()

            choice_list = []

            if choice1 is not None and len(choice1):
                choice_list.append(choice1)
                if ans == "a":
                    answer = choice1
            elif ans == "a":
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if choice2 is not None and len(choice2):
                choice_list.append(choice2)
                if ans == "b":
                    answer = choice2
            elif ans == "b":
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if choice3 is not None and len(choice3):
                choice_list.append(choice3)
                if ans == "c":
                    answer = choice3
            elif ans == "c":
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if choice4 is not None and len(choice4):
                choice_list.append(choice4)
                if ans == "d":
                    answer = choice4
            elif ans == "d":
                raise Exception('Invalid option chosen as answer in question %s in file %s', str(i), str(file_path))

            if answer is None:
                raise Exception('Invalid answer provided in question %s in file %s', str(i), str(file_path))

            choices = '|'.join(choice_list)

            difficulty = int(float(sheet.cell_value(i, 6)))

            if difficulty < 1 or difficulty > 3:
                raise Exception('Invalid difficulty provided in question %s in file %s', str(i), str(file_path))

#            choice1 = None
#            try:
#                choice1 = Choice.objects.get(value=str(sheet.cell_value(i, 2)))
#            except:
#                choice1 = Choice.objects.create(
#                    value=sheet.cell_value(i, 2))
#            choice2 = None
#            try:
#                choice2 = Choice.objects.get(value=str(sheet.cell_value(i, 3)))
#            except:
#                choice2 = Choice.objects.create(
#                    value=sheet.cell_value(i, 3))
#            choice3 = None
#            try:
#                choice3 = Choice.objects.get(value=str(sheet.cell_value(i, 4)))
#            except:
#                choice3 = Choice.objects.create(
#                    value=sheet.cell_value(i, 4))
#            choice4 = None
#            try:
#                choice4 = Choice.objects.get(value=str(sheet.cell_value(i, 5)))
#            except:
#                choice4 = Choice.objects.create(
#                    value=sheet.cell_value(i, 5))
#
#            difficulty = int(float(sheet.cell_value(i, 6)))
#
#            ans = sheet.cell_value(i, 7)
#
#            answer = None
#            if(ans == "A" or ans == "a"):
#                answer = choice1
#            elif(ans == "B" or ans == "b"):
#                answer = choice2
#            elif(ans == "C" or ans == "c"):
#                answer = choice3
#            elif(ans == "D" or ans == "d"):
#                answer = choice4
#            else:
#                answer = None

            sol = ""
            try:
                sol = sheet.cell_value(i, 8)
            except Exception as e:
                pass

            hint = ""
            image_path = ""
            video_url = None
            # logger.info(category_id,description,choice1,difficulty,answer,sol,hint,image_path,video_url)
            problem_obj = Problem.objects.create(description=str(description.encode("ascii", errors="ignore")), solution=str(sol.encode("ascii", errors="ignore")), hint=hint.encode(
                "ascii", errors="ignore"), category=category_id, typed_by=employee_obj, difficulty=str(difficulty), image=image_path, video=video_url)

            problem_obj.choices.add(choice1)
            problem_obj.choices.add(choice2)
            problem_obj.choices.add(choice3)
            problem_obj.choices.add(choice4)

            problem_obj.right_choices.add(answer)

            problem_obj.topics.add(topic_obj)
            problem_obj.save()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error importQuestionsFromExcel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Questions Are Uploaded.<br>Take note of above questions before refreshing the page."
        return False, rows_error


def import_descriptive_from_excel(file_path, employee_obj, topic_obj):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except:
        return False, "Excel File Read Error"

    rows_error = "Error at following Rows (Sr. No):<br>"

    for i in range(1, sheet.nrows):
        try:
            category_id = "3"

#            description = sheet.cell_value(i, 1)
#
#            answer = sheet.cell_value(i, 2)
            description = str(sheet.cell_value(i, 1)).strip()

            if len(description) == 0:
                raise Exception('Invalid description provided in question %s in file %s', str(i), str(file_path))

            answer = str(sheet.cell_value(i, 2)).strip()

            if len(answer) == 0:
                raise Exception('Invalid answer provided in question %s in file %s', str(i), str(file_path))
            problem_obj = Problem.objects.create(description=description,
                                                 solution=answer,
                                                 category=category_id,
                                                 typed_by=employee_obj,
                                                 difficulty="1",
                                                 hint="",
                                                 image=None,
                                                 video=None)
            problem_obj.topics.add(topic_obj)
            problem_obj.save()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error importDescriptiveQuestionFromExcel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Questions Are Uploaded.<br>Take note of above questions before refreshing the page."
        return False, rows_error


def import_video_from_excel(file_path, employee_obj, topic_obj):
    try:
        wb = xlrd.open_workbook("files/"+file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        return False, "Excel File Read Error"

    rows_error = "Error at following Rows (Sr. No):<br>"

    for i in range(1, sheet.nrows):
        try:
            category_id = "5"

            description = sheet.cell_value(i, 1)

            problem_obj = Problem.objects.create(description=description,
                                                 solution="",
                                                 category=category_id,
                                                 typed_by=employee_obj,
                                                 difficulty="1",
                                                 hint="",
                                                 image=None,
                                                 video=None,
                                                 pdf="")
            problem_obj.topics.add(topic_obj)
            problem_obj.save()

            #TopicProblem.objects.create(problem=problem_obj, topic=topic_obj)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error importDescriptiveQuestionFromExcel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Questions Are Uploaded.<br>Take note of above questions before refreshing the page."
        return False, rows_error

"""
"""


def import_applicants_from_excel(file_path, stream_obj, institute_obj):
    try:
        wb = xlrd.open_workbook("files/"+file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        return False, "Excel File Read Error"

    rows_error = "Error at following Rows (Sr. No):<br>"

    image_path = "pics/default-user.png" 

    for i in range(1, sheet.nrows):
        try:
            category = int(sheet.cell_value(i, 0))
            applicant_name = sheet.cell_value(i, 1)
            email_id = sheet.cell_value(i, 2)

            phone_number = int(sheet.cell_value(i, 3))


            applicant_year_of_passing = int(sheet.cell_value(i, 4))

            applicant_percentage = sheet.cell_value(i, 5)

            applicant_dob = sheet.cell_value(i, 6)
            if str(category) == "2":
                location = str(sheet.cell_value(i, 7))
            else:
                location = str(institute_obj.name)

            applicant_dob = xlrd.xldate.xldate_as_datetime(applicant_dob, wb.datemode)

            dob_datetime_obj = applicant_dob.strftime("%Y-%m-%d")

            applicant_objs_with_email_id = Applicant.objects.filter(
                email_id=str(email_id))
            applicant_objs_with_phone = Applicant.objects.filter(
                phone_number=str(phone_number))

            if (len(applicant_objs_with_phone) == 0 and len(applicant_objs_with_email_id) == 0):

                applicant_obj = Applicant.objects.create(image=image_path,
                                                     name=str(applicant_name),
                                                     email_id=str(email_id),
                                                     phone_number=str(phone_number),
                                                     college_name=institute_obj,
                                                     year_of_passing=str(applicant_year_of_passing),
                                                     percentage=float(
                                                         applicant_percentage),
                                                     is_registered=True,
                                                     stream=stream_obj,
                                                     username=str(phone_number),
                                                     status=None,
                                                     dob=dob_datetime_obj)
                # OTP = sendOTPAtGivenMobile("91"+str(applicant_phonenumber))
                # applicant_obj.set_password(str(OTP))
                if str(category) == "1":
                    applicant_obj.category = APPLICANT_CATEGORY[0][0]
                    applicant.location = location
                else:
                    applicant_obj.category = APPLICANT_CATEGORY[1][0]
                    applicant_obj.location = location
                applicant_obj.applicant_id = applicant_obj.pk
                applicant_obj.set_password("123456")
                applicant_obj.is_registered = True
                applicant_obj.save()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error import_applicant_from_excel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Applicants Are Created."
        return False, rows_error


"""

#def import_applicants_from_excel(file_path, stream_obj, event_obj):
#    try:
#        wb = xlrd.open_workbook("files/"+file_path)
#        sheet = wb.sheet_by_index(0)
#    except Exception as e:
#        return False, "Excel File Read Error"
#
#    rows_error = "Error at following Rows (Sr. No):<br>"
#
#    image_path = "pics/default-user.png"
#    for i in range(1, sheet.nrows):
#        try:
#            category = str(sheet.cell_value(i, 0))
#            print(category)
#            applicant_name = sheet.cell_value(i, 1)
#            email_id = sheet.cell_value(i, 2)
#
#            phone_number = int(sheet.cell_value(i, 3))
#
#
#            applicant_year_of_passing = int(sheet.cell_value(i, 4))
#
#            applicant_percentage = sheet.cell_value(i, 5)
#
#            applicant_dob = sheet.cell_value(i, 6)
#            institute = ""
#            location = ""
#            if str(category) == "2":
#                location = str(sheet.cell_value(i, 7))
#                institute = str(sheet.cell_value(i, 8))
#            else:
#                institute = str(sheet.cell_value(i, 7))
#                location = str(institute)
#
#            applicant_dob = xlrd.xldate.xldate_as_datetime(applicant_dob, wb.datemode)
#
#            dob_datetime_obj = applicant_dob.strftime("%Y-%m-%d")
#
#            applicant_objs_with_email_id = Applicant.objects.filter(
#                email_id=str(email_id))
#            applicant_objs_with_phone = Applicant.objects.filter(
#                phone_number=str(phone_number))
#
#            if (len(applicant_objs_with_phone) == 0 and len(applicant_objs_with_email_id) == 0):
#
#                applicant_obj = Applicant.objects.create(image=image_path,
#                                                     name=str(applicant_name),
#                                                     email_id=str(email_id),
#                                                     phone_number=str(phone_number),
#                                                     college_name=institute,
#                                                     year_of_passing=str(applicant_year_of_passing),
#                                                     percentage=float(
#                                                         applicant_percentage),
#                                                     is_registered=True,
#                                                     stream=stream_obj,
#                                                     username=str(phone_number),
#                                                     status=None,
#                                                     dob=dob_datetime_obj,
#                                                     event=event_obj)
#                # OTP = sendOTPAtGivenMobile("91"+str(applicant_phonenumber))
#                # applicant_obj.set_password(str(OTP))
#                if str(category) == "1":
#                    applicant_obj.category = APPLICANT_CATEGORY[0][0]
#                    applicant_obj.location = location
#                else:
#                    applicant_obj.category = APPLICANT_CATEGORY[1][0]
#                    applicant_obj.location = location
#                applicant_obj.applicant_id = applicant_obj.pk
#                password = "123456"
#                applicant_obj.set_password("123456")
#                #password = password_generator()
#                #applicant_obj.set_password(password)
#                applicant_obj.is_registered = True
#                applicant_obj.save()
#                send_registration_email_to_applicant(applicant_obj,password)
#        except Exception as e:
#            exc_type, exc_obj, exc_tb = sys.exc_info()
#            logger.error("Error import_applicant_from_excel: %s at %s",
#                         str(e), str(exc_tb.tb_lineno))
#            rows_error += str(i)+" "
#
#    if rows_error == "Error at following Rows (Sr. No):<br>":
#        return True, "Successfully"
#    else:
#        rows_error += "<br>Remaining Applicants Are Created."
#        return False, rows_error


def import_applicants_from_excel(file_path, stream_obj, event_obj):
    try:
        wb = xlrd.open_workbook("files/"+file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        return False, "Excel File Read Error"

    rows_error = "Error at following Rows (Sr. No):<br>"

    image_path = "pics/default-user.png"
    errors = []
    for i in range(1, sheet.nrows):
        try:
            category = str(sheet.cell_value(i, 0))
            print(category)
            applicant_name = sheet.cell_value(i, 1)
            email_id = sheet.cell_value(i, 2)

            phone_number = int(sheet.cell_value(i, 3))

            applicant_year_of_passing = int(sheet.cell_value(i, 4))

            applicant_percentage = sheet.cell_value(i, 5)

            applicant_dob = sheet.cell_value(i, 6)
            institute = ""
            location = ""

            if str(category) == "2":
                location = str(sheet.cell_value(i, 7))
                institute = str(sheet.cell_value(i, 8))
            else:
                institute = str(sheet.cell_value(i, 7))
                location = str(institute)

            applicant_dob = xlrd.xldate.xldate_as_datetime(applicant_dob, wb.datemode)

            dob_datetime_obj = applicant_dob.strftime("%Y-%m-%d")

            applicant_objs_with_email_id = Applicant.objects.filter(
                email_id=str(email_id))
            applicant_objs_with_phone = Applicant.objects.filter(
                phone_number=str(phone_number))

            if (len(applicant_objs_with_phone) == 0 and len(applicant_objs_with_email_id) == 0):

                applicant_obj = Applicant.objects.create(image=image_path,
                                                     name=str(applicant_name),
                                                     email_id=str(email_id),
                                                     phone_number=str(phone_number),
                                                     college_name=institute,
                                                     year_of_passing=str(applicant_year_of_passing),
                                                     percentage=float(
                                                         applicant_percentage),
                                                     is_registered=True,
                                                     stream=stream_obj,
                                                     username=str(phone_number),
                                                     status=None,
                                                     dob=dob_datetime_obj,
                                                     event=event_obj)
                # OTP = sendOTPAtGivenMobile("91"+str(applicant_phonenumber))
                # applicant_obj.set_password(str(OTP))
                if str(category) == "1":
                    applicant_obj.category = APPLICANT_CATEGORY[0][0]
                    applicant_obj.location = location
                else:
                    applicant_obj.category = APPLICANT_CATEGORY[1][0]
                    applicant_obj.location = location
                applicant_obj.applicant_id = applicant_obj.pk
                password = "123456"
                applicant_obj.set_password("123456")
                #password = password_generator()
                #applicant_obj.set_password(password)
                applicant_obj.is_registered = True
                applicant_obj.save()
                send_registration_email_to_applicant(applicant_obj,password)
            else:
                errors.append(f'{email_id} already exists')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error import_applicant_from_excel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i)+" "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return errors,True, "Successfully"
    else:
        rows_error += "<br>Remaining Applicants Are Created."
        return errors,False, rows_error




###### Excel Dump Creation for downloading the complete database
def get_value_or_na(input):
    if input is None:
        return "N/A"
    return input


def download_applicant_profiles(applicant_objs):

    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()
    sheet_name = "Applicant Profiles"

    sheet1 = export_nps_wb.add_sheet(
        sheet_name, cell_overwrite_ok=True)

    st = easyxf("align: horiz center; font: bold on")
    i = 0
    sheet1.write(0, i, "Applicant ID", st)
    i += 1
    sheet1.write(0, i, "Applicant Name", st)
    i += 1
    sheet1.write(0, i, "Email", st)
    i += 1
    sheet1.write(0, i, "Contact Number", st)
    i += 1
    sheet1.write(0, i, "Date of birth", st)
    i += 1
    sheet1.write(0, i, "Gender", st)
    i += 1
    sheet1.write(0, i, "Location", st)
    i += 1
    sheet1.write(0, i, "Institute", st)
    i += 1
    sheet1.write(0, i, "Stream", st)
    i += 1
    sheet1.write(0, i, "Specialization", st)
    i += 1
    sheet1.write(0, i, "Percentage", st)
    i += 1
    sheet1.write(0, i, "Graduation Year", st)
    i += 1
    sheet1.write(0, i, "Interview Type", st)
    i += 1
    sheet1.write(0, i, "Event", st)
    i += 1
    sheet1.write(0, i, "Adhar Number", st)
    i += 1
    sheet1.write(0, i, "Pan Number", st)
    i += 1
    sheet1.write(0, i, "Current Company", st)
    i += 1
    sheet1.write(0, i, "Current Designation", st)
    i += 1
    sheet1.write(0, i, "Current CTC", st)
    i += 1

    row = 1
    for applicant_obj in applicant_objs:
        try:
            i = 0
            sheet1.write(row, i, get_value_or_na(applicant_obj.applicant_id))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.name))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.email_id))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.phone_number))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.dob.strftime("%d/%m/%Y")))
            i += 1
            if get_value_or_na(applicant_obj.gender) == "N/A":
                sheet1.write(row, i, "N/A")
            elif applicant_obj.gender == "1":
                sheet1.write(row, i, "Male")
            elif applicant_obj.gender == "2":
                sheet1.write(row, i, "Female")
            else:
                sheet1.write(row, i, "Other")
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.location))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.college_name))
            i += 1
            if applicant_obj.stream:
                sheet1.write(row, i, get_value_or_na(applicant_obj.stream.name))
            else:
                sheet1.write(row, i, "N/A")
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.specialization))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.percentage))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.year_of_passing))
            i += 1
            if get_value_or_na(applicant_obj.category) == "N/A":
                sheet1.write(row, i, "N/A")
            elif applicant_obj.category == "1":
                sheet1.write(row, i, "Campus")
            elif applicant_obj.gender == "2":
                sheet1.write(row, i, "Walk-in")
            else:
                sheet1.write(row, i, "Posting")
            i += 1
            if applicant_obj.event:
                sheet1.write(row, i, get_value_or_na(applicant_obj.event.name))
            else:
                sheet1.write(row, i, "N/A")
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.id_proof_adhaar_number))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.id_proof_pan_number))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.current_company))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.current_designation))
            i += 1
            sheet1.write(row, i, get_value_or_na(applicant_obj.current_ctc))
            i += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error download_applicant_profiles:%s at %s", str(
                e), str(exc_tb.tb_lineno))
            pass
        row += 1

    filename = "ApplicantProfiles.xls"
    export_nps_wb.save(settings.MEDIA_ROOT + filename)
    return "/files/" + str(filename)


def download_quiz_excel(quiz_objs):

    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()
    sheet_name = "Quizzes"

    sheet1 = export_nps_wb.add_sheet(
        sheet_name, cell_overwrite_ok=True)

    st = easyxf("align: horiz center; font: bold on")
    i = 0
    sheet1.write(0, i, "Sr. No.", st)
    i += 1
    sheet1.write(0, i, "Quiz Name", st)
    i += 1
    sheet1.write(0, i, "Quiz ID", st)
    i += 1
    sheet1.write(0, i, "Instructions", st)
    i += 1
    sheet1.write(0, i, "No. of Attempts", st)
    i += 1
    sheet1.write(0, i, "No. Quiz Sections", st)
    i += 1

    row = 1
    for quiz_obj in quiz_objs:
        try:
            i = 0
            sheet1.write(row, i, str(row))
            i += 1
            sheet1.write(row, i, get_value_or_na(quiz_obj.title))
            i += 1
            sheet1.write(row, i, get_value_or_na(quiz_obj.pk))
            i += 1
            sheet1.write(row, i, get_value_or_na(quiz_obj.instruction))
            i += 1
            sheet1.write(row, i, get_value_or_na(len(quiz_obj.quizstatus_set.all())))
            i += 1
            sheet1.write(row, i, get_value_or_na(len(quiz_obj.quizsection_set.all())))
            i += 1

            quiz_sections = quiz_obj.quizsection_set.all()

            for quiz_section in quiz_sections:

                old_i = i

                sheet1.write(0, i, "Quiz section name")
                i += 1
                sheet1.write(0, i, "Quiz section weightage")
                i += 1
                sheet1.write(0, i, "Quiz section time")
                i += 1
                sheet1.write(0, i, "Quiz section type")
                i += 1
                sheet1.write(0, i, "No of questions")
                i += 1
                sheet1.write(0, i, "No of easy questions")
                i += 1
                sheet1.write(0, i, "No of medium questions")
                i += 1
                sheet1.write(0, i, "No of hard questions")
                i += 1
                sheet1.write(0, i, "Positive Threshold")
                i += 1
                sheet1.write(0, i, "Negative Threshold")
                i += 1

                i = old_i
                sheet1.write(row, i, get_value_or_na(quiz_section.topic.name))
                i += 1
                sheet1.write(row, i, get_value_or_na(quiz_section.weightage))
                i += 1
                sheet1.write(row, i, get_value_or_na(quiz_section.time))
                i += 1
                if quiz_section.is_quiz_section_static:
                    sheet1.write(row, i, get_value_or_na("Static"))
                else:
                    sheet1.write(row, i, get_value_or_na("Adaptive"))
                i += 1

                sheet1.write(row, i, get_value_or_na(quiz_section.no_questions))
                i += 1

                if quiz_section.is_quiz_section_static:
                    sheet1.write(row, i, get_value_or_na(quiz_section.easy_questions))
                    i += 1
                    sheet1.write(row, i, get_value_or_na(quiz_section.medium_questions))
                    i += 1
                    sheet1.write(row, i, get_value_or_na(quiz_section.hard_questions))
                    i += 1
                    sheet1.write(row, i, "N/A")
                    i += 1
                    sheet1.write(row, i, "N/A")
                    i += 1
                else:
                    sheet1.write(row, i, "N/A")
                    i += 1
                    sheet1.write(row, i, "N/A")
                    i += 1
                    sheet1.write(row, i, "N/A")
                    i += 1
                    sheet1.write(row, i, get_value_or_na(quiz_section.positive_threshold))
                    i += 1
                    sheet1.write(row, i, get_value_or_na(quiz_section.negative_threshold))
                    i += 1

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error download_quiz_:%s at %s", str(
                e), str(exc_tb.tb_lineno))
            pass
        row += 1

    filename = "Quizzes.xls"
    export_nps_wb.save(settings.MEDIA_ROOT + filename)
    return "/files/" + str(filename)


def download_topic_excel(topic_objs):

    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()
    sheet_name = "Topics"

    sheet1 = export_nps_wb.add_sheet(
        sheet_name, cell_overwrite_ok=True)

    st = easyxf("align: horiz center; font: bold on")
    i = 0
    sheet1.write(0, i, "Sr. No.", st)
    i += 1
    sheet1.write(0, i, "Topic Name", st)
    i += 1
    sheet1.write(0, i, "Category", st)
    i += 1
    sheet1.write(0, i, "No. of questions", st)
    i += 1
    sheet1.write(0, i, "No. of Easy Questions", st)
    i += 1
    sheet1.write(0, i, "No. of Medium Questions", st)
    i += 1
    sheet1.write(0, i, "No. of Hard Questions", st)
    i += 1

    row = 1
    for topic_obj in topic_objs:
        try:
            i = 0
            sheet1.write(row, i, str(row))
            i += 1
            sheet1.write(row, i, get_value_or_na(topic_obj.name))
            i += 1
            sheet1.write(row, i, get_value_or_na(topic_obj.get_category()))
            i += 1
            sheet1.write(row, i, get_value_or_na(topic_obj.no_questions()))
            i += 1
            sheet1.write(row, i, get_value_or_na(topic_obj.no_easy_question()))
            i += 1
            sheet1.write(row, i, get_value_or_na(topic_obj.no_medium_question()))
            i += 1
            sheet1.write(row, i, get_value_or_na(topic_obj.no_hard_question()))
            i += 1

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error download_topic:%s at %s", str(
                e), str(exc_tb.tb_lineno))
            pass
        row += 1

    filename = "Topics.xls"
    export_nps_wb.save(settings.MEDIA_ROOT + filename)
    return "/files/" + str(filename)



### Download Question Bank Excel Dump Topic Wise

def generate_topic_problem_excel(topic):
    from datetime import datetime
    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()

    objective_problems_in_topic = Problem.objects.filter(topics__in=[topic], category__in=['1', '2'])
    subjective_problems_in_topic = Problem.objects.filter(topics__in=[topic], category='3')
    video_problems_in_topic = Problem.objects.filter(topics__in=[topic], category='5')

    st = easyxf("align: horiz center; font: bold on")

    sheet1 = export_nps_wb.add_sheet(
        "Objective Questions", cell_overwrite_ok=True)
    sheet2 = export_nps_wb.add_sheet(
            "Subjective Questions", cell_overwrite_ok=True)
    sheet3 = export_nps_wb.add_sheet(
            "Video Questions", cell_overwrite_ok=True)

    sheet1.write(0, 0, "Sr. No.", st)
    sheet2.write(0, 0, "Sr. No.", st)
    sheet3.write(0, 0, "Sr. No.", st)

    sheet1.write(0, 1, "Question Description", st)
    sheet2.write(0, 1, "Question Description", st)
    sheet3.write(0, 1, "Question Description", st)

    sheet1.write(0, 2, "Option A", st)
    sheet2.write(0, 2, "Answer", st)

    sheet1.write(0, 3, "Option B", st)
    sheet1.write(0, 4, "Option C", st)
    sheet1.write(0, 5, "Option D", st)
    sheet1.write(0, 6, "Difficulty", st)
    sheet1.write(0, 7, "Correct Options", st)
    sheet1.write(0, 8, "Explanation", st)

    row_num = 1
    for problem in objective_problems_in_topic:
        sheet1.write(row_num, 0, str(row_num))
        sheet1.write(row_num, 1, problem.description)

        options = problem.get_option_list()
        correct_options = problem.get_correct_option_list()
        correct_option_str = []
        extra_options = []
        col_num = 2
        for option in options:
            if col_num<5:
                sheet1.write(row_num, col_num, option)
                col_num += 1
            else:
                extra_options.append(option)
            if option in correct_options:
                correct_option_str.append(chr(ord('a')+col_num-2))

        sheet1.write(row_num, 5, ','.join(extra_options))
        sheet1.write(row_num, 6, problem.difficulty)
        sheet1.write(row_num, 7, str(','.join(correct_option_str)))

        if problem.solution:
            sheet1.write(row_num, 8, problem.solution)

        row_num += 1

    row_num = 1
    for problem in subjective_problems_in_topic:
        sheet2.write(row_num, 0, str(row_num))
        sheet2.write(row_num, 1, problem.description)

        if problem.solution:
            sheet2.write(row_num, 2, problem.solution)

        row_num += 1

    row_num = 1
    for problem in video_problems_in_topic:
        sheet3.write(row_num, 0, str(row_num))
        sheet3.write(row_num, 1, problem.description)
        row_num += 1

    filename = topic.name + " - Problems - " + str(datetime.now().strftime("%d-%m-%Y %H:%M")) + ".xls"
    export_nps_wb.save(settings.MEDIA_ROOT + filename)
    file_path = "/files/" + str(filename)

    return file_path



###### Consolidated Downloading of videos


def download_consolidated_videos(file_name, start_date, end_date):

    file_path = None
    # start_date = None
    # end_date = None

    print(start_date, end_date)

    try:

        import os
        import datetime
        if start_date is None or end_date is None:
            quiz_status_list = QuizStatus.objects.filter(is_processed=True)
        else:
            quiz_status_list = QuizStatus.objects.filter(is_processed=True, completion_date__range=[start_date, end_date])
            # comment below line to go to the fetch file structure wise stored videos
            start_date = None

        if start_date is None or end_date is None:
            video_list = []
            for quiz_status in quiz_status_list:
                if quiz_status.video != '[]':
                    video_list.append(settings.MEDIA_ROOT + quiz_status.video)

            try:
                os.system("rm -rf " + settings.MEDIA_ROOT + file_name.split('.')[0] + "/")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- clearing folder: %s at %s", e, str(exc_tb.tb_lineno))

            try:
                os.system("rm " + settings.MEDIA_ROOT + file_name)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- clearing zip file: %s at %s", e, str(exc_tb.tb_lineno))

            #try:
            #    os.system("touch " + settings.MEDIA_ROOT + file_name)
            #except Exception as e:
            #    exc_type, exc_obj, exc_tb = sys.exc_info()
            #    logger.error("download_consolidated_videos --- clearing zip file: %s at %s", e, str(exc_tb.tb_lineno))


            try:
                os.system("mkdir " + settings.MEDIA_ROOT+file_name.split('.')[0])
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- creating folder: %s at %s", e, str(exc_tb.tb_lineno))

            target_folder = settings.MEDIA_ROOT + file_name.split('.')[0]

            for video_url in video_list:
                try:
                    os.system("cp " + video_url + " " + target_folder + "/" + video_url.split('/')[-1])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("download_consolidated_videos --- copying video: %s at %s", e, str(exc_tb.tb_lineno))

            file_path = '/files/' + file_name

            if os.path.exists(target_folder) and os.path.isdir(target_folder):
                if not os.listdir(target_folder):
                    print("Directory is empty")
                    return -1
                else:
                    print("Directory is not empty")
            else:
                print("Given Directory don't exists")
                return -1

            try:
                os.system("cd " + target_folder + "&& zip ../" + file_name + " *")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- zipping folder: %s at %s", e, str(exc_tb.tb_lineno))
                file_path = None
        else:

            try:
                os.system("rm -rf " + settings.MEDIA_ROOT + file_name.split('.')[0] + "/")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- clearing folder: %s at %s", e, str(exc_tb.tb_lineno))


            try:
                os.system("rm " + settings.MEDIA_ROOT + file_name)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- clearing zip file: %s at %s", e, str(exc_tb.tb_lineno))

            try:
                os.system("mkdir " + settings.MEDIA_ROOT + file_name.split('.')[0])
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- creating folder: %s at %s", e, str(exc_tb.tb_lineno))

            target_folder = settings.MEDIA_ROOT + file_name.split('.')[0]

            current_date = start_date

            while current_date <= end_date:

                year = str(current_date.year)
                month = str(current_date.month)
                day = str(current_date.day)

                current_folder = settings.MEDIA_ROOT + year + "/" + month + "/" + day + "/consolidated-videos/."

                print(current_folder)
                try:
                    os.system("cp -a " + current_folder + " " + target_folder + "/")
                    print("WORKED")
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("download_consolidated_videos --- copying video: %s at %s", e, str(exc_tb.tb_lineno))

                current_date = current_date + datetime.timedelta(days=1)

            file_path = '/files/' + file_name
            try:
                os.system("cd " + target_folder + "&& zip ../" + file_name + " *")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("download_consolidated_videos --- zipping folder: %s at %s", e, str(exc_tb.tb_lineno))
                file_path = None


        try:
            os.system("sudo rm -rf " + settings.MEDIA_ROOT + file_name.split('.')[0] + "/")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("download_consolidated_videos --- clearing folder: %s at %s", e, str(exc_tb.tb_lineno))

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("assign_applicant_course: %s at %s", e, str(exc_tb.tb_lineno))

    return file_path


def send_message_to_applicant(applicant_obj, content):

    try:
        phone_number = applicant_obj.phone_number

        content = content.replace("{{applicant_name}}", applicant_obj.name)
        if applicant_obj.event is not None:
            content = content.replace("{{event_name}}", applicant_obj.event.name)
        else:
            content = content.replace("{{event_name}}", "None")
        content = content.replace("{{phone_number}}", applicant_obj.phone_number)
        content = content.replace("{{email_id}}", applicant_obj.email_id)

        message = str(content)

        logger.info(message)

        url = "https://www.fast2sms.com/dev/bulk"

        api_key = "enter the api key here"

        querystring = {"authorization": api_key, "sender_id": "FSTSMS", "message": str(message), "language": "english",
                       "route": "p", "numbers": str(phone_number)}

        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        logger.info(response.text)

        if (response):
            logger.info("Message Sent Successfully to " + applicant_obj.name)
        else:
            logger.info("Message Failed for " + applicant_obj.name)
    except Exception as e:
        logger.error("Message error %s", e)




def get_all_things_about_quiz(applicant_id , quiz_status_id):
    response = {}
    from datetime import datetime, timedelta
    try:
             
        applicant_id = applicant_id
        applicant_obj = Applicant.objects.get(pk=int(applicant_id))
        quiz_status_obj = QuizStatus.admin_objects.get(
            pk=int(quiz_status_id))
   
        if quiz_status_obj.is_deleted:
            response['is_deleted'] = True
        else:
            response['is_deleted'] = False




        quiz_result_obj = QuizResult.objects.get(applicant=applicant_obj,
                                                 quiz=quiz_status_obj.quiz)

        generate_applicant_quiz_result(applicant_obj,
                                       quiz_status_obj.quiz,
                                       QuizResult)


        quiz_result_problems_list = get_quiz_result_problems_list(applicant_obj,
                                                     quiz_status_obj.quiz)
        #if len(quiz_status_obj.get_attempted_video_problem())>0:

        

        if "VID" in quiz_status_obj.quiz.type_of_questions():
            response["recruiter_remark"] = quiz_result_obj.recruiter_remark
        else:
            response["recruiter_remark"] = -1

        quiz_result = json.loads(quiz_result_obj.result)
        for quiz_section in quiz_result['quiz_section_result_list']:

            try:
                quiz_section_obj = QuizSection.objects.get(pk=int(quiz_section['id']))


                if quiz_section_obj.is_quiz_section_static:
                    quiz_section['allotted'] = {
                        'total': quiz_section_obj.no_questions,
                        'easy': quiz_section_obj.easy_questions,
                        'medium': quiz_section_obj.medium_questions,
                        'hard': quiz_section_obj.hard_questions
                    }
                    quiz_section['static'] = True
                else:
                    quiz_section['allotted'] = {
                        'total': quiz_section_obj.no_questions,
                        'easy': "NA*",
                        'medium': "NA*",
                        'hard': "NA*",
                    }
                    quiz_section['static'] = False

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("Error ApplicantReportCard: %s at %s",str(e), str(exc_tb.tb_lineno))

                quiz_section['allotted'] = {
                    'total': 'N/A',
                    'easy': 'N/A',
                    'medium': 'N/A',
                    'hard': 'N/A'
                }
        quiz_result["applicant_percentile"] = quiz_result_obj.get_applicant_percentile()

        response['section_timing'] = []
        if quiz_status_obj.is_deleted:
            data = json.loads(quiz_status_obj.quiz_history)
            response['section_timing'] = data.get('timings')
        else:
            quiz_section_results = QuizSectionResult.objects.filter(quiz_section__quiz=quiz_status_obj.quiz, applicant=applicant_obj)

            for quiz_section_result in quiz_section_results:
                response['section_timing'].append({
                    'section_name': quiz_section_result.quiz_section.topic.name,
                    'time_spent': quiz_section_result.get_duration()
                })

        response['sessions'] = []

        try:
            session_times = json.loads(quiz_status_obj.time_stamps)
            response['sessions'] = session_times
        except:
            pass

                #response['quiz_assign_time'] = quiz_status_obj.assigned_date.strftime('%d/%m/%Y, %I:%M %p')
        try:
            quiz_assign_time = quiz_status_obj.assigned_date + timedelta(hours=5, minutes=30)
        except Exception as e :
            response['quiz_assign_time'] = "Not Captured"
            logger.error("Error in get quiz result: %s", str(e))
        response['quiz_assign_time'] = quiz_assign_time.strftime('%d/%m/%Y, %I:%M %p')
        response['quiz_start_time'] = quiz_status_obj.get_quiz_start_time()
        response['quiz_end_time'] = quiz_status_obj.get_completion_date()

        if response['quiz_start_time'] == "N/A" and response['quiz_end_time'] == "N/A":
            response["status_code"] = 201
        else:
            response['status_code'] = 200

        response["quiz_result"] = quiz_result
            #response["status_code"] = 200
        response["status_message"] = "SUCCESS"
        response["problems_list"] = quiz_result_problems_list
        return response
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error GetQuizResultAPI: %s at %s",
                     str(e), str(exc_tb.tb_lineno))
        return response
        
