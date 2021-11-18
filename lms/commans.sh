ssh -i "lmsproject.pem" ubuntu@ec2-13-232-235-27.ap-south-1.compute.amazonaws.com

ubuntu@ec2-13-232-235-27.ap-south-1.compute.amazonaws.com
psql --host=lmsdatabase.c8hpn1snsqxi.ap-south-1.rds.amazonaws.com --port=5432 --username=lmsproject --password=LmsBhu0987 --dbname=lmsproject 
#https://13.235.128.45
13.232.94.2
ssh -i "abhijeetcodekeen.pem" ubuntu@13.232.112.104
http://13.232.112.104/


# FOR DUMPING DATA 
./manage.py dumpdata > db.json

ssh -i "abhijeet.pem" ubuntu@13.232.94.2

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

# FOR IMPORTING DATA 
./manage.py loaddata FILE_NAME


sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
  

# IP - http://13.232.227.45/


# ghp_u6gKNjKcARvvpDX5 
# ghp_Vti27z0G0kuvD4xkS 
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
fWojRBCqitap53JBUOq 




[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/ubuntu/codekeen/Codekeen
ExecStart=/home/ubuntu/codekeen/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          code_keen.wsgi:application

[Install]
WantedBy=multi-user.target



ws://13.232.227.45:8000/ws/room/1e7ea60b-c770-4e08-a9b9-d8cc7ff76043/

1. Landing page
2. Course detail page
3  Course learning page
4. Login
5. Registration
6. Account Page  with order page





[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/ubuntu/project/Codekeen
ExecStart=/home/ubuntu/project/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          code_keen.wsgi:application

[Install]
WantedBy=multi-user.target


server {
    listen 80;
    server_name 13.232.94.2;

    location = /favicon.ico { access_log off; log_not_found off; }
   

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}



deploy django on aws |  deploy django to aws | host django on aws | 
how to deploy django project on aws ec2 | 
deploy django app on aws ec2 | 
deploy django react aws | 
how to deploy django on aws | 
how to deploy django project on aws ec2 linux | 
deploy django aws elastic beanstalk | 
deploy django app on aws ec2 nginx | 
deploy django app on aws beanstalk | 
deploy django project on aws | 
deploy django on aws ec2 | 
deploy django docker aws | 
deploy django website on aws | 
deploy django in aws | 
deploy django app on aws free | 
how to deploy django project on aws | 
best way to deploy django on aws
django deployment | 
django deployment aws | 
django deployment checklist | 
django deployment digitalocean | 
django deployment on aws | 
deploy django google app engine | 
deploy django using nginx | 
django deployment wsgi | 
django deployment aws ec2 | 
django deployment apache | 
digitalocean deploy django | 
django deployment docker | 
django deployment nginx | 
heroku django deployment guide | 
django deployment on heroku | 
django continuous deployment | 
django deploy production server | 
django dev to deployment | 
deploy django using docker | 
django production deployment nginx | 
django deployment best practices | 
django deployment tools | 
django deployment static files | 
django deployment automation | 
deployment in django |
