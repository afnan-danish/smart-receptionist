import pyttsx3
import speech_recognition as sr
import datetime
from datetime import date
from cv2 import cv2
from tkinter import *
import sqlite3
import face_recognition
import os
import shutil



conn = sqlite3.connect('smart_collin.db')
db = conn.cursor()

#conn.execute('''CREATE TABLE apt_dtl (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         GENDER        CHAR(10) );''')

aid = '3'
today = date.today()
# Retrieve last id
def getLastId():
    cursor = conn.execute("SELECT id from apt_dtl Order By id DESC")
    for row in cursor:
        return row[0]+1




engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)

face_classifier = cv2.CascadeClassifier('C:/Users/Amina/AppData/Local/Programs/Python/Python37/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

'''
root = Tk()
root.attributes('-fullscreen',True)
mainloop()
'''
def speak(audio):
    print('text: ' + audio)             
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')          


def face_extractor(img):

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face

def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        #r.adjust_for_ambient_noise(source)
        r.pause_threshold =  1
        audio = r.listen(source)
    
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        speak(f'Sorry!!! I didn\'t get that! Try again!')
        query = ''
        myCommand()

    return query
 
#myCommand();

def getDtl():
    greetMe()
    user_gender = 'Dear'
    speak(f"Hello {user_gender}, I am smart collin.")
    speak('Tell me details for booking appointment')
    while True:
        speak(f"What is your name {user_gender}?")
        user_name = myCommand()
        speak(user_name)
        speak(f"Is your name is correct")
        name_confirn = myCommand()
        if name_confirn != 'no' or (name_confirn != 'nahi' or name_confirn != 'nope') :
            break


    speak(f"What is your age {user_gender}?")
    user_age = myCommand()

    #speak(f"What is your problem {user_gender}?")
    #user_issue = myCommand()
    speak(f"Okay {user_gender}, Your appointment get fixed.")
    speak("Thank you...")

    conn.execute("INSERT INTO apt_dtl (ID,NAME,AGE,GENDER,DATE) \
            VALUES ("+str(getLastId())+", '"+user_name+"', "+user_age+", '"+user_gender+"', '"+str(today)+"' )");
    conn.commit()

    #conn.close()


#Get information from database
def get_old_info(imagename):
    clt_id = imagename.split('-')
    #print(clt_id[0])
    tuplevalue = ()
    cursor = conn.execute("SELECT * from apt_dtl where ID = "+clt_id[1]+"")
    for row in cursor:
        #print(row[1])
        tuplevalue = (row[0],row[1],row[2],row[3],row[4])

    return tuplevalue


def copyImage(imagenm, idnumber):
    clt_id = imagenm.split('-')
    directory = r'faces/'
    for filename in os.listdir(directory):
        if filename.endswith(clt_id[1]+'-'+clt_id[2]):
            #print(os.path.join(filename))
            imagecopy = os.path.join(directory, filename)
            file_name_path = 'faces/'+str(clt_id[0])+'-'+str(idnumber)+'-img.jpg'
            img = cv2.imread(r''+imagecopy)
            print(imagecopy)
            print(file_name_path)
            #cv2.imwrite(file_name_path,img)
            shutil.copy(imagecopy, file_name_path)

    return

def reApt(matched_name):
    #print('Get Fixed')
    #print('match'+matched_name)
    #print(get_old_info(matched_name))
    tupleval = get_old_info(matched_name)
    conn.execute("INSERT INTO apt_dtl (ID,NAME,AGE,GENDER, DATE) \
            VALUES ("+str(getLastId())+", '"+tupleval[1]+"', "+str(tupleval[2])+", '"+tupleval[3]+"', '"+str(today)+"' )");
    conn.commit()
    #print(matched_name)
    #copyImage(matched_name, getLastId())
    

#Global Variabl
matched_name = ''
#function for matching the face
def matchFace(fimage):
    #print(fimage)
    global matched_name
    current_image = face_recognition.load_image_file(fimage)
    current_encoding = face_recognition.face_encodings(current_image)
    if len(current_encoding) > 0:
        current_encoding = current_encoding[0]
    
    
    directory = r'faces/'
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            #print(os.path.join(directory, filename))
            loaded_image = face_recognition.load_image_file(os.path.join(directory, filename))
            loaded_encoding = face_recognition.face_encodings(loaded_image)
            if len(loaded_encoding) > 0:
                loaded_encoding = loaded_encoding[0]
            if len(current_encoding) and len(loaded_encoding):
                results = face_recognition.compare_faces([current_encoding], loaded_encoding)
                if results[0] == True:
                    #print(os.path.join(directory, filename))
                    matched_name = os.path.join(filename)
                    return True
                #else:
                    #print("")
        else:
            continue



def mainFunc():
    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, frame = cap.read()
        face = cv2.resize(frame,(600,600))
        face = cv2.cvtColor(face, cv2.IMREAD_COLOR)

        if face_extractor(frame) is not None:
            count+=1
            if count>5:
                file_name_path = 'faces/'+str(count)+'-'+str(getLastId())+'-img.jpg'
                cv2.imwrite(file_name_path,face)
                cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Smart Collin',face)
            
            if count==5:
                file_name_temp = 'temp/temp.jpg'
                cv2.imwrite(file_name_temp,face)
                cv2.putText(face,"Please wait... Image is processing",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.imshow('Smart Collin',face)
                if matchFace(file_name_temp):
                    speak('Your detail already present, appointment get fixed.')
                    print(matched_name)
                    reApt(matched_name)
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            
            if count==4:
                cv2.putText(face,"Please wait",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        else:
            #print("Face not Found")
            pass
        cv2.imshow('Smart Collin',face)
        if cv2.waitKey(1)=='q' or count==50:
            cap.release()
            cv2.destroyAllWindows()
            getDtl()
            break

root = Tk()
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.state('zoomed')

root.title("Smart Collin Admin Panel")
root.configure(background="Powder Blue")    
    
progLoop = True
while progLoop==True:
    root.mainloop()
    #input("Please Enter")
    mainFunc()