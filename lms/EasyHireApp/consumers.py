from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json

from EasyHireApp.models import *
from EasyHireApp.utils import *
from EasyHireApp.constants import *
from channels.consumer import AsyncConsumer

import logging
logger=logging.getLogger(__name__)

import time
class QuizTimeConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info(f"Enter into Connect of websocket")
        self.room_name = self.scope['url_route']['kwargs']['quiz_uuid']
        self.room_group_name = 'quiz_uuid_%s' % self.room_name
        self.username=  self.scope['url_route']['kwargs']['username']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.user = self.scope["user"]
        '''
        quiz_config_id = self.room_name
        applicant_obj = Applicant.objects.get(username=self.username)
        quiz_config = get_quiz_obj_with_uuid(quiz_config_id, Quiz)
        quiz_section_id = None
        while True:
            if quiz_config.is_sectional_timed:
                if quiz_section_id is None:
                    QuizStatus.objects.filter(quiz=quiz_config, applicant=applicant_obj).update(time_remaining=60000)
        
        '''
        await self.accept()

    async def disconnect(self,close_code):
        logger.info(f"Enter into disconnect of websocket")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        #pass

    async def receive(self,text_data):
        logger.info(f"Enter into Receive of websocket")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'sync_time',
                'value':text_data,
            }
        )


    async def sync_time(self,event):
        logger.info(f"Enter into Synctime of websocket")
        payload = json.loads(event['value'])
        logger.info(payload)
        data = payload['data']
        quiz_config_id = data["quiz_config_id"]
        remaining_time = data["remaining_time"]
        quiz_section_id = data["quiz_section_id"]
        print((quiz_section_id))
        applicant_obj = Applicant.objects.get(username=self.username)

        quiz_config = get_quiz_obj_with_uuid(quiz_config_id, Quiz)
        if quiz_config.is_sectional_timed:
                if quiz_section_id is None:
                    QuizStatus.objects.filter(quiz=quiz_config, applicant=applicant_obj).update(time_remaining=remaining_time)
                else:
                    try:
                        quiz_section = QuizSection.objects.get(pk=int(quiz_section_id))

                        if remaining_time < quiz_section.time * 100000:
                            QuizSectionResult.objects.filter(applicant=applicant_obj, quiz_section=quiz_section).update(time_remaining=remaining_time)


                    except Exception as e:
                        logger.error("Error sync remaining time: %s", str(e))
        else:
            QuizStatus.objects.filter(quiz=quiz_config, applicant=applicant_obj).update(time_remaining=remaining_time)



