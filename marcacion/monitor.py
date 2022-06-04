import os
import threading
import cv2
from datetime import datetime
from marcacion.marcacion import registrarentrada


hora=""
dataPath = os.getcwd()
dataPath = os.path.join(dataPath, "CoreDatos")
imagePaths = os.listdir(dataPath)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modeloLBPHFace.xml')
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')


class Reconocimientofacial(object):
    def __init__(self,url):
        url=url
        self.video=cv2.VideoCapture(url)
    def __del__(self):
        self.video.release()

    def rec_facial(self):
        ret, frame = self.video.read()
        if ret== True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()
            faces = faceClassif.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y+h, x:x+w]
                rostro = cv2.resize(rostro, (500, 500),interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)
                now = datetime.now()
                hora= now.strftime('%H:%M:%S')
                if result[1] < 70:
                    try:
                        nombre=""
                        #con esto se resuelve que los valores esten fuera de rango
                        carnet =imagePaths[result[0]]
                        try:
                            nombre=registrarentrada(carnet)
                        except Exception as e:
                            nombre=e
                        #se hace consulta a la base de datos para obtener el nombre de la persona
                        #a quien pertenece el numero de carnet
                        cv2.putText(frame, '{}'.format(imagePaths[result[0]]),(x, y-25),2,1.1,(0, 255, 0),1,cv2.LINE_AA)
                        cv2.putText(frame, str(nombre)+" "+str(hora), (x+250, y-25), 2, 0.8, (255, 0, 255), 1, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
                        # obteniendo el nombre del reconocido para uso de BD
                        #print(result[1])
                                        
                    except Exception as identifier:
                        print(identifier)
                else:
                    cv2.putText(frame, 'Desconocido'+str(hora), (x, y-20), 2,0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
    