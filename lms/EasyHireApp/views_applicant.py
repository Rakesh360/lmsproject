from django.shortcuts import render, redirect, HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth import logout, authenticate, login


from EasyHireApp.models import *
from EasyHireApp.utils import *
from EasyHireApp.constants import *

import base64
import logging
import threading
import sys

logger = logging.getLogger(__name__)



def ApplicantLoginPage(request):
    if is_user_authenticated(request):
        return redirect("/")
    else:
        return render(request, 'EasyHireApp/login.html')

def ApplicantDashboard(request):
    if is_user_authenticated(request):
        applicant_obj = Applicant.objects.get(username=request.user.username)
        # quiz_status = applicant_obj.get_assigned_quiz_status()
        quiz_status_list = QuizStatus.objects.filter(applicant=applicant_obj).order_by('assigned_date')
        return render(request, "EasyHireApp/applicant-dashboard.html", {
                "applicant_obj":applicant_obj,
                # "quiz_status":quiz_status,
                "quiz_status_list": quiz_status_list,
        })
    else:
        return redirect("/login")

def ApplicantSignupPage(request):
    if is_user_authenticated(request):
        if request.user.role == "1":
            return redirect("/applicant/dashboard")
        else:
            return redirect("/administrator/dashboard")
    else:
        app_config = AppConfig.objects.all()[0]
        INSTITUTION_LIST = Institute.objects.filter(is_activated=True)
        #PROOF_OF_DOCUMENTS = IdentityProof.objects.all()
        STREAM_LIST = Stream.objects.all()
        EVENT_LIST = Event.objects.filter(is_activated=True)
        DEPARTMENT_LIST = Department.objects.all()
        return render(request, "EasyHireApp/signup.html", {
            "YEAR_OF_PASSING": YEAR_OF_PASSING,
            "STREAM_LIST": STREAM_LIST,
            "INSTITUTION_LIST": INSTITUTION_LIST,
            #"PROOF_OF_DOCUMENTS": PROOF_OF_DOCUMENTS,
            "app_config": app_config,
            "EVENT_LIST":EVENT_LIST,
            "DEPARTMENT_LIST":DEPARTMENT_LIST,
        })
