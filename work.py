import re
import cv2
import pytesseract as tess
from pytesseract import Output
import numpy as np
import os
import time
import mysql.connector
import sys 
import shutil 
from fpdf import FPDF
from os import listdir

tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_Cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

#Path  of where the frames is stored for aadhar detection
images = r"D:\python\doc_reader\New folder\data"

#path of photos folder
data_face = r"D:\python\doc_reader\New folder\data_face"

#Path of folder where pdf converter is used
final_image = r"D:\python\doc_reader\New folder\final_img"

#n = sys.argv[1]
n = r"D:\python\doc_reader\New folder\4.mp4"
#n=r"D:\python\doc_reader\akansha.mp4"
path_pdf, file_name = os.path.split(n)

file_name = file_name.replace(".mp4",".pdf")

#Path of  where pdf is made
pdf = r"D:\python\doc_reader\New folder\pdf/{}".format(file_name)
cap = cv2.VideoCapture(n)

frame_rate = 1
prev = 0
i = 0

get_adhar_no = []

def adhaar_read_data(text):
    res = text.split()
    name = None
    dob = None
    adh = None
    sex = None
    nameline = []
    dobline = []
    text0 = []
    text1 = []
    text2 = []
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n', '')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if 'female' in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"

    text1 = list(filter(None, text1))
    text0 = text1[:]

    try:

        # Cleaning first names
        name = text0[0]
        name = name.rstrip()
        name = name.lstrip()
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")
        name = re.sub('[^a-zA-Z] +', ' ', name)

        # Cleaning DOB
        dob = text0[1][-10:]
        dob = dob.rstrip()
        dob = dob.lstrip()
        dob = dob.replace('l', '/')
        dob = dob.replace('L', '/')
        dob = dob.replace('I', '/')
        dob = dob.replace('i', '/')
        dob = dob.replace('|', '/')
        dob = dob.replace('\"', '/1')
        dob = dob.replace(":", "")
        dob = dob.replace(" ", "")

        # Cleaning Adhaar number details

        aadhar_number = ''
        for word in res:
            if len(word) == 4 and word.isdigit():
                aadhar_number = aadhar_number + word + ' '
        #if len(aadhar_number)>=14:
        #    print("Aadhar number is :"+ aadhar_number)
        #else:
        #    print("Aadhar number not read")
        adh = aadhar_number
        data = {}
        data['Name'] = name
        data['Date of Birth'] = dob
        data['Adhaar Number'] = adh
        data['Sex'] = sex
        data['ID Type'] = "Adhaar"
        return data


    except Exception as e:
        print(e)


def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno + 1:]
            return textlist
    return textlist
    
# storing image path
#img_path = "D:/office_programs/doc_scanner/myImage0.jpg"
  
# storing pdf path
#pdf_path = "D:/office_programs/doc_scanner/file.pdf"

def face_reader(face):
    got_eyes = []
    got_mouth = []
    final = []
    
    img = cv2.imread(r"D:\python\doc_reader\New folder\data_face/"+face)
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray , 1.3, 5)
    mouths = mouth_Cascade.detectMultiScale(gray, 1.3,5)
    if len(eyes) != 0:
        got_eyes.append(face)
    if len(mouths) != 0:
        got_mouth.append(face)
    for im in got_eyes:
        if im in got_mouth:
            final.append(im)
    if len(final) == 0:
        for i in got_eyes:
            final.append(i)
        for j in got_mouth:
            final.append(j)

    i = 0
    for file in final:
        loc = r"D:\python\doc_reader\New folder\data_face/"+file
        dest = r"D:\python\doc_reader\New folder\final_img/"+file
        shutil.move(loc, dest)
        if i == 0:
            break

def convert2pdf(final_image):
    imagelist = listdir(final_image) # get list of all images
    pdf = FPDF('P','mm','A4') # create an A4-size pdf document 

    x,y,w,h = 20,0,100,100

    for image in imagelist:

        pdf.add_page()
        pdf.image(r"D:\python\doc_reader\New folder/final_img/" +image,x,y,w,h)

    pdf.output(r"D:\python\doc_reader\New folder\pdf/{}".format(file_name), 'F')
    print("pdf successful made")
     
try: 
    while True:
        time_elapsed = time.time() - prev
        ret, frame = cap.read()
        if  time_elapsed >1./ frame_rate:
            prev = time.time()
            cv2.resize(frame , (500,300))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x,y,w,h) in faces:
                # To draw a rectangle in a face 
                #cv2.rectangle(frame, (x,y),(x+w,y+h),(255,255,0),2) 
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                cv2.imwrite('data/frame{}.jpg'.format(str(i)), frame)
                cv2.imwrite('data_face/frame{}.jpg'.format(str(i)), roi_color)
            i += 1
    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    print()
         
         
get_adhar_no = []
tolist = []

try:
    folder_length = len(os.listdir(data_face))
    if folder_length != 0:
        for face in os.listdir(data_face):
            print(face_reader(face))
            break

            
    for image in os.listdir(images):
        if image.endswith('.jpg'):
            if len(tolist) == 0:
                os.chdir(images)
                # tessdata_dir_config = '/usr/local/share/tessdata/'
                img = cv2.imread(image)
                img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                kernel = np.ones((1, 1), np.uint8)
                img = cv2.dilate(img, kernel, iterations=1)
                img = cv2.erode(img, kernel, iterations=1)
                #cv2.imshow('bgr', img)                
    
                d = tess.image_to_data(img, output_type=Output.DICT, lang='eng', config=tessdata_dir_config)
                n_boxes = len(d['level'])
                all_text = tess.image_to_string(img)
                print(len(all_text))
                if len(all_text) == 0:
                    os.remove(img)
                if len(all_text) > 10:
                    # print(adhaar_read_data(all_text))
                    all_data = (adhaar_read_data(all_text))
                    print(all_data)
    
                    for key, value in all_data.items():
                        #print(key, value)
                        if key == 'Adhaar Number':
                            # get_ac = value.replace(" ", "")
                            if len(value) > 10:
                                get_adhar_no.append(value)
                                tolist.append(value)
                                value = value[:14]
                                v = "'" + value + "'"
                                #print(v)
                                print("AADHAR NO -->", value)
                                #cv2.imwrite('data_face/frame{}.jpg'.format(str(i)), image)
                                image_path = os.path.abspath(r"D:\python\doc_reader\New folder\data/" + image)
                                shutil.copy(image_path , final_image)
                                #shutil.copy(photo_path , final_image)
                                print('PDF making start')
                                print(convert2pdf(final_image))
                                

                else:
                    os.remove(image)
                    
except Exception as e:
    print()

if len(tolist) == 0:
	print("plz scan your adhaar card , this ain't your adhaar card.")

#for image in os.listdir(images):
 #   os.remove(image)

    
 
    
    
    
