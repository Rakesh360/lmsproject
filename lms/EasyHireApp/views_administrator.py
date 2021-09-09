from django.shortcuts import render, redirect, HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils import timezone

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth import logout,authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger

from EasyHireApp.models import *
from EasyHireApp.utils import *
from EasyHireApp.constants import *
from datetime import datetime, timedelta
import base64
import logging
import threading
import sys

logger = logging.getLogger(__name__)


def AdministratorLoginPage(request):
    if is_user_authenticated(request):
        return redirect("/")
    else:
        return render(request, 'EasyHireApp/employee-login.html')

def AdministratorAuthentication(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error. Please try again later.",
        "is_registered": False
    }
    try:
        if request.method == "POST":
            if is_user_authenticated(request):
                logger.info(request.user.role)
                if request.user.role == "1":
                    return redirect("/applicant/dashboard")
                elif request.user.role == "3":
                    if request.user.administrator.can_manage_applicants:
                        return redirect("/administrator/manage-applicants")
                    elif request.user.administrator.can_create_applicants:
                        return redirect("/master-list/create-applicants")
                    elif request.user.administrator.can_manage_quiz:
                        return redirect("/manage-quiz/")
                    elif request.user.administrator.can_manage_database:
                        return redirect("/master-list/events/")
                    else:
                        return ("/login")
                else:
                    return redirect("/administrator/manage-applicants")

            data = request.POST["data"]
            json_data = json.loads(data)
            username = json_data["username"]
            password = json_data["password"]

            administrator_objs = Administrator.objects.first()

            #if len(administrator_objs) > 0 and (administrator_objs[0].role =="2") :
                #user = authenticate(username=username, password=password)
            login(request, administrator_objs)
            administrator_obj = Administrator.objects.get(username=username)
            administrator_obj.is_active = True
            administrator_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"

          
    except Exception as e:
        logger.error("AdministratorAuthentication: "+str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def get_event_quizzes(event_objs):

    quiz_objs = []

    for event in event_objs:
        for quiz_section in event.quiz_section.all():
            if quiz_section.quiz not in quiz_objs:
                quiz_objs.append(quiz_section.quiz)
    return quiz_objs

def ManageApplicantsPage(request):
    try:
        if True:
            master_quiz_objs = []
            master_stream_objs = []
            master_department_objs = []
            if request.user.role == "2":
                #master_quiz_objs = Quiz.objects.all()
                master_quiz_objs = Quiz.objects.all().filter(is_activated=True)
                master_stream_objs = Stream.objects.all()
                #master_event_objs = Event.objects.all()
                master_department_objs = Department.objects.all()


            #master_quiz_objs = Quiz.objects.all()
            #master_institutes_objs = Institute.objects.all()
            #master_stream_objs = Stream.objects.all()
            #master_event_objs = Event.objects.all()
            #master_department_objs = Department.objects.all()
            filter_list = []
            applicant_objs = []
            list_of_sets_objs = []

            if request.user.role == "2":
                master_event_objs = Event.objects.all()
            else:
                master_event_objs = request.user.administrator.get_event_objs()
                #master_quiz_objs = get_event_quizzes(master_event_objs)
                master_quiz_objs = Quiz.objects.filter(is_activated=True)

            filter_list = []
            applicant_objs = []
            list_of_sets_objs = []

            if request.user.role == "2":
                applicant_objs = Applicant.objects.all()
            else:
                applicant_objs = Applicant.objects.filter(event__in = master_event_objs)
                list_of_sets_objs.append(set(applicant_objs))

            campus_applicant_objs = []
            if "is_campus" in request.GET and request.GET["is_campus"] == "True":
                campus_applicant_objs = get_list_of_campus_applicants(Applicant)
                list_of_sets_objs.append(set(campus_applicant_objs))
                filter_list.append("4")

            walkin_applicant_objs = []
            if "is_walkin" in request.GET and request.GET["is_walkin"] == "True":
                walkin_applicant_objs = get_list_of_walkin_applicants(Applicant)
                list_of_sets_objs.append(set(walkin_applicant_objs))
                filter_list.append("5")

            posting_applicant_objs = []
            if "is_posting" in request.GET and request.GET["is_posting"] == "True":
                posting_applicant_objs = get_list_of_posting_applicants(Applicant)
                list_of_sets_objs.append(set(posting_applicant_objs))
                filter_list.append("6")

            rejected_applicant_objs = []
            if "is_rejected" in request.GET and request.GET["is_rejected"] == "True":
                rejected_applicant_objs = get_list_of_rejected_applicants(Applicant)
                list_of_sets_objs.append(set(rejected_applicant_objs))
                filter_list.append("1")

            selected_applicant_objs = []
            if "is_selected" in request.GET and request.GET["is_selected"] == "True":
                selected_applicant_objs = get_list_of_selected_applicants(
                    Applicant)
                list_of_sets_objs.append(set(selected_applicant_objs))
                filter_list.append("2")

            nonapproved_applicant_objs = []
            if "is_nonapproved" in request.GET and request.GET["is_nonapproved"] == "True":
                nonapproved_applicant_objs = get_list_of_non_approved_applicants(
                    Applicant)
                list_of_sets_objs.append(set(nonapproved_applicant_objs))
                filter_list.append("3")
            male_applicant_objs = []
            if "is_male" in request.GET and request.GET["is_male"] == "True":
                male_applicant_objs = Applicant.objects.filter(gender="1")
                list_of_sets_objs.append(set(male_applicant_objs))
                filter_list.append("7")

            female_applicant_objs = []
            if "is_female" in request.GET and request.GET["is_female"] == "True":
                female_applicant_objs = Applicant.objects.filter(gender="2")
                list_of_sets_objs.append(set(female_applicant_objs))
                filter_list.append("8")

            others_applicant_objs = []
            if "is_others" in request.GET and request.GET["is_others"] == "True":
                others_applicant_objs = Applicant.objects.filter(gender="2")
                list_of_sets_objs.append(set(others_applicant_objs))
                filter_list.append("9")
            """
            institute_filter_list = []
            institutes_applicant_objs = []
            if "institute" in request.GET:
                institute_pk_list = request.GET.getlist("institute")
                institutes_objs = []
                for institute_pk in institute_pk_list:
                    institutes_objs.append(
                        Institute.objects.get(pk=int(institute_pk)))
                    institute_filter_list.append(int(institute_pk))
                institutes_applicant_objs = get_list_of_applicants_for_given_institute(
                    Applicant, institutes_objs)
                list_of_sets_objs.append(set(institutes_applicant_objs))
            quiz_filter_list = []
            quiz_applicant_objs = []
            if "quiz" in request.GET:
                quiz_pk_list = request.GET.getlist("quiz")
                quiz_objs = []
                for quiz_pk in quiz_pk_list:
                    quiz_objs.append(Quiz.objects.get(pk=int(quiz_pk)))
                    quiz_filter_list.append(int(quiz_pk))
                list_of_sets_objs.append(set(quiz_applicant_objs))
            """

            department_filter_list = []
            department_applicants_objs = []
            if "department" in request.GET:
                department_pk_list = request.GET.getlist("department")
                department_objs = []
                for department_pk in department_pk_list:
                    department_objs.append(Department.objects.get(pk=int(department_pk)))
                    department_filter_list.append(int(department_pk))
                for department_obj in department_objs:
                    applicant_objs = Applicant.objects.filter(department=department_obj)
                    for applicant_obj in applicant_objs:
                        department_applicants_objs.append(applicant_obj)
                list_of_sets_objs.append(set(department_applicants_objs))
            stream_filter_list = []
            stream_applicant_objs = []
            if "stream" in request.GET:
                stream_pk_list = request.GET.getlist("stream")
                stream_objs = []
                for stream_pk in stream_pk_list:
                    stream_objs.append(
                        Stream.objects.get(pk=int(stream_pk)))
                    stream_filter_list.append(int(stream_pk))
                stream_applicant_objs = get_list_of_applicants_for_given_stream(
                    Applicant, stream_objs)
                list_of_sets_objs.append(set(stream_applicant_objs))

            quiz_filter_list = []
            quiz_applicant_objs = []
            quiz_status_objs = []
            if "quiz" in request.GET:
                quiz_pk_list = request.GET.getlist("quiz")
                quiz_objs = []
                for quiz_pk in quiz_pk_list:
                    quiz_objs.append(Quiz.objects.get(pk=int(quiz_pk)))
                    quiz_filter_list.append(int(quiz_pk))
                for quiz_obj in quiz_objs:
                    quiz_status_objs = QuizStatus.objects.filter(quiz=quiz_obj)
                    for quiz_status_obj in quiz_status_objs:
                        applicant_obj = quiz_status_obj.applicant
                        quiz_applicant_objs.append(applicant_obj)
                list_of_sets_objs.append(set(quiz_applicant_objs))
            event_filter_list = []
            event_applicants_objs = []
            if "event" in request.GET:
                event_pk_list = request.GET.getlist("event")
                event_objs = []
                for event_pk in event_pk_list:
                    event_objs.append(Event.objects.get(pk=int(event_pk)))
                    event_filter_list.append(int(event_pk))
                for event_obj in event_objs:
                    applicant_objs = Applicant.objects.filter(event=event_obj)
                    for applicant_obj in applicant_objs:
                        event_applicants_objs.append(applicant_obj)
                list_of_sets_objs.append(set(event_applicants_objs))

            try:
                if "registered_between" in request.GET:
                    range_start_date = datetime.strptime(request.GET["r_start"] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                    range_end_date = datetime.strptime(request.GET["r_end"] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                    print(range_start_date, range_end_date)
                    filter_list.append("16")
                    registered_applicants = Applicant.objects.filter(date_joined__range=(range_start_date, range_end_date))
                    print(registered_applicants)
                    list_of_sets_objs.append(set(registered_applicants))
                    print(list_of_sets_objs)

                if "quiz_assigned_between" in request.GET:
                    range_start_date = datetime.strptime(request.GET["qa_start"] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                    range_end_date = datetime.strptime(request.GET["qa_end"] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                    print(range_start_date, range_end_date)
                    filter_list.append("13")
                    assigned_applicants = Applicant.objects.filter(attempted_datetime__range=(range_start_date, range_end_date), status=APPLICANT_AT_QUIZ)
                    list_of_sets_objs.append(set(assigned_applicants))
                if "quiz_completed_between" in request.GET:
                    filter_list.append("15")
                    range_start_date = datetime.strptime(request.GET["qc_start"] + " 00:00:00", "%Y-%m-%d %H:%M:%S")
                    range_end_date = datetime.strptime(request.GET["qc_end"] + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                    print(range_start_date, range_end_date)
                    completed_quiz_status = QuizStatus.objects.filter(is_completed=True, is_deleted=False, completion_time__range=(range_start_date, range_end_date))
                    quiz_completed_applicant_objs = set()
                    for quiz_status in completed_quiz_status:
                        quiz_completed_applicant_objs.add(quiz_status.applicant)
                    list_of_sets_objs.append(quiz_completed_applicant_objs)
                if "quiz_not_assigned" in request.GET:
                    filter_list.append("11")
                    not_assigned_applicants = Applicant.objects.all().exclude(status=APPLICANT_AT_QUIZ)
                    print(not_assigned_applicants)
                    list_of_sets_objs.append(set(not_assigned_applicants))
                if "quiz_assigned" in request.GET:
                    filter_list.append("12")
                    assigned_applicants = Applicant.objects.filter(status=APPLICANT_AT_QUIZ)
                    list_of_sets_objs.append(set(assigned_applicants))
                if "quiz_completed" in request.GET:
                    filter_list.append("14")
                    applicants = Applicant.objects.all()
                    quiz_completed_applicant_objs = set()
                    for applicant in applicants:
                        if applicant.is_quiz_ended():
                            quiz_completed_applicant_objs.add(applicant)
                    list_of_sets_objs.append(quiz_completed_applicant_objs)

            except Exception as e:
                print(str(e))

            date_applicant_objs = []
            start_date = ""
            if "date" in request.GET:
                start_date = request.GET["date"]
                date_format = "%Y-%m-%d"
                datetime_start = datetime.strptime(start_date, date_format).date()
                date_applicant_objs = Applicant.objects.filter(attempted_datetime__date=datetime_start)
                list_of_sets_objs.append(set(date_applicant_objs))
            else:
                if "all" in request.GET:
                    list_of_sets_objs.append(set(applicant_objs))
                    filter_list.append("10")
                elif ("is_campus" in request.GET) or ("is_walkin" in request.GET) or ("is_posting" in request.GET) \
                        or ("is_male" in request.GET) or ("is_female" in request.GET) or ("is_others" in request.GET) \
                        or ("is_selected" in request.GET) or ("is_rejected" in request.GET) or ("event" in request.GET) \
                        or ("is_nonapproved" in request.GET) or ("quiz" in request.GET) or ("group" in request.GET) \
                        or ("stream" in request.GET) or ("department" in request.GET) or ("institute" in request.GET) \
                        or ("registered_between" in request.GET) or ("quiz_assigned_between" in request.GET) \
                        or ("quiz_completed_between" in request.GET) or ("quiz_assigned" in request.GET) \
                        or ("quiz_completed" in request.GET) or ("quiz_tag" in request.GET) or \
                        ("student_tag" in request.GET) or ("quiz_not_assigned" in request.GET):
                    logger.info("Apply Filter")
                else:
                    start_date = datetime.now()
                    date_format = "%Y-%m-%d"
                    datetime_start = datetime.strftime(
                        start_date, date_format)
                    start_date = datetime_start
                    date_applicant_objs = Applicant.objects.filter(
                        attempted_datetime__date=datetime_start)
                    list_of_sets_objs.append(set(date_applicant_objs))
            """
            else:
                if "all" in request.GET:
                    list_of_sets_objs.append(set(applicant_objs))
                    filter_list.append("10")
                else:
                    start_date = datetime.now()
                    date_format = "%Y-%m-%d"
                    datetime_start = datetime.strftime(start_date, date_format)
                    start_date = datetime_start
                    date_applicant_objs = Applicant.objects.filter(attempted_datetime__date=datetime_start)
                    list_of_sets_objs.append(set(date_applicant_objs))
            """
            if len(list_of_sets_objs) > 0:
                applicant_objs = list(set.intersection(*list_of_sets_objs))

            applicant_info = ""

            #if "applicant-info" in request.GET:
            #    applicant_info = request.GET["applicant-info"]
            #    applicant_objs = list(set(Applicant.objects.filter(name__icontains = applicant_info))| \
            #                     set(Applicant.objects.filter(email_id__icontains = applicant_info))| \
            #                     set(Applicant.objects.filter(phone_number__icontains = applicant_info)))
            if "applicant-info" in request.GET:
                applicant_info = request.GET["applicant-info"]
                if request.user.role == "2":
                    applicant_objs = Applicant.objects.all()
                else:
                    applicant_objs = Applicant.objects.filter(event__in = request.user.administrator.get_event_objs())
                print(applicant_info)
                applicant_objs = list(set(applicant_objs.filter(name__icontains = applicant_info))|\
                                set(applicant_objs.filter(email_id__icontains = applicant_info))|\
                                set(applicant_objs.filter(phone_number__icontains = applicant_info)))



            return render(request, "EasyHireApp/administrator/manage-applicants.html", {
                #"master_institutes_objs": master_institutes_objs,
                "master_quiz_objs": master_quiz_objs,
                "applicant_objs": applicant_objs,
                "filter_list": filter_list,
                #"institute_filter_list": institute_filter_list,
                "quiz_filter_list": quiz_filter_list,
                "APPLICANT_APPLICATION_STATUS": APPLICANT_APPLICATION_STATUS,
                "master_event_objs":master_event_objs,
                "event_filter_list":event_filter_list,
                "master_stream_objs":master_stream_objs,
                "stream_filter_list":stream_filter_list,
                "master_department_objs":master_department_objs,
                "department_filter_list":department_filter_list,
                "male_applicant_objs":male_applicant_objs,
                "female_applicant_objs":female_applicant_objs,
                "others_applicant_objs":others_applicant_objs,
                "start_date":start_date,
                "applicant_info":applicant_info,
                "quiz_assigned_start_date": request.GET.get("qa_start", ""),
                "quiz_assigned_end_date": request.GET.get("qa_end", ""),
                "quiz_completed_start_date": request.GET.get("qc_start", ""),
                "quiz_completed_end_date": request.GET.get("qc_end", ""),
                "registered_between_start_date": request.GET.get("r_start", ""),
                "registered_between_end_date": request.GET.get("r_end", ""),

                #"quiz_filter_list": quiz_filter_list,         
                #"quiz_tag_filter_list": quiz_tag_filter_list, 
                #"student_tag_filter_list": student_tag_filter_list,

                "quiz_tag_objs": Tag.objects.filter(category="1"),
                "student_tag_objs": Tag.objects.filter(category="3"),


            })
        elif request.user.role == "3":
            return redirect("/master-list/create-applicants")
        else:
            return redirect("/login")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error ManageApplicantsPage: %s at %s",(e), str(exc_tb.tb_lineno))
    return HttpResponse("Invalid Access")
#
#def AssignTask(request):
#    response = {
#        "status_code": 500,
#        "status_message": "Internal Server Error"
#    }
#    try:
#        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
#            data = request.POST["data"]
#            data = json.loads(data)
#            applicant_objs = get_applicant_objs_from_applicant_id_list(
#                data["selected_applicant_id_list"], Applicant)
#            if data["selected_next_round"] == APPLICANT_AT_QUIZ:
#                quiz_obj = get_quiz_obj(
#                    data["selected_quiz_for_next_round"], Quiz)
#                if quiz_obj == None:
#                    response["status_code"] = 101
#                    response["status_message"] = "Kindly select valid quiz"
#                else:
#                    status, flag = schedule_applicant_quiz(applicant_objs,
#                                                     data["quiz_start_date"],
#                                                     data["quiz_start_time"],
#                                                     data["quiz_end_date"],
#                                                     data["quiz_end_time"],
#                                                     quiz_obj,
#                                                     QuizStatus)
#                    logger.info("Assign Task")
#                    logger.info(flag)
#                    logger.info(status)
#                    if status and flag:
#                        response["status_code"] = 200
#                        response["status_message"] = "Quiz has been scheduled successfully."
#                    elif status == False and flag == False:
#                        response["status_code"] = 101
#                        response["status_message"] = "Applicant is rejected between 30 days."
#                    else:
#                        response["status_code"] = 101
#                        response["status_message"] = "Unable to schedule quiz."
#            elif data["selected_next_round"] == APPLICANT_INTERVIEW:
#                status = schedule_applicant_interview(applicant_objs)
#                if status:
#                        response["status_code"] = 200
#                        response["status_message"] = "Selected for interview"
#                else:
#                    response["status_code"] = 101
#                    response["status_message"] = "Unable to select for Interview."
#            else:
#                response["status_code"] = 101
#                response["status_message"] = "Invalid option"
#        else:
#            response["status_code"] = 404
#            response["status_message"] = "Invalid Access"
#    except Exception as e:
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        logger.error("Error AssignTask: %s at %s",(e), str(exc_tb.tb_lineno))
#
#    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def AssignTask(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)
            print(applicant_objs)
            print(data["selected_applicant_id_list"])
            if data["selected_next_round"] == APPLICANT_AT_QUIZ:
                quiz_obj = get_quiz_obj(
                    data["selected_quiz_for_next_round"], Quiz)
                if quiz_obj == None:
                    response["status_code"] = 101
                    response["status_message"] = "Kindly select valid quiz"
                else:
                    errors,status, flag = schedule_applicant_quiz(applicant_objs,
                                                     data["quiz_start_date"],
                                                     data["quiz_start_time"],
                                                     data["quiz_end_date"],
                                                     data["quiz_end_time"],
                                                     quiz_obj,
                                                     QuizStatus)
                    print(errors)
                    logger.info("Assign Task")
                    logger.info(flag)
                    logger.info(status)
                    if status and flag and len(errors) <= 0:
                        response["status_code"] = 200
                        response["status_message"] = "Quiz has been scheduled successfully."
                        response['errors'] = errors
                    # elif status == False and flag == False:
                    #     response["status_code"] = 101
                    #     response["status_message"] = "Applicant is rejected between 30 days."
                    #     response['errors'] = errors
                    else:
                        response["status_code"] = 101
                        response["status_message"] = "Unable to schedule quiz."
                        response['errors'] = errors
            elif data["selected_next_round"] == APPLICANT_INTERVIEW:
                status = schedule_applicant_interview(applicant_objs)
                if status:
                        response["status_code"] = 200
                        response["status_message"] = "Selected for interview"
                else:
                    response["status_code"] = 101
                    response["status_message"] = "Unable to select for Interview."
            else:
                response["status_code"] = 101
                response["status_message"] = "Invalid option"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error AssignTask: %s at %s",(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def AcceptedApplicant(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            for applicant in applicant_objs:
                applicant.is_selected = True
                applicant.is_rejected = False
                applicant.save()
                send_status_change_msg_to_applicant(applicant,"selected")

            response["status_code"] = 200
            response["status_message"] = "success"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def RejectedApplicant(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            for applicant in applicant_objs:
                applicant.is_rejected = True
                applicant.is_selected = False
                applicant.save()
                print(applicant)
                send_status_change_msg_to_applicant(applicant,"rejected")

            response["status_code"] = 200
            response["status_message"] = "success"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def ResetApplicantAccount(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            for applicant in applicant_objs:
                applicant.reset_account()
                send_status_change_msg_to_applicant(applicant,"reset")

            response["status_code"] = 200
            response["status_message"] = "success"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

"""
def ApplicantReportCard(request, applicant_pk):
    if is_user_authenticated(request) and request.user.role == "2":
        applicant_obj = Applicant.objects.get(pk=int(applicant_pk))
        attempted_quiz_status_objs = applicant_obj.get_list_of_attempted_quiz()
        return render(request, 'EasyHireApp/applicant-details.html', {
            "applicant_obj": applicant_obj,
            "attempted_quiz_status_objs": attempted_quiz_status_objs,
        })
    else:
        return HttpResponse("<h5>Invalid Access</h5")
"""
def ApplicantReportCard(request, applicant_pk):
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            applicant_obj = Applicant.objects.get(pk=int(applicant_pk))
            if request.user.role == "2" or\
                request.user.administrator.has_access_to_all_events or\
                (applicant_obj.event is not None and request.user.administrator.has_access_to_event(event_pk=applicant_obj.event.pk)):

                attempted_quiz_status_objs = applicant_obj.get_list_of_attempted_quiz()
                attempted_quiz_status_deassigned_objs = applicant_obj.get_list_of_deassigned_attempted_quiz()

                logger.info(attempted_quiz_status_objs)
                quiz_image_list = []
                #import ast
                #for attempted_quiz_status_obj in attempted_quiz_status_objs:
                #    image_list = ast.literal_eval(attempted_quiz_status_obj.images)
                #    quiz_image_list.append({
                #        "quiz": attempted_quiz_status_obj.quiz.title,
                #        "images": image_list
                #    })
                return render(request, 'EasyHireApp/applicant-details.html', {
                    "applicant_obj": applicant_obj,
                    "attempted_quiz_status_objs": attempted_quiz_status_objs,
                    "attempted_quiz_status_deassigned_objs" : attempted_quiz_status_deassigned_objs
                #    "quiz_image_list": quiz_image_list
                })
            else:
                return HttpResponse("<h5>Invalid Access</h5>")
        else:
            return HttpResponse("<h5>Invalid Access</h5>")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error ApplicantReportCard: %s at %s",str(e), str(exc_tb.tb_lineno))





class GetDeassignedResultAPI(APIView):
     def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            authkey = request.data["authkey"]
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
                allow_access = True
            elif is_valid_authentication_key(authkey):
                allow_access = True

            if allow_access:
                data = request.data
             
               
            id = data["hiring_round_id"]
            quiz_history_obj = QuizHistory.objects.get(id = id)
            response = json.loads(quiz_history_obj.quiz_timing_info)
            payload_session = json.loads(quiz_history_obj.quiz_sessions)

            response['status_code'] = 200
            response['sessions'] = payload_session
            response['section_timing'] = payload_session.get('section_timings')
            response['quiz_assign_time'] =payload_session.get('quiz_assign_time')
            response['quiz_start_time'] = payload_session.get('quiz_start_time')
            response['quiz_end_time'] =payload_session.get('quiz_end_time')
            response["quiz_result"] = []
            print(response)
            return Response(response)
        except Exception as e:
            print(e)


GetDeassignedResultAPI = GetDeassignedResultAPI.as_view()        

class GetQuizResultAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        response["message"] = "Some error in views_administrator - GetQuizResultAPI"
        try:
            allow_access = False
            authkey = request.data["authkey"]
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
                allow_access = True
            elif is_valid_authentication_key(authkey):
                allow_access = True

            if allow_access:
                data = request.data
                applicant_id = data["student_id"]
                attempted_quiz_status_id = data["quiz_config_id"]
                applicant_obj = Applicant.objects.get(pk=int(applicant_id))
                quiz_status_obj = QuizStatus.admin_objects.get(pk=int(attempted_quiz_status_id))
                if quiz_status_obj.is_deleted:
                    response['is_deleted'] = True
                else:
                    response['is_deleted'] = False

                generate_applicant_quiz_result(applicant_obj,
                                               quiz_status_obj.quiz,quiz_status_obj,
                                               QuizResult)

                quiz_result_obj = QuizResult.objects.filter(applicant=applicant_obj,quiz_status=quiz_status_obj,quiz=quiz_status_obj.quiz)[0]
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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error GetQuizResultAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
        return Response(data=response)

GetQuizResult = GetQuizResultAPI.as_view()


def MasterInstitutes(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
        institutes_objs = Institute.objects.all()
        applicant_objs = Applicant.objects.all()
        no_applicants = []
        count = 0
        for institutes_obj in institutes_objs:
            for applicant_obj in applicant_objs:
                if(applicant_obj.college_name == institutes_obj):
                    count+=1
            no_applicants.append({
                "institutes": institutes_obj.name,
                "count":count
                })
            count = 0
        return render(request, "EasyHireApp/administrator/master_institutes.html", {
            "institutes_objs": institutes_objs,
            "applicant_objs":applicant_objs,
            "no_applicants":no_applicants
        })
    else:
        return redirect("/login")


def AddMasterInstitutes(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            name = data["name"]
            Institute.objects.create(name=name)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def DeactivateInstitute(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            institute = data["institute"]
            try:
                institute_obj = Institute.objects.get(name=institute)
                institute_obj.is_activated = False
                institute_obj.save()
            except Exception as e:
                print(e)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def ActivateInstitute(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            institute = data["institute"]
            try:
                institute_obj = Institute.objects.get(name=institute)
                institute_obj.is_activated = True
                institute_obj.save()
            except Exception as e:
                print(e)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
"""
def MasterApplicants(request):
    if is_user_authenticated(request):
        #institutes_objs = Institute.objects.filter(is_activated=True)
        applicant_objs = Applicant.objects.all()
        stream_objs = Stream.objects.all()
        return render(request, "EasyHireApp/administrator/master-applicants.html", {
            #"institutes_objs": institutes_objs,
            "applicant_objs":applicant_objs,
            "stream_objs":stream_objs
        })
    else:
        return redirect("/login")
"""
def MasterApplicants(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_create_applicants):
        if request.user.role == "2":
            event_objs = Event.objects.all()
        else:
            event_objs = request.user.administrator.get_event_objs()
        applicant_objs = Applicant.objects.all()
        stream_objs = Stream.objects.all()
        return render(request, "EasyHireApp/administrator/master-applicants.html", {
            "event_objs":event_objs,
            "applicant_objs":applicant_objs,
            "stream_objs":stream_objs
        })
    else:
        return redirect("/login")

def saveFile(uploaded_file):
    file_content = ContentFile(uploaded_file.read())
    file_path = default_storage.save(uploaded_file.name, file_content)
    return file_path
"""
class CreateApplicantExcelAPI(APIView):

    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            if is_user_authenticated(request):
                data = request.data
                uploaded_file = request.FILES.getlist('file')[0]
                logger.info("File %s", str(uploaded_file))

                institute_id = data["institute"]

                institute_obj = None
                try:
                    institute_obj = Institute.objects.get(pk=institute_id)
                    logger.info(
                        "CreateApplicantExcelAPI Found Institute %s", str(institute_obj))
                except:
                    logger.error(
                        "CreateApplicantExcelAPI Institute %s does not exist!", str(institute_obj))
                    return Response(data=response)

                stream_id = data["stream"]

                stream_obj = None
                try:
                    stream_obj = Stream.objects.get(pk=stream_id)
                    logger.info(
                        "CreateApplicantExcelAPI Found Stream %s", str(stream_obj))
                except:
                    logger.error(
                        "CreateApplicantExcelAPI Stream %s does not exist!", str(stream_obj))
                    return Response(data=response)

                adminstrator_obj = None
                try:
                    adminstrator_obj = Administrator.objects.get(username=request.user.username)
                    logger.info(
                        "CreateApplicantExcelAPI Employee uploading %s", str(adminstrator_obj))
                except:
                    logger.error(
                        "CreateApplicantExcelAPI Error getting employee")
                    return Response(data=response)

                file_extension = str(uploaded_file).split('.')[-1].lower()
                if(file_extension not in ["xlx", "xlsx"]):
                    logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                    response["status"] = 301
                else:
                    try:
                        file_path = saveFile(uploaded_file)
                        logger.info("File Saved %s", str(file_path))
                        import_success, message = None, None

                        import_success, message = import_applicants_from_excel(file_path, stream_obj, institute_obj)
                        if import_success:
                            response["status"] = 200
                        else:
                            response["status"] = 302
                            response["message"] = message

                            logger.info("Some error occured while importing applicants from excel file=%s", str(
                                uploaded_file))
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        logger.error("Error CreateApplicantExcelAPI: %s at %s", str(
                            e), str(exc_tb.tb_lineno))

                # response["status"] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error CreateApplicantExcelAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


CreateApplicantExcel = CreateApplicantExcelAPI.as_view()
"""

class CreateApplicantExcelAPI(APIView):

    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_create_applicants):
                data = request.data
                uploaded_file = request.FILES.getlist('file')[0]
                logger.info("File %s", str(uploaded_file))

                event_id = data["event"]

                event_obj = None
                try:
                    event_obj = Event.objects.get(pk=int(event_id))
                    logger.info(
                        "CreateApplicantExcelAPI Found Event %s", str(event_obj))
                except:
                    logger.error(
                        "CreateApplicantExcelAPI Event %s does not exist!", str(event_obj))
                    return Response(data=response)

                stream_id = data["stream"]

                stream_obj = None
                try:
                    stream_obj = Stream.objects.get(pk=stream_id)
                    logger.info(
                        "CreateApplicantExcelAPI Found Stream %s", str(stream_obj))
                except:
                    logger.error(
                        "CreateApplicantExcelAPI Stream %s does not exist!", str(stream_obj))
                    return Response(data=response)

                adminstrator_obj = None
                try:
                    adminstrator_obj = Administrator.objects.get(username=request.user.username)
                    logger.info(
                        "CreateApplicantExcelAPI Employee uploading %s", str(adminstrator_obj))
                except:
                    logger.error(
                        "CreateApplicantExcelAPI Error getting employee")
                    return Response(data=response)

                file_extension = str(uploaded_file).split('.')[-1].lower()
                if(file_extension not in ["xlx", "xlsx"]):
                    logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                    response["status"] = 301
                else:
                    try:
                        file_path = saveFile(uploaded_file)
                        logger.info("File Saved %s", str(file_path))
                        import_success, message = None, None
                        errors, import_success, message = import_applicants_from_excel(file_path, stream_obj, event_obj)
                        if len(errors) <= 0:
                            errors.append('No errors found!')

                        if import_success:
                            response["status"] = 200
                            response['errors'] = errors
                        else:
                            response["status"] = 302
                            response["message"] = message
                            response['errors'] = errors
                            logger.info("Some error occured while importing applicants from excel file=%s", str(
                                uploaded_file))
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        logger.error("Error CreateApplicantExcelAPI: %s at %s", str(
                            e), str(exc_tb.tb_lineno))

                # response["status"] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error CreateApplicantExcelAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

CreateApplicantExcel = CreateApplicantExcelAPI.as_view()


def removeStopWords(sentence):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

def CommonWords(A, B):
    str1_words = set(A)
    str2_words = set(B)
    common = str1_words & str2_words
    logger.info(common)
    return len(common)

class GetTextAnalysisOfAttemptedProblemAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data
            attempted_problem_id = data["attempted_problem_id"]
            attempted_problem_obj = ProblemAttempted.admin_objects.get(pk=int(attempted_problem_id))
            quiz_status_id = data["quiz_status_id"]
            quiz_status_obj = QuizStatus.admin_objects.get(pk=int(quiz_status_id))
            quiz_obj = quiz_status_obj.quiz
            applicant_id = data["applicant_id"]
            applicant_obj = Applicant.objects.get(pk=int(applicant_id))
            quiz_result_obj = QuizResult.objects.filter(quiz=quiz_obj,
                                                    applicant=applicant_obj).order_by('-pk')[0]
            #total_score = quiz_result_obj.generate_quiz_description_result()
            total_score = quiz_result_obj.generate_quiz_description_result()
            quiz_result_obj.description_score = total_score
            quiz_result_obj.save()
            solution = attempted_problem_obj.problem.solution
            answer = removeStopWords(attempted_problem_obj.answer)
            solution_list = removeStopWords(solution)
            common_words = CommonWords(solution_list, answer)
#            try:
#                score = (common_words/len(solution_list))*100
#            except Exception as e:
#                logger.error(e)
#                score = 0
            score = attempted_problem_obj.calculated_score
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
            response["solution"] = solution
            response["common_words"] = common_words
            response["answer"] = attempted_problem_obj.answer
            response["score"] = round(score,2)
            response["is_deleted"] = attempted_problem_obj.is_deleted

            #response["total_score"] = total_score
            # response["text_analysis"] = json.loads(attempted_problem_obj.text_analysis)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("getTextAnalysis :%s at %s", str(
                        e), str(exc_tb.tb_lineno))

        return Response(data=response)


GetTextAnalysisOfAttemptedProblem = GetTextAnalysisOfAttemptedProblemAPI.as_view()

class SaveModifiedScoreOfAttemptedProblemAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data
            attempted_problem_id = int(data["attempted_problem_id"])
            quiz_status_id = int(data['quiz_status_id'])
            score = float(data['score'])
            print("in save api",score)
            attempted_problem_obj = ProblemAttempted.objects.get(pk=attempted_problem_id)
            attempted_problem_obj.calculated_score = score
            attempted_problem_obj.save()
            print(attempted_problem_obj.calculated_score)
            quiz_status_obj = QuizStatus.objects.get(pk=quiz_status_id)
            applicant_percentage = quiz_status_obj.generate_quiz_description_result()
            # print(applicant_score)
            quiz_status_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
            #response["score"] = round(score,2)
            response["score"] = attempted_problem_obj.get_descriptive_percentage()
            response["applicant_percentage"] = applicant_percentage
            #response["total_score"] = total_score
            # response["text_analysis"] = json.loads(attempted_problem_obj.text_analysis)
        except Exception as e:
            logger.error("SaveQuizConfigAPI: "+str(e))

        return Response(data=response)


SaveModifiedScoreOfAttemptedProblem = SaveModifiedScoreOfAttemptedProblemAPI.as_view()


class SaveRemarksAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data
            quiz_config_id = int(data["quiz_config_id"])
            applicant_id = int(data['student_id'])
            remarks = data["remarks"].strip()

            quiz_status_obj = QuizStatus.objects.get(pk=quiz_config_id)
            quiz_result_obj = QuizResult.objects.get(quiz=quiz_status_obj.quiz, applicant=quiz_status_obj.applicant, quiz_status=quiz_status_obj)
            quiz_result_obj.recruiter_remark = remarks

            quiz_result_obj.save()
            
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
            response["remarks"]=remarks
        except Exception as e:
            logger.error("SaveRemarksAPI: "+str(e))
        print(response)
        return Response(data=response)


SaveRemarks = SaveRemarksAPI.as_view()


def get_value_or_na(input):
    if input == "" or input is None:
        return "N/A"
    return input

"""
def MasterStreams(request):
    if is_user_authenticated(request) and request.user.role == "2":
        stream_objs = Stream.objects.all()
        return render(request, "EasyHireApp/administrator/master_streams.html", {
            "stream_objs": stream_objs,
        })
    else:
        return redirect("/login")
"""
def MasterStreams(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
        stream_objs = Stream.objects.all()
        applicant_objs = Applicant.objects.all()
        no_applicants = []
        count = 0
        for stream_obj in stream_objs:
            for applicant_obj in applicant_objs:
                if(applicant_obj.stream == stream_obj):
                    count+=1
            no_applicants.append({
                "stream": stream_obj.name,
                "count":count
                })
            count = 0
        return render(request, "EasyHireApp/administrator/master_streams.html", {
            "stream_objs": stream_objs,
            "no_applicants":no_applicants,
            #"applicant_objs":applicant_objs
        })
    else:
        return redirect("/login")

def AddMasterStreams(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            name = data["name"]
            Stream.objects.create(name=name)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def DeleteMasterStreams(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            stream_id = data["stream_id"]
            stream_obj = Stream.objects.get(pk=int(stream_id))
            stream_obj.delete()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)



def MasterTags(request):
    # feature admin rights
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
        tag_objs = Tag.objects.all()

        quiz_tag_objs = Tag.objects.filter(category="1")
        topic_tag_objs = Tag.objects.filter(category="2")
        student_tag_objs = Tag.objects.filter(category="3")

        return render(request, "EasyHireApp/administrator/master_tags.html", {
            "TAG_CATEGORY_CHOICES": TAG_CATEGORY_CHOICES,
            "quiz_tag_objs": quiz_tag_objs,
            "topic_tag_objs": topic_tag_objs,
            "student_tag_objs": student_tag_objs,
        })
    else:
        return redirect("/login")


def SaveTag(request):
    response = {'status_code': 500}
    # feature admin rights
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):

        data = json.loads(request.POST['data'])

        tag_pk = int(data['tag_pk'])
        category = data['category']
        title = data['title']

        existing_tag_with_same_title = Tag.objects.filter(title=title, category=category).exclude(pk=tag_pk)

        if len(existing_tag_with_same_title):
            response['status_code'] = 101
            response['message'] = "Tag with same title in this category exists"
        else:
            try:
                tag_obj = Tag.objects.get(pk=tag_pk)
            except:
                tag_obj = Tag.objects.create()
            tag_obj.category = category
            tag_obj.title = title
            tag_obj.save()

            response['status_code'] = 200

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def AssignTag(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        # feature admin rights
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            try:
                selected_tag = Tag.objects.get(pk=data['student_tag_pk'])
            except:
                selected_tag = None

            for applicant in applicant_objs:
                applicant.tag = selected_tag
                applicant.save()
                print(applicant)

            response["status_code"] = 200
            response["status_message"] = "success"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


"""def DownloadApplicantReport(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)
            from xlwt import Workbook
            export_nps_wb = Workbook()
            sheet_name = "Applicant Results Sheet"
            sheet1 = export_nps_wb.add_sheet(
                sheet_name, cell_overwrite_ok=True)
            sheet1.write(0, 0, "Applicant Name")
            sheet1.write(0, 1, "Email")
            sheet1.write(0, 2, "Institute")
            sheet1.write(0, 3, "Graduation Year")
            sheet1.write(0, 4, "Score")
            sheet1.write(0, 5, "Percentile")
            sheet1.write(0, 6, "Sections Name")
            sheet1.write(0, 7, "Total Question")
            sheet1.write(0, 8, "Question Attempted")
            sheet1.write(0, 9, "Correct Answers")
            sheet1.write(0, 10, "Norm Score")
            index = 1
            for applicant_obj in applicant_objs:
                try:
                    sheet1.write(index, 0, applicant_obj.name)
                    sheet1.write(index, 1, applicant_obj.email_id)
                    sheet1.write(index, 2, applicant_obj.college_name)
                    sheet1.write(index, 3, applicant_obj.year_of_passing)
                    quiz_result_objs = list(
                        QuizResult.objects.filter(applicant=applicant_obj))
                    logger.info(quiz_result_objs)
                    ending_index = 0
                    flag = False
                    for quiz_result_obj in quiz_result_objs:

                        if quiz_result_obj.result == None:
                            continue

                        result = json.loads(quiz_result_obj.result)
                        total_sections = len(
                            result["quiz_section_result_list"])

                        sheet1.write(index, 4, result["applicant_total_score"])
                        sheet1.write(
                            index, 5, quiz_result_obj.get_applicant_percentile())
                        index_inner = 6
                        index_header = 11
                        for i in range(0, total_sections):
                            if i == 0:
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["section_name"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["total_questions"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["no_questions_attempted"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["right_answers"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["diff_score"])
                                index_inner += 1
                            else:
                                sheet1.write(0, index_header, "Sections Name")
                                index_header += 1
                                sheet1.write(0, index_header, "Total Question")
                                index_header += 1
                                sheet1.write(0, index_header,
                                             "Question Attempted")
                                index_header += 1
                                sheet1.write(0, index_header,
                                             "Correct Answers")
                                index_header += 1
                                sheet1.write(0, index_header, "Norm Score")
                                index_header += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["section_name"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["total_questions"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["no_questions_attempted"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["right_answers"])
                                index_inner += 1
                                sheet1.write(
                                    index, index_inner, result["quiz_section_result_list"][i]["diff_score"])
                                index_inner += 1
                                flag = True
                                ending_index = index_header
                        if flag == True:
                            for quiz_result_obj in quiz_result_objs:
                                if quiz_result_obj.result == None:
                                    continue
                                result = json.loads(quiz_result_obj.result)
                                total_sections = len(
                                    result["quiz_section_result_list"])
                                if total_sections == 0:
                                    sheet1.write(0, ending_index, "Descriptive Score")
                                    sheet1.write(
                                        index, ending_index, quiz_result_obj.description_score)
                        flag = False
                        #quiz_obj = quiz_result_obj.quiz
                        #quiz_stauts_objs = QuizStatus.objects.filter(applicant=applicant_obj,quiz=quiz_obj)
                    index += 1
                except Exception as e:
                    index += 1
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("Error DownloadApplicantReport:%s at %s", str(
                        e), str(exc_tb.tb_lineno))
                    pass

            filename = "applicant-score-sheet" + str(timezone.now()) + ".xls"
            export_nps_wb.save(settings.MEDIA_ROOT + filename)
            path_to_file = settings.MEDIA_ROOT + str(filename)
            response['file_url'] = "/files/" + str(filename)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error DownloadApplicantReport: %s at %s",
                     str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
"""

"""def DownloadApplicantReport(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            from xlwt import Workbook
            export_nps_wb = Workbook()
            sheet_name = "Applicant Results Sheet"

            sheet1 = export_nps_wb.add_sheet(
                sheet_name, cell_overwrite_ok=True)

            sheet1.write(0, 0, "Applicant Name")
            sheet1.write(0, 1, "Email")
            sheet1.write(0, 2, "Institute")
            sheet1.write(0, 3, "Graduation Year")
            sheet1.write(0, 4, "Section Name")
            sheet1.write(0, 5, "Score")
            sheet1.write(0, 6, "Total Question")
            sheet1.write(0, 7, "Question Attempted")
            sheet1.write(0, 8, "Correct Answer")
            row = 1
            for applicant_obj in applicant_objs:
                try:
                    quiz_status_objs = QuizStatus.objects.filter(
                        applicant=applicant_obj)
                    for quiz_status_obj in quiz_status_objs:
                        sheet1.write(row, 0, applicant_obj.name)
                        sheet1.write(row, 1, applicant_obj.email_id)
                        sheet1.write(row, 2, applicant_obj.college_name)
                        sheet1.write(row, 3, applicant_obj.year_of_passing)
                        quiz_result_obj = []
                        try:
                            quiz_result_obj = QuizResult.objects.get(applicant=applicant_obj,
                                                                     quiz=quiz_status_obj.quiz)
                            if quiz_result_obj.result == None:
                                continue
                            result = json.loads(quiz_result_obj.result)
                            total_sections = len(
                                result["quiz_section_result_list"])
                            if total_sections == 0:
                                sheet1.write(row, 4, "Subjective")
                                sheet1.write(
                                    row, 5, quiz_result_obj.description_score)
                                row += 1
                            else:
                                for i in range(0, total_sections):
                                    sheet1.write(row, 0, applicant_obj.name)
                                    sheet1.write(
                                        row, 1, applicant_obj.email_id)
                                    sheet1.write(
                                        row, 2, applicant_obj.college_name)
                                    sheet1.write(
                                        row, 3, applicant_obj.year_of_passing)
                                    sheet1.write(
                                        row, 4, result["quiz_section_result_list"][i]["section_name"])
                                    sheet1.write(
                                        row, 5, result["quiz_section_result_list"][i]["diff_score"])
                                    sheet1.write(
                                        row, 6, result["quiz_section_result_list"][i]["total_questions"])
                                    sheet1.write(
                                        row, 7, result["quiz_section_result_list"][i]["no_questions_attempted"])
                                    sheet1.write(
                                        row, 8, result["quiz_section_result_list"][i]["right_answers"])
                                    row += 1
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            logger.error("Error DownloadApplicantReport:%s at %s", str(
                                e), str(exc_tb.tb_lineno))
                            pass
                            row += 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("Error DownloadApplicantReport:%s at %s", str(
                        e), str(exc_tb.tb_lineno))
                    pass
            filename = "applicant-score-sheet" + str(timezone.now()) + ".xls"
            export_nps_wb.save(settings.MEDIA_ROOT + filename)
            path_to_file = settings.MEDIA_ROOT + str(filename)
            response['file_url'] = "/files/" + str(filename)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error DownloadApplicantReport: %s at %s",
                     str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
def DownloadApplicantReport(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            from xlwt import Workbook
            export_nps_wb = Workbook()
            sheet_name = "Applicant Results Sheet"

            sheet1 = export_nps_wb.add_sheet(
                sheet_name, cell_overwrite_ok=True)

            sheet1.write(0, 0, "Applicant Registration")
            sheet1.write(0, 1, "Applicant Name")
            sheet1.write(0, 2, "Email")
            sheet1.write(0, 3, "Institute")
            sheet1.write(0, 4, "Graduation Year")
            sheet1.write(0, 5, "Attempted Date")
            sheet1.write(0, 6, "Section Name")
            sheet1.write(0, 7, "Score")
            sheet1.write(0, 8, "Total Question")
            sheet1.write(0, 9, "Question Attempted")
            sheet1.write(0, 10, "Correct Answer")
            row = 1
            for applicant_obj in applicant_objs:
                try:
                    quiz_status_objs = QuizStatus.objects.filter(
                        applicant=applicant_obj)
                    for quiz_status_obj in quiz_status_objs:
                        sheet1.write(row, 0, str(
                            applicant_obj.date_joined.strftime("%d-%m-%Y %H:%M %p")))
                        sheet1.write(row, 1, applicant_obj.name)
                        sheet1.write(row, 2, applicant_obj.email_id)
                        sheet1.write(row, 3, applicant_obj.college_name)
                        sheet1.write(row, 4, applicant_obj.year_of_passing)
                        sheet1.write(row, 5, str(
                            applicant_obj.attempted_datetime.strftime("%d-%m-%Y %H:%M %p")))
                        quiz_result_obj = []
                        try:
                            quiz_result_obj = QuizResult.objects.get(applicant=applicant_obj,
                                                                     quiz=quiz_status_obj.quiz)
                            if quiz_result_obj.result == None:
                                continue
                            result = json.loads(quiz_result_obj.result)
                            total_sections = len(
                                result["quiz_section_result_list"])
                            if total_sections == 0:
                                sheet1.write(row, 6, "Subjective")
                                sheet1.write(
                                    row, 7, quiz_result_obj.description_score)
                                row += 1
                            else:
                                for i in range(0, total_sections):
                                    sheet1.write(row, 0, str(
                                        applicant_obj.date_joined.strftime("%d-%m-%Y %H:%M %p")))
                                    sheet1.write(row, 1, applicant_obj.name)
                                    sheet1.write(
                                        row, 2, applicant_obj.email_id)
                                    sheet1.write(
                                        row, 3, applicant_obj.college_name)
                                    sheet1.write(
                                        row, 4, applicant_obj.year_of_passing)
                                    sheet1.write(
                                        row, 5, str(applicant_obj.attempted_datetime.strftime("%d-%m-%Y %H:%M %p")))
                                    sheet1.write(
                                        row, 6, result["quiz_section_result_list"][i]["section_name"])
                                    sheet1.write(
                                        row, 7, result["quiz_section_result_list"][i]["diff_score"])
                                    sheet1.write(
                                        row, 8, result["quiz_section_result_list"][i]["total_questions"])
                                    sheet1.write(
                                        row, 9, result["quiz_section_result_list"][i]["no_questions_attempted"])
                                    sheet1.write(
                                        row, 10, result["quiz_section_result_list"][i]["right_answers"])
                                    row += 1
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            logger.error("Error DownloadApplicantReport:%s at %s", str(
                                e), str(exc_tb.tb_lineno))
                            pass
                            row += 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("Error DownloadApplicantReport:%s at %s", str(
                        e), str(exc_tb.tb_lineno))
                    pass
            filename = "applicant-score-sheet" + str(timezone.now()) + ".xls"
            export_nps_wb.save(settings.MEDIA_ROOT + filename)
            path_to_file = settings.MEDIA_ROOT + str(filename)
            response['file_url'] = "/files/" + str(filename)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error DownloadApplicantReport: %s at %s",
                     str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)"""

def DownloadApplicantReport(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)

            from xlwt import Workbook, easyxf
            export_nps_wb = Workbook()
            sheet_name = "Applicant Profile Sheet"

            sheet1 = export_nps_wb.add_sheet(
                sheet_name, cell_overwrite_ok=True)
            
            #sheet2 = export_nps_wb.add_sheet("Applicant Results Sheet", cell_overwrite_ok=True)
            
            st = easyxf("align: horiz center; font: bold on, color-index blue;")
            st2 = easyxf("align: horiz center;")
            i=0
            sheet1.write(0, i, "Applicant ID", st)
            i+=1
            sheet1.write(0, i, "Applicant Name", st)
            i+=1
            sheet1.write(0, i, "Email", st)
            i+=1
            sheet1.write(0, i, "Contact Number", st)
            i+=1
            sheet1.write(0, i, "Date of birth", st)
            i+=1
            sheet1.write(0, i, "Gender", st)
            i+=1
            sheet1.write(0, i, "Location", st)
            i+=1
            sheet1.write(0, i, "Institute", st)
            i+=1
            sheet1.write(0, i, "Stream", st)
            i+=1
            sheet1.write(0, i, "Specialization", st)
            i+=1
            sheet1.write(0, i, "Percentage", st)
            i+=1
            sheet1.write(0, i, "Graduation Year", st)
            i+=1
            sheet1.write(0, i, "Interview Type", st)
            i+=1
            sheet1.write(0, i, "Event", st)
            i+=1
            sheet1.write(0, i, "Adhar Number", st)
            i+=1
            sheet1.write(0, i, "Pan Number", st)
            i+=1
            sheet1.write(0, i, "Current Company", st)
            i+=1
            sheet1.write(0, i, "Current Designation", st)
            i+=1
            sheet1.write(0, i, "Current CTC", st)
            i+=1
            sheet1.write(0, i, "Quiz name (Completed Time)", st)
            i+=1
            sheet1.write(0, i, "Quiz score", st)
            i+=1

            #sheet2.write(0, 0, "Applicant Name", st)
            #sheet2.write(0, 1, "Quiz Name (completed on)", st)
            #sheet2.write(0, 2, "Quiz score below name", st)

            row = 1
            row2 = 1
            for applicant_obj in applicant_objs:
                i=0
                sheet1.write(row, i, get_value_or_na(applicant_obj.applicant_id))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.name))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.email_id))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.phone_number))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.dob.strftime("%d/%m/%Y")))
                i+=1
                if get_value_or_na(applicant_obj.gender) == "N/A":
                    sheet1.write(row, i, "N/A")
                elif applicant_obj.gender == "1":
                    sheet1.write(row, i, "Male")
                elif applicant_obj.gender == "2":
                    sheet1.write(row, i, "Female")
                else:
                    sheet1.write(row, i, "Other")
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.location))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.college_name))
                i+=1
                #sheet1.write(row, i, get_value_or_na(applicant_obj.stream.name))
                if applicant_obj.stream:
                    sheet1.write(row, i, get_value_or_na(applicant_obj.stream.name))
                else:
                    sheet1.write(row, i, "N/A")
                #sheet1.write(row, i, "Stream Value")
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.specialization))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.percentage))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.year_of_passing))
                i+=1
                if get_value_or_na(applicant_obj.category) =="N/A":
                    sheet1.write(row, i, "N/A")
                elif applicant_obj.category == "1":
                    sheet1.write(row, i, "Campus")
                elif applicant_obj.gender == "2":
                    sheet1.write(row, i, "Walk-in")
                else:
                    sheet1.write(row, i, "Posting")
                i+=1
                if applicant_obj.event:
                    sheet1.write(row, i, get_value_or_na(applicant_obj.event.name))
                else:
                    sheet1.write(row, i, "N/A")
                #sheet1.write(row, i, get_value_or_na(applicant_obj.event.name))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.id_proof_adhaar_number))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.id_proof_pan_number))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.current_company))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.current_designation))
                i+=1
                sheet1.write(row, i, get_value_or_na(applicant_obj.current_ctc))
                i+=1

                #sheet2.write(row2, 0, get_value_or_na(applicant_obj.name))

                try:
                    quiz_status_objs = QuizStatus.objects.filter(
                        applicant=applicant_obj)

                    i2=1

                    for quiz_status_obj in quiz_status_objs:
                        try:
                            try:
                                quiz_result_obj = QuizResult.admin_objects.get(applicant=applicant_obj,quiz_status=quiz_status_obj,
                                                                     quiz=quiz_status_obj.quiz)
                            except:
                                quiz_result_obj = QuizResult.admin_objects.create(applicant=applicant_obj,quiz_status=quiz_status_obj,
                                                                     quiz=quiz_status_obj.quiz)

                            quiz_result_obj.generate_quiz_result()

                            result = json.loads(quiz_result_obj.result)

                            sheet1.write(row, i, quiz_status_obj.quiz.title + ' (' + quiz_status_obj.get_completion_date() + ')')
                            i+=1

                            result_string = ""

                            subjective_percentage = 0
                            no_subjective_section = 0
                            recruiter_remark = -1

                            for quiz_section in result['quiz_section_result_list']:

                                if quiz_section['type'] == "OBJ":
                                    result_string += quiz_section['section_name'] + "(OBJ): score:" +str(quiz_section['diff_score']) +" %"
                                    result_string+=" || "

                                elif quiz_section['type'] == "SUB":
                                    if quiz_section['diff_score'] == -1:
                                        subjective_percentage = -1
                                    elif subjective_percentage != -1:
                                        subjective_percentage += quiz_section['diff_score']
                                    no_subjective_section += 1
                                else:

                                    recruiter_remark = quiz_section['recruiter_remark']

                            if no_subjective_section != 0:

                                if subjective_percentage == -1:
                                    result_string += "SUB: Pending || "
                                else:
                                    result_string += "SUB: Applicant Percentage: "+str(round(subjective_percentage/no_subjective_section,2))+" % || " 

                            if recruiter_remark != -1:

                                result_string += "VID: Recruiter's Remark: "+recruiter_remark+" || "

                            result_string = result_string[:-4]

                            sheet1.write(row, i, result_string)
                            i+=1

                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            logger.error("Error DownloadApplicantReport:%s at %s", str(
                                e), str(exc_tb.tb_lineno))
                            pass
