from django.db import models
import sys
from django.utils import timezone
from EasyHireApp.constants import *
from django.db.models import Q, Count
import django.conf
import pytz
import re
import random
import datetime
import json
import math
import uuid
import logging
import os
from accounts.models import Student

logger = logging.getLogger(__name__)


class QuizStatusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class ProblemAttemptedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class QuizSectionResultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class QuizResultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)



class VideoBatchProcessingTime(models.Model):
    start_time = models.CharField(max_length=2, choices=BATCH_PROCESS_STARTING_HOURS, blank=False)
    number_of_hours = models.CharField(max_length=2, choices=BATCH_PROCESS_NUMBER_OF_HOURS, blank=False)

    class Meta:
        verbose_name = 'VideoBatchProcessingTime'
        verbose_name_plural = 'VideoBatchProcessingTime'

    def __str__(self):
        return self.start_time

    def save(self, *args, **kwargs):
        super(VideoBatchProcessingTime, self).save(*args, **kwargs)


class Institute(models.Model):

    name = models.CharField(max_length=1000, null=False, blank=False)

    is_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Institute'
        verbose_name_plural = 'Institutes'


class Event(models.Model):

    name = models.CharField(max_length=1000, null=True, blank=True)

    quiz_section = models.ManyToManyField(
        'EasyHireApp.QuizSection',blank=True)

    is_activated = models.BooleanField(default=True)


    category = models.CharField(max_length=10, choices=APPLICANT_CATEGORY, default="4")

    def get_category(self):
        category_map = {
            '1': 'Campus',
            '2': 'Walk-in',
            '3': 'Posting',
            '4': 'All',
        }
        return category_map[self.category]

    def __str__(self):
        return self.name

    def get_all_quiz(self):
        quiz_objs = set()
        for quiz_setion in self.quiz_section.all():
            quiz_objs.add(quiz_setion.quiz)
        return quiz_objs

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

class Department(models.Model):

    name = models.CharField(max_length=1000, null=False, blank=False)

    is_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

