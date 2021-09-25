import requests, json


def send_notify_by_order( message_title , message_body , image = None):
    errors = []
    #fcm_api = "AAAANTpxmAQ:APA91bGr23ZEb9qQZOaoWAMkTcgs2D4EEoSG2HX-OPEja5T4lJ51QxrKjxbkwxshybT05vMH44KPa379fjEobBQygsL4_5c6HDAoBBcT9rdWQfGNYOaitxn3G5I3zqrKM1-30D2DXAEY"
    
    fcm_api = "AAAAKQWX0c8:APA91bGUh1n-W-_zEgychNe7YR8qOynpRIb07y5gY7xVSDRL7kWnpVEdkgS3dNM_TQ8BfPgxREMjHWqyTuDeyHM-Oec0g2ukZEvhHKTTKfp7jPtTZpOZzTKWxYXQsCUVol3hrE4C870F"
    token= "c8Zk8gcJS7qaUuPUAWt_is:APA91bGzTDgC6wfTlDSSigZimbHwUhPIej8l9Wz27O7YPjFxoITWV0KvI5tf1JjlnNwHoDuuSqjEslKmu-JcQ-kuAnQPy-C8zbmJvULTRSgiZ40wZgCU4_7eOv-qKXYG94BtrBhYcEIB"
    registration_id = token
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
    return
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
    