#                        try:
#                            quiz_result_obj = QuizResult.objects.get(applicant=applicant_obj,
#                                                                     quiz=quiz_status_obj.quiz)
#                            if quiz_result_obj.result == None:
#                                continue
#                            result = json.loads(quiz_result_obj.result)
#                            #sheet1.write(row, i, quiz_status_obj.quiz.title + ' (' + str(quiz_status_obj.completion_date.strftime('%d/%m/%Y %H:%M')) + ')')
#                            sheet1.write(row, i, quiz_status_obj.quiz.title + ' (' + quiz_status_obj.get_completion_date() + ')')
#                            i+=1
#                            sheet1.write(row, i, result['applicant_total_score'])
#                            i+=1
#
#                            #sheet2.write(row2, i2, quiz_status_obj.quiz.title + ' (' + str(quiz_status_obj.completion_date.strftime('%d/%m/%Y %H:%M')) + ')', st2)
#                            #sheet2.write(row2+1, i2, result['applicant_total_score'], st2)
#                            i2 += 1
#
#                        except Exception as e:
#                            exc_type, exc_obj, exc_tb = sys.exc_info()
#                            logger.error("Error DownloadApplicantReport:%s at %s", str(
#                                e), str(exc_tb.tb_lineno))
#                            pass
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("Error DownloadApplicantReport:%s at %s", str(
                        e), str(exc_tb.tb_lineno))
                    pass
                row += 1
                row2 += 2

            filename = "applicant-score-sheet" + str(timezone.now()) + ".xls"
            export_nps_wb.save(settings.MEDIA_ROOT + filename)
            path_to_file = settings.MEDIA_ROOT + str(filename)
            response['file_url'] = "/files/" + str(filename)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error DownloadApplicantReport: %s at %s",
                     str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)




