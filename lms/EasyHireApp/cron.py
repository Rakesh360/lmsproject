def remove_rtf_tags(text):
    import re
    TAG_RE = re.compile(r'<[^>]+>')
    TAG_RE_2 = re.compile(r'&[^;]+;')
    return TAG_RE.sub('', TAG_RE_2.sub('', text))


def batch_process_video_questions(shell=False):
    try:
        from EasyHireApp.views import VideoBatchProcessingTime, QuizStatus, ProblemAttempted
        from EasyHireApp.utils import generate_random_string_of_length_N, logger

        logger.info("hiring crontab started")

        from django.core.files.storage import default_storage
        from django.conf import settings

        import datetime
        import os
        import time
        import sys
        #try:
        #    os.system("chown ubuntu:ubuntu -R log")
        #except Exception as e:
        #    print("ERROR File Ownership:", str(e))
        print("Entered in CronJob of Batch Processing - ",
            "[ Time when the process started: ", datetime.datetime.now(), " ]")

        print(datetime.datetime.now().hour)
        time_range = VideoBatchProcessingTime.objects.first()

        print(time_range)
        applicant_list = []

        if time_range.start_time == str(datetime.datetime.now().hour) or shell:

            number_of_hours_to_run = int(time_range.number_of_hours)

            blank_video_path = settings.MEDIA_ROOT + 'videos/blank.webm'

            start = time.time()
            end = time.time()
            videos_to_be_deleted = set()

            pending_quiz_status_list = QuizStatus.objects.filter(is_completed=True, is_processed=False)

            print(pending_quiz_status_list)

            for quiz_status in pending_quiz_status_list:

                print(quiz_status)

                quiz_section_list = quiz_status.quiz.quizsection_set.all()

                question_number = 1
                try:
                    video_urls = open(
                        "/home/ubuntu/macleods/EasyHire/files/video_urls.txt", "w")
                except Exception as e:
                    print(e)

                print(quiz_section_list)

                for quiz_section in quiz_section_list:

                    problem_attempted_list = ProblemAttempted.objects.filter(
                        quiz_section=quiz_section, applicant=quiz_status.applicant)

                    topic = quiz_section.topic.name

                    print(topic)

                    for problem_attempted in problem_attempted_list:
                        try:
                            problem = problem_attempted.problem

                            if problem.category == "5":

                                # description = remove_rtf_tags(problem.description)
                                description = "Question- " + \
                                    remove_rtf_tags(problem.description)
                                print(description)
                                description_words = description.strip().split()
                                description_lines = open(
                                    settings.MEDIA_ROOT+"description_lines.txt", "w")

                                line = ""
                                line_length = 50

                                for word in description_words:
                                    if len(line) + len(word) < line_length:
                                        line += " "+word
                                    else:
                                        description_lines.write(
                                            line.strip()+"\n\n")
                                        line = word

                                if len(line.strip()):
                                    description_lines.write(line.strip()+"\n\n")

                                description_lines.close()
                                description_video_title = settings.MEDIA_ROOT + \
                                    'title_'+str(question_number)+'.webm'
                                print(description_video_title)

                                # os.system('ffmpeg -i '+blank_video_path+' -vf "[in]drawtext=fontfile=OpenSans-Bold.ttf: \
                                # text=\'Question '+str(question_number)+'\': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
                                # boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/3, drawtext=fontfile=OpenSans-Bold.ttf: \
                                # text=\'Quiz section- '+topic+'\': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
                                # boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/2, drawtext=fontfile=OpenSans-Bold.ttf: \
                                # text=\''+description+'\': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
                                # boxborderw=5: x=(w-text_w)/2: y=h-(h-text_h)/3[out]" -threads 4 -codec:a copy '+description_video_title+' -y')

                                os.system('ffmpeg -i '+blank_video_path+' -vf "[in]drawtext=fontfile=OpenSans-Bold.ttf: \
                                text=\'Question '+str(question_number)+'\': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
                                boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/3, drawtext=fontfile=OpenSans-Bold.ttf: \
                                text=\'Quiz section- '+topic+'\': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
                                boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/2, drawtext=fontfile=OpenSans-Bold.ttf: \
                                textfile='+settings.MEDIA_ROOT+'description_lines.txt : fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
                                boxborderw=5: x=(w-text_w)/2: y=h-(h-text_h)/2[out]" -threads 4 -codec:a copy '+description_video_title+' -y')

                                video_urls.write(
                                    "file '"+description_video_title+"'\n")

                                if problem_attempted.video_url is None or problem_attempted.video_url == "":
                                    text1 = "This question was either not answered"
                                    text2 = "or was skipped by the applicant."
                                    print("NOT ANSWERED")
                                    random_string = generate_random_string_of_length_N(
                                        9)
                                    #re_encoded_video_name = str(quiz_status.applicant.name).replace(
                                    #    " ", "") + "_" + random_string
                                    re_encoded_video_name = str(quiz_status.applicant.name).replace(" ", "") + "_" + str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')) + "_not_answered_" + random_string

                                    re_encoded_video_name = re_encoded_video_name+"_video.webm"
                                    print(re_encoded_video_name)
                                    re_encoded_answer_video_url = settings.MEDIA_ROOT + re_encoded_video_name

                                    os.system('ffmpeg -i '+blank_video_path+' -vf "[in]drawtext=fontfile=OpenSans-Bold.ttf: \
                                    text='+text1+': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
                                    boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/3, drawtext=fontfile=OpenSans-Bold.ttf: \
                                    text='+text2+': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
                                    boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/2[out]" -threads 4 -codec:a copy '+re_encoded_answer_video_url+' -y')

                                else:
                                    answer_video_url = settings.MEDIA_ROOT + problem_attempted.video_url
                                    random_string = generate_random_string_of_length_N(
                                        9)
                                    #re_encoded_video_name = str(quiz_status.applicant.name).replace(
                                    #    " ", "") + "_" + random_string
                                    re_encoded_video_name = "reencoded_at_"+str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))+"_"+problem_attempted.video_url

                                    re_encoded_video_name = re_encoded_video_name+"_video.webm"
                                    print(re_encoded_video_name)
                                    re_encoded_answer_video_url = settings.MEDIA_ROOT + re_encoded_video_name
                                    print(re_encoded_answer_video_url)
                                    os.system('sudo ffmpeg -i '+answer_video_url +
                                            ' -vcodec libvpx-vp9 -cpu-used -5 -deadline realtime '+re_encoded_answer_video_url)

                                video_urls.write(
                                    "file '"+re_encoded_answer_video_url+"'\n")

                                #problem_attempted.video_url = re_encoded_video_name
                                #problem_attempted.save()

                                print(re_encoded_answer_video_url)
                                #videos_to_be_deleted.add(description_video_title)
                                #videos_to_be_deleted.add(answer_video_url)

                                question_number += 1
                        except Exception as e:
                            print(str(e))

                video_urls.close()

                random_string = generate_random_string_of_length_N(9)
                #applicant_video_name = str(quiz_status.applicant.name).replace(
                #    " ", "") + "_" + random_string
                applicant_video_name = str(quiz_status.applicant.name).replace(" ", "") + "_" +  str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))+"_consolidated_" + random_string
                #applicant_video_name = str(quiz_status.applicant.name).replace(" ", "") + "_" + str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))+"_consolidated_" + random_string

                if question_number != 1:
                    output_file_name = applicant_video_name+"_video.webm"
                    print(output_file_name)
                    applicant_list.append(quiz_status.applicant.name)
                    try:
                        os.system('sudo ffmpeg -f concat -safe 0 -i '+settings.MEDIA_ROOT +
                                'video_urls.txt -c copy '+settings.MEDIA_ROOT+output_file_name)
                    except Exception as e:
                        print(e)
                    quiz_status.video = output_file_name
                quiz_status.is_processed = True
                quiz_status.save()

                end = time.time()
                if end-start >= 3600*number_of_hours_to_run:
                    break

            # for video in videos_to_be_deleted:
                # os.remove(video)
            print(*applicant_list,sep="\n")
            print(end-start)
        else:
            print("Batch Processing time slot has not started")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error batch_process_video_questions: %s at %s",str(e), str(exc_tb.tb_lineno))
        print(f"Error batch_process_video_questions: {str(e)} at line no. [{str(exc_tb.tb_lineno)}]")

