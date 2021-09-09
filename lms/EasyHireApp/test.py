def remove_rtf_tags(text):
    import re
    TAG_RE = re.compile(r'<[^>]+>')
    TAG_RE_2 = re.compile(r'&[^;]+;')
    return TAG_RE.sub('', TAG_RE_2.sub('', text))


def batch_process_video_questions(shell=False):
    def remove_rtf_tags(text):
        import re
        TAG_RE = re.compile(r'<[^>]+>')
        TAG_RE_2 = re.compile(r'&[^;]+;')
        return TAG_RE.sub('', TAG_RE_2.sub('', text))


    import sys
    from EasyHireApp.views import VideoBatchProcessingTime, QuizStatus, ProblemAttempted
    from EasyHireApp.utils import generate_random_string_of_length_N, logger

    logger.info("hiring crontab started")

    from django.core.files.storage import default_storage
    from django.conf import settings

    import datetime
    import os
    import time

    try:
        #import sys
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
                    #video_urls = open("/home/ubuntu/macleods/EasyHire/files/video_urls.txt", "w")
                    video_urls = open(f"{settings.MEDIA_ROOT}video_urls.txt", "w")
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


batch_process_video_questions(shell=True)