class Stream(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Stream'
        verbose_name_plural = 'Streams'

class IdentityProof(models.Model):

    document_name = models.CharField(max_length=100)

    def __str__(self):
        return self.document_name

    class Meta:
        verbose_name = 'IdentityProof'
        verbose_name_plural = 'IdentityProof'





class AppConfig(models.Model):

    is_quiz_activated = models.BooleanField(default=False)

    is_id_proof_required = models.BooleanField(default=True)

    is_employment_declaration_required = models.BooleanField(default=False)

    def __str__(self):
        return "AppConfig"

    class Meta:
        verbose_name = 'AppConfig'
        verbose_name_plural = 'AppConfig'


class Topic(models.Model):

    name = models.CharField(max_length=200, unique=True)

    category = models.CharField(max_length=10, choices=PROBLEM_CATEGORY_CHOICES, blank=True, null=True)

    tag = models.ForeignKey('EasyHireApp.Tag', on_delete=models.SET_NULL, blank=True, null=True)

    is_activated = models.BooleanField(null=True, blank= True,default=True)

    def get_category(self):
        category_map = {
            None: None,
            '1': "Objective",
            '3': "Descriptive",
            '5': "Video",
             '': None,
        }

        try:
            return category_map[self.category]
        except:
            logger.error("%s %s", self.name, self.category)
            print("%s %s", self.name, self.category)
            return None

    def shorten_name(self):
        if len(self.name) <= 21:
            return self.name
        else:
            return self.name[:20]+"..."

    def __str__(self):
        return self.name

    def is_editable(self):

        quiz_section_with_topic = QuizSection.objects.filter(topic=self)

        for quiz_section in quiz_section_with_topic:
            if not quiz_section.quiz.is_editable():
                return False

        return True

    #### Fetching All Questions

    def no_questions(self):
        return len(Problem.objects.filter(topics__in=[self]).distinct())

    def no_easy_question(self):
         return len(Problem.objects.filter(topics__in=[self], difficulty=DIFFICULTY_EASY).distinct())
    def no_medium_question(self):
        return len(Problem.objects.filter(topics__in=[self], difficulty=DIFFICULTY_MEDIUM).distinct())
    def no_hard_question(self):
        return len(Problem.objects.filter(topics__in=[self], difficulty=DIFFICULTY_HARD).distinct())

    #### Fetching only Activated Questions
    def no__easy_activated_question(self):
        return len(Problem.objects.filter(topics__in=[self], difficulty=DIFFICULTY_EASY , is_active=True).distinct())

    def no__medium_activated_question(self):
        return len(Problem.objects.filter(topics__in=[self], difficulty=DIFFICULTY_MEDIUM , is_active=True).distinct())

    def no__hard_activated_question(self):
        return len(Problem.objects.filter(topics__in=[self], difficulty=DIFFICULTY_HARD , is_active=True).distinct())

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class Problem(models.Model):

    image = models.ImageField(upload_to='problem', null=True, blank=True)

    video = models.TextField(null=True, blank=True)

    pdf = models.TextField(null=True, blank=True)

    graph_url = models.TextField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    solution = models.TextField(blank=True, null=True)

    hint = models.TextField(null=True, blank=True)

    answer = models.CharField(max_length=2000, blank=True)

    options = models.CharField(max_length=2000, blank=True)

    correct_options = models.CharField(max_length=2000, null=True,blank=True)

    category = models.CharField(max_length=1,
                                null=False,
                                blank=False,
                                choices=PROBLEM_CATEGORY_CHOICES)

    typed_by = models.CharField(max_length=200, blank=True ,null=True)

    difficulty = models.CharField(max_length=1,
                                  null=False,
                                  blank=False,
                                  choices=DIFFICULTY_CHOICES)

    topics = models.ManyToManyField(Topic, blank=True)

    date = models.DateField(auto_now=True)

    total_attempts = models.IntegerField(default=0)

    correct_attempts = models.IntegerField(default=0)

    text_to_speech = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'
        ordering = ['-id']

    def __str__(self):
        return self.description[:30]

    def is_editable(self):

        for topic in self.topics.all():
            if not topic.is_editable():
                return False
        return True

    def get_problem_difficuly_title(self):
        if self.difficulty == "1":
            return "Easy"
        if self.difficulty == "2":
            return "Medium"
        return "Hard" 

    def get_shorten_description(self):
        return self.description[:70]

    def get_option_list(self):
        try:
            option_list = self.options.split("|")
            updated_option_list = [
                option for option in option_list if option != ""]
            return updated_option_list
        except Exception as e:
            logger.error("No options provided for Problem")
            return []

    def get_correct_option_list(self):
        try:
            option_list = self.correct_options.split("|")
            updated_option_list = [
                option for option in option_list if option != ""]
            return updated_option_list
        except Exception as e:
            logger.error("correct option is null")
            return []

    def get_video_url_list(self):
        video_url_list = []
        try:
            video_url_list = json.loads(self.video)["items"]
        except Exception as e:
            pass
        return video_url_list

    def get_graph_url_list(self):
        try:
            urls = json.loads(self.graph_url)["items"]
            return urls
        except Exception as e:
            return []

    def clear_problem_topics(self):
        return self.topics.clear()

    def remove_rtf_tags(self):
        import re
        TAG_RE = re.compile(r'<[^>]+>') 
        TAG_RE_2 = re.compile(r'&[^;]+;')
        return TAG_RE.sub('', TAG_RE_2.sub('', self.description))


class Quiz(models.Model):

    title = models.CharField(max_length=100, null=False)

    tag = models.ForeignKey('EasyHireApp.Tag', on_delete=models.SET_NULL, blank=True, null=True)

    instruction = models.TextField(null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    quiz_start_datetime = models.DateTimeField(default=timezone.now)

    is_quiz_started = models.BooleanField(default=False)

    is_sectional_timed = models.BooleanField(default=True)

    buffer_time = models.IntegerField(default=15)

    is_activated = models.BooleanField(null=True, blank= True,default=True)

    def __str__(self):
        return self.title

    def is_editable(self):
        quiz_status = QuizStatus.objects.filter(quiz=self)

        if len(quiz_status):
            return False
        return True

    def save(self, *args, **kwargs):
        super(Quiz, self).save(*args, **kwargs)

    def get_shorten_quiz_instruction(self):
        return str(self.instruction.encode("ascii", errors="ignore")[:100])+"..."

    def get_topic_list(self):
        quiz_section_objs = QuizSection.objects.filter(quiz=self)
        topic_list = [
            quiz_section_obj.topic for quiz_section_obj in quiz_section_objs]
        return topic_list

    def total_sections(self):
        return len(QuizSection.objects.filter(quiz=self))

    def total_quiz_time(self):
        quiz_section_objs = QuizSection.objects.filter(quiz=self)
        total_time = 0
        for quiz_section_obj in quiz_section_objs:
            total_time += quiz_section_obj.time
        return total_time

    def total_no_of_questions(self):
        quiz_section_objs = QuizSection.objects.filter(quiz=self)
        total_questions = 0
        for quiz_section_obj in quiz_section_objs:
            total_questions += quiz_section_obj.no_questions
        return total_questions

    def get_initial_time(self):
        if self.is_sectional_timed:
            return self.buffer_time
        return self.total_quiz_time()


    def no_of_questions(self):

        questions_types = {
            "SUB": 0,
            "VID": 0
        }

        quiz_sections = QuizSection.objects.filter(quiz=self)

        for quiz_section in quiz_sections:
            subjective_problems = list(Problem.objects.filter(category="3", topics__in=[quiz_section.topic]))
            if len(subjective_problems):
                questions_types["SUB"] += quiz_section.no_questions

            video_problems = list(Problem.objects.filter(category="5", topics__in=[quiz_section.topic]))
            if len(video_problems):
                questions_types["VID"] += quiz_section.no_questions

        return questions_types

    def type_of_questions(self):

        questions_types = set()

        quiz_sections = QuizSection.objects.filter(quiz=self)

        for quiz_section in quiz_sections:
            subjective_problems = Problem.objects.filter(category="3", topics__in=[quiz_section.topic])
            if len(subjective_problems):
                questions_types.add("SUB")
            video_problems = Problem.objects.filter(category="5", topics__in=[quiz_section.topic])
            if len(video_problems):
                questions_types.add("VID")

        return list(questions_types)


    def get_section_with_question_count_for_sms(self):

        questions_types = {
            "OBJ": 0,
            "SUB": 0,
            "VID": 0
        }

        quiz_sections = QuizSection.objects.filter(quiz=self)

        for quiz_section in quiz_sections:
            objective_problems = list(Problem.objects.filter(category__in=["1","2"], topics__in=[quiz_section.topic]))
            if len(objective_problems):
                questions_types["OBJ"] += quiz_section.no_questions

            subjective_problems = list(Problem.objects.filter(category="3", topics__in=[quiz_section.topic]))
            if len(subjective_problems):
                questions_types["SUB"] += quiz_section.no_questions

            video_problems = list(Problem.objects.filter(category="5", topics__in=[quiz_section.topic]))
            if len(video_problems):
                questions_types["VID"] += quiz_section.no_questions

        return f"{questions_types['OBJ']} - Objective, {questions_types['SUB']} - Subjective, and {questions_types['VID']} - Viva"

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizes'


class QuizSection(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    no_questions = models.IntegerField(default=0)

    time = models.IntegerField(default=0)

    weightage = models.IntegerField(default=0)

    positive_threshold = models.IntegerField(default=0)

    negative_threshold = models.IntegerField(default=0)

    is_quiz_section_static = models.BooleanField(default=False)

    easy_questions = models.IntegerField(default=0)

    medium_questions = models.IntegerField(default=0)

    hard_questions = models.IntegerField(default=0)

    def __str__(self):
        return self.topic.name + " - " + self.quiz.title

    class Meta:
        verbose_name = 'QuizSection'
        verbose_name_plural = 'QuizSection'


class ProblemAttempted(models.Model):

    quiz_section = models.ForeignKey(QuizSection, on_delete=models.CASCADE, null=True)

    applicant = models.ForeignKey(Student, on_delete=models.CASCADE)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    answer = models.TextField(null=True, blank=True)

    start_time = models.DateTimeField(blank=True, null=True)

    end_time = models.DateTimeField(blank=True, null=True)

    options = models.CharField(max_length=1000, null=True, blank=True)

    calculated_score = models.FloatField(default=-1, null=True, blank=True)


    # text_analysis = models.TextField(null=True, blank=True)

    video_url = models.CharField(max_length=200, null=True, blank=True)

    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    quiz_status  = models.ForeignKey('EasyHireApp.QuizStatus' , on_delete=models.CASCADE , null=True, blank=True)

    objects = ProblemAttemptedManager()
    admin_objects = models.Manager()

    def __str__(self):
        return self.applicant.name + " - " + self.quiz_section.quiz.title + " - " + self.quiz_section.topic.name

    def get_duration(self):

        if self.start_time is None or self.end_time is None:
            return "N/A"
        total_seconds = (self.end_time - self.start_time).total_seconds()

        # if total_seconds >= 3600:
        # secs = total_seconds % 60
        # total_minutes = (total_seconds-secs)/60
        # mins = total_minutes % 60
        # hours = (total_minutes-mins)/60
        # return str(int(hours))+":"+str(int(mins))+":"+str(int(secs))

        return str(int(total_seconds))+" s"

    def get_descriptive_percentage(self):
        if self.calculated_score == -1:
            return "Not Evaluated"
        else:
            #return str(self.calculated_score)+" %"
            return str(int(self.calculated_score/20))+"/5"

    def get_attempted_option_list(self):
        if self.options == None or self.options == "":
            return []
        option_list = self.options.split("|")
        updated_option_list = [
            option for option in option_list if option != ""]
        return updated_option_list

    # def generate_text_analysis(self):
    #     text_analysis = {}
    #     text_analysis["tone_analysis"] = get_tone_analysis(self.answer)
    #     text_analysis["personality_insights"] = get_text_personality_insights(self.answer)
    #     json_data = get_text_analysis(self.answer)
    #     if json_data["result"] == "success":
    #         score_id = json_data["score_id"]
    #         highlighted_text_json = get_highlighted_text(score_id)
    #         json_data["highlighted_text_json"] = highlighted_text_json

    #     text_analysis["text_analysis"] = json_data
    #     self.text_analysis = json.dumps(text_analysis)
    #     self.save()

    def is_selected_option_correct(self):

        if self.problem.category == PROBLEM_CATEGORY_DESCRIPTIVE:
            return True

        if self.problem.category == PROBLEM_CATEGORY_AUDIO:
            return True

        if self.problem.category == PROBLEM_CATEGORY_VIDEO:
            return True

        correct_choices = self.problem.get_correct_option_list()

        if len(correct_choices) == 0:
            return False

        attempted_options = self.get_attempted_option_list()

        if len(attempted_options) == 0:
            return False

        updated_attempted_options = [option.lower()
                                     for option in attempted_options]

        for correct_choice in correct_choices:
            lower_correct_choice = correct_choice.lower()
            if lower_correct_choice not in updated_attempted_options:
                return False
        return True

    # def get_applicant_tone_analysis(self):
    #     try:
    #         text_analysis = json.loads(self.text_analysis)
    #         return text_analysis["tone_analysis"]
    #     except Exception as e:
    #         return {}

    # def get_applicant_personality_insights(self):
    #     try:
    #         text_analysis = json.loads(self.text_analysis)
    #         return text_analysis["personality_insights"]
    #     except Exception as e:
    #         return {}

    class Meta:
        verbose_name = 'ProblemAttempted'
        verbose_name_plural = 'ProblemAttempted'


class QuizSectionResult(models.Model):

    quiz_section = models.ForeignKey(
        QuizSection, on_delete=models.SET_NULL, null=True)

    applicant = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    no_question_attempted = models.IntegerField(default=0)

    calibration = models.FloatField(default=0.0)

    used_difficulties = models.FloatField(default=0.0)

    right_answers = models.IntegerField(default=0)

    correct_answer_counter = models.IntegerField(default=0)

    incorrect_answer_counter = models.IntegerField(default=0)

    datetime = models.DateTimeField(default=timezone.now)

    time_remaining = models.IntegerField(default=-1)

    is_completed = models.BooleanField(default=False)

    observations = models.TextField(default="{\"calibration_list\":[], \"problem_pk_list\":[],}")

    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    objects = QuizSectionResultManager()
    admin_objects = models.Manager()

    def get_duration(self):

        attempted_problems = ProblemAttempted.objects.filter(applicant=self.applicant, quiz_section=self.quiz_section)

        # print(attempted_problems)
        total_seconds = 0

        for problem in attempted_problems:
            if problem.start_time is None or problem.end_time is None:
                total_seconds += 0
            else:
                total_seconds += (problem.end_time - problem.start_time).total_seconds()

        secs = total_seconds % 60
        total_minutes = (total_seconds - secs) / 60
        mins = total_minutes % 60
        hours = (total_minutes - mins) / 60
        if hours != 0:
            return str(int(hours)) + " h " + str(int(mins)) + " m " + str(int(secs))+" s"
        return str(int(mins)) + " m " + str(int(secs))+" s"

    def get_attempted_problem_list(self):
        try:
            attempted_problem_obj_list = ProblemAttempted.objects.filter(applicant=self.applicant,
                                                                         quiz_section=self.quiz_section)
            problem_obj_list = []
            for attempted_problem in attempted_problem_obj_list:
                problem_obj_list.append(attempted_problem.problem)
            return problem_obj_list
        except Exception as e:
            print("get_attempted_problem_list: ", e)
            return []

    def __str__(self):
        try:
            return self.applicant.name + " - " + self.quiz_section.quiz.title + " - " + self.quiz_section.topic.name
        except Exception as e:
            return "None"


class QuizStatus(models.Model):

    applicant = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    assigned_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    quiz_start_time = models.DateTimeField(null=True, blank=True)

    quiz_end_time = models.DateTimeField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)

    is_processed = models.BooleanField(default=False)

    is_transferred = models.BooleanField(default=False, null=True, blank=True)
    transferred_time = models.DateTimeField(blank=True, null=True)

    completion_date = models.DateTimeField(blank=True, null=True)

    last_problem_time = models.DateTimeField(blank=True, null=True)

    time_remaining = models.IntegerField(null=True, blank=True)
    images = models.TextField(default=[])
    video = models.TextField(default=[])

    time_stamps = models.TextField(default="[]", blank=True, null=True)

    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    is_deleted_date_time = models.DateTimeField(blank=True, null=True)

    quiz_history = models.TextField(null=True , blank=True)

    objects = QuizStatusManager()
    admin_objects = models.Manager()

    def __str__(self):
        if not self.is_deleted:
            return self.applicant.name + " - " + self.quiz.title
        else:
            return self.applicant.name + " - " + self.quiz.title +" - "+ "De-Assgined"

    def image_list(self):
        if self.images == "[]":
            return []
        string = self.images[1:-1]
        images = string.split(',')
        return images[:3]

    def get_percentage(self):
        if self.quiz_history:
            data = json.loads(self.quiz_history)
            return data.get('descriptive_percentage')
        return "Not calculated"

    def get_recruiter_remark(self):
        if self.quiz_history:
            data = json.loads(self.quiz_history)
            return data.get('recruiter_remark')
        return "Not added"

    def get_completion_date(self):
        from datetime import timedelta
        if self.completion_date:
            time_obj = self.completion_date + timedelta(hours=5, minutes=30)
            return time_obj.strftime('%d/%m/%Y %I:%M %p')
        else:
            return "N/A"

    def get_quiz_start_time(self):
        try:
            problem = ProblemAttempted.objects.filter(applicant=self.applicant, quiz_section__in=self.quiz.quizsection_set.all()).order_by("pk")[0]
            if problem.start_time is None:
                return "N/A"
            start_time = problem.start_time + datetime.timedelta(hours=5, minutes=30)
            return start_time.strftime('%d/%m/%Y %I:%M %p')
            #return problem.start_time.strftime('%d/%m/%Y %I:%M %p')

        except Exception as e:
            logger.info("No quiz Start time") 
            return "N/A"

    def is_allowed_to_take_quiz(self):

        if self.quiz_start_time == None or self.quiz_end_time == None:
            return True

        current_time = datetime.datetime.now()
        ez = pytz.timezone(settings.TIME_ZONE)
        current_time = ez.localize(current_time)

        if current_time >= self.quiz_start_time and current_time <= self.quiz_end_time:
            return True
        else:
            return False

    def get_attempted_descriptive_problem(self):
        attempted_problem_obj_list = ProblemAttempted.objects.filter(quiz_section__quiz=self.quiz,quiz_status=self,
                                                                     applicant=self.applicant,
                                                                     problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)
        return attempted_problem_obj_list




    def get_attempted_video_problem(self):
        attempted_problem_obj_list = list(ProblemAttempted.admin_objects.filter(quiz_section__quiz=self.quiz,quiz_status=self,
                                                                      applicant=self.applicant,
                                                                      problem__category=PROBLEM_CATEGORY_VIDEO))
        attempted_problem_obj_list.reverse()
        return attempted_problem_obj_list

    def is_quiz_ended(self):
        quiz_status = self
        logger.info("Status %s",quiz_status)
        assigned_quiz = quiz_status.quiz
        logger.info(assigned_quiz)
        available_section_objs = QuizSection.objects.filter(quiz=assigned_quiz)
        logger.info("Total %s", available_section_objs)
        completed_section_counter = 0
        if quiz_status.time_remaining != None and quiz_status.time_remaining <= 0 and quiz_status.time_remaining != -1:

            for quiz_section in available_section_objs:
                try:
                    quiz_section_result = QuizSectionResult.objects.get(quiz_section=quiz_section, applicant=self.applicant)
                except Exception as e:
                    logger.error("Is quiz ended %s", str(e))
                    quiz_section_result = QuizSectionResult.objects.create(quiz_section=quiz_section, applicant=self.applicant)

                quiz_section_result.is_completed = True
                quiz_section_result.save()

            print("quiz completed 1")
            return True
        for quiz_section in available_section_objs:
            try:
                quiz_section_result_obj = QuizSectionResult.objects.get(applicant=self.applicant,
                                                                        quiz_section=quiz_section)
                if quiz_section_result_obj.is_completed:
                    completed_section_counter += 1
            except Exception as e:
                pass
        logger.info("Complete %s",completed_section_counter)
        logger.info("Available %s",available_section_objs)
        if completed_section_counter == len(available_section_objs):

            print("quiz completed 2")
            logger.info("quiz completed")
            return True
        else:
            return False

    def generate_quiz_description_result(self):
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        applicant_total_score = 0
        total_questions = 0
        quiz_sections = QuizSection.objects.filter(quiz=self.quiz)
        total_quiz_sections = len(quiz_sections)
        quiz_section_result_list = []
        for quiz_section in quiz_sections:
            try:
                quiz_section_result_obj = QuizSectionResult.objects.get(applicant=self.applicant,
                                                                        quiz_section=quiz_section)
            except Exception as e:
                print("generate quiz section result error - ",str(e))
                continue

            attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
                                                                     quiz_section=quiz_section,
                                                                     problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)

            total_questions += attempted_problem_objs.count()
            for attempted_problem_obj in attempted_problem_objs:
                '''solution = attempted_problem_obj.problem.solution
                answer = attempted_problem_obj.answer
                stop_words = set(stopwords.words('english')) 
                word_tokens = word_tokenize(answer) 
                filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                filtered_sentence = [] 
                for w in word_tokens:
                    if w not in stop_words: 
                        filtered_sentence.append(w)
                answer = filtered_sentence
                solution_list = solution
                word_tokens = word_tokenize(solution_list) 
                filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                filtered_sentence = [] 
                for w in word_tokens:
                    if w not in stop_words: 
                        filtered_sentence.append(w)
                solution_list = filtered_sentence
                str1_words = set(answer)
                str2_words = set(solution_list)
                common = str1_words & str2_words 
                common_words = len(common)
                try:
                    applicant_total_score += (common_words/len(solution_list))*100
                except Exception:
                    applicant_total_score += 0'''
                if attempted_problem_obj.calculated_score==-1:
                    return -1
                else:
                    score = attempted_problem_obj.calculated_score
                applicant_total_score += score
        try:
            total_questions = self.quiz.no_of_questions()['SUB']
            applicant_total_score = applicant_total_score / total_questions
        except Exception:
            applicant_total_score = 0
        return round(applicant_total_score, 2)

    class Meta:
        verbose_name = 'QuizStatus'
        verbose_name_plural = 'QuizStatus'






class QuizHistory(models.Model):
    applicant = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    quiz_name = models.TextField(null = True , blank=True)
    image_list = models.TextField(default="{}" , null=True , blank=True)
    quiz_status  = models.ForeignKey('EasyHireApp.QuizStatus' , on_delete=models.CASCADE , null=True, blank=True)
    quiz_history = models.TextField(default="{}" , null=True , blank=True)
    quiz_timing_info = models.TextField(default="{}" , null=True , blank=True)
    quiz_sessions = models.TextField(default="{}" , null=True, blank=True)

    is_blank = models.BooleanField(default=False , null=True, blank=True)
    is_deleted_date_time = models.DateTimeField(auto_now_add=True , null=True , blank=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.quiz_name}"

    def get_single_choice_problem(self):
        if self.quiz_history == "{}":
            return []
        data = json.loads(self.quiz_history)
        return data.get('single_choice_section')

    def get_multi_choice_problem(self):
        if self.quiz_history == "{}":
            return []
        data = json.loads(self.quiz_history)
        return data.get('single_multi_choice_section')

    def get_attempted_descriptive_problem(self):
        if self.quiz_history == "{}":
            return []
        data = json.loads(self.quiz_history)
        return data.get('descriptive_section')
        

    def get_attempted_video_problem(self):
        if self.quiz_history == "{}":
            return []
        data = json.loads(self.quiz_history)
        return data.get('video_section')


    def get_image_list(self):
        if self.image_list == "{}":
            return []
        images_list = self.image_list
        string = images_list[1:-1]
        images = string.split(',')
        return images[:3]
        
    def get_remakrs(self):
        data = json.loads(self.quiz_sessions)
        print(data.get('recruiter_remark'))
        if data.get('recruiter_remark'):
            return data.get('recruiter_remark')

        return "Not added"


    def get_descriptive_percentage(self):
        data = json.loads(self.quiz_sessions)
        if data.get('descriptive_percentage'):
            return data.get('descriptive_percentage')
        return "N/A"



class QuizResult(models.Model):

    applicant = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    result = models.TextField(null=True, blank=True)

    description_score = models.CharField(default=0, null=True, blank=True, max_length=10)

    recruiter_remark = models.TextField(default="", blank=True, null=True)
    quiz_status  = models.ForeignKey('EasyHireApp.QuizStatus' , on_delete=models.CASCADE , null=True, blank=True)

    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    objects = QuizResultManager()
    admin_objects = models.Manager()

    def __str__(self):
        if self.quiz_status:
            return self.applicant.name + " - " + self.quiz.title + '-> '+ str(self.quiz_status.pk)
        else:
            return self.applicant.name + " - " + self.quiz.title + " QuizStatusPK - Not Saved"

    def generate_quiz_description_result(self):
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        total_questions = 0
        applicant_total_score = 0
        quiz_sections = QuizSection.objects.filter(quiz=self.quiz)
        total_quiz_sections = len(quiz_sections)
        quiz_section_result_list = []
        for quiz_section in quiz_sections:

            try:
                quiz_section_result_obj = QuizSectionResult.objects.get(applicant=self.applicant,
                                                                        quiz_section=quiz_section)
            except Exception as e:
                print(str(e))
                continue

            attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
                                                                     quiz_section=quiz_section,
                                                                     problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)
            for attempted_problem_obj in attempted_problem_objs:
                '''
                solution = attempted_problem_obj.problem.solution
                answer = attempted_problem_obj.answer
                stop_words = set(stopwords.words('english')) 
                word_tokens = word_tokenize(answer) 
                filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                filtered_sentence = [] 
                for w in word_tokens:
                    if w not in stop_words: 
                        filtered_sentence.append(w)
                answer = filtered_sentence
                solution_list = solution
                word_tokens = word_tokenize(solution_list) 
                filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                filtered_sentence = [] 
                for w in word_tokens:
                    if w not in stop_words: 
                        filtered_sentence.append(w)
                solution_list = filtered_sentence
                str1_words = set(answer)
                str2_words = set(solution_list)
                common = str1_words & str2_words 
                common_words = len(common)
                try:
                    applicant_total_score += (common_words/len(solution_list))*100
                except Exception:
                    applicant_total_score += 0'''
                if attempted_problem_obj.calculated_score == -1:
                    self.descriptive_score = -1
                    self.save()
                    applicant_total_score = -1
                    return -1
                elif applicant_total_score != -1:
                    score = attempted_problem_obj.calculated_score
                    applicant_total_score += score

            total_questions += len(attempted_problem_objs)

        try:
            total_questions = self.quiz.no_of_questions()['SUB']
            applicant_total_score = applicant_total_score / total_questions
        except Exception:
            applicant_total_score = 0
        self.description_score = round(applicant_total_score,2)
        self.save()
        return round(applicant_total_score,2)
    class Meta:
        verbose_name = 'QuizStatus'
        verbose_name_plural = 'QuizStatus'

    def get_applicant_score(self):
        applicant_total_score = 0
        try:
            #applicant_total_score = json.loads(self.result)["quiz_section_result_list"][0]["diff_score"]
            #applicant_total_score = json.loads(self.result)["applicant_total_score"]
            result = json.loads(self.result)
            score = {
                "OBJ":"None",
                "SUB":"None",
                "VID":"None",
            }

            for section in result["quiz_section_result_list"]:
                if section['type'] == "OBJ":
                    score['OBJ'] = section['diff_score']
                    break

            flag_has_subjective = False

            for section in result["quiz_section_result_list"]:
                if section['type'] == "SUB":
                    flag_has_subjective = True
                    break
            if flag_has_subjective:
                descriptive_score = self.generate_quiz_description_result()
                if descriptive_score == -1:
                    score['SUB'] = "Pending"
                else:
                    score['SUB'] = descriptive_score


            for section in result["quiz_section_result_list"]:
                if section['type'] == "VID":
                    if section['recruiter_remark'] is None or section['recruiter_remark'] == "" :
                        score['VID'] = "Evaluation Pending"
                        break
                    else:
                        score['VID'] = section['recruiter_remark']
            logger.info("Brief Quiz Result",score)
            return score
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("get applicant score: %s at %s", str(e), str(exc_tb.tb_lineno))
        return {"OBJ":0}

    def get_applicant_quiz_score(self):
        applicant_total_score = None
        try:
            quiz_attempted = json.loads(self.result)[
                "quiz_section_result_list"]
            logger.info("Quiz Attempted %s", len(quiz_attempted))
            if len(quiz_attempted) > 0:
                applicant_total_score = json.loads(
                    self.result)["applicant_total_score"]
        except Exception as e:
            pass
        return applicant_total_score

    def get_applicant_percentile(self):
        applicant_obj_list = []
        same_score = 0
        less_score = 0

        applicant_score = self.get_applicant_score()["OBJ"]
        if applicant_score == "None":
            return 100
        quiz_results = QuizResult.objects.filter(
            quiz=self.quiz).filter(~Q(applicant=self.applicant))
        for quiz_result in quiz_results:
            other_applicant_score = quiz_result.get_applicant_score()["OBJ"]
            if other_applicant_score == "None":
                continue
            if quiz_result.applicant not in applicant_obj_list:
                logger.info("Other Applicant Score --> %s Applicant Score --> %s ", str( other_applicant_score), str(applicant_score))
                if other_applicant_score == applicant_score:
                    same_score += 1
                elif other_applicant_score < applicant_score:
                    less_score += 1
                applicant_obj_list.append(quiz_result.applicant)

        total_applicant = len(applicant_obj_list)
        if total_applicant == 0:
            return 100

        percentile = ((less_score+(0.5*same_score))*100)/float(total_applicant)
        return round(percentile, 2)

