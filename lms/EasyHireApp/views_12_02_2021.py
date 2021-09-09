from django.core.paginator import EmptyPage
from django.shortcuts import render, redirect, HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

from EasyHireApp.models import *
from EasyHireApp.utils import *
from EasyHireApp.views_applicant import *
from EasyHireApp.constants import *
from EasyHireApp.views_administrator import *

import pytz
import base64
import logging
import threading
import sys
import math

logger = logging.getLogger(__name__)


def HomePage(request):
    if request.user.is_authenticated and request.user.role == "1":
        return redirect("/applicant/dashboard/")
    elif request.user.is_authenticated and request.user.role == "2":
        return redirect("/administrator/manage-applicants/")
    elif request.user.is_authenticated and request.user.role == "3":
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
        return render(request, 'EasyHireApp/home.html', {})


def UserLogout(request):
    if is_user_authenticated(request):
        if request.user.role == "1":
            applicant_obj = Applicant.objects.get(username=request.user.username)
            applicant_obj.is_applicant_online = False
            applicant_obj.save()
        logout(request)
    return redirect("/")


# Quiz
def ManageQuiz(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        quiz_objs = Quiz.objects.all()
        return render(request, "EasyHireApp/quiz/manage-quiz.html", {
            "quiz_objs": quiz_objs
        })
    else:
        return redirect("/login")


def ManageTopics(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        topics = Topic.objects.all()
        return render(request, 'EasyHireApp/quiz/manage-only-topic.html', {
            "topics": topics
        })
    else:
        return redirect("/login")


def AddQuizConfig(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        data = request.POST["data"]
        json_data = json.loads(data)
        quiz_title = json_data["quiz_title"]
        # try:
        #    Quiz.objects.get(title=ascii_string(quiz_title))
        # except Exception as e:
        #    Quiz.objects.create(title=ascii_string(quiz_title))
        if Quiz.objects.filter(title=ascii_string(quiz_title)).count() == 0:
            Quiz.objects.create(title=ascii_string(quiz_title))
        return HttpResponse("200")
    else:
        return HttpResponse("404")
        # return render(request, 'EasyHireApp/administrator/404.html', {})


def AddTopic(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        data = request.POST["data"]
        json_data = json.loads(data)
        topic_name = json_data["topic_name"]
        category = json_data["category"]
        try:
            Topic.objects.get(name=ascii_string(topic_name))
        except Exception as e:
            Topic.objects.create(name=ascii_string(topic_name), category=category)
        return HttpResponse("200")
    else:
        return HttpResponse("404")


def SaveTopicCategory(request):
    response = {
        "status_code": 500,
    }
    if is_user_authenticated(request):
        if request.user.role == "2" or request.user.administrator.can_manage_quiz:
            data = json.loads(request.POST["data"])

            topic_obj = Topic.objects.get(pk=int(data['topic_pk']))

            category = data['category']

            if category == "1" or category == "2":
                category = ['1', '2']
            else:
                category = [category]

            problem_attempted = Problem.objects.filter(topics__in=[topic_obj]).exclude(category__in=category)

            print(category, problem_attempted)

            if len(problem_attempted):
                response["status_code"] = 400
                response["status_message"] = "Conflict in problem categories... cannot save topic category"
            else:
                topic_obj.category = category[0]
                topic_obj.save()
                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    else:
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def DeleteQuiz(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        data = request.POST["data"]
        json_data = json.loads(data)
        quiz_id = json_data["quiz_id"]
        Quiz.objects.get(pk=int(quiz_id)).delete()
        return HttpResponse("200")
    else:
        return HttpResponse("404")


def DeleteTopic(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        data = request.POST["data"]
        json_data = json.loads(data)
        topic_id = json_data["topic_id"]
        Topic.objects.get(pk=int(topic_id)).delete()
        return HttpResponse("200")
    else:
        return HttpResponse("404")


def RenameTopic(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        data = request.POST["data"]
        json_data = json.loads(data)
        topic_id = json_data["topic_id"]
        topic_name = json_data["topic_name"]
        topic_obj = Topic.objects.get(pk=int(topic_id))
        topic_obj.name = str(topic_name)
        topic_obj.save()
        return HttpResponse("200")
    else:
        return HttpResponse("404")


def AddProblem(request):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        objective_topics = Topic.objects.filter(category__in=["1", "2"])
        descriptive_topics = Topic.objects.filter(category__in=["3"])
        audio_topics = Topic.objects.filter(category__in=["4"])
        video_topics = Topic.objects.filter(category__in=["5"])
        return render(request, 'EasyHireApp/quiz/add-problem.html', {
            "PROBLEM_CATEGORY_CHOICES": list(PROBLEM_CATEGORY_CHOICES),
            "DIFFICULTY_CHOICES": list(DIFFICULTY_CHOICES),
            "objective_topics": objective_topics,
            "descriptive_topics": descriptive_topics,
            "video_topics": video_topics,
            "audio_topics": audio_topics,
            "is_editable": True
        })
    else:
        return redirect("/login")


def EditProblem(request, problem_pk):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        adminstrator_obj = Administrator.objects.get(username=str(request.user.username))
        problem_obj = Problem.objects.get(pk=int(problem_pk))

        is_editable = False
        if problem_obj.typed_by == adminstrator_obj and problem_obj.is_editable():
            is_editable = True

        objective_topics = Topic.objects.filter(category__in=["1", "2"])
        descriptive_topics = Topic.objects.filter(category__in=["3"])
        audio_topics = Topic.objects.filter(category__in=["4"])
        video_topics = Topic.objects.filter(category__in=["5"])

        return render(request, "EasyHireApp/quiz/add-problem.html", {
            "problem_obj": problem_obj,
            "PROBLEM_CATEGORY_CHOICES": list(PROBLEM_CATEGORY_CHOICES),
            "DIFFICULTY_CHOICES": list(DIFFICULTY_CHOICES),
            "objective_topics": objective_topics,
            "descriptive_topics": descriptive_topics,
            "video_topics": video_topics,
            "audio_topics": audio_topics,
            "choices": [],
            "is_editable": is_editable
        })
    else:
        return redirect("/login")


def RenderTopicProblem(request, topic_pk):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        topic_obj = Topic.objects.get(pk=int(topic_pk))
        problem_objs = Problem.objects.filter(topics__in=[topic_obj])
        can_delete = problem_objs.first().is_editable()

        can_delete = False
        if len(problem_objs):
            can_delete = problem_objs.first().is_editable()

        page = request.GET.get('page')
        paginator = Paginator(problem_objs, 10)
        try:
            problem_objs = paginator.page(page)
        except PageNotAnInteger:
            problem_objs = paginator.page(1)
        except EmptyPage:
            problem_objs = paginator.page(paginator.num_pages)

        if topic_obj.category is None:
            topics = Topic.objects.all().exclude(pk=topic_obj.pk)
        else:
            topics = Topic.objects.filter(category=topic_obj.category).exclude(pk=topic_obj.pk)

        topic_tag_objs = Tag.objects.filter(category="2")

        return render(request, 'EasyHireApp/quiz/topic.html', {
            "problem_objs": problem_objs,
            "topic_obj": topic_obj,
            "topics": topics,
            "topic_tag_objs": topic_tag_objs,
            "can_delete" : can_delete,
        })
    else:
        return redirect("/login")


class SaveProblemAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data
            if not isinstance(data, dict):
                data = json.loads(data)

            image_file = data['file']

            path = None
            if str(image_file) != "undefined" and str(image_file) != "null":
                path = default_storage.save(settings.IMAGE_UPLOAD_PATH + "/" + image_file.name.replace(" ", ""),
                                            ContentFile(image_file.read()))

            json_data = json.loads(data['data'])
            json_data["image_path"] = path
            problem_id = save_problem(json_data, request, Administrator, Problem, Topic)

            if problem_id != -1:
                response["status_code"] = 200

            response["problem_id"] = problem_id
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SaveProblemAPI: %s at %s", str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


SaveProblem = SaveProblemAPI.as_view()


def saveFile(uploaded_file):
    file_content = ContentFile(uploaded_file.read())
    file_path = default_storage.save(uploaded_file.name, file_content)
    return file_path


def import_video_from_excel(file_path, employee_obj, topic_obj):
    try:
        wb = xlrd.open_workbook("files/" + file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        return False, "Excel File Read Error"

    rows_error = "Error at following Rows (Sr. No):<br>"

    for i in range(1, sheet.nrows):
        try:
            category_id = "5"

            description = sheet.cell_value(i, 1)
            if len(description) == 0:
                raise Exception('Invalid description provided in question %s in file %s', str(i), str(file_path))

            try:
                solution = sheet.cell_value(i, 2)
            except Exception as e:
                solution = ""

            problem_obj = Problem.objects.create(description=description,
                                                 solution=str(solution),
                                                 category=category_id,
                                                 typed_by=employee_obj,
                                                 difficulty="1",
                                                 hint="",
                                                 image=None,
                                                 video=None,
                                                 pdf="")
            problem_obj.topics.add(topic_obj)
            problem_obj.save()

            # TopicProblem.objects.create(problem=problem_obj, topic=topic_obj)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error importDescriptiveQuestionFromExcel: %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            rows_error += str(i) + " "

    if rows_error == "Error at following Rows (Sr. No):<br>":
        return True, "Successfully"
    else:
        rows_error += "<br>Remaining Questions Are Uploaded.<br>Take note of above questions before refreshing the page."
        return False, rows_error


class UploadQuestionsExcelAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            if is_user_authenticated(request) and (
                    request.user.role == "2" or request.user.administrator.can_manage_quiz):
                data = request.data
                uploaded_file = request.FILES.getlist('file')[0]
                logger.info("File %s", str(uploaded_file))

                topic_pk = data["topic_pk"]
                type_of_questions = data["type_of_questions"]

                logger.info("Topic pk=%s", str(topic_pk))
                logger.info("Type of questions=%s", str(type_of_questions))

                topic_obj = None
                try:
                    topic_obj = Topic.objects.get(pk=topic_pk)
                    logger.info(
                        "UploadQuestionsExcelAPI Found Topic %s", str(topic_obj))
                except:
                    logger.error(
                        "UploadQuestionsExcelAPI Topic %s does not exist!", str(topic_pk))
                    return Response(data=response)

                adminstrator_obj = None
                try:
                    adminstrator_obj = Administrator.objects.get(username=request.user.username)
                    logger.info(
                        "UploadQuestionsExcelAPI Employee uploading %s", str(adminstrator_obj))
                except:
                    logger.error(
                        "UploadQuestionsExcelAPI Error getting employee")
                    return Response(data=response)

                file_extension = str(uploaded_file).split('.')[-1].lower()
                if (file_extension not in ["xls", "xlsx"]):
                    logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                    response["status"] = 301
                else:
                    try:
                        file_path = saveFile(uploaded_file)
                        logger.info("File Saved %s", str(file_path))
                        import_success, message = None, None

                        if type_of_questions == "1":
                            import_success, message = import_descriptive_from_excel(
                                file_path, adminstrator_obj, topic_obj)
                        #                        else:
                        #                            import_success, message = import_mcq_from_excel(
                        #                                file_path, adminstrator_obj, topic_obj)
                        elif type_of_questions == "2":
                            import_success, message = import_mcq_from_excel(
                                file_path, adminstrator_obj, topic_obj)
                        elif type_of_questions == "3":
                            import_success, message = import_video_from_excel(file_path, adminstrator_obj, topic_obj)
                        if import_success:
                            response["status"] = 200
                        else:
                            response["status"] = 302
                            response["message"] = message

                            logger.info("Some error occured while importing questions from excel file=%s",
                                        str(uploaded_file))
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        logger.error("Error UploadQuestionsExcelAPI: %s at %s", str(
                            e), str(exc_tb.tb_lineno))

                # response["status"] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error UploadQuestionsExcelAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


UploadQuestionsExcel = UploadQuestionsExcelAPI.as_view()


def DeleteProblem(request, topic_pk):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        topic_obj = Topic.objects.get(pk=int(topic_pk))
        problem_id_list = []
        if "problem_id" in request.GET:
            problem_id_list = request.GET.getlist("problem_id")
        for problem_id in problem_id_list:
            problem_obj = Problem.objects.get(pk=int(problem_id))
            problem_obj.topics.remove(topic_obj)
            problem_obj.save()
        return redirect("/manage-quiz/topic/" + str(topic_pk))
    else:
        return redirect("/")


def RenderQuizConfig(request, quiz_config_pk):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        quiz_obj = Quiz.objects.get(pk=int(quiz_config_pk))
        quiz_section_objs = QuizSection.objects.filter(quiz=quiz_obj)
        topics = Topic.objects.all()

        quiz_status = QuizStatus.objects.filter(quiz=quiz_obj, is_completed=False)
        is_editable = True
        if len(quiz_status):
            is_editable = False

        other_quiz_objs = Quiz.objects.all().exclude(pk=int(quiz_config_pk))

        # change tag
        quiz_tag_objs = Tag.objects.filter(category="1")

        return render(request, 'EasyHireApp/quiz/quiz-config.html', {
            "quiz_obj": quiz_obj,
            "topics": topics,
            "quiz_section_objs": quiz_section_objs,
            "is_editable": is_editable,
            "other_quiz_objs": other_quiz_objs,
            # change tag
            "quiz_tag_objs":quiz_tag_objs,
        })
    else:
        return redirect("/login")


"""def AddQuizSection(request):
    response = {
        "status_code": 404,
        "status_message": "Invalid Access"
    }
    if is_user_authenticated(request):
        if request.user.role == "2":
            data = request.POST["data"]
            json_data = json.loads(data)
            quiz_config_id = json_data["quiz_config_id"]
            quiz_section_weightage = json_data["quiz_section_weightage"]
            quiz_section_topic_id = json_data["quiz_section_topic_id"]
            quiz_section_no_questions = json_data["quiz_section_no_questions"]
            quiz_section_time = json_data["quiz_section_time"]

            quiz_obj = Quiz.objects.get(pk=int(quiz_config_id))
            topic_obj = Topic.objects.get(pk=int(quiz_section_topic_id))

            logger.info(topic_obj)
            logger.info(len(Problem.objects.filter(topics__in=[topic_obj])))

            if len(Problem.objects.filter(topics__in=[topic_obj])) < float(quiz_section_no_questions):
                logger.info(quiz_section_no_questions)
                response["status_code"] = 310
                response["status_message"] = str(
                    topic_obj.name) + " doesn't contains "+str(quiz_section_no_questions) + " questions."
                return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

            quiz_section_obj = None
            try:
                quiz_section_obj = QuizSection.objects.get(quiz=quiz_obj,
                                                           topic=topic_obj)
            except Exception as e:
                quiz_section_obj = QuizSection.objects.create(quiz=quiz_obj,
                                                              topic=topic_obj)

            positive_threshold = math.ceil((int(quiz_section_no_questions))/6)
            negative_threshold = math.ceil(positive_threshold/2)
            quiz_section_obj.weightage = quiz_section_weightage
            quiz_section_obj.no_questions = quiz_section_no_questions
            quiz_section_obj.time = quiz_section_time
            quiz_section_obj.positive_threshold = positive_threshold
            quiz_section_obj.negative_threshold = negative_threshold
            quiz_section_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    else:
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)"""


def AddQuizSection(request):
    response = {
        "status_code": 404,
        "status_message": "Invalid Access"
    }
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        if request.user.role == "2":
            data = request.POST["data"]
            logger.info(data)
            json_data = json.loads(data)
            quiz_config_id = json_data["quiz_config_id"]
            quiz_section_weightage = json_data["quiz_section_weightage"]
            quiz_section_topic_id = json_data["quiz_section_topic_id"]
            quiz_section_no_questions = json_data["quiz_section_no_questions"]
            quiz_section_time = json_data["quiz_section_time"]
            quiz_type = json_data["type"]
            quiz_easy_question = json_data["quiz_easy_question"]
            quiz_medium_question = json_data["quiz_medium_question"]
            quiz_hard_question = json_data["quiz_hard_question"]

            quiz_obj = Quiz.objects.get(pk=int(quiz_config_id))
            topic_obj = Topic.objects.get(pk=int(quiz_section_topic_id))

            logger.info(topic_obj)
            logger.info(len(Problem.objects.filter(topics__in=[topic_obj])))

            if len(Problem.objects.filter(topics__in=[topic_obj])) < float(quiz_section_no_questions):
                logger.info(quiz_section_no_questions)
                response["status_code"] = 310
                response["status_message"] = str(
                    topic_obj.name) + " doesn't contains " + str(quiz_section_no_questions) + " questions."
                return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

            quiz_section_obj = None
            try:
                quiz_section_obj = QuizSection.objects.get(quiz=quiz_obj,
                                                           topic=topic_obj)
            except Exception as e:
                quiz_section_obj = QuizSection.objects.create(quiz=quiz_obj,
                                                              topic=topic_obj)

            if quiz_type == "2":
                quiz_section_obj.is_quiz_section_static = True
                quiz_section_obj.easy_questions = quiz_easy_question
                quiz_section_obj.medium_questions = quiz_medium_question
                quiz_section_obj.hard_questions = quiz_hard_question
            else:
                quiz_section_obj.is_quiz_section_static = False
                quiz_section_obj.easy_questions = 0
                quiz_section_obj.medium_questions = 0
                quiz_section_obj.hard_questions = 0
            positive_threshold = math.ceil((int(quiz_section_no_questions)) / 6)
            negative_threshold = math.ceil(positive_threshold / 2)
            quiz_section_obj.weightage = quiz_section_weightage
            quiz_section_obj.no_questions = quiz_section_no_questions
            quiz_section_obj.time = quiz_section_time
            quiz_section_obj.positive_threshold = positive_threshold
            quiz_section_obj.negative_threshold = negative_threshold
            quiz_section_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    else:
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def DeleteQuizSection(request, quiz_section_pk):
    if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):
        if request.user.role == "2":
            quiz_section_obj = QuizSection.objects.get(pk=int(quiz_section_pk))
            quiz_config_pk = quiz_section_obj.quiz.pk
            quiz_section_obj.delete()
            return redirect("/manage-quiz/quiz/edit/" + str(quiz_config_pk))
        else:
            return HttpResponse("<h5>Invalid request</h5>")
    else:
        return HttpResponse("<h5>Invalid request</h5>")


class SaveQuizConfigAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data

            if not isinstance(data, dict):
                data = json.loads(data)

            data = json.loads(data["data"])
            quiz_id = data["quiz_id"]
            quiz_title = data["quiz_title"]
            quiz_instruction = data["quiz_instruction"]
            include_personality_profiler = data["include_personality_profiler"]
            is_sectional_timed = data["is_sectional_timed"]
            quiz_obj = Quiz.objects.get(pk=int(quiz_id))
            # quiz_obj.title = quiz_title
            quiz_obj_with_title = Quiz.objects.filter(title=quiz_title).exclude(pk=quiz_obj.pk)

            # change tag
            tag_obj = None
            try:
                tag_obj = Tag.objects.get(pk=int(data['tag_pk']))
            except:
                pass
            quiz_obj.tag = tag_obj

            if len(quiz_obj_with_title) == 0:
                response['status_code'] = 200
                quiz_obj.title = quiz_title
            else:
                response['status_code'] = 201
            quiz_obj.instruction = quiz_instruction
            quiz_obj.include_profiler = include_personality_profiler
            quiz_obj.is_sectional_timed = is_sectional_timed
            if is_sectional_timed:
                try:
                    buffer_time = int(data["buffer_time"])
                    if 1 < buffer_time <= 30:
                        quiz_obj.buffer_time = buffer_time
                except:
                    pass
            quiz_obj.save()
        except Exception as e:
            logger.error("SaveQuizConfigAPI: " + str(e))

        return Response(data=response)


SaveQuizConfig = SaveQuizConfigAPI.as_view()


def StartTestPage(request, quiz_uuid):
    if is_user_authenticated(request):
        if str(request.user.role) == "1":
            quiz_config = get_quiz_obj_with_uuid(quiz_uuid, Quiz)
            return render(request, 'EasyHireApp/test-instruction.html', {
                "quiz_config": quiz_config
            })
        else:
            return HttpResponse("<h5>Invalid Page Access</h5>")
    else:
        return redirect("/login")


def QuizPaper(request, quiz_uuid):
    if is_user_authenticated(request):
        if request.user.role == "1":
            quiz_config = get_quiz_obj_with_uuid(quiz_uuid, Quiz)

            """
            if quiz_config.is_quiz_started:
                logger.info("quiz is already started")
                quiz_seconds = (quiz_config.total_quiz_time()+1) * 60

                est = pytz.timezone(settings.TIME_ZONE)
                updated_quiz_start_datetime = quiz_config.quiz_start_datetime.astimezone(est) + datetime.timedelta(seconds=quiz_seconds)

                current_datetime = datetime.datetime.now().astimezone(est)

                logger.info(current_datetime)
                logger.info(updated_quiz_start_datetime)

                if current_datetime >= updated_quiz_start_datetime:
                    return redirect("/login")
            else:
                logger.info("quiz is started")
                quiz_config.is_quiz_started = True
                quiz_config.quiz_start_datetime = timezone.now()
                quiz_config.save()
            """

            quiz_status_obj = None
            try:
                from datetime import datetime
                quiz_status_obj = QuizStatus.objects.get(applicant=request.user.applicant, quiz=quiz_config)
                time_stamps = quiz_status_obj.time_stamps
                if time_stamps is None or time_stamps == "":
                    time_stamps = "[]"
                time_stamps = json.loads(time_stamps)
                time_stamps.append({
                    'login': str(datetime.now().strftime("%d-%B-%Y, %H:%M")),
                    'logout': "N/A"
                })
                quiz_status_obj.time_stamps = json.dumps(time_stamps)
                quiz_status_obj.save()
            except Exception as e:
                logger.error("QUIZ PAPER %s", str(e))

            quiz_sections = QuizSection.objects.filter(quiz=quiz_config)
            return render(request, 'EasyHireApp/quiz-paper.html', {
                "quiz_config": quiz_config,
                "quiz_sections": quiz_sections,
                "quiz_status_obj":quiz_status_obj.pk ,
            })
        else:
            return HttpResponse("<h5>Invalid Page Access</h5>")
    else:
        return redirect("/login")


def GetQuizConfig(request):
    response = {}
    response["status_code"] = 500
    try:
        if is_user_authenticated(request):
            quiz_uuid = request.GET["quiz_uuid"]
            quiz_config = get_quiz_obj_with_uuid(quiz_uuid, Quiz)

            quiz_sections = QuizSection.objects.filter(quiz=quiz_config)
            applicant_obj = Applicant.objects.get(
                username=request.user.username)

            quiz_status = QuizStatus.objects.get(
                quiz=quiz_config, applicant=applicant_obj)

            response["time"] = quiz_config.get_initial_time()
            response["quiz_uuid"] = quiz_uuid
            response["quiz_section"] = []

            remaining_time = quiz_status.time_remaining
            if remaining_time == None:
                remaining_time = -1

            quiz_section_category_map = {
                '1': 'Objective',
                '2': 'Objective',
                '3': 'Subjective',
                '4': 'Audio Viva',
                '5': 'Video Viva',
                None: "None"
            }

            incomplete_section_found = 0

            for quiz_section in quiz_sections:
                quiz_section_result_objs = QuizSectionResult.objects.filter(applicant=applicant_obj,
                                                                            quiz_section=quiz_section)

                is_completed = False
                completed = ''
                if len(quiz_section_result_objs) > 0:
                    is_completed = quiz_section_result_objs[0].is_completed
                    if quiz_section_result_objs[0].time_remaining > 0 and is_completed == False:
                        incomplete_section_found = quiz_section.pk
                    if is_completed:
                        completed = 'Completed'

                response["quiz_section"].append({
                    "id": quiz_section.pk,
                    "topic_name": quiz_section.topic.name,
                    "no_questions": quiz_section.no_questions,
                    "time": quiz_section.time,
                    "weightage": quiz_section.weightage,
                    "is_completed": is_completed,
                    "category": quiz_section_category_map[quiz_section.topic.category],
                    "message": completed
                })

            if incomplete_section_found and quiz_config.is_sectional_timed:
                for quiz_section in response['quiz_section']:
                    if quiz_section['id'] != incomplete_section_found:
                        if quiz_section['is_completed']:
                            quiz_section['message'] = 'Completed'
                        else:
                            quiz_section['message'] = 'Pending'
                            quiz_section['is_completed'] = True

            response["remaining_time"] = remaining_time
            response["status_code"] = 200
        else:
            response["status_code"] = 300
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error GetQuizSection: %s at %s", str(), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def GetQuizSection(request):
    response = {}
    response["status_code"] = 500
    try:
        if is_user_authenticated(request):

            applicant_obj = Applicant.objects.get(
                username=request.user.username)
            quiz_uuid = request.GET["quiz_uuid"]
            quiz_section_id = request.GET["quiz_section_id"]

            quiz_config = get_quiz_obj_with_uuid(quiz_uuid, Quiz)

            quiz_section = QuizSection.objects.get(quiz=quiz_config,
                                                   pk=int(quiz_section_id))

            problem_obj, quiz_section_result_obj = initiate_quiz_section(applicant_obj,
                                                                         quiz_config,
                                                                         quiz_section,
                                                                         QuizSectionResult,
                                                                         Problem)

            if problem_obj is None:
                response["status_code"] = 301
                return Response(data=response)

            response["status_code"] = 200
            response["time"] = quiz_section.time
            response["problem_id"] = problem_obj.pk

            cleanr = re.compile('<.*?>')
            problem_description = re.sub(cleanr, '', problem_obj.description)
            response["problem_description"] = problem_obj.description
            response["problem_category"] = problem_obj.category

            option_list = problem_obj.get_option_list()
            response["problem_choices"] = []
            for option in option_list:
                response["problem_choices"].append({
                    "value": option,
                    "display": option
                })

            response["problem_image"] = None
            response["problem_video"] = None
            response["problem_pdf"] = None
            response["problem_graph"] = None
            response["is_embed"] = False
            response["text_to_speech"] = problem_obj.text_to_speech
            response['time_remaining'] = quiz_section_result_obj.time_remaining
            response['is_sectional_timed'] = quiz_config.is_sectional_timed

            if problem_obj.image is not None:
                try:
                    response["problem_image"] = str(problem_obj.image.url)
                except Exception as e:
                    pass

            if str(problem_obj.video) != "None":
                response["problem_video"] = problem_obj.get_video_url_list()
                response["is_embed"] = []
                for video_url in response["problem_video"]:
                    if video_url.find("embed") != -1:
                        response["is_embed"].append(True)
                    else:
                        response["is_embed"].append(False)

            if problem_obj.pdf != None:
                try:
                    response["problem_pdf"] = str(problem_obj.pdf)
                except Exception as e:
                    pass

            if problem_obj.graph_url != None:
                response["problem_graph"] = problem_obj.get_graph_url_list()

            response["total_problems"] = quiz_section.no_questions
            response["no_questions_attempted"] = quiz_section_result_obj.no_question_attempted
        else:
            response["status_code"] = 300
    except Exception as e:
        logger.error("GetQuizSection: " + str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


class FetchNextProblemAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data["data"]
            request_packet = json.loads(str(data))
            applicant_obj = Applicant.objects.get(
                username=str(request.user.username))
            quiz_status_obj = request_packet.get["quiz_status_obj"]
            next_problem_obj, quiz_section_obj = get_next_problem(request_packet,
                                                                  applicant_obj,
                                                                  quiz_status_obj,
                                                                  Quiz,
                                                                  QuizSection,
                                                                  QuizSectionResult,
                                                                  Problem,
                                                                  ProblemAttempted)

            if next_problem_obj != None:
                response["problem_id"] = next_problem_obj.pk
                response["topic_name"] = quiz_section_obj.topic.name

                problem_obj = next_problem_obj

                cleanr = re.compile('<.*?>')
                problem_description = re.sub(
                    cleanr, '', problem_obj.description)
                response["problem_description"] = problem_obj.description
                response["problem_category"] = problem_obj.category

                option_list = problem_obj.get_option_list()
                random.shuffle(option_list)
                response["problem_choices"] = []
                for option in option_list:
                    response["problem_choices"].append({
                        "value": option,
                        "display": option
                    })

                response["problem_image"] = None
                response["problem_video"] = None
                response["problem_pdf"] = None
                response["problem_graph"] = None
                response["is_embed"] = False
                response["text_to_speech"] = problem_obj.text_to_speech

                if problem_obj.image != None:
                    try:
                        response["problem_image"] = str(problem_obj.image.url)
                    except Exception as e:
                        pass

                if str(problem_obj.video) != "None":
                    response["problem_video"] = problem_obj.get_video_url_list()
                    response["is_embed"] = []
                    for video_url in response["problem_video"]:
                        if video_url.find("embed") != -1:
                            response["is_embed"].append(True)
                        else:
                            response["is_embed"].append(False)

                if problem_obj.pdf != None:
                    try:
                        response["problem_pdf"] = str(problem_obj.pdf)
                    except Exception as e:
                        pass

                if problem_obj.graph_url != None:
                    response["problem_graph"] = problem_obj.get_graph_url_list()

            else:
                response["problem_id"] = -1

            response["status_code"] = 200
        except Exception as e:
            logger.error("FetchNextProblemAPI: " + str(e))

        return Response(data=response)


FetchNextProblem = FetchNextProblemAPI.as_view()


def TestComplete(request):
    response = {
        "status_code": 500,
        "is_quiz_ended": False
    }
    try:
        if is_user_authenticated(request) and request.method == "POST":

            applicant_obj = Applicant.objects.get(
                username=str(request.user.username))

            quiz_config_uuid = request.POST["unique_quiz_config_id"]
            time_up = request.POST['time_up'] == "true"
            """
            quiz_section_id = request.POST["quiz_section_id"]

            quiz_config = get_quiz_obj_with_uuid(quiz_config_uuid, Quiz)

            current_quiz_section = QuizSection.objects.get(pk=int(quiz_section_id),
                                                           quiz=quiz_config)
            """
            quiz_config = get_quiz_obj_with_uuid(quiz_config_uuid, Quiz)
            quiz_status = QuizStatus.objects.get(quiz=quiz_config, applicant=applicant_obj)
            quiz_section_id = request.POST["quiz_section_id"]

            print(time_up)

            if time_up:
                if quiz_config.is_sectional_timed:
                    try:
                        current_quiz_section = QuizSection.objects.get(quiz=quiz_config, pk=int(quiz_section_id))
                        applicant_completed_quiz_section(applicant_obj, current_quiz_section, QuizSectionResult)
                    except Exception as e:
                        logger.error("Error: time up quiz section complete: %s", str(e))
                        end_quiz(quiz_config, applicant_obj, QuizSectionResult)
                else:
                    end_quiz(quiz_config, applicant_obj, QuizSectionResult)
            else:
                try:
                    print("time is not up")
                    current_quiz_section = QuizSection.objects.get(quiz=quiz_config, pk=int(quiz_section_id))
                    applicant_completed_quiz_section(applicant_obj, current_quiz_section, QuizSectionResult)
                except Exception as e:
                    logger.error("Error: quiz section complete: %s", str(e))

            is_quiz_ended = quiz_status.is_quiz_ended()

            if is_quiz_ended:
                response["status_code"] = 200
                response["is_quiz_ended"] = True
                quiz_status.is_completed = True
                quiz_status.completion_date = datetime.now()
                quiz_status.save()
                send_quiz_submission_msg_to_applicant(applicant_obj,quiz_status.quiz.title)

                generate_result_task = threading.Thread(target=generate_applicant_quiz_result,
                                                        args=(applicant_obj, quiz_config, QuizResult,))
                generate_result_task.daemon = True
                generate_result_task.start()
                return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)

            response["status_code"] = 200
            response["is_quiz_ended"] = False
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
        else:
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    except Exception as e:
        logger.error("TestComplete: " + str(e))


def SyncRemainingQuizTime(request):
    response = {}
    response["status_code"] = 500
    response["status_message"] = "Internal Server Error"
    try:
        if is_user_authenticated(request) and request.user.role == "1":
            data = request.POST["data"]
            data = json.loads(data)
            quiz_config_id = data["quiz_config_id"]
            remaining_time = data["remaining_time"]
            quiz_section_id = data["quiz_section_id"]
            applicant_obj = Applicant.objects.get(username=request.user.username)

            quiz_config = get_quiz_obj_with_uuid(quiz_config_id, Quiz)

            if quiz_config.is_sectional_timed:
                if quiz_section_id is None:
                    QuizStatus.objects.filter(quiz=quiz_config, applicant=applicant_obj).update(time_remaining=remaining_time)
                else:
                    try:
                        quiz_section = QuizSection.objects.get(pk=int(quiz_section_id))
                        QuizSectionResult.objects.filter(applicant=applicant_obj, quiz_section=quiz_section).update(time_remaining=remaining_time)
                    except Exception as e:
                        logger.error("Error sync remaining time: %s", str(e))
            else:
                QuizStatus.objects.filter(quiz=quiz_config, applicant=applicant_obj).update(time_remaining=remaining_time)

            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        logger.error("SyncRemainingQuizTime: " + str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def SaveApplicantScreenShot(request):
    print(request)
    response = {}
    response["status_code"] = 500
    response["status_message"] = "Internal Server Error"
    try:
        if is_user_authenticated(request) and request.user.role == "1":

            applicant_obj = Applicant.objects.get(
                username=request.user.username)

            applicant_image = request.POST['applicant_image']
            quiz_uuid = request.POST["quiz_uuid"]
            print(quiz_uuid)
            random_string = generate_random_string_of_length_N(9)
            applicant_image_name = str(applicant_obj.name).replace(
                " ", "") + "_" + random_string
            print(applicant_image_name)

            image_name = applicant_image_name + "_pic.png"

            format, imgstr = applicant_image.split(';base64,')

            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

            image_path = default_storage.save("pics/" + image_name, data)
            quiz_obj = Quiz.objects.get(uuid=quiz_uuid)
            quiz_status_obj = QuizStatus.objects.get(applicant=applicant_obj,
                                                     quiz=quiz_obj)
            try:
                import ast
                image_list = ast.literal_eval(quiz_status_obj.images)
            except Exception:
                image_list = []
            image_path = "/files/" + image_path
            image_list.append(image_path)
            quiz_status_obj.images = image_list
            quiz_status_obj.save()
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("SaveApplicantScreenShot: %s at %s",
                     e, str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def SaveApplicantVideo(request):
    print(request)
    response = {}

    response["status_code"] = 500
    response["status_message"] = "Internal Server Error"
    try:
        if is_user_authenticated(request) and request.user.role == "1":

            applicant_obj = Applicant.objects.get(username=request.user.username)

            video_url = request.POST['video_data_url']
            quiz_uuid = request.POST['quiz_uuid']
            problem_id = request.POST['problem_id']
            # print("ASDSDF")
            print(quiz_uuid)
            # print(video_url)
            # print(problem_id)
            # print("HERHEHR")
            if video_url == "null":
                logger.error("VIDEO NOT ANSWERED")
                response["status_code"] = 200
                response["status_message"] = "SUCCESS"
                response["url"] = None
                return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
            random_string = generate_random_string_of_length_N(9)
            # applicant_video_name = str(applicant_obj.name).replace(" ", "") + "_" + random_string
            applicant_video_name = str(applicant_obj.name).replace(" ", "") + "_" + str(
                datetime.now().strftime('%d_%m_%Y_%H_%M')) + "_original_" + random_string
            print(applicant_video_name)

            video_name = applicant_video_name + "_video.webm"

            # file_ = open("video.txt","w")
            # file_.write(video_url)
            # file_.close()

            # print(video_url)

            # os.system('ffmpeg -i \''+video_url+'\' '+settings.BASE_DIR+'/files/videos/wow_'+video_name)

            format, imgstr = video_url.split(';base64,')

            ext = "webm"

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

            print("here")
            video_path = default_storage.save(video_name, data)
            video_path = video_path
            logger.info(video_path)
            print(video_path)
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
            response["url"] = video_path
        else:
            response["status_code"] = 404
            response["status_message"] = "Invalid Access"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("SaveApplicantVideo: %s at %s",
                     e, str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

# clip1= VideoFileClip('videoplayback.mp4')
# clip2= VideoFileClip('videoplayback1.mp4')

# final_clip = concatenate_videoclips([clip1,clip2])

# final_clip.write_videofile('newvideo1.mp4')
import os


def merge_quiz_videos(quiz_status_obj, applicant_obj):
    try:
        print("In function merge videos")

        print(quiz_status_obj, applicant_obj)
        try:
            import ast
            video_list = ast.literal_eval(quiz_status_obj.video)
        except Exception:
            video_list = []

        print(video_list)

        if len(video_list) > 0:

            print("here")

            file = open("input.txt", "w")

            for v in video_list:
                file.write("file '" + settings.BASE_DIR + v + "'\n")

            file.close()

            random_string = generate_random_string_of_length_N(9)
            applicant_video_name = str(applicant_obj.name).replace(
                " ", "") + "_" + random_string

            print(applicant_video_name)
            video_name = "/files/videos/" + applicant_video_name + "_video.webm"

            os.system('ffmpeg -f concat -safe 0 -i input.txt -c copy ' + settings.BASE_DIR + video_name)

            for v in video_list:
                os.remove(settings.BASE_DIR + v)

            quiz_status_obj.video = video_name
            quiz_status_obj.save()

            # final_clip.write_videofile("files/"+video_name)
    except Exception as e:
        print(str(e))


def SaveQuizReloadTime(request):
    response = {'status': "500"}
    try:
        from datetime import datetime

        if is_user_authenticated(request) and request.user.role == "1":

            print("save reload time")

            quiz_uuid = request.POST['quiz_uuid']

            quiz = get_quiz_obj_with_uuid(quiz_uuid, Quiz)

            quiz_status = QuizStatus.objects.get(applicant=request.user.applicant, quiz=quiz)

            time_stamps = quiz_status.time_stamps

            if time_stamps is None:
                time_stamps = "[]"

            time_stamps = json.loads(time_stamps)

            if len(time_stamps):
                time_stamps[len(time_stamps) - 1]['logout'] = str(datetime.now().strftime("%d-%B-%Y, %H:%M"))
            else:
                time_stamps.append({
                    'login': "N/A",
                    'logout': str(datetime.now().strftime("%d-%B-%Y, %H:%M")),
                })
            # print("SAVED LOGOUT")

            quiz_status.time_stamps = json.dumps(time_stamps)
            quiz_status.save()
            response['status'] = "200"
    except Exception as e:
        logger.error(str(e))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


###### For Downloading Excel Database Dump
def GetDatabasePage(request):
    #if is_user_authenticated(request) and request.user.role == "2" and request.user.username == "hr_test":
    if is_user_authenticated(request) and request.user.role == "2":
        return render(request, 'EasyHireApp/download_database.html')

    return redirect('/login')


def DownloadDatabaseExcel(request):
    response = {
        'status_code': "500",
        'file_path': None,
    }

    #if request.user.role == "2" and request.method == "POST" and request.user.username == "hr_test":
    if request.user.role == "2" and request.method == "POST":
        data = json.loads(request.POST['data'])
        print("DATA", data)

        if data['option'] == "1":
            # file_path = download_applicant_profiles(Applicant.objects.all())
            try:
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['end_date'] + " 23:59", "%Y-%m-%d %H:%M")
                applicant_objs = Applicant.objects.filter(date_joined__range=[start_date, end_date])
            except Exception as e:
                logger.error("Download database excel %s", str(e))
                applicant_objs = Applicant.objects.all()
            file_path = download_applicant_profiles(applicant_objs)

        elif data['option'] == "2":
            file_path = download_quiz_excel(Quiz.objects.all())
        elif data['option'] == "3":
            file_path = download_topic_excel(Topic.objects.all())
        elif data['option'] in ["4", "5"]:
            start_date = None
            end_date = None
            try:
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['end_date'] + " 23:59", "%Y-%m-%d %H:%M")
            except Exception as e:
                logger.error("Download consolidated videos %s", str(e))
            file_name = "Consolidated-Videos-" + str(datetime.now().strftime('%d-%m-%Y')) + ".zip"
            file_path = download_consolidated_videos(file_name, start_date, end_date)

        else:
            file_path = None

        if file_path == "-1":
            response['status_code'] = "300"
        else:
            response['status_code'] = "200"
            response['file_path'] = file_path

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


def ToggleProblemVisibility(request):
    response = {'status':500, 'message':"None"}
    try:
        if is_user_authenticated(request) and (request.user.role == "2" or request.user.administrator.can_manage_quiz):

            data = json.loads(request.POST['data'])

            problem = Problem.objects.get(pk=int(data['problem_pk']))

            if problem.is_active:
                problem.is_active = False
                response['message'] = "inactive"
            else:
                problem.is_active = True
                response['message'] = "active"
            problem.save()
            response['status'] = 200
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("ToggleProblemVisibility: %s at %s",
                     str(e), str(exc_tb.tb_lineno))

    return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)


class ImportTopicQuestionsAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            if is_user_authenticated(request) and request.user.role == "2":
                data = request.data

                source_topic_pk = int(data["source_topic_pk"])
                destination_topic_pk = int(data["destination_topic_pk"])
                delete_and_import = data['delete_and_import'] == "true"

                source_topic_obj = None
                try:
                    source_topic_obj = Topic.objects.get(pk=source_topic_pk)
                except:
                    logger.error(
                        "ImportTopicQuestionAPI Topic %s does not exist!", str(source_topic_pk))
                    return Response(data=response)

                destination_topic_obj = None
                try:
                    destination_topic_obj = Topic.objects.get(pk=destination_topic_pk)
                except:
                    logger.error(
                        "ImportTopicQuestionAPI Topic %s does not exist!", str(destination_topic_pk))
                    return Response(data=response)

                if delete_and_import:
                    problem_in_topics = Problem.objects.filter(topics__in=[destination_topic_obj])
                    for problem in problem_in_topics:
                        problem.topics.remove(destination_topic_obj)
                        problem.save()

                problem_to_be_copied = Problem.objects.filter(topics__in=[source_topic_obj])

                for problem in problem_to_be_copied:
                    if destination_topic_obj not in problem.topics.all():
                        problem.topics.add(destination_topic_obj)
                        problem.save()

                response['status'] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error ImportTopicQuestionAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


ImportTopicQuestions = ImportTopicQuestionsAPI.as_view()




def ChangeTopicTag(request):
    response = {
        "status_code": 500,
    }
    if is_user_authenticated(request):
        if (request.user.role == "2" or request.user.administrator.can_manage_quiz):
            data = json.loads(request.POST["data"])

            topic_obj = Topic.objects.get(pk=int(data['topic_pk']))

            tag_obj = None
            try:
                tag_obj = Tag.objects.get(pk=int(data['tag_pk']))
            except:
                pass

            topic_obj.tag = tag_obj
            topic_obj.save()

            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    else:
        return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