"""
class ApplicantSignUpAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data["data"]
            file = request.data["file"]
            json_data = json.loads(data)

            resume_path = default_storage.save("resumes/"+file.name.replace(" ", ""),
                                               ContentFile(file.read()))

            applicant_image = json_data["applicant_image"]
            applicant_phonenumber = json_data["applicant_phonenumber"]
            image_name = str(applicant_phonenumber)+"_pic.png"

            format, imgstr = applicant_image.split(';base64,')
            ext = format.split('/')[-1]
            # You can save this as file instance.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

            image_path = default_storage.save("pics/"+image_name, data)

            applicant_name = json_data["applicant_name"]
            applicant_emailid = json_data["applicant_emailid"]
            applicant_dob = json_data["applicant_dob"]
            applicant_college = json_data["applicant_college"]
            applicant_year_of_passing = json_data["applicant_year_of_passing"]
            applicant_stream = json_data["applicant_stream"]
            applicant_percentage = json_data["applicant_percentage"]
            applicant_hiring_process_id = json_data["applicant_hiring_process_id"]
            applicant_category = json_data["applicant_category"]
            #is_id_proof_required = json_data["is_id_proof_required"]
            #type_of_id_proof = json_data["type_of_id_proof"]
            #proof_id_number = json_data["proof_id_number"]
            applicant_location = json_data["applicantLocation"]
            id_proof_adhaar_number = json_data["id_proof_adhaar_number"]
            id_proof_pan_number = json_data["id_proof_pan_number"]
            applicant_department = json_data["applicant_department"]
            applicant_gender = json_data["applicant_gender"] 

            logger.info(json_data)
            if applicant_category == "1":
                applicant_location = "Campus"
            elif applicant_category == "3":
                applicant_location = "Posting"


            applicant_event = json_data["applicant_event"]
            applicant_objs_with_email_id = Applicant.objects.filter(
                email_id=str(applicant_emailid))
            applicant_objs_with_phone = Applicant.objects.filter(
                phone_number=str(applicant_phonenumber))

            applicant_aadhar_obj = Applicant.objects.filter(id_proof_adhaar_number=str(id_proof_adhaar_number))
            if( len(applicant_aadhar_obj) > 0):
                response["status_code"] = 305
                response["status_message"] = "Applicant matching details already exists"
            elif (len(applicant_objs_with_phone) == 0 and len(applicant_objs_with_email_id) == 0):

                dob_datetime_obj = datetime.datetime.strptime(
                    str(applicant_dob), "%Y-%m-%d")

                #institute = Institute.objects.get(pk=int(applicant_college))
                logger.info(applicant_stream)
                stream = Stream.objects.get(pk=int(applicant_stream))

                logger.info(applicant_event)
                event = Event.objects.get(pk=int(applicant_event))

                logger.info(applicant_department)
                department = Department.objects.get(pk=int(applicant_department))

                applicant_obj = Applicant.objects.create(image=image_path,
                                                     name=ascii_string(
                                                         applicant_name),
                                                     email_id=ascii_string(
                                                         applicant_emailid),
                                                     phone_number=ascii_string(
                                                         applicant_phonenumber),
                                                     dob=dob_datetime_obj,
                                                     college_name=applicant_college,
                                                     year_of_passing=ascii_string(
                                                         applicant_year_of_passing),
                                                     stream=stream,
                                                     percentage=float(
                                                         applicant_percentage),
                                                     is_registered=True,
                                                     username=ascii_string(
                                                         applicant_phonenumber),
                                                     status=None,
                                                     resume=resume_path,
                                                     category=applicant_category,
                                                     location=str(applicant_location),
                                                     id_proof_adhaar_number=str(id_proof_adhaar_number),
                                                     event=event, department=department, gender=applicant_gender)

                if id_proof_pan_number !="":
                    applicant_obj.id_proof_pan_number = id_proof_pan_number
                    applicant_obj.save()

                # OTP = sendOTPAtGivenMobile("91"+str(applicant_phonenumber))
                # applicant_obj.set_password(str(OTP))
                #applicant_obj.set_password("123456")
                password = str(applicant_phonenumber) #password_generator()
                applicant_obj.set_password(str(password))
                applicant_obj.is_registered = True
                applicant_obj.save()
                send_registration_email_to_applicant(applicant_obj, password)
                send_registration_msg_to_applicant(applicant_obj,password)

                try:
                    applicant_event_quiz = json_data["applicant_event_quiz"]
                    if(applicant_event_quiz != "none"):
                        event_obj = QuizSection.objects.get(pk=int(applicant_event_quiz))
                        logger.info("QuizSection %s", event_obj)
                        quiz_obj = event_obj.quiz
                        try:
                            quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
                                                                     quiz=quiz_obj)
                        except Exception as e:
                            quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
                                                                        quiz=quiz_obj)

                        quiz_status_obj.time_remaining = -1
                        quiz_status_obj.save()
                        applicant_obj.clear_attempted_quiz(quiz_obj)
                        applicant_obj.status = APPLICANT_AT_QUIZ
                        applicant_obj.attempted_datetime = timezone.now()
                        applicant_obj.is_rejected = False
                        applicant_obj.is_approved = True
                        applicant_obj.save()
                except Exception as e:
                    logger.error("Auto Assign Quiz: %s",e)
                    pass

                response["status_code"] = 200
                response["status_message"] = "Applicant registration done successfully."
            else:
                response["status_code"] = 405
                response["status_message"] = "Applicant matching details already exists"
        except Exception as e:
            response["status_message"] = "Internal Server Error"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ApplicantSignUpAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))

        return Response(data=response)

ApplicantSignUp = ApplicantSignUpAPI.as_view()
"""