#    def generate_quiz_result(self):
#        applicant_total_score = 0
#        quiz_sections = QuizSection.objects.filter(quiz=self.quiz)
#        total_quiz_sections = len(quiz_sections)
#        quiz_section_result_list = []
#        try:
#	        for quiz_section in quiz_sections:
#                    try:
#                        quiz_section_result_obj = QuizSectionResult.objects.get(applicant=self.applicant, quiz_section=quiz_section)
#                    except Exception as e:
#                        print(str(e))
#                        continue
#
#                    attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
#	                                                                     quiz_section=quiz_section,
#	                                                                     problem__category__in=[PROBLEM_CATEGORY_SINGLE_CORRECT, PROBLEM_CATEGORY_MULTI_CORRECT])
#	            if len(attempted_problem_objs) > 0:
#	                attempts = {
#	                    "easy": 0,
#	                    "medium": 0,
#	                    "hard": 0,
#	                    "total": 0
#	                }
#
#	                correct = {
#	                    "easy": 0,
#	                    "medium": 0,
#	                    "hard": 0,
#	                    "total": 0
#	                }
#
#	                total_easy = 0
#	                total_medium = 0
#	                total_hard = 0
#
#	                for attempted_problem_obj in attempted_problem_objs:
#
#	                    if attempted_problem_obj.problem.difficulty == DIFFICULTY_EASY:
#	                        attempts["easy"] += 1
#	                        if attempted_problem_obj.is_selected_option_correct():
#	                            correct["easy"] += 1
#	                            correct["total"] += 1
#
#	                    elif attempted_problem_obj.problem.difficulty == DIFFICULTY_MEDIUM:
#	                        attempts["medium"] += 1
#	                        if attempted_problem_obj.is_selected_option_correct():
#	                            correct["medium"] += 1
#	                            correct["total"] += 1
#	                    else:
#	                        attempts["hard"] += 1
#	                        if attempted_problem_obj.is_selected_option_correct():
#	                            correct["hard"] += 1
#	                            correct["total"] += 1
#
#	                    attempts["total"] += 1
#
#	                abs_easy = 0
#	                if attempts["easy"] != 0:
#	                    abs_easy = round(correct["easy"]/attempts["easy"]*100, 2)
#	                    # abs_easy = round((float(correct["easy"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)
#
#	                abs_medium = 0
#	                if attempts["medium"] != 0:
#	                    abs_medium = round(correct["medium"]/attempts["medium"]*100, 2)
#	                    # abs_medium = round((float(correct["medium"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)
#
#	                abs_hard = 0
#	                if attempts["hard"] != 0:
#	                    abs_hard = round(correct["hard"]/attempts["hard"]*100, 2)
#	                    # abs_hard = round((float(correct["hard"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)
#
#	                total_abs_per = 0
#	                if attempts["total"] != 0:
#	                    total_abs_per = round(
#	                        correct["total"]/attempts["total"]*100, 2)
#
#	                abs_per = {
#	                    "easy": abs_easy,
#	                    "medium": abs_medium,
#	                    "hard": abs_hard,
#	                    "total": total_abs_per,
#	                }
#
#	                pass_score = 1*attempts["easy"]+ 2*attempts["medium"]+ 3*attempts["hard"]
#	                pass_score = pass_score*0.6
#	                try:
#	                    correct_easy = 0
#	                    correct_medium = 0
#	                    correct_hard = 0
#	                    if attempts["easy"] > 0:
#	                        correct_easy = ((correct["easy"]/attempts["easy"])*0.17)
#	                    if attempts["medium"] > 0:
#	                       correct_medium = ((correct["medium"]/attempts["medium"])*0.17)
#	                    if attempts["hard"] > 0:
#	                        correct_hard = ((correct["hard"]/attempts["hard"])*0.17)
#
#	                    adjusted_diff_score = (correct_easy + correct_medium + correct_hard) *100
#	                except Exception as e:
#	                    logger.info("Ajusted score %s", e)
#	                adjusted_diff_score = round(adjusted_diff_score,2)
#	                pass_or_fail = "FAIL"
#	                if math.ceil(adjusted_diff_score) >= math.ceil(pass_score):
#	                    pass_or_fail = "PASS"
#	                else:
#	                    pass_or_fail = "FAIL"
#	                #diff_score = round(adjusted_diff_score*100/pass_score, 2)
#	                #logger.info(attempts["total"])
#	                #diff_score = ((1*(correct["easy"]) + (2*correct["medium"]) + (3*correct["hard"]))/((1*attempts["easy"]) + (2 * attempts["medium"]) + (3 * attempts["hard"])))*100
#	                diff_score = (((1*correct["easy"]) + (2 * correct["medium"]) + (3 * correct["hard"])) / (
#	                    (1*attempts["easy"]) + (2 * attempts["medium"]) + (3 * attempts["hard"])))*100
#	                temp_dict = {
#	                    "id": quiz_section.pk,
#	                    "section_name": quiz_section.topic.name,
#	                    "is_completed": quiz_section_result_obj.is_completed,
#	                    "total_questions": quiz_section.no_questions,
#	                    "no_questions_attempted": attempts["total"],
#	                    "right_answers": correct["total"],
#	                    "attempts": attempts,
#	                    "correct": correct,
#	                    "abs_per": abs_per,
#	                    "total_abs_per": total_abs_per,
#	                    "pass_score": round(pass_score,2),
#	                    "adjusted_diff_score": adjusted_diff_score,
#	                    "diff_score": round(diff_score,2),
#	                    "pass_or_fail":pass_or_fail,
#	                    "type":"OBJ"
#	                }
#	                logger.info(temp_dict)
#	                applicant_total_score += total_abs_per
#	                quiz_section_result_list.append(temp_dict)
#	            
#	            ############# descriptive
#
#	            attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
#	                                                                     quiz_section=quiz_section,
#	                                                                     problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)
#
#	            if(len(attempted_problem_objs)):
#
#	                average_score = 0
#	                correct_answers = 0
#
#	                for attempted_problem_obj in attempted_problem_objs:
#
#	                    if attempted_problem_obj.calculated_score != -1:
#	                        
#	                        average_score += attempted_problem_obj.calculated_score
#	                        if attempted_problem_obj.calculated_score != 0:
#	                            correct_answers +=1
#	                    else:
#
#	                        average_score = -1
#	                        break
#	                
#	                if average_score != -1:
#	                    average_score = round(average_score/len(attempted_problem_objs),2)
#
#	                if correct_answers >= 0.6*len(attempted_problem_objs):
#	                    pass_or_fail = "PASS"
#	                else:
#	                    pass_or_fail = "FAIL"
#
#	                temp_dict = {
#	                    "id": quiz_section.pk,
#	                    "type": "SUB",
#	                    "section_name": quiz_section.topic.name,
#	                    "is_completed": quiz_section_result_obj.is_completed,
#	                    "total_questions": quiz_section.no_questions,
#	                    "no_questions_attempted": len(attempted_problem_objs),
#	                    "right_answers": correct_answers,
#	                    "diff_score": average_score,
#	                    "pass_or_fail": pass_or_fail,
#	                }
#
#	                quiz_section_result_list.append(temp_dict)
#
#	            ######## video section
#
#	            attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
#	                                                                     quiz_section=quiz_section,
#	                                                                     problem__category=PROBLEM_CATEGORY_VIDEO)
#
#	            if(len(attempted_problem_objs)):
#
#	                if self.recruiter_remark is None or self.recruiter_remark == "":
#	                    remarks = "Pending"
#	                else:
#	                    remarks = self.recruiter_remark
#
#	                temp_dict = {
#	                    "id": quiz_section.pk,
#	                    "type": "VID",
#	                    "section_name": quiz_section.topic.name,
#	                    "is_completed": quiz_section_result_obj.is_completed,
#	                    "recruiter_remark": remarks
#	                }
#
#	                quiz_section_result_list.append(temp_dict)
#        except Exception as e:
#            logger.info(str(e))
#
#        if total_quiz_sections > 0:
#            applicant_total_score = round(applicant_total_score/total_quiz_sections, 2)
#        else:
#            applicant_total_score = -1
#
#        self.result = json.dumps({
#            "applicant_total_score": applicant_total_score,
#            "quiz_section_result_list": quiz_section_result_list,
#        })
#        self.save()



    def generate_quiz_result(self):
        applicant_total_score = 0
        quiz_sections = QuizSection.objects.filter(quiz=self.quiz)
        total_quiz_sections = 0
        quiz_section_result_list = []
        try:
            for quiz_section in quiz_sections:
                try:
                    quiz_section_result_obj = QuizSectionResult.objects.get(
                        applicant=self.applicant, quiz_section=quiz_section)
                except Exception as e:
                    print(str(e))
                    continue

                problem_objs = Problem.objects.filter(topics__in=[quiz_section.topic], category__in=[PROBLEM_CATEGORY_SINGLE_CORRECT, PROBLEM_CATEGORY_MULTI_CORRECT])

                if len(problem_objs):
                    total_quiz_sections += 1

                attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
                                                                        quiz_section=quiz_section,
                                                                        problem__category__in=[PROBLEM_CATEGORY_SINGLE_CORRECT, PROBLEM_CATEGORY_MULTI_CORRECT])
                if len(problem_objs) > 0:
                    attempts = {
                        "easy": 0,
                        "medium": 0,
                        "hard": 0,
                        "total": 0
                    }

                    correct = {
                        "easy": 0,
                        "medium": 0,
                        "hard": 0,
                        "total": 0
                    }

                    total_easy = 0
                    total_medium = 0
                    total_hard = 0

                    for attempted_problem_obj in attempted_problem_objs:

                        if attempted_problem_obj.problem.difficulty == DIFFICULTY_EASY:
                            attempts["easy"] += 1
                            if attempted_problem_obj.is_selected_option_correct():
                                correct["easy"] += 1
                                correct["total"] += 1

                        elif attempted_problem_obj.problem.difficulty == DIFFICULTY_MEDIUM:
                            attempts["medium"] += 1
                            if attempted_problem_obj.is_selected_option_correct():
                                correct["medium"] += 1
                                correct["total"] += 1
                        else:
                            attempts["hard"] += 1
                            if attempted_problem_obj.is_selected_option_correct():
                                correct["hard"] += 1
                                correct["total"] += 1

                        attempts["total"] += 1