#def remove_rtf_tags(text):
#    import re
#    TAG_RE = re.compile(r'<[^>]+>')
#    TAG_RE_2 = re.compile(r'&[^;]+;')
#    return TAG_RE.sub('', TAG_RE_2.sub('', text))
#
#def batch_process_video_questions():
#	try:
#            from EasyHireApp.views import VideoBatchProcessingTime, QuizStatus, ProblemAttempted
#	    from EasyHireApp.utils import generate_random_string_of_length_N
#	    from django.core.files.storage import default_storage
#	    from django.conf import settings
#
#	    import datetime
#	    import os
#	    import time
#	    print("Processing Started!" , "[ Time when the process started: ", datetime.datetime.now() , " ]")
#	    print(datetime.datetime.now().hour)
#	    time_range = VideoBatchProcessingTime.objects.first()
#	    print(time_range)
#
#	    if time_range.start_time == str(datetime.datetime.now().hour):
#
#	        number_of_hours_to_run = int(time_range.number_of_hours)
#
#	        blank_video_path = settings.MEDIA_ROOT + 'videos/blank.webm'
#
#	        start = time.time()
#	        end = time.time()
#	        videos_to_be_deleted = set()
#
#	        pending_quiz_status_list = QuizStatus.objects.filter(
#	            is_completed=True, is_processed=False)
#
#	        for quiz_status in pending_quiz_status_list:
#
#	            print(quiz_status)
#
#	            quiz_section_list = quiz_status.quiz.quizsection_set.all()
#
#	            question_number = 1
#	            try:
#	                video_urls = open("/home/ubuntu/macleods/EasyHire/files/video_urls.txt","w")
#	            except Exception as e:
#	                print(e)
#
#	            print(quiz_section_list)
#
#	            for quiz_section in quiz_section_list:
#
#	                problem_attempted_list = ProblemAttempted.objects.filter(
#	                    quiz_section=quiz_section, applicant=quiz_status.applicant)
#
#	                topic = quiz_section.topic.name
#
#	                print(topic)
#
#	                for problem_attempted in problem_attempted_list:
#	                    try:
#	                        problem = problem_attempted.problem
#
#	                        if problem.category == "5":
#
#	                            #description = remove_rtf_tags(problem.description)
#	                            description = "Question- "+ remove_rtf_tags(problem.description)
#	                            print(description)
#	                            description_words = description.strip().split()
#	                            description_lines = open(settings.MEDIA_ROOT+"description_lines.txt","w")
#
#	                            line = ""
#	                            line_length = 50
#
#	                            for word in description_words:
#	                                if len(line) + len(word) < line_length:
#	                                    line+=" "+word
#	                                else:
#	                                    description_lines.write(line.strip()+"\n\n")
#	                                    line = word
#
#	                            if len(line.strip()):
#	                                description_lines.write(line.strip()+"\n\n")
#
#	                            description_lines.close()
#	                            description_video_title = settings.MEDIA_ROOT + \
#	                                'title_'+str(question_number)+'.webm'
#	                            print(description_video_title)
#
#	                            #os.system('ffmpeg -i '+blank_video_path+' -vf "[in]drawtext=fontfile=OpenSans-Bold.ttf: \
#	                            #text=\'Question '+str(question_number)+'\': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
#	                            #boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/3, drawtext=fontfile=OpenSans-Bold.ttf: \
#	                            #text=\'Quiz section- '+topic+'\': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
#	                            #boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/2, drawtext=fontfile=OpenSans-Bold.ttf: \
#	                            #text=\''+description+'\': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
#	                            #boxborderw=5: x=(w-text_w)/2: y=h-(h-text_h)/3[out]" -threads 4 -codec:a copy '+description_video_title+' -y')
#
#	                            os.system('ffmpeg -i '+blank_video_path+' -vf "[in]drawtext=fontfile=OpenSans-Bold.ttf: \
#	                            text=\'Question '+str(question_number)+'\': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
#	                            boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/3, drawtext=fontfile=OpenSans-Bold.ttf: \
#	                            text=\'Quiz section- '+topic+'\': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
#	                            boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/2, drawtext=fontfile=OpenSans-Bold.ttf: \
#	                            textfile='+settings.MEDIA_ROOT+'description_lines.txt : fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
#	                            boxborderw=5: x=(w-text_w)/2: y=h-(h-text_h)/2[out]" -threads 4 -codec:a copy '+description_video_title+' -y')
#
#	                            video_urls.write("file '"+description_video_title+"'\n")
#
#	                            if problem_attempted.video_url is None or problem_attempted.video_url == "":
#	                                text1 = "This question was either not answered"
#	                                text2 = "or was skipped by the applicant."
#	                                print("NOT ANSWERED")
#	                                random_string = generate_random_string_of_length_N(9)
#	                                re_encoded_video_name = str(quiz_status.applicant.name).replace(
#	                                    " ", "") + "_" + random_string
#
#	                                re_encoded_video_name = re_encoded_video_name+"_video.webm"
#	                                print(re_encoded_video_name)
#	                                re_encoded_answer_video_url = settings.MEDIA_ROOT + re_encoded_video_name
#
#	                                os.system('ffmpeg -i '+blank_video_path+' -vf "[in]drawtext=fontfile=OpenSans-Bold.ttf: \
#	                                text='+text1+': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
#	                                boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/3, drawtext=fontfile=OpenSans-Bold.ttf: \
#	                                text='+text2+': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
#	                                boxborderw=5: x=(w-text_w)/2: y=(h-text_h)/2[out]" -threads 4 -codec:a copy '+re_encoded_answer_video_url+' -y')
#
#	                            else:
#	                                answer_video_url = settings.MEDIA_ROOT + problem_attempted.video_url
#	                                random_string = generate_random_string_of_length_N(9)
#	                                re_encoded_video_name = str(quiz_status.applicant.name).replace(
#	                                    " ", "") + "_" + random_string
#
#	                                re_encoded_video_name = re_encoded_video_name+"_video.webm"
#	                                print(re_encoded_video_name)
#	                                re_encoded_answer_video_url = settings.MEDIA_ROOT + re_encoded_video_name
#	                                print(re_encoded_answer_video_url)
#	                                os.system('sudo ffmpeg -i '+answer_video_url+' -vcodec libvpx-vp9 -cpu-used -5 -deadline realtime '+re_encoded_answer_video_url)
#
#	                            video_urls.write("file '"+re_encoded_answer_video_url+"'\n")
#
#	                            problem_attempted.video_url = re_encoded_video_name
#	                            problem_attempted.save()
#
#	                            print(re_encoded_answer_video_url)
#
#	                            videos_to_be_deleted.add(description_video_title)
#	                            videos_to_be_deleted.add(answer_video_url)
#
#	                            question_number += 1
#	                    except Exception as e:
#	                        print(str(e))
#	            video_urls.close()
#
#	            random_string = generate_random_string_of_length_N(9)
#	            applicant_video_name = str(quiz_status.applicant.name).replace(
#	                " ", "") + "_" + random_string
#
#	            output_file_name = applicant_video_name+"_video.webm"
#	            print(output_file_name)
#	            try:
#	                os.system('sudo ffmpeg -f concat -safe 0 -i '+settings.MEDIA_ROOT+'video_urls.txt -c copy '+settings.MEDIA_ROOT+output_file_name)
#	            except Exception as e:
#	                print(e)
#	            quiz_status.video = output_file_name
#	            quiz_status.is_processed = True
#	            quiz_status.save()
#
#	            end = time.time()
#	            if end-start >= 3600*number_of_hours_to_run:
#	                break
#
#	        #for video in videos_to_be_deleted:
#	            #os.remove(video)
#
#	        print(end-start)
#	    else:
#	        print("no")
#
#    except Excetion as e:
#        print(str(e))
#
#
##batch_process_video_questions()