class ApplicantSignUpAPI(APIView):
    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        response["status_message"] = "Invalid Server Error"
        try:
            data = request.data["data"]
            file = request.data["file"]
            json_data = json.loads(data)
            resume_path = default_storage.save("resumes/"+file.name.replace(" ", ""),
                                               ContentFile(file.read()))
            applicant_image = json_data["applicant_image"]
            applicant_phonenumber = json_data["applicant_phonenumber"]
            image_name = str(applicant_phonenumber)+"_pic.png"
            format, imgstr = applicant_image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            image_path = default_storage.save("pics/"+image_name, data)
            applicant_name = json_data["applicant_name"]
            applicant_emailid = json_data["applicant_emailid"]
            applicant_dob = json_data["applicant_dob"]
            applicant_hiring_process_id = json_data["applicant_hiring_process_id"]
            id_proof_adhaar_number = json_data["id_proof_adhaar_number"]
            id_proof_pan_number = json_data["id_proof_pan_number"]
            applicant_location = json_data["applicantLocation"]
            applicant_gender = json_data["applicant_gender"]
            applicant_event_quiz = json_data["applicant_event_quiz"]
            applicant_event = json_data["applicant_event"]
            applicant_category = json_data["applicant_category"]
            #logger.info(json_data)
            applicant_objs_with_email_id = Applicant.objects.filter(
                email_id=str(applicant_emailid))
            applicant_objs_with_phone = Applicant.objects.filter(
                phone_number=str(applicant_phonenumber))
            applicant_aadhar_obj = Applicant.objects.filter(
                id_proof_adhaar_number=str(id_proof_adhaar_number))
            if(len(applicant_aadhar_obj) > 0):
                response["status_code"] = 305
                response["status_message"] = "Applicant matching details already exists"
            elif (len(applicant_objs_with_phone) == 0 and len(applicant_objs_with_email_id) == 0):
                dob_datetime_obj = datetime.datetime.strptime(
                    str(applicant_dob), "%Y-%m-%d")
                event = Event.objects.get(pk=int(applicant_event))
                if applicant_category == "1":
                    applicant_college = json_data["applicant_college"]
                    applicant_year_of_passing = json_data["applicant_year_of_passing"]
                    applicant_stream = json_data["applicant_stream"]
                    applicant_percentage = json_data["applicant_percentage"]
                    applicant_department = json_data["applicant_department"]
                    applicant_specialization = json_data["applicant_specialization"]
                    stream = Stream.objects.get(pk=int(applicant_stream))
                    department = Department.objects.get(
                        pk=int(applicant_department))
                    applicant_obj = Applicant.objects.create(image=image_path,
                                                             name=ascii_string(
                                                                 applicant_name),
                                                             email_id=ascii_string(
                                                                 applicant_emailid),
                                                             phone_number=ascii_string(
                                                                 applicant_phonenumber),
                                                             dob=dob_datetime_obj,
                                                             college_name=applicant_college,
                                                             year_of_passing=ascii_string(
                                                                 applicant_year_of_passing),
                                                             stream=stream,
                                                             percentage=float(
                                                                 applicant_percentage),
                                                             is_registered=True,
                                                             username=ascii_string(
                                                                 applicant_phonenumber),
                                                             status=None,
                                                             resume=resume_path,
                                                             category=applicant_category,
                                                             location=str(
                                                                 applicant_location),
                                                             event=event, department=department,
                                                             gender=applicant_gender,specialization=str(applicant_specialization))
                elif applicant_category == "2":
                    applicant_current_company = json_data["applicant_current_company"]
                    applicant_current_ctc = json_data["applicant_current_ctc"]
                    applicant_current_designation = json_data["applicant_current_designation"]
                    applicant_department = json_data["applicant_department"]
                    department = Department.objects.get(
                        pk=int(applicant_department))
                    applicant_obj = Applicant.objects.create(image=image_path,
                                                             name=ascii_string(
                                                                 applicant_name),
                                                             email_id=ascii_string(
                                                                 applicant_emailid),
                                                             phone_number=ascii_string(
                                                                 applicant_phonenumber),
                                                             dob=dob_datetime_obj,
                                                             stream=None,
                                                             is_registered=True,
                                                             username=ascii_string(
                                                                 applicant_phonenumber),
                                                             status=None,
                                                             resume=resume_path,
                                                             category=applicant_category,
                                                             location=str(
                                                                 applicant_location),
                                                             event=event,
                                                             department=department,
                                                             gender=applicant_gender,
                                                             current_company=ascii_string(
                                                                 applicant_current_company),
                                                             current_ctc=ascii_string(
                                                                 applicant_current_ctc),
                                                             current_designation=ascii_string(applicant_current_designation))
                if id_proof_pan_number != "":
                    applicant_obj.id_proof_pan_number = id_proof_pan_number
                    applicant_obj.save()
                if id_proof_adhaar_number != "":
                    applicant_obj.id_proof_adhaar_number = str(id_proof_adhaar_number)
                    applicant_obj.save()
                password = str(applicant_phonenumber)  # password_generator()
                applicant_obj.set_password(str(password))
                applicant_obj.is_registered = True
                applicant_obj.save()
                #send_registration_email_to_applicant(applicant_obj, password)
                send_registration_msg_to_applicant(applicant_obj, password)
                #save_applicant_data_at_irecruit(applicant_obj)
                try:
                    if(applicant_event_quiz != "none"):
                        event_obj = QuizSection.objects.get(
                            pk=int(applicant_event_quiz))
                        logger.info("QuizSection %s", event_obj)
                        quiz_obj = event_obj.quiz
                        try:
                            quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
                                                                     quiz=quiz_obj)
                        except Exception as e:
                            quiz_status_obj = QuizStatus.objects.create(applicant=applicant_obj,
                                                                        quiz=quiz_obj)
                        quiz_status_obj.time_remaining = -1
                        quiz_status_obj.save()
                        applicant_obj.clear_attempted_quiz(quiz_obj)
                        applicant_obj.status = APPLICANT_AT_QUIZ
                        applicant_obj.attempted_datetime = timezone.now()
                        applicant_obj.is_rejected = False
                        applicant_obj.is_approved = True
                        applicant_obj.save()
                        send_quiz_assigned_msg_to_applicant(applicant_obj,quiz_obj)
                except Exception as e:
                    logger.error("Auto Assign Quiz: %s", e)
                    pass
                response["status_code"] = 200
                response["status_message"] = "Applicant registration done successfully."
                # content = "Dear {{applicant_name}}, you have successfully registered to Macleods EasyHire. Stay tuned\
                #  for further updates!"
                # send_message_to_applicant(applicant_obj, content)
            else:
                response["status_code"] = 405
                response["status_message"] = "Applicant matching details already exists"
        except Exception as e:
            response["status_message"] = "Internal Server Error"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ApplicantSignUpAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))
        return Response(data=response)