#                    abs_easy = 0
#                    if attempts["easy"] != 0:
#                        abs_easy = round(correct["easy"]/attempts["easy"]*100, 2)
#                        # abs_easy = round((float(correct["easy"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)
#
#                    abs_medium = 0
#                    if attempts["medium"] != 0:
#                        abs_medium = round(
#                            correct["medium"]/attempts["medium"]*100, 2)
#                        # abs_medium = round((float(correct["medium"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)
#
#                    abs_hard = 0
#                    if attempts["hard"] != 0:
#                        abs_hard = round(correct["hard"]/attempts["hard"]*100, 2)
#                        # abs_hard = round((float(correct["hard"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)
#
#                    total_abs_per = 0
#                    if attempts["total"] != 0:
#                        total_abs_per = round(
#                            correct["total"]/attempts["total"]*100, 2)


                    abs_easy = 0
                    if quiz_section.is_quiz_section_static and quiz_section.easy_questions:
                        abs_easy = round(correct["easy"]/quiz_section.easy_questions*100, 2)
                    elif attempts["easy"] != 0:
                        abs_easy = round(correct["easy"]/attempts["easy"]*100, 2)
                        # abs_easy = round((float(correct["easy"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)

                    abs_medium = 0
                    if quiz_section.is_quiz_section_static and quiz_section.medium_questions:
                        abs_medium = round(correct["medium"]/quiz_section.medium_questions*100, 2)
                    elif attempts["medium"] != 0:
                        abs_medium = round(correct["medium"]/attempts["medium"]*100, 2)
                    # abs_medium = round((float(correct["medium"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)

                    abs_hard = 0
                    if quiz_section.is_quiz_section_static and quiz_section.hard_questions:
                        abs_hard = round(correct["hard"]/quiz_section.hard_questions*100, 2)
                    elif attempts["hard"] != 0:
                        abs_hard = round(correct["hard"]/attempts["hard"]*100, 2)
                    # abs_hard = round((float(correct["hard"]/quiz_section_result_obj.quiz_section.no_questions))*0.17,2)

                    total_abs_per = 0
                    if quiz_section.no_questions != 0:
                        total_abs_per = round(correct["total"]/quiz_section.no_questions*100, 2)

                    abs_per = {
                        "easy": abs_easy,
                        "medium": abs_medium,
                        "hard": abs_hard,
                        "total": total_abs_per,
                    }

                    pass_score = 1*attempts["easy"] + 2 * \
                        attempts["medium"] + 3*attempts["hard"]
                    pass_score = pass_score*0.6
                    try:
                        correct_easy = 0
                        correct_medium = 0
                        correct_hard = 0