def SaveApplicantAtIRecruit(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_applicants):
            data = request.POST["data"]
            data = json.loads(data)
            applicant_objs = get_applicant_objs_from_applicant_id_list(
                data["selected_applicant_id_list"], Applicant)
            for applicant_obj in applicant_objs:
                try:
                    last_quiz_status = applicant_obj.get_assigned_quiz_status()
                    quiz_result_obj = QuizResult.objects.get(applicant=applicant_obj, quiz=last_quiz_status.quiz)
                    push_applicant_data_at_irecruit(applicant_obj, quiz_result_obj)
                except Exception as e:
                    logger.error(str(e)+ "  -  Can not push at iRecruit")
                    pass
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error SaveApplicantAtIRecruit: %s at %s",
                        str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def MasterAdministrator(request):
    if is_user_authenticated(request) and request.user.role == "2":
        administrator_objs = Administrator.objects.filter(role="3")
        #event_objs = Event.objects.all()
        event_objs = Event.objects.filter(is_activated=True)
        context = {
        "administrator_objs":administrator_objs,
        "event_objs":event_objs,
        }
        print(administrator_objs)
        return render(request, "EasyHireApp/administrator/create-administrator.html",context)
    else:
        return redirect("/login")

#def CreateAdministrator(request):
#    response = {
#        "status_code": 500,
#        "status_message": "Internal Server Error"
#    }
#    try:
#        if is_user_authenticated(request) and request.user.role == "2":
#            data = request.POST["data"]
#            data = json.loads(data)
#            username = data["username"]
#            try:
#                User.objects.get(username=username)
#                response["status_code"]= 301
#            except Exception:
#                name = data["name"]
#                email = data["email"]
#                password = data["password"]
#                administator_obj = Administrator.objects.create(username=username,
#                                            first_name=name,
#                                            email=email,
#                                            role="3")
#                administator_obj.set_password(password)
#                administator_obj.administrator_id = administator_obj.pk
#                administator_obj.save()
#                response["status_code"] = 200
#                response["status_message"] = "SUCCESS"
#        else:
#            response["status_code"] = 404
#            response["status_message"] = "Invalid Access"
#    except Exception as e:
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        logger.error("Error CreateAdministrator: %s at %s",
#                        str(e), str(exc_tb.tb_lineno))
#
#    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def CreateAdministrator(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            username = data["username"]
            try:
                user = User.objects.get(username=username)
                if user.pk != int(data['administrator_id']):
                    response["status_code"] = 301
                else:
                    raise Exception
            except Exception:
                name = data["name"]
                email = data["email"]
                password = data["password"]
                events = data["events"]
                # feature admin rights
                print(data)
                if data['administrator_id'] == "-1":
                    no_active_administrators = Administrator.objects.filter(role="3", is_active=True).count()
                    if no_active_administrators < MAX_ACTIVE_ADMINISTRATOR:
                        administrator_obj = Administrator.objects.create(username=username,
                                                first_name=name,
                                                email=email,
                                                role="3")
                    else:
                        response['max_admin'] = MAX_ACTIVE_ADMINISTRATOR
                        response['status_message'] = "Invalid access"
                        response['status_code'] = 400
                        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
                else:
                    administrator_obj = Administrator.objects.get(administrator_id=int(data['administrator_id']))


                print(administrator_obj)
                if password != "":
                    administrator_obj.set_password(password)
                administrator_obj.save()
                administrator_obj.administrator_id = str(administrator_obj.pk)

                administrator_obj.can_create_applicants = False
                administrator_obj.can_manage_applicants = False
                administrator_obj.can_manage_quiz = False
                administrator_obj.can_manage_database = False
                administrator_obj.has_access_to_all_events = False

                if "can_create_applicants" in data['rights']:
                    administrator_obj.can_create_applicants = True
                if "can_manage_applicants" in data['rights']:
                    administrator_obj.can_manage_applicants = True
                if "can_manage_quiz" in data['rights']:
                    administrator_obj.can_manage_quiz = True
                if "can_manage_database" in data['rights']:
                    administrator_obj.can_manage_database = True
                if "has_access_to_all_events" in data['rights']:
                    administrator_obj.has_access_to_all_events = True

                administrator_obj.event_list.clear()

                administrator_obj.save()

                for event_pk in events:
                    try:
                        event = Event.objects.get(pk=int(event_pk))
                        administrator_obj.event_list.add(event)
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        logger.error("Error CreateAdministrator: %s at %s",
                                     str(e), str(exc_tb.tb_lineno))

                administrator_obj.save()

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error CreateAdministrator: %s at %s",
                        str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)