ApplicantSignUp = ApplicantSignUpAPI.as_view()

def ApplicantSignUpSuccess(request):
    return render(request, "EasyHireApp/success-registered.html", {})


def ApplicantVerification(request):
    response = {}
    response["status_code"] = 500
    response["status_message"] = "Internal Server Error"
    response["is_registered"] = False
    try:
        if request.method == "GET":
            phone_number = request.GET["phone_number"]
            email_id = request.GET["email_id"]

            applicant_objs_based_on_email = Applicant.objects.filter(
                email_id=email_id)
            applicant_objs_based_on_phone = Applicant.objects.filter(
                phone_number=ascii_string(phone_number))

            logger.info(applicant_objs_based_on_email)
            logger.info(applicant_objs_based_on_phone)

            response["status_code"] = 200
            response["status_message"] = "Authorized"

            if len(applicant_objs_based_on_email) > 0 or len(applicant_objs_based_on_phone) > 0:
                response["is_registered"] = True
                return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid request"
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    except Exception as e:
        logger.error(e)
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

"""def ApplicantAuthentication(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error. Please try again later.",
        "is_registered": False
    }
    try:
        if request.method == "POST":

            if is_user_authenticated(request):
                if request.user.role == "1":
                    return redirect("/applicant/dashboard")
                else:
                    return redirect("/administrator/manage-applicant")

            data = request.POST["data"]
            json_data = json.loads(data)
            username = json_data["username"]
            password = json_data["password"]

            applicant_objs = Applicant.objects.filter(username=username)
            if applicant_objs[0].is_applicant_online == False:
                if len(applicant_objs) > 0:
                    applicant_objs[0].is_applicant_online = True
                    applicant_objs[0].save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    response["status_code"] = 200
                    response["status_message"] = "SUCCESS"
                    response["role"] = request.user.role
                else:
                    response["status_code"] = 405
                    response["status_message"] = "Unauthorized user"
            else:
                response["status_code"] = 305
                response["status_message"] = "Session is running."
    except Exception as e:
        logger.error("ApplicantAuthentication: "+str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)"""