def get_length(filename):
    try:
        import subprocess
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return float(result.stdout)
    except Exception as e:
        print(e)
        return 0


def get_total_video_duration(shell=False):
    condition = True

    total_duration = 0

    if shell or condition:

        from EasyHireApp.views import QuizStatus, ProblemAttempted
        from django.conf import settings

        quiz_status_list = QuizStatus.objects.all().exclude(video="[]")

        for quiz_status in quiz_status_list:

            consolidated_video_duration = get_length(settings.MEDIA_ROOT + quiz_status.video)

            if consolidated_video_duration == 0:
                continue

            video_problem_attempted = ProblemAttempted.objects.filter(problem__category="5",
                                                                      applicant=quiz_status.applicant,
                                                                      quiz_section__in=quiz_status.quiz.quizsection_set.all())

            for problem in video_problem_attempted:

                consolidated_video_duration -= 3

                if problem.video_url is None:
                    consolidated_video_duration -= 3

            total_duration += consolidated_video_duration

        return total_duration


def auto_complete_quiz():
    try:
        from EasyHireApp.views import QuizStatus, ProblemAttempted, QuizSectionResult
        from EasyHireApp.utils import end_quiz
        import datetime
        from django.utils import timezone
        hour_delay = 3
        incomplete_quiz_status = QuizStatus.objects.filter(is_completed=False)

        for quiz_status in incomplete_quiz_status:
            try:
                problem = ProblemAttempted.objects.filter(applicant=quiz_status.applicant,
                                                          quiz_section__in=quiz_status.quiz.quizsection_set.all()).order_by("pk")[0]
                print(timezone.now(), problem.start_time+datetime.timedelta(hours=hour_delay))
                if problem.start_time+datetime.timedelta(hours=hour_delay) <= timezone.now():
                    end_quiz(quiz_status.quiz, quiz_status.applicant, QuizSectionResult)
                    pass
            except Exception as e:
                print("Error completing quiz status: %s", str(e))

    except Exception as e:
        print("Error auto complete quiz: %s", str(e))

