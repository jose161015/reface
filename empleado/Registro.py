import cv2
import os
import numpy
from django.shortcuts import redirect

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml")


class VideoCamara(object):
    # modulo para video Streaming para registro
    def __init__(self,nombre,carnet,cantidadimagenes):
        self.video = cv2.VideoCapture(0)
        self.nombre = nombre
        self.cantImagenes = cantidadimagenes
        self.carnet = carnet
        

    def __del__(self):
        self.video.release()
    
    def rostroscap(self,carnet,imgcant):
        #valida cantidad de imagenes capturadas
        coreDatos = os.getcwd()
        pathcore = os.path.join(coreDatos, "CoreDatos")
        path = os.path.join(pathcore, carnet)
        cantimgs = len(os.listdir(path))
        if cantimgs < imgcant:
            #print("Imagenes completas de: " + carnet)
            return True
        else:
            return False             

    def captura(self):
        # Directorio donde se encuentra la carpeta con el nombre de la persona
        dir_faces = os.getcwd()
        path = os.path.join(dir_faces, self.nombre)
        size = 4

        coreDatos = os.getcwd()
        pathcore = os.path.join(coreDatos, "CoreDatos")
        path = os.path.join(pathcore, self.nombre)

        if not os.path.isdir(pathcore):
            os.mkdir(pathcore)
            print("Se creo la carpeta CoreDatos")
            # Si no hay una carpeta con el nombre ingresado entonces se crea
        if not os.path.isdir(path):
            os.mkdir(path)
            print("Se creo la base de imagenes: " + self.nombre)

       

        img_width, img_height = 110, 100

        # test para el XML
        # test = face_detection_videocam.load('IAG4USAM/modulos/haarcascade_frontalface_default.xml')
        # print(test)
        rval, img = self.video.read()
            
        # convertimos la imagen a blanco y negro
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.flip(img, 1, 0)

        # redimensionar la imagen
        mini = cv2.resize(
        gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

        faces = face_cascade.detectMultiScale(mini)
        faces = sorted(faces, key=lambda x: x[3])
        if faces:
            face_i = faces[0]
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y: y + h, x: x + w]
            face_resize = cv2.resize(face, (img_width, img_height))
            
            if self.rostroscap(self.nombre,self.cantImagenes):
                # Dibujamos un rectangulo en las coordenadas del rostro
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #Ponemos el nombre en el rectagulo
                cv2.putText(img, self.nombre, (x + 80, y - 10),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255),2)

                # El nombre de cada foto es el numero del ciclo
                # Obtenemos el nombre de la foto
            
                pin = (sorted([int(n[: n.find(".")])
                for n in os.listdir(path) if n[0] != "."] + [0])[-1] + 1)
                # Metemos la foto en el directorio
                cv2.imwrite("%s/%s.png" % (path, pin), face_resize)
            
            else:
                #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(img, 'Captura Terminada', (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0),2) 
                 
        ret, jpeg = cv2.imencode(".jpg", img)
        
        return jpeg.tobytes()

    def capturaCompletada(self):
        #para detener el proceso de registro
        self.contador=1
        self.cantimgs = 0
        if self.contador > self.cantimgs:
            data = [{'estadocap':'terminado'}]
            return  data

def entrenar():
    dataPath = os.getcwd()
    dataPath = os.path.join(dataPath,"CoreDatos") #Cambia a la ruta donde hayas almacenado Data
    peopleList = os.listdir(dataPath)
    #print('Lista de personas: ', peopleList)
    print("PathCore: " + dataPath)


    labels = []
    facesData = []
    label = 0


    for nameDir in peopleList:
        #personPath = os.path.join(dataPath,nameDir)
        personPath = dataPath  + "/" + nameDir
        
        for fileName in os.listdir(personPath):
            #print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName,0))
            #image = cv2.imread(personPath+'/'+fileName,0)
            #cv2.imshow('image',image)
            #cv2.waitKey(10)
        label = label + 1

    print('labels= ',labels)
    #print('Numero de etiquetas 0: ',np.count_nonzero(np.array(labels)==0))
    #print('Numero de etiquetas 1: ',np.count_nonzero(np.array(labels)==1))

    # Métodos para entrenar el reconocedor
    #face_recognizer = cv2.face.EigenFaceRecognizer_create()
    #face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    print("Aprendiendo rostros...")
    face_recognizer.train(facesData, numpy.array(labels))

    # Almacenando el modelo obtenido
    #face_recognizer.write('modeloEigenFace.xml')
    #face_recognizer.write('modeloFisherFace.xml')
    face_recognizer.write('modeloLBPHFace.xml')
    print("Modelo de rostros listo...")