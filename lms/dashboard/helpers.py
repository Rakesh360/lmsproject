import requests, json


def send_notify_by_order(user_objs , message_title , message_body , image = None):
    errors = []
    fcm_api = "AAAANTpxmAQ:APA91bGr23ZEb9qQZOaoWAMkTcgs2D4EEoSG2HX-OPEja5T4lJ51QxrKjxbkwxshybT05vMH44KPa379fjEobBQygsL4_5c6HDAoBBcT9rdWQfGNYOaitxn3G5I3zqrKM1-30D2DXAEY"
    for user_obj in user_objs:
        try:
            registration_id = user_obj.student.fcm_token
            url = "https://fcm.googleapis.com/fcm/send"
            
            headers = {
            "Content-Type":"application/json",
            "Authorization": 'key='+fcm_api}

            payload = {
                "registration_ids" :[registration_id],
                "priority" : "high",
                "notification" : {
                    "body" : message_body,
                    "title" : message_title,
                    "image" : "https://pitig.com/media/cowin.jpg",
                    "icon": "https://pitig.com/static/images/favicon.png",
                    "click_action": "https://pitig.com/cowin/"
                }
            }

            result = requests.post(url,  data=json.dumps(payload), headers=headers )
            print(result.json())
    
        except Exception as e:
            print(e)
            errors.append(str(e))
    return errors
    