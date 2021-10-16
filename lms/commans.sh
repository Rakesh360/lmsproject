ssh -i "lmsproject.pem" ubuntu@ec2-13-232-235-27.ap-south-1.compute.amazonaws.com

ubuntu@ec2-13-232-235-27.ap-south-1.compute.amazonaws.com
psql --host=lmsdatabase.c8hpn1snsqxi.ap-south-1.rds.amazonaws.com --port=5432 --username=lmsproject --password=LmsBhu0987 --dbname=lmsproject 

# FOR DUMPING DATA 
./manage.py dumpdata > db.json

# FOR IMPORTING DATA 
./manage.py loaddata FILE_NAME


sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
  

# IP - http://13.232.227.45/


# ghp_u6gKNjKcARvvpDX5 ccOQdVpHBH1DHS0dsE0Z
# ghp_Vti27z0G0kuvD4xkS ls; cd ..
fWojRBCqitap53JBUOq 





ws://13.232.227.45:8000/ws/room/1e7ea60b-c770-4e08-a9b9-d8cc7ff76043/

1. Landing page
2. Course detail page
3  Course learning page
4. Login
5. Registration
6. Account Page  with order page

