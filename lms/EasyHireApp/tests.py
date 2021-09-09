#from django.test import TestCase

# Create your tests here.
############ to delete a file mistakenly sent through ftp
from ftpretty import ftpretty

# Mention the host
host = "115.242.2.155"

# Supply the credentisals
f = ftpretty(host, 'prakash/ftp', 'M@c!30d$#222' )

#f.get('/Users/sahil/Desktop/test/','python-devel-2.7.18-2.3.x86_64.rpm')
#f.put('/home/ujjwal/Desktop/Misc/kotak_uat_oct/kotak_uat_new/Prasad-Dnyaneshwar-Parekar-QC-Generalised.pdf','/test/')
f.delete('test/UjjwalAgarwal_13_01_2021_16_56_consolidated_KXXFRAYJ_video.webm')
print("Successfully transferred")