def ApplicantAuthentication(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error. Please try again later.",
        "is_registered": False
    }
    try:
        if request.method == "POST":
            if is_user_authenticated(request):
                if request.user.role == "1":
                    return redirect("/applicant/dashboard")
                else:
                    return redirect("/administrator/manage-applicant")
            data = request.POST["data"]
            json_data = json.loads(data)
            username = json_data["username"]
            password = json_data["password"]
            try:
                applicant_objs = Applicant.objects.get(username=username)
                time_difference = (
                    timezone.now() - applicant_objs.last_attempt_datetime).seconds
                if int(time_difference) >= int(settings.EASYHIRE_SESSION_AGE):
                    applicant_objs.is_applicant_online = False
                    applicant_objs.save()
                if applicant_objs.is_applicant_online == False:
                    applicant_objs.is_applicant_online = True
                    applicant_objs.last_attempt_datetime = timezone.now()
                    applicant_objs.save()
                    logger.info(username)
                    logger.info(password)
                    #user = authenticate(username=username, password=password)
                    user = applicant_objs
                    logger.info(user)
                    login(request, user)
                    response["status_code"] = 200
                    response["status_message"] = "SUCCESS"
                    response["role"] = request.user.role
                else:
                    response["status_code"] = 305
                    response["status_message"] = "Session is running."
            except Exception as e:
                logger.info(e)
                response["status_code"] = 405
                response["status_message"] = "Unauthorized user"
    except Exception as e:
        logger.error("ApplicantAuthentication: "+str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def ForgotPasswordPage(request):
    return render(request, "EasyHireApp/forgot-password.html")

def ResetPassword(request, phone_number):
    try:
        applicant_obj = Applicant.objects.get(username=phone_number)
        # OTP = send_otp_at_given_mobile_number("91"+str(phone_number))
        password = password_generator()
        logger.info(password)

        applicant_obj.set_password(password)
        applicant_obj.save()

        send_registration_email_to_applicant(applicant_obj, password)
        send_registration_msg_to_applicant(applicant_obj, password)

        return HttpResponse("200")
    except Exception as e:
        logger.error(e)
        return HttpResponse("500")


"""class MacleodsSignUpAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            logger.info("Inside MAcleodsSignupAPI")
            applicant_phonenumber = request.data["applicant_phonenumber"]
            applicant_name = request.data["applicant_name"]
            applicant_emailid = request.data["applicant_emailid"]
            applicant_dob = request.data["applicant_dob"]
            applicant_college = request.data["applicant_college"]
            applicant_year_of_passing = request.data["applicant_year_of_passing"]
            applicant_stream = request.data["applicant_stream"]
            applicant_percentage = request.data["applicant_percentage"]
            applicant_category =APPLICANT_CATEGORY[2][0]
            try:
                id_proof_adhaar_number = json_data["id_proof_adhaar_number"]
                id_proof_pan_number = json_data["id_proof_pan_number"]
            except Exception:
                id_proof_adhaar_number = ""
                id_proof_pan_number = ""

            applicant_objs_with_email_id = Applicant.objects.filter(
                email_id=str(applicant_emailid))
            applicant_objs_with_phone = Applicant.objects.filter(
                phone_number=str(applicant_phonenumber))

            if (len(applicant_objs_with_phone) == 0 and len(applicant_objs_with_email_id) == 0):

                dob_datetime_obj = datetime.datetime.strptime(
                    str(applicant_dob), "%Y-%m-%d")
                try:
                    institute = Institute.objects.get(name=applicant_college)
                except Exception:
                    institute = Institute.objects.create(name=applicant_college)

                try:
                    stream = Stream.objects.get(name=applicant_stream)
                except Exception:
                    stream = Stream.objects.create(name=applicant_stream)

                applicant_obj = Applicant.objects.create(name=str(applicant_name),
                                                     email_id=str(
                                                         applicant_emailid),
                                                     phone_number=str(
                                                         applicant_phonenumber),
                                                     dob=dob_datetime_obj,
                                                     college_name=str(applicant_college),
                                                     year_of_passing=str(
                                                         applicant_year_of_passing),
                                                     stream=stream,
                                                     percentage=float(
                                                         applicant_percentage),
                                                     is_registered=True,
                                                     username=str(
                                                         applicant_phonenumber),
                                                     status=None,
                                                     category=applicant_category)
                if id_proof_pan_number != "":
                    applicant_obj.id_proof_pan_number = str(
                        id_proof_pan_number)
                if id_proof_adhaar_number != "":
                    applicant_obj.id_proof_adhaar_number = str(
                        id_proof_adhaar_number)
                applicant_obj.set_password("123456")
                applicant_obj.is_registered = True
                applicant_obj.save()
                logger.info("Applicant %s", applicant_obj)
                response["status_code"] = 200
            else:
                response["status_code"] = 405
        except Exception as e:
            response["status_message"] = "Internal Server Error"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("MacleodsSignUpAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))

        return Response(data=response)

MacleodsSignUp = MacleodsSignUpAPI.as_view()"""

class MacleodsSignUpAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        response["status_message"] = "Internal Server Error"
        try:
            logger.info("Inside MacleodsSignupAPI")
            applicant_category = request.data["applicant_category"]
            applicant_phonenumber = request.data["applicant_phonenumber"]
            applicant_name = request.data["applicant_name"]
            applicant_emailid = request.data["applicant_emailid"]
            applicant_dob = request.data["applicant_dob"]
            applicant_location = request.data["applicant_location"]
            applicant_gender = request.data["applicant_gender"]
            id_proof_adhaar_number = request.data["id_proof_adhaar_number"]
            dob_datetime_obj = datetime.datetime.strptime(
                    str(applicant_dob), "%Y-%m-%d")
            try:
                id_proof_pan_number = request.data["id_proof_pan_number"]
            except Exception:
                id_proof_pan_number = ""

            applicant_objs_with_email_id = Applicant.objects.filter(
                email_id=str(applicant_emailid))
            applicant_objs_with_phone = Applicant.objects.filter(
                phone_number=str(applicant_phonenumber))

            if(len(applicant_objs_with_email_id) == 0 and len(applicant_objs_with_phone) == 0):
                if applicant_category == "1":
                    applicant_college = request.data["applicant_college"]
                    applicant_year_of_passing = request.data["applicant_year_of_passing"]
                    applicant_stream = request.data["applicant_stream"]
                    applicant_percentage = request.data["applicant_percentage"]
                    applicant_specialization = request.data["applicant_specialization"]
                    stream = Stream.objects.get(name=applicant_stream)
                    applicant_obj = Applicant.objects.create(name=ascii_string(
                        applicant_name),
                        email_id=ascii_string(
                        applicant_emailid),
                        phone_number=ascii_string(
                        applicant_phonenumber),
                        dob=dob_datetime_obj,
                        college_name=applicant_college,
                        year_of_passing=ascii_string(
                        applicant_year_of_passing),
                        stream=stream,
                        percentage=float(
                        applicant_percentage),
                        is_registered=True,
                        username=ascii_string(
                        applicant_phonenumber),
                        status=None,
                        category=applicant_category,
                        location=str(
                        applicant_location),
                        id_proof_adhaar_number=str(
                        id_proof_adhaar_number),
                        gender=applicant_gender,
                        specialization=str(applicant_specialization))
                elif applicant_category == "2":
                    applicant_current_company = request.data["applicant_current_company"]
                    applicant_current_ctc = request.data["applicant_current_ctc"]
                    applicant_current_designation = request.data["applicant_current_designation"]
                    applicant_obj = Applicant.objects.create(name=ascii_string(
                        applicant_name),
                        email_id=ascii_string(
                        applicant_emailid),
                        phone_number=ascii_string(
                        applicant_phonenumber),
                        dob=dob_datetime_obj,
                        stream=None,
                        is_registered=True,
                        username=ascii_string(
                        applicant_phonenumber),
                        status=None,
                        category=applicant_category,
                        location=str(
                        applicant_location),
                        id_proof_adhaar_number=str(
                        id_proof_adhaar_number),
                        department=None,
                        gender=applicant_gender,
                        current_company=ascii_string(
                        applicant_current_company),
                        current_ctc=ascii_string(
                        applicant_current_ctc),
                        current_designation=ascii_string(applicant_current_designation))
                if id_proof_pan_number != "":
                    applicant_obj.id_proof_pan_number = str(
                        id_proof_pan_number)
                    applicant_obj.save()
                applicant_obj.set_password("123456")
                applicant_obj.is_registered = True
                applicant_obj.save()
                logger.info("Applicant %s", applicant_obj)
                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
            else:
                response["status_code"] = 405
                response["status_message"] = "Applicant matching details already exists"
        except Exception as e:
            response["status_message"] = "Internal Server Error"
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("MacleodsSignUpAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))
        return Response(data=response)


MacleodsSignUp = MacleodsSignUpAPI.as_view()

