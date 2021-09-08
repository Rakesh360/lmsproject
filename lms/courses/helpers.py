
from .models import *
from django.db.models import Q
import datetime
def course_to_json(course_objs):
           
    payload = []

    for course_obj in course_objs:
        course_package_dict = {}
        course_package_dict['uid'] = course_obj.uid
        course_package_dict['package_title'] = course_obj.package_title

        course_package_dict['package_description'] = course_obj.package_description
        course_package_dict['actual_price'] = course_obj.actual_price
        course_package_dict['selling_price'] = course_obj.selling_price
        course_package_dict['sell_from'] = course_obj.selling_price
        course_package_dict['sell_till'] = course_obj.selling_price
        course_package_dict['web_image'] = '/media/' + str(course_obj.web_image)
        course_package_dict['mobile_image'] ='/media/' + str(course_obj.mobile_image)

        subjects = [] 
        for subject in course_obj.pacakge_subjects.all():
            subject_dict = {}
            subject_dict['subject_title'] = subject.subject.subject_title
            chapters = []
            for chapter in subject.pacakge_subject_chapters.all():
                chapter_dict = {}
                chapter_dict['chapter_title'] = chapter.subject_chapter.chapter_title
                lessons = []
                for lesson in chapter.pacakge_subject_chapters_lessons.all():
                    lesson_dict = {}
                    lesson_dict['sequence'] = lesson.sequence
                    lesson_dict['lesson_title'] = lesson.lesson.lesson_title
                    lesson_dict['lesson_type'] = lesson.lesson.lesson_type
                    lesson_dict['is_free'] = lesson.lesson.is_free
                    lesson_dict['created_at'] = lesson.created_at
                    lesson_dict['video_link'] = ''
                    lesson_dict['video_uploaded_on'] = ''
                    lesson_dict['document_file'] = ''
                    try:
                        if lesson.lesson.lesson_type == 'Video':
                            lesson_dict['video_link'] = lesson.lesson.video.video_link
                            lesson_dict['video_uploaded_on'] = lesson.lesson.video.video_uploaded_on
                        elif lesson.lesson.lesson_type == 'Document':
                            lesson_dict['document_file'] = '/media/' +str(lesson.lesson.document.document_file)
                        elif lesson.lesson.lesson_type == 'Video + Document':
                            lesson_dict['document_file'] = '/media/' +str(lesson.lesson.document.document_file)
                            lesson_dict['video_link'] = lesson.lesson.video.video_link
                            lesson_dict['video_uploaded_on'] = lesson.lesson.video.video_uploaded_on
                    

                    except Exception as e:
                        print(e)

                    lessons.append(lesson_dict)
                chapter_dict['lessons'] = lessons
                    
                chapters.append(chapter_dict)
        
            subject_dict['chapters'] = chapters
            subjects.append(subject_dict)
            subject_dict = {}

        course_package_dict['subjects'] = subjects
        live_class = []
        #from datetime import date
        for live in course_obj.live.filter(Q(live_date=datetime.date.today(),live_time__gte=datetime.time()) |Q(live_date__gt=datetime.date.today())):
            live_class.append({
                'live_name' : live.live_name,
                'live_url' : live.live_url,
                'image' : '/media/' +  str(live.image),
                'live_date' : str(live.live_date),
                'live_time' : str(live.live_time),
                'live_uid' : live.uid
                
            })
        course_package_dict['live'] = live_class

        payload.append(course_package_dict)


    return payload