def send_reminders():
    import sys
    from django.utils import timezone
    from datetime import datetime, timedelta

    import logging
    logger = logging.getLogger(__name__)
    print("Entered in send_reminders: " + str(timezone.now()))

    try:
        from EasyHireApp.models import QuizStatus, Applicant
        from EasyHireApp.utils import send_reminder_msg_to_applicant
        # from datetime import datetime, timedelta

        print("Entered in send_reminders")

        time_delay = timedelta(days=7)
        unit_for_reminder = 3

        quiz_status_not_started = QuizStatus.objects.filter(is_completed=False,
                                                            assigned_date__gte=timezone.now() - time_delay,
                                                            quiz_start_time=None)

        quiz_status_incomplete = QuizStatus.objects.filter(is_completed=False,
                                                           assigned_date__gte=timezone.now() - time_delay).exclude(
            quiz_start_time=None)

        applicant_reminder_not_started = []
        quiz_status_reminder_not_started = []

        applicant_reminder_incomplete = []
        quiz_status_reminder_incomplete = []

        for quiz_status in quiz_status_not_started:

            time_difference = timezone.now() - quiz_status.assigned_date

            print((time_difference.seconds // 60), timezone.now(), quiz_status.assigned_date, quiz_status)

            if (time_difference.seconds // 60) % unit_for_reminder == 0:
                applicant_reminder_not_started.append(quiz_status.applicant)
                quiz_status_reminder_not_started.append(quiz_status.quiz)

        for quiz_status in quiz_status_incomplete:

            time_difference = timezone.now() - quiz_status.assigned_date

            print(timezone.now(), quiz_status.assigned_date)

            if (time_difference.seconds // 60) % unit_for_reminder == 0:
                applicant_reminder_incomplete.append(quiz_status.applicant)
                quiz_status_reminder_incomplete.append(quiz_status.quiz)

        # msg_content_not_started = "Please take the test which is assigned to you at the earliest"
        # msg_content_incomplete = "Please complete the test which is assigned to you at the earliest"

        print("Applicant who did not start quiz")
        print(*list(applicant_reminder_not_started), sep="\n")
        print("Applicant who did not complete quiz")
        print(*list(applicant_reminder_incomplete), sep="\n")

        # send_reminder_msg_to_applicant(list(applicant_reminder_not_started), msg_content_not_started)
        # send_reminder_msg_to_applicant(list(applicant_reminder_incomplete), msg_content_incomplete)

        ### Sending reminder SMS for not started
        i=0
        for applicant in applicant_reminder_not_started:
            send_reminder_msg_to_applicant(applicant, quiz_status_reminder_not_started[i], "not started")
            print(f"Reminder to start sent successfully to {applicant.name} for quiz - {str(quiz_status_reminder_not_started[i].title)}")
        
        ### Sending reminder SMS for started but not completed
        i=0
        for applicant in applicant_reminder_incomplete:
            send_reminder_msg_to_applicant(applicant, quiz_status_reminder_incomplete[i], "not completed")
            print(f"Reminder to complete sent successfully to {applicant.name} for quiz - {str(quiz_status_reminder_incomplete[i].title)}")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("send_reminders: %s at %s", str(e),str(exc_tb.tb_lineno))


def send_file(path):
    from ftpretty import ftpretty
    import sys
    from EasyHireApp.utils import logger
    from django.conf import settings

    # Mention the host
    host = "115.242.2.155"

    # Supply the credentisals
    f = ftpretty(host, 'prakash/ftp', 'M@c!30d$#222' )

    #f.put('/home/ujjwal/Desktop/Misc/kotak_uat_oct/kotak_uat_new/Prasad-Dnyaneshwar-Parekar-QC-Generalised.pdf','/test/')
    #f.delete("/test/UjjwalAgarwal_13_01_2021_16_56_consolidated_KXXFRAYJ_video.webm")

    final_path = settings.MEDIA_ROOT+path
    print(f"Received Path: {path} \n Actual Path: {final_path}")
    try:
        f.put(final_path,'/test/')
        print("Successfully transferred")
        logger.info("Successfully transferred video on path %s", str(path))
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("send_file-%s: %s", str(path),str(e))
        print(f"send_file - {str(path)}: {str(e)}")  
        return False

def transfer_consolidated_videos():
    from EasyHireApp.views import QuizStatus
    from EasyHireApp.utils import logger
    from datetime import datetime
    import sys
    qs = QuizStatus.objects.filter(is_transferred=False, is_completed=True)

    for q in qs:
        try:
            path = q.video
            if path != "[]" and send_file(path):
                q.is_transferred=True
                q.transferred_time=datetime.now()
                q.save()
            else:
                pass
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("transfer_consolidated_videos - QuizStatus pk - %s: %s", str(q.pk),str(e))
            print(f"transfer_consolidated_videos - QuizStatus pk - {q.pk}: {str(e)}")

#qs = QuizStatus.objects.all()
#for q in qs:
#    print(f"{str(q.pk)} - is_completed-{str(q.is_completed)} is_processed-{str(q.is_processed)} video-{str(q.video)}")            