def DeactivateAdministrator(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            administrator_id = data["administrator_id"]
            try:
                administator_obj = Administrator.objects.get(pk=int(administrator_id))
                administator_obj.is_active = False
                administator_obj.save()
            except Exception as e:
                print(e)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def ActivateAdministrator(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            administrator_id = data["administrator_id"]
            no_active_administrators = Administrator.objects.filter(role="3", is_active=True).count()
            if no_active_administrators < MAX_ACTIVE_ADMINISTRATOR:
                try:
                    administator_obj = Administrator.objects.get(pk=int(administrator_id))
                    administator_obj.is_active = True
                    administator_obj.save()
                    response["status_code"] = 200
                    response["status_message"] = "SUCCESS"
                except Exception as e:
                    print(e)
            else:
                response['max_admin'] = MAX_ACTIVE_ADMINISTRATOR
                response['status_code'] = 400
                response['status_message'] = 'Invalid operation'
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error ActivateAdministrator: %s at %s",
                        str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def MasterEvents(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
        if request.user.role == "2":
            event_objs = Event.objects.all()
        else:
            event_objs = request.user.administrator.get_event_objs()
        applicant_objs = Applicant.objects.all()
        no_applicants = []
        count = 0
        for event_obj in event_objs:
            for applicant_obj in applicant_objs:
                if(applicant_obj.event == event_obj):
                    count+=1
            no_applicants.append({
                "event": event_obj.name,
                "count":count
                })
            count = 0
        #quiz_section_objs = QuizSection.objects.all()
        quiz_objs = Quiz.objects.all()
        return render(request, "EasyHireApp/administrator/master_events.html", {
            "event_objs": event_objs,
            "no_applicants":no_applicants,
            #"applicant_objs":applicant_objs,
            #"quiz_section_objs":quiz_section_objs,
            "quiz_objs":quiz_objs
        })
    else:
        return redirect("/login")

def AddMasterEvents(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            name = data["name"]
            """
            quiz_id = data["event_quiz"]
            quiz_section_obj = QuizSection.objects.get(pk=int(quiz_id))
            Event.objects.create(name=name, quiz_section=quiz_section_obj)
            """
            event_obj = Event.objects.create(name=name, category=data["category"])
            quiz_ids = data["event_quiz"]
            quiz_section_obj = []
            #for quiz_id in quiz_ids:
            #    quiz_section_obj = QuizSection.objects.get(pk=int(quiz_id))
            #    event_obj.quiz_section.add(quiz_section_obj)
            for quiz_id in quiz_ids:
                quiz_section_objs = QuizSection.objects.filter(quiz__pk=int(quiz_id))
                event_obj.quiz_section.add(*list(quiz_section_objs))
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        logger.error("AddMasterEvent %s",e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def DeleteMasterEvents(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            event_obj = Event.objects.get(pk=int(event_id))
            event_obj.delete()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def MasterDepartments(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
        department_objs = Department.objects.all()
        applicant_objs = Applicant.objects.all()
        no_applicants = []
        count = 0
        for department_obj in department_objs:
            for applicant_obj in applicant_objs:
                if(applicant_obj.department == department_obj):
                    count+=1
            no_applicants.append({
                "department": department_obj.name,
                "count":count
                })
            count = 0
        return render(request, "EasyHireApp/administrator/manage_departments.html", {
            "department_objs": department_objs,
            "no_applicants":no_applicants,
            #"applicant_objs":applicant_objs
        })
    else:
        return redirect("/login")

def AddMasterDepartments(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            name = data["name"]
            Department.objects.create(name=name)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def DeleteMasterDepartments(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            department_id = data["department_id"]
            department_obj = Department.objects.get(pk=int(department_id))
            department_obj.delete()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        logger.error(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

"""
def EditMasterEvents(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            quiz_id = data["event_quiz"]
            quiz_section_obj = QuizSection.objects.get(pk=int(quiz_id))
            logger.info(quiz_section_obj)
            event_obj = Event.objects.get(pk=int(event_id))
            logger.info(event_obj)
            event_obj.quiz_section = quiz_section_obj
            event_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        logger.error("EditEvent %s",e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
"""
def EditMasterEvents(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            event_obj = Event.objects.get(pk=int(event_id))
            event_obj.category = data['category']
            event_obj.quiz_section.clear()
            #quiz_section_obj = QuizSection.objects.get(pk=int(quiz_id))
            quiz_ids = data["event_quiz"]
            quiz_section_obj = []
            #for quiz_id in quiz_ids:
            #    quiz_section_obj = QuizSection.objects.get(pk=int(quiz_id))
            #    event_obj.quiz_section.add(quiz_section_obj)
            for quiz_id in quiz_ids:
                quiz_section_objs = QuizSection.objects.filter(quiz__pk=int(quiz_id))
                event_obj.quiz_section.add(*list(quiz_section_objs))
            event_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def GetQuizSectionList(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        data = request.POST["data"]
        data = json.loads(data)
        event_id = data["event_id"]
        event_obj = Event.objects.get(pk=int(event_id))
        quiz_section_objs = event_obj.quiz_section.all()
        quiz_section_list = []
        quiz_section_id_list = []
        quiz_objs = []
        for quiz_section_obj in quiz_section_objs:
            if quiz_section_obj.quiz not in quiz_objs:
                quiz_section_list.append(quiz_section_obj.quiz.title)
                quiz_section_id_list.append(quiz_section_obj.pk)
                quiz_objs.append(quiz_section_obj.quiz)
        response["event_id"] = quiz_section_id_list
        response["quiz_section"] = quiz_section_list
        response["status_code"] = 200
    except Exception as e:
        logger.error(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def ActivateEvent(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            try:
                event_obj = Event.objects.get(pk=int(event_id))
                event_obj.is_activated = True
                event_obj.save()
            except Exception as e:
                logger.error(e)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        logger.error(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

def DeactivateEvent(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            try:
                event_obj = Event.objects.get(pk=int(event_id))
                event_obj.is_activated = False
                event_obj.save()
            except Exception as e:
                logger.error(e)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        logger.error(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
"""
def DownloadEventExcel(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and request.user.role == "2":
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            event_obj = Event.objects.filter(pk=int(event_id))
            applicant_objs = Applicant.objects.filter(event=event_obj[0])
            quiz_attempted = 0
            from xlwt import Workbook
            export_nps_wb = Workbook()
            sheet_name = "Event Sheet"
            sheet1 = export_nps_wb.add_sheet(sheet_name)
            sheet1.write(0, 0, "Event")
            sheet1.write(0, 1, "Qualification")
            sheet1.write(0, 2, "Total Applicant")
            sheet1.write(0, 3, "Quiz Attempted")
            sheet1.write(0, 4, "Quiz Pending")
            sheet1.write(0, 5, "Avg. Score")
            index = 1
            quiz_section_objs = event_obj[0].quiz_section.all()
            try:
                for quiz_section_obj in quiz_section_objs:
                    sheet1.write(index, 0,event_obj[0].name)
                    sheet1.write(index, 1,quiz_section_obj.quiz.title)
                    total_applicant_objs = QuizSectionResult.objects.filter(quiz_section=quiz_section_obj)
                    sheet1.write(index, 2,len(total_applicant_objs))
                    quiz_section_results = QuizSectionResult.objects.filter(quiz_section=quiz_section_obj)
                    quiz_completed = 0
                    quiz_pending = 0
                    for quiz_section_result in quiz_section_results:
                        if quiz_section_result.is_completed == True:
                            quiz_completed += 1
                        else:
                            quiz_pending +=1
                    sheet1.write(index, 3,quiz_completed)
                    sheet1.write(index, 4,quiz_pending)

                    quiz_result_objs = QuizResult.objects.filter(quiz=quiz_section_obj.quiz)
                    total_appliant_quiz = len(quiz_result_objs)
                    average_result = 0.0
                    total_score = 0.0
                    for quiz_result_obj in quiz_result_objs:
                        try:
                            json_result = json.loads(quiz_result_obj.result)
                        except Exception:
                            pass
                        score = float(json_result['applicant_total_score'])
                        score = round(score,2)
                        total_score += score
                    try:
                        average_result = float(total_score/float(total_appliant_quiz))
                    except Exception as e:
                        average_result = 0.0
                    print(average_result)
                    sheet1.write(index, 5,float(average_result))
                    index = index + 1
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("Error DownloadEventExcel:%s at %s",str(e), str(exc_tb.tb_lineno))
                index+=1
                pass

            filename = "event-excel-sheet" + str(timezone.now()) +".xls"
            export_nps_wb.save(settings.MEDIA_ROOT +  filename)
            path_to_file = settings.MEDIA_ROOT + str(filename)
            print(path_to_file)
            response['file_url'] = "/files/" + str(filename)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error DownloadEventExcel: %s at %s",
                        str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

"""
def DownloadEventExcel(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_database):
            data = request.POST["data"]
            data = json.loads(data)
            event_id = data["event_id"]
            event_obj = Event.objects.filter(pk=int(event_id))
            applicant_objs = Applicant.objects.filter(event=event_obj[0])
            quiz_attempted = 0
            from xlwt import Workbook
            export_nps_wb = Workbook()
            sheet_name = "Event Sheet"
            sheet1 = export_nps_wb.add_sheet(sheet_name)
            sheet1.write(0, 0, "Event")
            sheet1.write(0, 1, "Qualification")
            sheet1.write(0, 2, "Total Applicant")
            sheet1.write(0, 3, "Quiz Attempted")
            sheet1.write(0, 4, "Quiz Pending")
            sheet1.write(0, 5, "Avg. Score")
            index = 1
            quiz_section_objs = event_obj[0].quiz_section.all()
            try:
                for quiz_section_obj in quiz_section_objs:
                    sheet1.write(index, 0,event_obj[0].name)
                    sheet1.write(index, 1,quiz_section_obj.quiz.title)
                    applicant_objs = Applicant.objects.filter(event=event_obj[0])
                    quiz_section_result_objs = QuizSectionResult.objects.filter(quiz_section=quiz_section_obj)
                    total_applicants = 0
                    quiz_completed = 0
                    quiz_pending = 0
                    average_result = 0.0
                    total_score = 0.0
                    json_result = ""
                    for quiz_section_result_obj in quiz_section_result_objs:
                        for applicant_obj in applicant_objs:
                            if quiz_section_result_obj.applicant.pk == applicant_obj.pk:
                                total_applicants = total_applicants + 1
                    sheet1.write(index, 2,total_applicants)
                    for quiz_section_result_obj in quiz_section_result_objs:
                        for applicant_obj in applicant_objs:
                            if quiz_section_result_obj.applicant.pk == applicant_obj.pk:
                                print(applicant_obj)
                                quiz_pending = 0
                                if quiz_section_result_obj.is_completed == True:
                                    quiz_completed += 1
                            try:
                                quiz_result_obj = QuizResult.objects.get(quiz=quiz_section_result_obj.quiz_section.quiz,applicant = quiz_section_result_obj.applicant)
                                average_result = 0.0
                                total_score = 0.0
                                try:
                                    json_result = json.loads(quiz_result_obj.result)
                                except Exception:
                                    pass
                                score = float(json_result['applicant_total_score'])
                                score = round(score,2)
                                total_score += score
                                try:
                                    average_result = float(float(total_score)/float(total_appliant_quiz))
                                except Exception as e:
                                    average_result = 0.0
                            except Exception:
                                pass
                    sheet1.write(index, 3,quiz_completed)
                    sheet1.write(index, 4,(total_applicants-quiz_completed))
                    # quiz_result_objs = QuizResult.objects.filter(quiz=quiz_section_obj.quiz)
                    # total_appliant_quiz = len(quiz_result_objs)
                    sheet1.write(index, 5,float(average_result))
                    index = index + 1
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("Error DownloadEventExcel:%s at %s",str(e), str(exc_tb.tb_lineno))
                index+=1
                pass

            filename = "event-excel-sheet.xls"
            export_nps_wb.save(settings.MEDIA_ROOT +  filename)
            path_to_file = settings.MEDIA_ROOT + str(filename)
            print(path_to_file)
            response['file_url'] = "/files/" + str(filename)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error DownloadEventExcel: %s at %s",
                        str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def GetEventList(request):
    response = {
        "status_code": 500,
        "status_message": "Internal Server Error"
    }
    try:
        data = request.POST["data"]
        data = json.loads(data)
        category = data["category"]

        event_objs = Event.objects.filter(category__in=["4",category], is_activated=True)

        event_list = []

        for event in event_objs:
            event_list.append({
                'pk': event.pk,
                'name': event.name
            })
        response["events"] = event_list
        response["status_code"] = 200
    except Exception as e:
        logger.error(e)

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)





def EditApplicantsPage(request):
    try:
        #if is_user_authenticated(request) and request.user.username == "hr_test":
        if is_user_authenticated(request):
            master_quiz_objs = Quiz.objects.all()
            #master_institutes_objs = Institute.objects.all()
            master_stream_objs = Stream.objects.all()
            master_event_objs = Event.objects.all()

            master_department_objs = Department.objects.all()
            filter_list = []
            applicant_objs = []
            list_of_sets_objs = []

            applicant_objs = Applicant.objects.all()

            campus_applicant_objs = []
            if "is_campus" in request.GET and request.GET["is_campus"] == "True":
                campus_applicant_objs = get_list_of_campus_applicants(Applicant)
                list_of_sets_objs.append(set(campus_applicant_objs))
                filter_list.append("4")

            walkin_applicant_objs = []
            if "is_walkin" in request.GET and request.GET["is_walkin"] == "True":
                walkin_applicant_objs = get_list_of_walkin_applicants(Applicant)
                list_of_sets_objs.append(set(walkin_applicant_objs))
                filter_list.append("5")

            posting_applicant_objs = []
            if "is_posting" in request.GET and request.GET["is_posting"] == "True":
                posting_applicant_objs = get_list_of_posting_applicants(Applicant)
                list_of_sets_objs.append(set(posting_applicant_objs))
                filter_list.append("6")

            rejected_applicant_objs = []
            if "is_rejected" in request.GET and request.GET["is_rejected"] == "True":
                rejected_applicant_objs = get_list_of_rejected_applicants(Applicant)
                list_of_sets_objs.append(set(rejected_applicant_objs))
                filter_list.append("1")

            selected_applicant_objs = []
            if "is_selected" in request.GET and request.GET["is_selected"] == "True":
                selected_applicant_objs = get_list_of_selected_applicants(
                    Applicant)
                list_of_sets_objs.append(set(selected_applicant_objs))
                filter_list.append("2")

            nonapproved_applicant_objs = []
            if "is_nonapproved" in request.GET and request.GET["is_nonapproved"] == "True":
                nonapproved_applicant_objs = get_list_of_non_approved_applicants(
                    Applicant)
                list_of_sets_objs.append(set(nonapproved_applicant_objs))
                filter_list.append("3")
            male_applicant_objs = []
            if "is_male" in request.GET and request.GET["is_male"] == "True":
                male_applicant_objs = Applicant.objects.filter(gender="1")
                list_of_sets_objs.append(set(male_applicant_objs))
                filter_list.append("7")

            female_applicant_objs = []
            if "is_female" in request.GET and request.GET["is_female"] == "True":
                female_applicant_objs = Applicant.objects.filter(gender="2")
                list_of_sets_objs.append(set(female_applicant_objs))
                filter_list.append("8")

            others_applicant_objs = []
            if "is_others" in request.GET and request.GET["is_others"] == "True":
                others_applicant_objs = Applicant.objects.filter(gender="2")
                list_of_sets_objs.append(set(others_applicant_objs))
                filter_list.append("9")
           
            department_filter_list = []
            department_applicants_objs = []
            if "department" in request.GET:
                department_pk_list = request.GET.getlist("department")
                department_objs = []
                for department_pk in department_pk_list:
                    department_objs.append(Department.objects.get(pk=int(department_pk)))
                    department_filter_list.append(int(department_pk))
                for department_obj in department_objs:
                    applicant_objs = Applicant.objects.filter(department=department_obj)
                    for applicant_obj in applicant_objs:
                        department_applicants_objs.append(applicant_obj)
                list_of_sets_objs.append(set(department_applicants_objs))
            stream_filter_list = []
            stream_applicant_objs = []
            if "stream" in request.GET:
                stream_pk_list = request.GET.getlist("stream")
                stream_objs = []
                for stream_pk in stream_pk_list:
                    stream_objs.append(
                        Stream.objects.get(pk=int(stream_pk)))
                    stream_filter_list.append(int(stream_pk))
                stream_applicant_objs = get_list_of_applicants_for_given_stream(
                    Applicant, stream_objs)
                list_of_sets_objs.append(set(stream_applicant_objs))

            quiz_filter_list = []
            quiz_applicant_objs = []
            quiz_status_objs = []
            if "quiz" in request.GET:
                quiz_pk_list = request.GET.getlist("quiz")
                quiz_objs = []
                for quiz_pk in quiz_pk_list:
                    quiz_objs.append(Quiz.objects.get(pk=int(quiz_pk)))
                    quiz_filter_list.append(int(quiz_pk))
                for quiz_obj in quiz_objs:
                    quiz_status_objs = QuizStatus.objects.filter(quiz=quiz_obj)
                    for quiz_status_obj in quiz_status_objs:
                        applicant_obj = quiz_status_obj.applicant
                        quiz_applicant_objs.append(applicant_obj)
                list_of_sets_objs.append(set(quiz_applicant_objs))
            event_filter_list = []
            event_applicants_objs = []
            if "event" in request.GET:
                event_pk_list = request.GET.getlist("event")
                event_objs = []
                for event_pk in event_pk_list:
                    event_objs.append(Event.objects.get(pk=int(event_pk)))
                    event_filter_list.append(int(event_pk))
                for event_obj in event_objs:
                    applicant_objs = Applicant.objects.filter(event=event_obj)
                    for applicant_obj in applicant_objs:
                        event_applicants_objs.append(applicant_obj)
                list_of_sets_objs.append(set(event_applicants_objs))

            date_applicant_objs = []
            start_date = ""
            if "date" in request.GET:
                start_date = request.GET["date"]
                date_format = "%Y-%m-%d"
                datetime_start = datetime.strptime(start_date, date_format).date()
                date_applicant_objs = Applicant.objects.filter(attempted_datetime__date=datetime_start)
                list_of_sets_objs.append(set(date_applicant_objs))
            else:
                if "all" in request.GET:
                    list_of_sets_objs.append(set(applicant_objs))
                    filter_list.append("10")
                elif ("is_campus" in request.GET) or ("is_walkin" in request.GET) or ("is_posting" in request.GET) \
                        or ("is_male" in request.GET) or ("is_female" in request.GET) or ("is_others" in request.GET) \
                        or ("is_selected" in request.GET) or ("is_rejected" in request.GET) or ("event" in request.GET) \
                        or ("is_nonapproved" in request.GET) or ("quiz" in request.GET) or ("group" in request.GET) \
                        or ("stream" in request.GET) or ("department" in request.GET) or ("institute" in request.GET):
                    logger.info("Apply Filter")
                else:
                    start_date = datetime.now()
                    date_format = "%Y-%m-%d"
                    datetime_start = datetime.strftime(
                        start_date, date_format)
                    start_date = datetime_start
                    date_applicant_objs = Applicant.objects.filter(
                        attempted_datetime__date=datetime_start)
                    list_of_sets_objs.append(set(date_applicant_objs))
         
            if len(list_of_sets_objs) > 0:
                applicant_objs = list(set.intersection(*list_of_sets_objs))

            # debug_change add filter

            applicant_info = ""

            if "applicant-info" in request.GET:
                applicant_info = request.GET["applicant-info"]
                # debug admin rights
                applicant_objs = Applicant.objects.all().order_by("pk")
                print(applicant_info)
                applicant_objs = list(set(applicant_objs.filter(name__icontains = applicant_info))|\
                                set(applicant_objs.filter(email_id__icontains = applicant_info))|\
                                set(applicant_objs.filter(phone_number__icontains = applicant_info)))

            return render(request, "EasyHireApp/administrator/edit-applicants.html", {
                #"master_institutes_objs": master_institutes_objs,
                "master_quiz_objs": master_quiz_objs,
                "applicant_objs": applicant_objs,
                "filter_list": filter_list,
                #"institute_filter_list": institute_filter_list,
                "quiz_filter_list": quiz_filter_list,
                "APPLICANT_APPLICATION_STATUS": APPLICANT_APPLICATION_STATUS,
                "master_event_objs":master_event_objs,
                "event_filter_list":event_filter_list,
                "master_stream_objs":master_stream_objs,
                "stream_filter_list":stream_filter_list,
                "master_department_objs":master_department_objs,
                "department_filter_list":department_filter_list,
                "male_applicant_objs":male_applicant_objs,
                "female_applicant_objs":female_applicant_objs,
                "others_applicant_objs":others_applicant_objs,
                "start_date":start_date,
                # debug_change add filter
                "applicant_info":applicant_info,
            })
        else:
            return redirect("/login")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error EditApplicantsPage: %s at %s",(e), str(exc_tb.tb_lineno))
    return HttpResponse("Invalid Access")

class GetApplicantQuizzesAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            if is_user_authenticated(request) and (request.user.role == "2"):
                allow_access = True
           
            if allow_access:
                data = request.data

                applicant_id = data["applicant_id"]

                applicant_obj = Applicant.objects.get(pk=int(applicant_id))

                event_objs = Event.objects.all()

                event_list = []

                for event in event_objs:
                    event_list.append({'pk':event.pk, 'name':event.name})

                assigned_quiz_objs = QuizStatus.objects.filter(applicant=applicant_obj)

                assigned_quizzes = []

                for quiz_status in assigned_quiz_objs:
                    assigned_quizzes.append({'pk':quiz_status.pk, 'name':quiz_status.quiz.title})

                if applicant_obj.event:
                    response["assigned_event"] = applicant_obj.event.pk
                else:
                    response["assigned_event"] = None
                response["assigned_quizzes"] = assigned_quizzes
                response["event_list"] = event_list
                response["applicant_name"] = applicant_obj.name 
                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error GetApplicantQuizzesAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

GetApplicantQuizzes = GetApplicantQuizzesAPI.as_view()

class UpdateApplicantTaskAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            if is_user_authenticated(request) and (request.user.role == "2"):
                allow_access = True
           
            if allow_access:
                data = request.data

                applicant_id = data["applicant_id"]

                applicant_obj = Applicant.objects.get(pk=int(applicant_id))

                if int(data['update_event']) == 1:
                    try:
                        event_obj = Event.objects.get(pk=int(data['event_pk']))
                    except:
                        event_obj = None

                    applicant_obj.event = event_obj
                    applicant_obj.save()
                else:
                    quiz_status_pk_list = json.loads(data['deassigned_quiz_list'])

                    for quiz_status_pk in quiz_status_pk_list:
                        delete_quiz_history(quiz_status_pk)

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error GetApplicantQuizzesAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

UpdateApplicantTask = UpdateApplicantTaskAPI.as_view()


#
#def delete_quiz_history(quiz_status_pk):
#
#    try:
#
#        quiz_status = QuizStatus.objects.get(pk=int(quiz_status_pk))
#
#        quiz = quiz_status.quiz
#
#        quiz_sections = QuizSection.objects.filter(quiz = quiz)
#
#        attempted_problem_list = ProblemAttempted.objects.filter(quiz_section__in=quiz_sections, applicant=quiz_status.applicant)
#
#        quiz_section_results = QuizSectionResult.objects.filter(quiz_section__in = quiz_sections, applicant__pk = quiz_status.applicant.pk)
#
#
#        data = get_all_things_about_quiz(quiz_status.applicant.pk  , quiz_status.pk)
#
#        section_timings = []
#        for quiz_section_result in quiz_section_results:
#            payload = {}
#            payload['time_spent'] = quiz_section_result.get_duration()
#            payload['section_name'] = quiz_section_result.quiz_section.topic.name
#            section_timings.append(payload)
#
#        quiz_result_obj = QuizResult.objects.get(applicant=quiz_status.applicant,
#                                                         quiz=quiz_status.quiz)
#
#
#        
#        attempted_problem_single_choice_objs = ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
#                                                                quiz_status = quiz_status,
#                                                                    applicant=quiz_status.applicant,
#                                                                    problem__category=PROBLEM_CATEGORY_SINGLE_CORRECT)
#
#
#        single_choice_section = []
#
#        for attempted_problem_single_choice_obj in attempted_problem_single_choice_objs:
#            payload = {}
#            payload['question'] = attempted_problem_single_choice_obj.problem.description
#            payload['options'] = attempted_problem_single_choice_obj.options
#            payload['calculated_score'] = (attempted_problem_single_choice_obj.calculated_score)
#            single_choice_section.append(payload)
#
#
#        attempted_problem_multi_choice_objs   =ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
#                                                                quiz_status = quiz_status,
#                                                                    applicant=quiz_status.applicant,
#                                                                    problem__category=PROBLEM_CATEGORY_MULTI_CORRECT) 
#
#
#        single_multi_choice_section = []
#
#        for attempted_problem_multi_choice_obj in attempted_problem_multi_choice_objs:
#            payload = {}
#            payload['question'] = attempted_problem_multi_choice_obj.problem.description
#            payload['options'] = attempted_problem_multi_choice_obj.options
#            payload['calculated_score'] = (attempted_problem_multi_choice_obj.calculated_score)
#            single_multi_choice_section.append(payload)
#
#
#
#        attempted_problem_descriptive_objs = ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
#                                                                quiz_status = quiz_status,
#                                                                    applicant=quiz_status.applicant,
#                                                                    problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)
#
#
#         
#
#
#        descriptive_section = []
#
#        for attempted_problem_descriptive_obj in attempted_problem_descriptive_objs:
#            payload = {}
#            payload['question'] = attempted_problem_descriptive_obj.problem.description
#            payload['answer'] = attempted_problem_descriptive_obj.answer
#            payload['calculated_score'] = (attempted_problem_descriptive_obj.calculated_score)
#            descriptive_section.append(payload)
#
#
#        attempted_problem_video_section_objs = ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
#                                                                    quiz_status = quiz_status,
#                                                                    applicant=quiz_status.applicant,
#                                                                    problem__category=PROBLEM_CATEGORY_VIDEO)
#        
#        video_section = []
#        for attempted_problem_video_section_obj in attempted_problem_video_section_objs:
#            payload = {}
#            payload['question'] = attempted_problem_video_section_obj.problem.description
#            payload['video_url'] = attempted_problem_video_section_obj.video_url
#            video_section.append(payload)
#
#
#        quiz_history = {"single_choice_section" :single_choice_section,"single_multi_choice_section" :single_multi_choice_section , "descriptive_section" :descriptive_section , "video_section": video_section}
#
#
#        quiz_assign_time = "N/A"
#        try:
#            quiz_assign_time = quiz_status.assigned_date + timedelta(hours=5, minutes=30)
#        except Exception as e:
#            quiz_assign_time = "N/A"
#
#
#        quiz_sessions  =  json.dumps({
#            'timings' : section_timings,
#            'descriptive_percentage' : quiz_status.generate_quiz_description_result(),
#            'recruiter_remark' : quiz_result_obj.recruiter_remark,
#            'quiz_assign_time' : str(quiz_assign_time),
#            'quiz_start_time' : str(quiz_status.get_quiz_start_time()),
#            'quiz_end_time' : str(quiz_status.get_completion_date())  ,
#            'section_timings' : section_timings    
#            })
#
#
#
#        quiz_history = QuizHistory(applicant=quiz_status.applicant,
#        quiz_status=quiz_status,
#        quiz_timing_info=json.dumps(data),
#        quiz_history=json.dumps(quiz_history),
#        quiz_sessions = quiz_sessions,
#        image_list = quiz_status.images,
#        quiz_name = quiz_status.quiz.title
#        )
#
#        quiz_history.save()
#
#      
#
#        quiz_status.quiz_history = json.dumps({
#            'timings' : section_timings,
#            'descriptive_percentage' : quiz_status.generate_quiz_description_result(),
#            'recruiter_remark' : quiz_result_obj.recruiter_remark,
#            'quiz_assign_time' : str(quiz_assign_time),
#            'quiz_start_time' : str(quiz_status.get_quiz_start_time()),
#            'quiz_end_time' : str(quiz_status.get_completion_date())      
#            })
#
#
#        
#        attempted_problem_list.update(is_deleted=True)
#
#        quiz_section_results.update(is_deleted=True)
#
#        quiz_result = QuizResult.objects.filter(quiz=quiz, applicant__pk = quiz_status.applicant.pk)
#        #quiz_result.delete()
#        quiz_result.update(is_deleted=True)
#
#
#        quiz_status.is_deleted = True
#        quiz_status.is_deleted_date_time = datetime.now()
#        quiz_status.save()
#
#        try:
#            if len(QuizStatus.objects.filter(applicant=quiz_status.applicant.pk , is_deleted = False)) == 0:
#                applicant_obj = Applicant.objects.get(pk = quiz_status.applicant.pk)
#                applicant_obj.status = None
#                applicant_obj.save()
#        except Exception as e:
#            exc_type, exc_obj, exc_tb = sys.exc_info()
#            logger.error("Error deassign quiz: %s at %s",
#                        str(e), str(exc_tb.tb_lineno))
#
#
#
#
#    except Exception as e:
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        logger.error("Error delete_quiz_history: %s at %s",
#                        str(e), str(exc_tb.tb_lineno))




def delete_quiz_history(quiz_status_pk):

    try:

        quiz_status = QuizStatus.objects.get(pk=int(quiz_status_pk))

        quiz = quiz_status.quiz

        quiz_sections = QuizSection.objects.filter(quiz = quiz)

        attempted_problem_list = ProblemAttempted.objects.filter(quiz_section__in=quiz_sections, applicant=quiz_status.applicant)

        quiz_section_results = QuizSectionResult.objects.filter(quiz_section__in = quiz_sections, applicant__pk = quiz_status.applicant.pk)


        data = get_all_things_about_quiz(quiz_status.applicant.pk  , quiz_status.pk)

        section_timings = []
        for quiz_section_result in quiz_section_results:
            payload = {}
            payload['time_spent'] = quiz_section_result.get_duration()
            payload['section_name'] = quiz_section_result.quiz_section.topic.name
            section_timings.append(payload)
        
        quiz_result_obj = None
        try:
            quiz_result_obj = QuizResult.objects.get(applicant=quiz_status.applicant,
                                                         quiz=quiz_status.quiz)


        
            attempted_problem_single_choice_objs = ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
                                                                quiz_status = quiz_status,
                                                                    applicant=quiz_status.applicant,
                                                                    problem__category=PROBLEM_CATEGORY_SINGLE_CORRECT)


            single_choice_section = []

            for attempted_problem_single_choice_obj in attempted_problem_single_choice_objs:
                payload = {}
                payload['question'] = attempted_problem_single_choice_obj.problem.description
                payload['options'] = attempted_problem_single_choice_obj.options
                payload['calculated_score'] = (attempted_problem_single_choice_obj.calculated_score)
                single_choice_section.append(payload)


            attempted_problem_multi_choice_objs   =ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
                                                                quiz_status = quiz_status,
                                                                    applicant=quiz_status.applicant,
                                                                    problem__category=PROBLEM_CATEGORY_MULTI_CORRECT) 


            single_multi_choice_section = []

            for attempted_problem_multi_choice_obj in attempted_problem_multi_choice_objs:
                payload = {}
                payload['question'] = attempted_problem_multi_choice_obj.problem.description
                payload['options'] = attempted_problem_multi_choice_obj.options
                payload['calculated_score'] = (attempted_problem_multi_choice_obj.calculated_score)
                single_multi_choice_section.append(payload)



            attempted_problem_descriptive_objs = ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
                                                                quiz_status = quiz_status,
                                                                    applicant=quiz_status.applicant,
                                                                    problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)


         


            descriptive_section = []

            for attempted_problem_descriptive_obj in attempted_problem_descriptive_objs:
                payload = {}
                payload['question'] = attempted_problem_descriptive_obj.problem.description
                payload['answer'] = attempted_problem_descriptive_obj.answer
                payload['calculated_score'] = (attempted_problem_descriptive_obj.calculated_score)
                descriptive_section.append(payload)


            attempted_problem_video_section_objs = ProblemAttempted.admin_objects.filter(quiz_section__quiz=quiz,
                                                                    quiz_status = quiz_status,
                                                                    applicant=quiz_status.applicant,
                                                                    problem__category=PROBLEM_CATEGORY_VIDEO)
        
            video_section = []
            for attempted_problem_video_section_obj in attempted_problem_video_section_objs:
                payload = {}
                payload['question'] = attempted_problem_video_section_obj.problem.description
                payload['video_url'] = attempted_problem_video_section_obj.video_url
                video_section.append(payload)


            quiz_history = {"single_choice_section" :single_choice_section,"single_multi_choice_section" :single_multi_choice_section , "descriptive_section" :descriptive_section , "video_section": video_section}


            quiz_assign_time = "N/A"
            try:
                quiz_assign_time = quiz_status.assigned_date + timedelta(hours=5, minutes=30)
            except Exception as e:
                quiz_assign_time = "N/A"


            quiz_sessions  =  json.dumps({
                'timings' : section_timings,
                'descriptive_percentage' : quiz_status.generate_quiz_description_result(),
                'recruiter_remark' : quiz_result_obj.recruiter_remark,
                'quiz_assign_time' : str(quiz_assign_time),
                'quiz_start_time' : str(quiz_status.get_quiz_start_time()),
                'quiz_end_time' : str(quiz_status.get_completion_date())  ,
                'section_timings' : section_timings    
                })



            quiz_history = QuizHistory(applicant=quiz_status.applicant,
            quiz_status=quiz_status,
            quiz_timing_info=json.dumps(data),
            quiz_history=json.dumps(quiz_history),
            quiz_sessions = quiz_sessions,
            image_list = quiz_status.images,
            quiz_name = quiz_status.quiz.title
            )

            quiz_history.save()
        except Exception as e:
            QuizHistory.objects.create(applicant=quiz_status.applicant,
            quiz_status=quiz_status,quiz_name = quiz_status.quiz.title , is_blank=True)



        if quiz_result_obj is None:
            quiz_status.quiz_history = json.dumps({
                'timings' : section_timings,
                'descriptive_percentage' : quiz_status.generate_quiz_description_result(),
                'recruiter_remark' : quiz_result_obj.recruiter_remark,
                'quiz_assign_time' : str(quiz_assign_time),
                'quiz_start_time' : str(quiz_status.get_quiz_start_time()),
                'quiz_end_time' : str(quiz_status.get_completion_date())      
                })
        else:
            quiz_status.quiz_history = json.dumps({
                'timings' : section_timings,
                'descriptive_percentage' : quiz_status.generate_quiz_description_result(),
                'recruiter_remark' : '',
                'quiz_assign_time' : str(quiz_assign_time),
                'quiz_start_time' : str(quiz_status.get_quiz_start_time()),
                'quiz_end_time' : str(quiz_status.get_completion_date())      
                })


        
        attempted_problem_list.update(is_deleted=True)

        quiz_section_results.update(is_deleted=True)

        quiz_result = QuizResult.objects.filter(quiz=quiz, applicant__pk = quiz_status.applicant.pk)
        #quiz_result.delete()
        quiz_result.update(is_deleted=True)


        quiz_status.is_deleted = True
        quiz_status.is_deleted_date_time = datetime.now()
        quiz_status.save()

        try:
            if len(QuizStatus.objects.filter(applicant=quiz_status.applicant.pk , is_deleted = False)) == 0:
                applicant_obj = Applicant.objects.get(pk = quiz_status.applicant.pk)
                applicant_obj.status = None
                applicant_obj.save()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error deassign quiz: %s at %s",
                        str(e), str(exc_tb.tb_lineno))




    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error delete_quiz_history: %s at %s",
                        str(e), str(exc_tb.tb_lineno))


def UpdateApplicantProfile(request):

    response = {'status': 500, 'message': "Internal server error, try again later"}

    if is_user_authenticated(request) and request.user.role == "2":

        try:

            data = json.loads(request.POST['data'])

            applicant = Applicant.objects.get(pk=int(data['applicant_pk']))


            applicant.name = data['name']

            other_applicant = Applicant.objects.filter(email_id=data['email_id']).exclude(pk=int(data['applicant_pk']))
            if len(other_applicant):
                response['message'] = "Applicant with this email id already exists"
                raise Exception("Applicant with this email id already exists")
            applicant.email_id = data['email_id']

            other_applicant = Applicant.objects.filter(phone_number=data['phone_number']).exclude(pk=int(data['applicant_pk']))
            if len(other_applicant):
                response['message'] = "Applicant with this phone number already exists"
                raise Exception("Applicant with this phone number already exists")
            applicant.phone_number = data['phone_number']
            applicant.username = applicant.phone_number

            other_applicant = Applicant.objects.filter(id_proof_adhaar_number=data['adhaar']).exclude(
                pk=int(data['applicant_pk']))
            if len(other_applicant):
                response['message'] = "Applicant with this adhaar number already exists"
                raise Exception("Applicant with this adhaar number already exists")
            applicant.id_proof_adhaar_number = data['adhaar']

            other_applicant = Applicant.objects.filter(id_proof_pan_number=data['pan']).exclude(
                pk=int(data['applicant_pk']))
            if len(other_applicant):
                response['message'] = "Applicant with this PAN number already exists"
                raise Exception("Applicant with this PAN number already exists")
            applicant.id_proof_pan_number = data['pan']
            applicant.save()

            if len(data['password']):
                applicant.set_password(data['password'])
                applicant.save()
                applicant.is_applicant_online = False
                applicant.save()

            response['status'] = 200

        except Exception as e:
            print(str(e))
            logger.error("Error UpdateApplicantProfile: %s", str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)



##### Question Banks Excel Download Excel Dump Topic wise

def GetTopicProblemExcel(request):

    response = {
        'status_code': 500,
        'file_path': None,
    }
    try:
        #if is_user_authenticated(request) and request.user.role == "2" and request.method == 'POST' and request.user.username == "hr_test":
        if is_user_authenticated(request) and request.user.role == "2" and request.method == 'POST':
            data = json.loads(request.POST['data'])

            topic_pk = int(data['topic_pk'])
            topic = Topic.objects.get(pk=topic_pk)

            file_path = generate_topic_problem_excel(topic)

            response['status_code'] = 200
            response['file_path'] = file_path

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error GetTopicProblemExcel: %s at %s", e, str(exc_tb.tb_lineno))
    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


class ActivateQuizAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            # feature admin rights
            # fc
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
                allow_access = True

            if allow_access:
                data = request.data
                # print(data)
                quiz_id = int(data["quiz_id"])

                quiz_obj = Quiz.objects.get(pk=quiz_id)
                quiz_obj.is_activated = True
                quiz_obj.save()

                quiz_objs_with_same_name = Quiz.objects.filter(title=quiz_obj.title).exclude(pk=quiz_id)

                for quiz_obj in quiz_objs_with_same_name:
                    quiz_obj.is_activated = False
                    quiz_obj.save()

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error ActivateQuizAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

ActivateQuiz = ActivateQuizAPI.as_view()

class DeactivateQuizAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            # feature admin rights
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
                allow_access = True

            if allow_access:
                data = request.data
                # print(data)
                quiz_id = int(data["quiz_id"])

                quiz_obj = Quiz.objects.get(pk=quiz_id)

                quiz_obj.is_activated = False

                quiz_obj.save()

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error DeactivateQuizAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

DeactivateQuiz = DeactivateQuizAPI.as_view()



class CopyQuizContentAPI(APIView):
    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            # feature admin rights
            if is_user_authenticated(request) and request.user.role == "2":
                allow_access = True

            if allow_access:
                data = request.data
                # print(data)

                source_quiz_pk = int(data['source_quiz_pk'])
                destination_quiz_pk = int(data['destination_quiz_pk'])

                source_quiz = Quiz.objects.get(pk=source_quiz_pk)
                destination_quiz = Quiz.objects.get(pk=destination_quiz_pk)

                if destination_quiz.is_editable():
                    source_quiz_sections = QuizSection.objects.filter(quiz=source_quiz)

                    destination_quiz_sections = QuizSection.objects.filter(quiz=destination_quiz)
                    destination_quiz_sections.delete()

                    for quiz_section in source_quiz_sections:
                        quiz_section.pk = None
                        quiz_section.quiz = destination_quiz
                        quiz_section.save()

                    destination_quiz.instruction = source_quiz.instruction
                    destination_quiz.is_sectional_timed = source_quiz.is_sectional_timed
                    destination_quiz.buffer_time = source_quiz.buffer_time
                    destination_quiz.save()

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error CopyQuizContentAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


CopyQuizContent = CopyQuizContentAPI.as_view()



class ActivateTopicAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            # feature admin rights
            # fc
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
                allow_access = True

            if allow_access:
                data = request.data
                # print(data)
                topic_id = int(data["topic_id"])

                topic_obj = Topic.objects.get(pk=topic_id)
                topic_obj.is_activated = True
                topic_obj.save()

                topic_objs_with_same_name = Quiz.objects.filter(title=topic_obj.title).exclude(pk=quiz_id)

                for topic_obj in topic_objs_with_same_name:
                    topic_obj.is_activated = False
                    topic_obj.save()

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error ActivateTopicAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

ActivateTopic = ActivateTopicAPI.as_view()

class DeactivateTopicAPI(APIView):

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            allow_access = False
            # feature admin rights
            if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
                allow_access = True

            if allow_access:
                data = request.data
                # print(data)
                topic_id = int(data["topic_id"])
                print(f"Topic Id - {topic_id} is getting deactivated")
                topic_obj = Topic.objects.get(pk=topic_id)
                topic_obj.is_activated = False
                topic_obj.save()
                print(f"Topic Id - {topic_id} is successfully deactivated with is_activated={topic_obj.is_activated}")

                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error DeactivateTopicAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)

DeactivateTopic = DeactivateTopicAPI.as_view()
