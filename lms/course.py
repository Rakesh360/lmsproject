from re import sub
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lms.settings'
django.setup()
import uuid
import json

from courses.models import *
from faker import Faker
fake = Faker()
import random
# [
# {
#     'subject' : 'Subject name',
#     'subject_chapters' : [
#         {
#             'chaper_name' : 'Chapter name',
#             'lessons' : [

#             ]
#         }
#     ]
# }
# ]
import datetime
def add_courses():
    data = []
    for i in range(0 , 5):
       
        subjects = Subject.objects.all()
        subject_list = []
        for subject in subjects:
            chapter_list  = []
            for chapter in SubjectChapters.objects.filter(subject = subject):
                lesson_list = []
                for lesson in Lessons.objects.filter(subject_chapters= chapter):
                    lesson_list.append({
                        "lesson_title" : lesson.lesson_title,
                        "video_uploaded_on" : lesson.video_uploaded_on,
                        "video_link" : lesson.video_link,
                        "leson_added" : str(datetime.date.today())
                    })

                chapter_list.append({
                    "chapter_title" : chapter.chapter_title,
                    "lessons" : lesson_list
                    })

            subject_list.append({
                "subject" : subject.subject_title,
                "chapters" : chapter_list
                })
        
        CoursePackage.objects.create(
            package_title = fake.name(),
            package_description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. ",
            package_image = 'image.png',
            actual_price = random.randint(800 , 5000),
            selling_price = random.randint(500 , 1000),
            sell_from = (datetime.date.today()),
            sell_till =  (datetime.date.today()),
            course_validity =  (datetime.date.today()),
            web_image = 'no-image.png',
            mobile_image = 'np-image.png',
            course_package_info = json.dumps(subject_list)
                    )

        print(data)
    # written to file or not
       
        file1 = open(f'{uuid.uuid4()}.json', 'w')
        file1.writelines(json.dumps(subject_list))
        file1.close()

add_courses()