#                        if attempts["easy"] > 0:
#                            correct_easy = (
#                                (correct["easy"]/attempts["easy"])*0.17)
#                        if attempts["medium"] > 0:
#                            correct_medium = (
#                                (correct["medium"]/attempts["medium"])*0.17)
#                        if attempts["hard"] > 0:
#                            correct_hard = (
#                                (correct["hard"]/attempts["hard"])*0.17)
                        if quiz_section.is_quiz_section_static and quiz_section.easy_questions:
                            correct_easy = ((correct["easy"] / quiz_section.easy_questions) * 0.17)
                        elif attempts["easy"] > 0:
                            correct_easy = ((correct["easy"]/attempts["easy"])*0.17)

                        if quiz_section.is_quiz_section_static and quiz_section.medium_questions:
                            correct_medium = ((correct["medium"] / quiz_section.medium_questions) * 0.17)
                        elif attempts["medium"] > 0:
                            correct_medium = ((correct["medium"]/attempts["medium"])*0.17)

                        if quiz_section.is_quiz_section_static and quiz_section.hard_questions:
                            correct_medium = ((correct["hard"] / quiz_section.hard_questions) * 0.17)
                        elif attempts["hard"] > 0:
                            correct_hard = ((correct["hard"]/attempts["hard"])*0.17)

                        adjusted_diff_score = (
                            correct_easy + correct_medium + correct_hard) * 100
                    except Exception as e:
                        logger.info("Ajusted score %s", e)
                    adjusted_diff_score = round(adjusted_diff_score, 2)
                    pass_or_fail = "FAIL"
                    if math.ceil(adjusted_diff_score) >= math.ceil(pass_score):
                        pass_or_fail = "PASS"
                    else:
                        pass_or_fail = "FAIL"
                    #diff_score = round(adjusted_diff_score*100/pass_score, 2)
                    # logger.info(attempts["total"])
                    #diff_score = ((1*(correct["easy"]) + (2*correct["medium"]) + (3*correct["hard"]))/((1*attempts["easy"]) + (2 * attempts["medium"]) + (3 * attempts["hard"])))*100
                    #try:
                    #    diff_score = (((1*correct["easy"]) + (2 * correct["medium"]) + (3 * correct["hard"])) / (
                    #        (1*attempts["easy"]) + (2 * attempts["medium"]) + (3 * attempts["hard"])))*100
                    #except Exception as e:
                    #    diff_score = 0
                    #    logger.error("No problem attempted by the candidate")

                    try:
                        if quiz_section.is_quiz_section_static:
                            diff_score = (((1*correct["easy"]) + (2 * correct["medium"]) + (3 * correct["hard"])) / (
                                (1*quiz_section.easy_questions) + (2 * quiz_section.medium_questions) + (3 * quiz_section.hard_questions)))*100
                        else:
                            diff_score = (((1 * correct["easy"]) + (2 * correct["medium"]) + (3 * correct["hard"])) / (
                                    (1 * attempts["easy"]) + (2 * attempts["medium"]) + (3 * attempts["hard"]))) * 100
                    except:
                        diff_score = 0

                    temp_dict = {
                        "id": quiz_section.pk,
                        "section_name": quiz_section.topic.name,
                        "is_completed": quiz_section_result_obj.is_completed,
                        "total_questions": quiz_section.no_questions,
                        "no_questions_attempted": attempts["total"],
                        "right_answers": correct["total"],
                        "attempts": attempts,
                        "correct": correct,
                        "abs_per": abs_per,
                        "total_abs_per": total_abs_per,
                        "pass_score": round(pass_score, 2),
                        "adjusted_diff_score": adjusted_diff_score,
                        "diff_score": round(diff_score, 2),
                        "pass_or_fail": pass_or_fail,
                        "type": "OBJ"
                    }
                    logger.info(temp_dict)
                    applicant_total_score += total_abs_per
                    quiz_section_result_list.append(temp_dict)

                # descriptive

                attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
                                                                        quiz_section=quiz_section,
                                                                        problem__category=PROBLEM_CATEGORY_DESCRIPTIVE)

                problem_objs = Problem.objects.filter(topics__in=[quiz_section.topic], category__in=[PROBLEM_CATEGORY_DESCRIPTIVE])

                if(len(problem_objs)):

                    average_score = 0
                    correct_answers = 0

                    for attempted_problem_obj in attempted_problem_objs:

                        if attempted_problem_obj.calculated_score != -1:

                            average_score += attempted_problem_obj.calculated_score
                            if attempted_problem_obj.calculated_score != 0:
                                correct_answers += 1
                        else:

                            average_score = -1
                            break

                    if average_score != -1 and len(attempted_problem_objs):
                        average_score = round(
                            average_score/len(attempted_problem_objs), 2)

                    if  correct_answers > 0 and  correct_answers >= 0.6*len(attempted_problem_objs):
                        pass_or_fail = "PASS"
                    else:
                        pass_or_fail = "FAIL"

                    temp_dict = {
                        "id": quiz_section.pk,
                        "type": "SUB",
                        "section_name": quiz_section.topic.name,
                        "is_completed": quiz_section_result_obj.is_completed,
                        "total_questions": quiz_section.no_questions,
                        "no_questions_attempted": len(attempted_problem_objs),
                        "right_answers": correct_answers,
                        "diff_score": average_score,
                        "pass_or_fail": pass_or_fail,
                    }

                    quiz_section_result_list.append(temp_dict)

                # video section

                attempted_problem_objs = ProblemAttempted.objects.filter(applicant=self.applicant,
                                                                        quiz_section=quiz_section,
                                                                        problem__category=PROBLEM_CATEGORY_VIDEO)

                problem_objs = Problem.objects.filter(topics__in=[quiz_section.topic], category__in=[PROBLEM_CATEGORY_VIDEO])


                if(len(problem_objs)):

                    if self.recruiter_remark is None or self.recruiter_remark == "":
                        remarks = "Pending"
                    else:
                        remarks = self.recruiter_remark

                    temp_dict = {
                        "id": quiz_section.pk,
                        "type": "VID",
                        "section_name": quiz_section.topic.name,
                        "is_completed": quiz_section_result_obj.is_completed,
                        "recruiter_remark": remarks
                    }

                    quiz_section_result_list.append(temp_dict)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("generate_quiz_result: %s at %s", str(e), str(exc_tb.tb_lineno))


        if total_quiz_sections > 0:
            applicant_total_score = round(
                applicant_total_score/total_quiz_sections, 2)
        else:
            applicant_total_score = -1

        self.result = json.dumps({
            "applicant_total_score": applicant_total_score,
            "quiz_section_result_list": quiz_section_result_list,
        })
        self.save()

    class Meta:
        verbose_name = 'QuizResult'
        verbose_name_plural = 'QuizResult'





