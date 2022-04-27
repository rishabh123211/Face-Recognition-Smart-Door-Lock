# facerec.py

import cv2
import sys
import numpy
import os
import urllib
import numpy as np
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'

gmail_user = "rishabh**********@gmail.com"
gmail_pwd = "rk122*********"
FROM = 'rishabh*********@gmail.com'
TO = ['rishu**************@gmail.com'] #must be a list


def mail():
    
    msg = MIMEMultipart()
    time.sleep(1)
    msg['Subject'] ="SECURITY"

    #BODY with 2 argument

    #body=sys.argv[1]+sys.argv[2]
    body="THIS IS FROM RISHABH KUMAR REGARDING SECURITY BREACH"          
    msg.attach(MIMEText(body,'plain'))
    time.sleep(1)


    ###IMAGE
    fp = open("1.jpg", 'rb')   		
    time.sleep(1)
    img = MIMEImage(fp.read())
    time.sleep(1)
    fp.close()
    time.sleep(1)
    msg.attach(img)
    time.sleep(1)


    try:
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            print ("smtp.gmail")
            server.ehlo()
            print ("ehlo")
            server.starttls()
            print ("starttls")
            server.login(gmail_user, gmail_pwd)
            print ("reading mail & password")
            server.sendmail(FROM, TO, msg.as_string())
            print ("from")
            server.close()
            print ('successfully sent the mail')
    except:
            print ("failed to send mail")


print('Training...')

# Create a list of images and a list of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, labels) = [numpy.array(lis) for lis in [images, labels]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.face.FisherFaceRecognizer_create()
model.train(images, labels)

# Part 2: Use fisherRecognizer on camera stream
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)

##url="http://10.7.81.89:8080/shot.jpg"
while True:
    
    (_, im) = webcam.read()

##    imgPath=urllib.urlopen(url)
##    imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
##    im=cv2.imdecode(imgNp,-1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        #Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1]<500:
            print (names[prediction[0]])
            cv2.putText(im,names[prediction[0]],(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        else:
            cv2.putText(im,'Scanning',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break