def find_incomplete_quizzes():

    quiz_status_list = QuizStatus.objects.all()
    student_list = []

    for quiz_status in quiz_status_list:

        quiz_sections = QuizSection.objects.filter(quiz=quiz_status.quiz)
        has_video_problems = False

        for quiz_section in quiz_sections:
            problems = Problem.objects.filter(topics__in=[quiz_section.topic], category=PROBLEM_CATEGORY_VIDEO)
            if len(problems):
                has_video_problems = True
                break

        if not has_video_problems:
            continue


        quiz_section_results = QuizSectionResult.objects.filter(quiz_section__quiz=quiz_status.quiz,
                                                                applicant=quiz_status.applicant)

        if quiz_status.time_remaining != -1 and quiz_status.time_remaining is not None and quiz_status.time_remaining <= 0 and quiz_status.is_completed == False:
            student_list.append(quiz_status.applicant.name)
        else:
            completed_qs = 0
            for qs in quiz_section_results:
                if qs.is_completed:
                    completed_qs += 1
            if completed_qs == len(quiz_status.quiz.quizsection_set.all()) and quiz_status.is_completed == False:
                student_list.append(quiz_status.applicant.name)

    return student_list




class Tag(models.Model):

    category = models.CharField(max_length=10, choices=TAG_CATEGORY_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


def get_topic_conflicts():

    topics = Topic.objects.all()

    conflict = []

    for topic in topics:

        objective = Problem.objects.filter(category__in=['1', '2'], topics__in=[topic])
        subjective = Problem.objects.filter(category="3", topics__in=[topic])
        audio = Problem.objects.filter(category="4", topics__in=[topic])
        video = Problem.objects.filter(category="5", topics__in=[topic])

        count = 0
        category = ""
        if len(objective):
            count += 1
            category = "1"

        if len(subjective):
            count += 1
            category = "3"

        if len(audio):
            count += 1
            category = "4"
        if len(video):
            count += 1
            category = "5"

        if count > 1:
            category = None

        topic.category = category
        topic.save()

    print(*conflict, sep="\n")



    



























"""
>>0. update events/tasks 
>>1. active/deactivate problem
>>2. copy quiz and topics from other ones
>>3. filters
>>4. max active co-ordinator limit
>>5. sms on quiz assignment, quiz 
>>6. multiple quiz 
"""
